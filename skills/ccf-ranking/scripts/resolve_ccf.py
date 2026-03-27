#!/usr/bin/env python3
"""Backward-compatible wrapper for the richer CCF resolver."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from resolve_ccf_rank import enrich_ccf_records, resolve_ccf_venue

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
if str(AUTHORITY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AUTHORITY_SCRIPTS))

from shared_schema import load_jsonl, save_jsonl


def main():
    parser = argparse.ArgumentParser(description="Resolve CCF ranks with audit metadata")
    parser.add_argument("--input", help="Input JSONL paper DB")
    parser.add_argument("--output", "-o", help="Output JSONL paper DB")
    parser.add_argument("--snapshot", help="Optional CCF snapshot JSON")
    parser.add_argument("--aliases", help="Optional CCF aliases JSON")
    parser.add_argument("--venue", help="Resolve one venue and print rank only")
    args = parser.parse_args()

    if args.venue:
        match = resolve_ccf_venue(args.venue, snapshot_file=args.snapshot, aliases_file=args.aliases)
        print(match.get("ccf_rank") or "")
        return

    if not args.input or not args.output:
        raise SystemExit("--input and --output are required unless --venue is used")

    records = load_jsonl(args.input)
    enriched = enrich_ccf_records(records, snapshot_file=args.snapshot, aliases_file=args.aliases)
    save_jsonl(enriched, args.output)


if __name__ == "__main__":
    main()
