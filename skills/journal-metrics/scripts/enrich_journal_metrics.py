#!/usr/bin/env python3
"""Backward-compatible wrapper for the auditable journal metric resolver."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from resolve_journal_metrics import enrich_journal_metric_records

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
if str(AUTHORITY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AUTHORITY_SCRIPTS))

from shared_schema import load_jsonl, save_jsonl


def main():
    parser = argparse.ArgumentParser(description="Enrich paper records with auditable journal metrics")
    parser.add_argument("--input", required=True, help="Input JSONL paper DB")
    parser.add_argument("--output", "-o", required=True, help="Output JSONL paper DB")
    parser.add_argument("--source-of-record", help="Optional source-of-record JSON")
    parser.add_argument("--open-fallback", help="Optional open fallback JSON")
    parser.add_argument("--local-override", help="Optional local override CSV or JSON")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    enriched = enrich_journal_metric_records(
        records,
        source_of_record_file=args.source_of_record,
        open_fallback_file=args.open_fallback,
        local_override_file=args.local_override,
    )
    save_jsonl(enriched, args.output)


if __name__ == "__main__":
    main()
