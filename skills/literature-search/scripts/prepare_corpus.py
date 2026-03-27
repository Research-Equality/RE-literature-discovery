#!/usr/bin/env python3
"""Merge, deduplicate, triage, and hand off a corpus to the authority layer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
QUALITY_SCRIPTS = Path(__file__).resolve().parents[2] / "paper-quality-filter" / "scripts"
RESOLVER_SCRIPTS = Path(__file__).resolve().parents[2] / "venue-authority-resolver" / "scripts"
for path in (AUTHORITY_SCRIPTS, QUALITY_SCRIPTS, RESOLVER_SCRIPTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from apply_quality_filter import apply_quality_filter
from rank_papers import rank_records
from resolve_authority import resolve_records
from shared_schema import load_jsonl, merge_records, normalize_paper, save_jsonl, token_overlap_score


def deduplicate(records: list[dict]) -> list[dict]:
    """Merge duplicates using canonical IDs and exact normalized titles."""
    by_id: dict[str, dict] = {}
    by_title: dict[str, str] = {}
    ordered_ids: list[str] = []

    for record in records:
        paper = normalize_paper(record)
        title_key = paper.get("title", "").lower()
        paper_id = paper["paper_id"]
        if paper_id in by_id:
            by_id[paper_id] = merge_records(by_id[paper_id], paper)
            continue
        if title_key and title_key in by_title:
            existing_id = by_title[title_key]
            by_id[existing_id] = merge_records(by_id[existing_id], paper)
            continue
        by_id[paper_id] = paper
        by_title[title_key] = paper_id
        ordered_ids.append(paper_id)
    return [by_id[paper_id] for paper_id in ordered_ids]


def initial_triage(records: list[dict], query: str, min_relevance: float, max_papers: int) -> list[dict]:
    """Apply rough lexical relevance triage before authority-aware ranking."""
    triaged = []
    for record in records:
        paper = normalize_paper(record)
        paper["relevance_score"] = round(
            max(paper.get("relevance_score") or 0.0, token_overlap_score(query, paper.get("title", ""), paper.get("abstract", ""))),
            4,
        )
        triaged.append(paper)
    triaged = [paper for paper in triaged if (paper.get("relevance_score") or 0.0) >= min_relevance]
    triaged.sort(key=lambda paper: (-(paper.get("relevance_score") or 0.0), -(paper.get("citation_count") or 0)))
    if max_papers > 0:
        triaged = triaged[:max_papers]
    return triaged


def main():
    parser = argparse.ArgumentParser(description="Prepare a corpus and hand it to the authority layer")
    parser.add_argument("--query", required=True, help="Query used for triage and ranking")
    parser.add_argument("--inputs", nargs="+", required=True, help="Input JSONL search result files")
    parser.add_argument("--merged-output", required=True, help="Merged JSONL output")
    parser.add_argument("--triaged-output", required=True, help="Triaged JSONL output before authority ranking")
    parser.add_argument("--authority-output", required=True, help="Authority-ranked JSONL output")
    parser.add_argument("--profile", default="cs", help="Ranking profile (default: cs)")
    parser.add_argument("--min-relevance", type=float, default=0.12, help="Early triage relevance threshold")
    parser.add_argument("--max-papers", type=int, default=80, help="Maximum papers kept after early triage")
    parser.add_argument("--peer-reviewed-only", action="store_true", help="Drop non-peer-reviewed papers during quality filtering")
    parser.add_argument("--exclude-preprints", action="store_true", help="Drop preprints during quality filtering")
    args = parser.parse_args()

    all_records = []
    for path in args.inputs:
        all_records.extend(load_jsonl(path))

    merged = deduplicate(all_records)
    save_jsonl(merged, args.merged_output)

    triaged = initial_triage(merged, args.query, args.min_relevance, args.max_papers)
    save_jsonl(triaged, args.triaged_output)

    resolved = resolve_records(triaged)
    filtered = apply_quality_filter(
        resolved,
        peer_reviewed_only=args.peer_reviewed_only,
        exclude_preprints=args.exclude_preprints,
    )
    ranked = rank_records(filtered, query=args.query, profile_name=args.profile)
    save_jsonl(ranked, args.authority_output)


if __name__ == "__main__":
    main()
