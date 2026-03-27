#!/usr/bin/env python3
"""Resolve bundled or custom CCF-style venue ranks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
if str(AUTHORITY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AUTHORITY_SCRIPTS))

from shared_schema import load_jsonl, normalize_paper, save_jsonl


def load_mapping(mapping_file: str | None = None) -> dict[str, str]:
    """Load venue aliases into a normalized rank map."""
    default_path = Path(__file__).resolve().parent.parent / "references" / "ccf_venues.sample.json"
    path = Path(mapping_file) if mapping_file else default_path
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)

    mapping: dict[str, str] = {}
    for item in payload.get("venues", []):
        rank = str(item.get("rank", "")).upper()
        names = [item.get("venue", "")] + list(item.get("aliases", []))
        for name in names:
            key = " ".join(str(name).lower().split())
            if key:
                mapping[key] = rank
    return mapping


def resolve_ccf_rank(venue: str, mapping: dict[str, str]) -> str | None:
    """Resolve the closest bundled CCF-style rank for a venue."""
    key = " ".join(venue.lower().split())
    if not key:
        return None
    if key in mapping:
        return mapping[key]

    for alias, rank in mapping.items():
        if alias in key or key in alias:
            return rank
    return None


def enrich_ccf(records: list[dict], mapping_file: str | None = None) -> list[dict]:
    """Add CCF and core-rank metadata to records."""
    mapping = load_mapping(mapping_file)
    enriched = []
    for record in records:
        paper = normalize_paper(record)
        rank = resolve_ccf_rank(paper.get("venue", ""), mapping)
        if rank:
            paper["ccf_rank"] = rank
            if not paper.get("core_rank"):
                paper["core_rank"] = "A" if rank == "A" else rank
        enriched.append(paper)
    return enriched


def main():
    parser = argparse.ArgumentParser(description="Enrich paper records with CCF ranks")
    parser.add_argument("--input", help="Input JSONL paper DB")
    parser.add_argument("--output", "-o", help="Output JSONL paper DB")
    parser.add_argument("--mapping", help="Optional custom mapping JSON")
    parser.add_argument("--venue", help="Resolve one venue name and print the rank")
    args = parser.parse_args()

    mapping = load_mapping(args.mapping)
    if args.venue:
        print(resolve_ccf_rank(args.venue, mapping) or "")
        return

    if not args.input or not args.output:
        raise SystemExit("--input and --output are required unless --venue is used")

    records = load_jsonl(args.input)
    enriched = enrich_ccf(records, args.mapping)
    save_jsonl(enriched, args.output)


if __name__ == "__main__":
    main()
