#!/usr/bin/env python3
"""Compute authority-aware ranking scores for literature corpora."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

PROFILE_SCRIPTS = Path(__file__).resolve().parents[2] / "field-ranking-profile" / "scripts"
if str(PROFILE_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(PROFILE_SCRIPTS))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from get_profile import get_profile
from shared_schema import clamp, ensure_list, load_jsonl, log_normalize, normalize_paper, save_jsonl

CCF_SCORES = {"A": 1.0, "B": 0.78, "C": 0.55}
CORE_SCORES = {"A*": 1.0, "A": 0.85, "B": 0.65, "C": 0.45}
QUARTILE_SCORES = {"Q1": 1.0, "Q2": 0.75, "Q3": 0.5, "Q4": 0.3}
VENUE_TYPE_SCORES = {
    "conference": 0.85,
    "journal": 0.9,
    "workshop": 0.5,
    "preprint": 0.3,
    "other": 0.4,
}
STOPWORDS = {"a", "an", "and", "for", "in", "of", "on", "the", "to", "with"}


def tokenize(text: str) -> set[str]:
    """Tokenize free text into lowercase keywords."""
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in STOPWORDS}


def compute_relevance_score(record: dict, query: str | None = None) -> float:
    """Compute or preserve relevance score."""
    existing = record.get("relevance_score")
    if existing is not None and query is None:
        return clamp(float(existing))

    if not query:
        return clamp(float(existing)) if existing is not None else 0.5

    query_terms = tokenize(query)
    if not query_terms:
        return clamp(float(existing)) if existing is not None else 0.5

    title_terms = tokenize(record.get("title", ""))
    abstract_terms = tokenize(record.get("abstract", ""))
    overlap = len(query_terms & (title_terms | abstract_terms)) / len(query_terms)
    title_bonus = 0.2 if query_terms <= title_terms else 0.0
    seed = clamp(overlap + title_bonus)
    if existing is None:
        return seed
    return clamp(max(float(existing), seed))


def compute_citation_score(record: dict, max_citations: int) -> float:
    """Normalize citation count against the current corpus."""
    return log_normalize(record.get("citation_count", 0) or 0, max_citations)


def compute_recency_score(record: dict, profile: dict) -> float:
    """Prefer recent work without erasing foundational classics."""
    year = record.get("year")
    if not year:
        return 0.25
    current_year = datetime.now().year
    horizon = max(int(profile.get("recency_horizon_years", 8)), 1)
    age = max(current_year - year, 0)
    return clamp(1.0 - age / horizon, 0.15, 1.0)


def compute_authority_score(record: dict, profile: dict) -> tuple[float, dict]:
    """Compute authority score from venue metadata, not evidence strength."""
    weights = profile.get("authority_weights", {})
    total = sum(max(float(v), 0.0) for v in weights.values()) or 1.0

    ccf_component = CCF_SCORES.get(record.get("ccf_rank"), 0.0)
    core_component = CORE_SCORES.get(record.get("core_rank"), 0.0)
    journal_component = max(
        QUARTILE_SCORES.get(record.get("jcr_quartile"), 0.0),
        QUARTILE_SCORES.get(record.get("cas_quartile"), 0.0),
        clamp((record.get("impact_factor") or 0.0) / 20.0),
        core_component,
    )
    peer_component = 1.0 if record.get("peer_reviewed") else 0.0
    venue_component = VENUE_TYPE_SCORES.get(record.get("venue_type"), 0.4)
    preprint_penalty = 1.0 if record.get("is_preprint") else 0.0

    raw = (
        weights.get("ccf_rank", 0.0) * max(ccf_component, core_component)
        + weights.get("journal_metrics", 0.0) * journal_component
        + weights.get("peer_reviewed", 0.0) * peer_component
        + weights.get("venue_type", 0.0) * venue_component
        - weights.get("preprint_penalty", 0.0) * preprint_penalty
    ) / total
    return clamp(raw), {
        "ccf_component": round(max(ccf_component, core_component), 3),
        "journal_component": round(journal_component, 3),
        "peer_component": round(peer_component, 3),
        "venue_component": round(venue_component, 3),
        "preprint_penalty": round(preprint_penalty, 3),
    }


def compute_final_score(record: dict, profile: dict) -> float:
    """Combine ranking dimensions into the single final score."""
    weights = profile.get("final_weights", {})
    relevance = record.get("relevance_score") or 0.0
    authority = record.get("authority_score") or 0.0
    citation = record.get("citation_score") or 0.0
    recency = record.get("recency_score") or 0.0
    evidence = record.get("evidence_score")
    if evidence is None:
        evidence = profile.get("fallback_evidence_score", 0.5)

    return clamp(
        weights.get("relevance", 0.0) * relevance
        + weights.get("authority", 0.0) * authority
        + weights.get("citation", 0.0) * citation
        + weights.get("recency", 0.0) * recency
        + weights.get("evidence", 0.0) * evidence
    )


def bucket_for_score(record: dict, profile: dict) -> str:
    """Assign a selection bucket for downstream writing."""
    thresholds = profile.get("bucket_thresholds", {})
    score = record.get("final_score") or 0.0
    caution_flags = ensure_list(record.get("caution_flags"))

    if score >= thresholds.get("core", 0.78):
        bucket = "core"
    elif score >= thresholds.get("supporting", 0.6):
        bucket = "supporting"
    elif score >= thresholds.get("background", 0.4):
        bucket = "background"
    else:
        bucket = "watchlist"

    if "preprint" in caution_flags and bucket == "core":
        bucket = "supporting"
    if len(caution_flags) >= 3 and bucket in {"core", "supporting"}:
        bucket = "background"
    return bucket


def ranking_reason(record: dict) -> str:
    """Build a compact audit trail string."""
    parts = [f"relevance={record['relevance_score']:.2f}"]
    if record.get("ccf_rank"):
        parts.append(f"CCF {record['ccf_rank']}")
    elif record.get("jcr_quartile"):
        parts.append(f"JCR {record['jcr_quartile']}")
    if record.get("peer_reviewed"):
        parts.append("peer-reviewed")
    if record.get("is_preprint"):
        parts.append("preprint")
    parts.append(f"citations={record.get('citation_count', 0)}")
    if record.get("evidence_score") is not None:
        parts.append(f"evidence={record['evidence_score']:.2f}")
    return "; ".join(parts)


def rank_records(records: list[dict], *, query: str | None = None, profile_name: str = "cs", profile_file: str | None = None) -> list[dict]:
    """Rank records and attach score breakdowns."""
    profile = get_profile(profile_name, profile_file)
    normalized = [normalize_paper(record) for record in records]
    max_citations = max((record.get("citation_count", 0) or 0) for record in normalized) if normalized else 0

    ranked = []
    for paper in normalized:
        paper["relevance_score"] = round(compute_relevance_score(paper, query), 4)
        paper["citation_score"] = round(compute_citation_score(paper, max_citations), 4)
        paper["recency_score"] = round(compute_recency_score(paper, profile), 4)
        authority_score, authority_breakdown = compute_authority_score(paper, profile)
        paper["authority_score"] = round(authority_score, 4)
        paper["ranking_breakdown"] = {
            "authority": authority_breakdown,
            "weights": profile.get("final_weights", {}),
        }
        paper["final_score"] = round(compute_final_score(paper, profile), 4)
        paper["selection_bucket"] = bucket_for_score(paper, profile)
        paper["ranking_reason"] = ranking_reason(paper)
        ranked.append(paper)

    ranked.sort(
        key=lambda paper: (
            -(paper.get("final_score") or 0.0),
            -(paper.get("authority_score") or 0.0),
            -(paper.get("citation_count") or 0),
            -(paper.get("year") or 0),
        )
    )
    return ranked


def write_summary(records: list[dict], output_path: str):
    """Write a compact markdown ranking summary."""
    lines = [
        "# Authority-Aware Ranking Summary",
        "",
        "| Bucket | Count |",
        "| --- | ---: |",
    ]
    buckets = {}
    for record in records:
        bucket = record.get("selection_bucket", "unranked")
        buckets[bucket] = buckets.get(bucket, 0) + 1
    for bucket in ("core", "supporting", "background", "watchlist", "unranked"):
        if bucket in buckets:
            lines.append(f"| {bucket} | {buckets[bucket]} |")
    lines.extend(
        [
            "",
            "## Top Papers",
            "",
            "| Title | Score | Bucket | Reason |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for record in records[:10]:
        lines.append(
            f"| {record.get('title', '')} | {record.get('final_score', 0):.3f} | {record.get('selection_bucket', '')} | {record.get('ranking_reason', '')} |"
        )
    Path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Rank paper records with authority-aware scoring")
    parser.add_argument("--input", required=True, help="Input JSONL paper DB")
    parser.add_argument("--output", "-o", required=True, help="Output JSONL paper DB")
    parser.add_argument("--query", help="Optional query used to recompute relevance score")
    parser.add_argument("--profile", default="cs", help="Field ranking profile (default: cs)")
    parser.add_argument("--profile-file", help="Optional custom profile JSON")
    parser.add_argument("--summary", help="Optional markdown summary path")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    ranked = rank_records(records, query=args.query, profile_name=args.profile, profile_file=args.profile_file)
    save_jsonl(ranked, args.output)
    if args.summary:
        write_summary(ranked, args.summary)


if __name__ == "__main__":
    main()
