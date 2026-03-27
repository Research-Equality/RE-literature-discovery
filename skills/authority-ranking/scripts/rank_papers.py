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
from shared_schema import clamp, ensure_list, ensure_mapping, load_jsonl, log_normalize, normalize_paper, save_jsonl, utc_now_iso

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
FRONTIER_FLAGS = {"preprint_only", "high_authority_low_evidence"}


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
    ccf_confidence = ensure_mapping(record.get("match_confidence")).get("ccf", 1.0 if record.get("ccf_rank") else 0.0)
    journal_confidence = ensure_mapping(record.get("match_confidence")).get(
        "journal_metrics",
        record.get("journal_metric_match_confidence", 1.0 if record.get("metric_source") else 0.0),
    )

    ccf_component = CCF_SCORES.get(record.get("ccf_rank"), 0.0) * (ccf_confidence or 0.0)
    core_component = CORE_SCORES.get(record.get("core_rank"), 0.0)
    journal_component = max(
        QUARTILE_SCORES.get(record.get("jcr_quartile"), 0.0),
        QUARTILE_SCORES.get(record.get("cas_quartile"), 0.0),
        clamp((record.get("impact_factor") or 0.0) / 20.0),
        core_component,
    ) * (journal_confidence or 0.0)
    peer_component = 1.0 if record.get("peer_reviewed") else 0.0
    venue_component = VENUE_TYPE_SCORES.get(record.get("venue_type"), 0.4)
    preprint_penalty = 1.0 if record.get("is_preprint") else 0.0

    raw = (
        weights.get("ccf_rank", 0.0) * max(ccf_component, core_component * 0.5)
        + weights.get("journal_metrics", 0.0) * journal_component
        + weights.get("peer_reviewed", 0.0) * peer_component
        + weights.get("venue_type", 0.0) * venue_component
        - weights.get("preprint_penalty", 0.0) * preprint_penalty
    ) / total
    return clamp(raw), {
        "ccf": round(ccf_component, 4),
        "journal_metrics": round(journal_component, 4),
        "peer_reviewed": round(peer_component, 4),
        "venue_type": round(venue_component, 4),
        "preprint_penalty": round(preprint_penalty, 4),
        "ccf_match_confidence": round(ccf_confidence or 0.0, 4),
        "journal_match_confidence": round(journal_confidence or 0.0, 4),
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
    caution_flags = set(ensure_list(record.get("caution_flags")))

    if caution_flags & FRONTIER_FLAGS:
        return "frontier"
    if score >= thresholds.get("core", 0.78):
        return "core"
    if score >= thresholds.get("supporting", 0.6):
        return "supporting"
    return "background"


def build_authority_reason(record: dict) -> str:
    """Build an auditable plain-language authority reason."""
    parts = []
    if record.get("ccf_rank"):
        match_type = record.get("ccf_match_type") or "exact"
        parts.append(f"CCF {record['ccf_rank']} ({match_type})")
    if record.get("jcr_quartile"):
        parts.append(f"JCR {record['jcr_quartile']}")
    if record.get("cas_quartile"):
        parts.append(f"CAS {record['cas_quartile']}")
    if record.get("impact_factor") is not None:
        parts.append(f"IF {record['impact_factor']}")
    if record.get("peer_reviewed"):
        parts.append("peer-reviewed")
    if record.get("is_preprint"):
        parts.append("preprint-only")
    warnings = ensure_list(record.get("ccf_warnings")) + ensure_list(record.get("journal_metric_warnings"))
    if warnings:
        parts.append(f"warnings={','.join(sorted(set(warnings)))}")
    return "; ".join(parts)


def ranking_reason(record: dict) -> str:
    """Build a compact audit trail string."""
    parts = [f"relevance={record['relevance_score']:.2f}"]
    parts.append(f"authority={record['authority_score']:.2f}")
    parts.append(f"citations={record.get('citation_count', 0)}")
    parts.append(f"recency={record['recency_score']:.2f}")
    if record.get("evidence_score") is not None:
        parts.append(f"evidence={record['evidence_score']:.2f}")
    if record.get("selection_bucket"):
        parts.append(f"bucket={record['selection_bucket']}")
    return "; ".join(parts)


def build_ranking_components(record: dict, profile: dict, authority_breakdown: dict) -> dict:
    """Build the canonical ranking_components payload."""
    return {
        "scores": {
            "relevance": round(record["relevance_score"], 4),
            "authority": round(record["authority_score"], 4),
            "citation": round(record["citation_score"], 4),
            "recency": round(record["recency_score"], 4),
            "evidence": round(record.get("evidence_score") if record.get("evidence_score") is not None else profile.get("fallback_evidence_score", 0.5), 4),
            "final": round(record["final_score"], 4),
        },
        "weights": profile.get("final_weights", {}),
        "authority_breakdown": authority_breakdown,
    }


def rank_records(records: list[dict], *, query: str | None = None, profile_name: str = "cs", profile_file: str | None = None) -> list[dict]:
    """Rank records and attach score breakdowns."""
    profile = get_profile(profile_name, profile_file)
    normalized = [normalize_paper(record) for record in records]
    max_citations = max((record.get("citation_count", 0) or 0) for record in normalized) if normalized else 0
    verified_at = utc_now_iso()

    ranked = []
    for paper in normalized:
        paper["relevance_score"] = round(compute_relevance_score(paper, query), 4)
        paper["citation_score"] = round(compute_citation_score(paper, max_citations), 4)
        paper["recency_score"] = round(compute_recency_score(paper, profile), 4)
        authority_score, authority_breakdown = compute_authority_score(paper, profile)
        paper["authority_score"] = round(authority_score, 4)
        paper["final_score"] = round(compute_final_score(paper, profile), 4)
        paper["selection_bucket"] = bucket_for_score(paper, profile)
        paper["authority_reason"] = build_authority_reason(paper)
        paper["ranking_reason"] = ranking_reason(paper)
        paper["ranking_components"] = build_ranking_components(paper, profile, authority_breakdown)
        paper["ranking_profile"] = {
            "name": profile.get("name", profile_name),
            "final_weights": profile.get("final_weights", {}),
            "authority_weights": profile.get("authority_weights", {}),
        }
        paper["last_verified_at"] = {**ensure_mapping(paper.get("last_verified_at")), "ranking": verified_at}
        ranked.append(normalize_paper(paper))

    ranked.sort(
        key=lambda paper: (
            -(paper.get("final_score") or 0.0),
            -(paper.get("authority_score") or 0.0),
            -(paper.get("citation_count") or 0),
            -(paper.get("year") or 0),
        )
    )
    return ranked


def infer_analysis_paths(output_path: str) -> tuple[str, str]:
    """Infer default report and audit paths from the ranked output path."""
    parent = Path(output_path).resolve().parent
    analysis_dir = parent / "analysis"
    return str(analysis_dir / "ranking_report.md"), str(analysis_dir / "resolution_audit.jsonl")


def write_ranking_report(records: list[dict], output_path: str):
    """Write a compact but auditable ranking report."""
    lines = [
        "# Authority-Aware Ranking Report",
        "",
        "| Bucket | Count |",
        "| --- | ---: |",
    ]
    buckets = {}
    for record in records:
        bucket = record.get("selection_bucket", "unranked")
        buckets[bucket] = buckets.get(bucket, 0) + 1
    for bucket in ("core", "supporting", "background", "frontier", "unranked"):
        if bucket in buckets:
            lines.append(f"| {bucket} | {buckets[bucket]} |")

    lines.extend(
        [
            "",
            "## Top Papers",
            "",
            "| Title | Final | Bucket | Authority Reason |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for record in records[:12]:
        lines.append(
            f"| {record.get('title', '')} | {record.get('final_score', 0):.3f} | {record.get('selection_bucket', '')} | {record.get('authority_reason', '')} |"
        )

    caution_counts = {}
    for record in records:
        for flag in ensure_list(record.get("caution_flags")):
            caution_counts[flag] = caution_counts.get(flag, 0) + 1
    if caution_counts:
        lines.extend(["", "## Caution Flags", "", "| Flag | Count |", "| --- | ---: |"])
        for flag, count in sorted(caution_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {flag} | {count} |")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_resolution_audit(records: list[dict], output_path: str):
    """Write a JSONL audit trail for matching and ranking decisions."""
    audit_records = []
    for record in records:
        audit_records.append(
            {
                "paper_id": record.get("paper_id"),
                "title": record.get("title"),
                "venue": record.get("venue"),
                "selection_bucket": record.get("selection_bucket"),
                "ccf": {
                    "rank": record.get("ccf_rank"),
                    "match_type": record.get("ccf_match_type"),
                    "match_confidence": record.get("ccf_match_confidence"),
                    "source": record.get("ccf_source"),
                    "version": record.get("ccf_version"),
                    "verified_at": record.get("ccf_verified_at"),
                    "warnings": record.get("ccf_warnings", []),
                },
                "journal_metrics": {
                    "jcr_quartile": record.get("jcr_quartile"),
                    "impact_factor": record.get("impact_factor"),
                    "cas_quartile": record.get("cas_quartile"),
                    "metric_source": record.get("metric_source"),
                    "metric_year": record.get("metric_year"),
                    "metric_license_note": record.get("metric_license_note"),
                    "is_official_metric": record.get("is_official_metric"),
                    "warnings": record.get("journal_metric_warnings", []),
                },
                "ranking": {
                    "authority_reason": record.get("authority_reason"),
                    "ranking_reason": record.get("ranking_reason"),
                    "ranking_components": record.get("ranking_components", {}),
                    "ranking_profile": record.get("ranking_profile", {}),
                },
                "audit_fields": {
                    "source_of_truth": record.get("source_of_truth", {}),
                    "source_version": record.get("source_version", {}),
                    "resolved_from": record.get("resolved_from", {}),
                    "match_confidence": record.get("match_confidence", {}),
                    "last_verified_at": record.get("last_verified_at", {}),
                },
                "caution_flags": record.get("caution_flags", []),
                "quality_flags": record.get("quality_flags", []),
            }
        )
    save_jsonl(audit_records, output_path)


def main():
    parser = argparse.ArgumentParser(description="Rank paper records with authority-aware scoring")
    parser.add_argument("--input", required=True, help="Input JSONL paper DB")
    parser.add_argument("--output", "-o", required=True, help="Output JSONL paper DB")
    parser.add_argument("--query", help="Optional query used to recompute relevance score")
    parser.add_argument("--profile", default="cs", help="Field ranking profile (default: cs)")
    parser.add_argument("--profile-file", help="Optional custom profile JSON")
    parser.add_argument("--report", help="Optional markdown report path")
    parser.add_argument("--audit-output", help="Optional JSONL audit path")
    parser.add_argument("--summary", help="Deprecated alias for --report")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    ranked = rank_records(records, query=args.query, profile_name=args.profile, profile_file=args.profile_file)
    save_jsonl(ranked, args.output)

    default_report, default_audit = infer_analysis_paths(args.output)
    report_path = args.report or args.summary or default_report
    audit_path = args.audit_output or default_audit
    write_ranking_report(ranked, report_path)
    write_resolution_audit(ranked, audit_path)


if __name__ == "__main__":
    main()
