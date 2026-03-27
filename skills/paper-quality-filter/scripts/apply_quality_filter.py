#!/usr/bin/env python3
"""Attach quality and caution flags, with optional metadata-based filtering."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
if str(AUTHORITY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AUTHORITY_SCRIPTS))

from shared_schema import ensure_list, load_jsonl, normalize_paper, save_jsonl


def apply_quality_filter(
    records: list[dict],
    *,
    peer_reviewed_only: bool = False,
    exclude_preprints: bool = False,
    min_year: int | None = None,
    max_caution_flags: int | None = None,
) -> list[dict]:
    """Enrich records with quality metadata and optionally exclude weak records."""
    kept = []
    for record in records:
        paper = normalize_paper(record)
        caution_flags = ensure_list(paper.get("caution_flags"))
        quality_flags = ensure_list(paper.get("quality_flags"))

        weak_metadata = False
        has_authority_signal = any(
            [
                bool(paper.get("peer_reviewed")),
                bool(paper.get("is_preprint")),
                bool(paper.get("ccf_rank")),
                bool(paper.get("jcr_quartile")),
                bool(paper.get("cas_quartile")),
                paper.get("impact_factor") is not None,
            ]
        )
        if not paper.get("abstract"):
            caution_flags.append("missing_abstract")
            weak_metadata = True
        if not paper.get("year"):
            caution_flags.append("missing_year")
            weak_metadata = True
        if not paper.get("venue"):
            caution_flags.append("missing_venue")
            weak_metadata = True
        if paper.get("is_preprint"):
            caution_flags.append("preprint")
            if not paper.get("peer_reviewed"):
                caution_flags.append("preprint_only")
        if paper.get("citation_count", 0) == 0 and not paper.get("is_preprint") and (paper.get("year") or 0) < 2024:
            caution_flags.append("zero_citations")
        if paper.get("peer_reviewed"):
            quality_flags.append("peer_reviewed")
        if paper.get("ccf_rank") in {"A", "B"}:
            quality_flags.append("ranked_cs_venue")
        if paper.get("jcr_quartile") == "Q1":
            quality_flags.append("q1_journal")
        if (paper.get("year") or 0) >= 2024:
            quality_flags.append("recent")
        if not has_authority_signal:
            weak_metadata = True
        if weak_metadata:
            caution_flags.append("weak_metadata")

        paper["caution_flags"] = sorted(set(caution_flags))
        paper["quality_flags"] = sorted(set(quality_flags))

        if peer_reviewed_only and not paper.get("peer_reviewed"):
            continue
        if exclude_preprints and paper.get("is_preprint"):
            continue
        if min_year and paper.get("year") and paper["year"] < min_year:
            continue
        if max_caution_flags is not None and len(paper["caution_flags"]) > max_caution_flags:
            continue
        kept.append(paper)
    return kept


def main():
    parser = argparse.ArgumentParser(description="Filter or flag paper quality metadata")
    parser.add_argument("--input", required=True, help="Input JSONL paper DB")
    parser.add_argument("--output", "-o", required=True, help="Output JSONL paper DB")
    parser.add_argument("--peer-reviewed-only", action="store_true", help="Keep only peer-reviewed records")
    parser.add_argument("--exclude-preprints", action="store_true", help="Drop preprints")
    parser.add_argument("--min-year", type=int, help="Drop records older than this year")
    parser.add_argument("--max-caution-flags", type=int, help="Drop records with more caution flags than this")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    kept = apply_quality_filter(
        records,
        peer_reviewed_only=args.peer_reviewed_only,
        exclude_preprints=args.exclude_preprints,
        min_year=args.min_year,
        max_caution_flags=args.max_caution_flags,
    )
    save_jsonl(kept, args.output)


if __name__ == "__main__":
    main()
