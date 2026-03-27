#!/usr/bin/env python3
"""Enrich paper records with pluggable journal metrics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
if str(AUTHORITY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AUTHORITY_SCRIPTS))

from shared_schema import load_jsonl, normalize_paper, save_jsonl


def load_metrics(metrics_file: str | None = None) -> dict[str, dict]:
    """Load journal metric aliases."""
    default_path = Path(__file__).resolve().parent.parent / "references" / "journal_metrics.sample.json"
    path = Path(metrics_file) if metrics_file else default_path
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)

    mapping: dict[str, dict] = {}
    for item in payload.get("journals", []):
        aliases = [item.get("venue", "")] + list(item.get("aliases", []))
        info = {
            "jcr_quartile": item.get("jcr_quartile"),
            "impact_factor": item.get("impact_factor"),
            "cas_quartile": item.get("cas_quartile"),
            "core_rank": item.get("core_rank"),
        }
        for alias in aliases:
            key = " ".join(str(alias).lower().split())
            if key:
                mapping[key] = info
    return mapping


def resolve_journal_metrics(venue: str, mapping: dict[str, dict]) -> dict:
    """Resolve metrics by venue or alias match."""
    key = " ".join(venue.lower().split())
    if not key:
        return {}
    if key in mapping:
        return dict(mapping[key])
    for alias, info in mapping.items():
        if alias in key or key in alias:
            return dict(info)
    return {}


def enrich_journal_metrics(records: list[dict], metrics_file: str | None = None) -> list[dict]:
    """Add journal metric metadata to matching records."""
    mapping = load_metrics(metrics_file)
    enriched = []
    for record in records:
        paper = normalize_paper(record)
        if paper.get("venue_type") != "journal":
            enriched.append(paper)
            continue
        metrics = resolve_journal_metrics(paper.get("venue", ""), mapping)
        for key, value in metrics.items():
            if value is not None and not paper.get(key):
                paper[key] = value
        enriched.append(paper)
    return enriched


def main():
    parser = argparse.ArgumentParser(description="Enrich paper records with journal metrics")
    parser.add_argument("--input", required=True, help="Input JSONL paper DB")
    parser.add_argument("--output", "-o", required=True, help="Output JSONL paper DB")
    parser.add_argument("--metrics-file", help="Optional custom metrics JSON")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    enriched = enrich_journal_metrics(records, args.metrics_file)
    save_jsonl(enriched, args.output)


if __name__ == "__main__":
    main()
