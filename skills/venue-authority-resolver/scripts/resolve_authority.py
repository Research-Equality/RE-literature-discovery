#!/usr/bin/env python3
"""Resolve venue authority metadata without assigning final scores."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
CCF_SCRIPTS = Path(__file__).resolve().parents[2] / "ccf-ranking" / "scripts"
JOURNAL_SCRIPTS = Path(__file__).resolve().parents[2] / "journal-metrics" / "scripts"
for path in (AUTHORITY_SCRIPTS, CCF_SCRIPTS, JOURNAL_SCRIPTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from resolve_ccf_rank import enrich_ccf_records
from resolve_journal_metrics import enrich_journal_metric_records
from shared_schema import ensure_list, ensure_mapping, load_jsonl, normalize_paper, save_jsonl


def resolve_records(
    records: list[dict],
    *,
    ccf_snapshot: str | None = None,
    ccf_aliases: str | None = None,
    journal_source_of_record: str | None = None,
    journal_open_fallback: str | None = None,
    journal_local_override: str | None = None,
) -> list[dict]:
    """Resolve venue-type, review status, CCF rank, and journal metrics."""
    normalized = [normalize_paper(record) for record in records]
    normalized = enrich_ccf_records(normalized, snapshot_file=ccf_snapshot, aliases_file=ccf_aliases)
    normalized = enrich_journal_metric_records(
        normalized,
        source_of_record_file=journal_source_of_record,
        open_fallback_file=journal_open_fallback,
        local_override_file=journal_local_override,
    )

    resolved = []
    for paper in normalized:
        caution_flags = ensure_list(paper.get("caution_flags"))
        quality_flags = ensure_list(paper.get("quality_flags"))

        if paper.get("is_preprint") and "preprint" not in caution_flags:
            caution_flags.append("preprint")
        if paper.get("peer_reviewed") and "peer_reviewed" not in quality_flags:
            quality_flags.append("peer_reviewed")
        if paper.get("ccf_rank"):
            quality_flags.append(f"ccf:{paper['ccf_rank']}")
        if paper.get("jcr_quartile"):
            quality_flags.append(f"jcr:{paper['jcr_quartile']}")
        if paper.get("cas_quartile"):
            quality_flags.append(f"cas:{paper['cas_quartile']}")
        if paper.get("is_preprint") and not paper.get("peer_reviewed"):
            caution_flags.append("preprint_only")
        if not paper.get("venue") or not paper.get("year") or paper.get("ccf_match_type") == "unresolved":
            caution_flags.append("weak_metadata")
        if paper.get("ccf_warnings"):
            caution_flags.extend(paper["ccf_warnings"])
        if paper.get("journal_metric_warnings"):
            caution_flags.extend(paper["journal_metric_warnings"])

        paper["caution_flags"] = sorted(set(caution_flags))
        paper["quality_flags"] = sorted(set(quality_flags))
        paper["source_of_truth"] = ensure_mapping(paper.get("source_of_truth"))
        paper["source_version"] = ensure_mapping(paper.get("source_version"))
        paper["resolved_from"] = ensure_mapping(paper.get("resolved_from"))
        paper["match_confidence"] = ensure_mapping(paper.get("match_confidence"))
        paper["last_verified_at"] = ensure_mapping(paper.get("last_verified_at"))
        resolved.append(normalize_paper(paper))
    return resolved


def main():
    parser = argparse.ArgumentParser(description="Resolve venue authority metadata")
    parser.add_argument("--input", required=True, help="Input JSONL paper DB")
    parser.add_argument("--output", "-o", required=True, help="Output JSONL paper DB")
    parser.add_argument("--ccf-snapshot", help="Optional custom CCF snapshot JSON")
    parser.add_argument("--ccf-aliases", help="Optional custom CCF aliases JSON")
    parser.add_argument("--journal-source-of-record", help="Optional source-of-record JSON")
    parser.add_argument("--journal-open-fallback", help="Optional open fallback JSON")
    parser.add_argument("--journal-local-override", help="Optional local override CSV or JSON")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    resolved = resolve_records(
        records,
        ccf_snapshot=args.ccf_snapshot,
        ccf_aliases=args.ccf_aliases,
        journal_source_of_record=args.journal_source_of_record,
        journal_open_fallback=args.journal_open_fallback,
        journal_local_override=args.journal_local_override,
    )
    save_jsonl(resolved, args.output)


if __name__ == "__main__":
    main()
