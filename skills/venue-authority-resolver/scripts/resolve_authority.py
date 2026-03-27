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

from enrich_journal_metrics import enrich_journal_metrics
from resolve_ccf import enrich_ccf
from shared_schema import ensure_list, load_jsonl, normalize_paper, save_jsonl


def resolve_records(
    records: list[dict],
    *,
    ccf_mapping: str | None = None,
    journal_metrics_file: str | None = None,
) -> list[dict]:
    """Resolve venue-type, review status, CCF rank, and journal metrics."""
    normalized = [normalize_paper(record) for record in records]
    normalized = enrich_ccf(normalized, ccf_mapping)
    normalized = enrich_journal_metrics(normalized, journal_metrics_file)

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

        paper["caution_flags"] = sorted(set(caution_flags))
        paper["quality_flags"] = sorted(set(quality_flags))
        resolved.append(normalize_paper(paper))
    return resolved


def main():
    parser = argparse.ArgumentParser(description="Resolve venue authority metadata")
    parser.add_argument("--input", required=True, help="Input JSONL paper DB")
    parser.add_argument("--output", "-o", required=True, help="Output JSONL paper DB")
    parser.add_argument("--ccf-mapping", help="Optional custom CCF mapping JSON")
    parser.add_argument("--journal-metrics", help="Optional custom journal metrics JSON")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    resolved = resolve_records(
        records,
        ccf_mapping=args.ccf_mapping,
        journal_metrics_file=args.journal_metrics,
    )
    save_jsonl(resolved, args.output)


if __name__ == "__main__":
    main()
