#!/usr/bin/env python3
"""Validate and write a maintained CCF snapshot."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def load_records(path: str) -> list[dict]:
    """Load raw records from JSON or CSV."""
    input_path = Path(path)
    if input_path.suffix.lower() == ".csv":
        with open(input_path, encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            return [dict(row) for row in reader]
    with open(input_path, encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, dict):
        return list(payload.get("venues", payload.get("records", [])))
    return list(payload)


def normalize_record(record: dict) -> dict:
    """Normalize one snapshot row."""
    canonical = str(record.get("canonical") or record.get("venue") or "").strip()
    official_name = str(record.get("official_name") or canonical).strip()
    rank = str(record.get("rank") or "").upper().strip()
    if not canonical or rank not in {"A", "B", "C"}:
        raise SystemExit(f"Invalid CCF record: {record}")

    abbreviations = record.get("abbreviations") or record.get("aliases") or []
    if isinstance(abbreviations, str):
        abbreviations = [part.strip() for part in abbreviations.split(";") if part.strip()]

    return {
        "canonical": canonical,
        "official_name": official_name,
        "rank": rank,
        "area": str(record.get("area") or "").strip(),
        "abbreviations": abbreviations,
    }


def main():
    parser = argparse.ArgumentParser(description="Update the repository CCF official snapshot")
    parser.add_argument("--input", required=True, help="Input JSON or CSV records")
    parser.add_argument(
        "--output",
        default="skills/ccf-ranking/data/ccf_official_snapshot.json",
        help="Output snapshot JSON",
    )
    parser.add_argument("--version", required=True, help="Snapshot version tag")
    parser.add_argument("--verified-at", required=True, help="Verification timestamp")
    parser.add_argument(
        "--source-note",
        default="Repository-maintained official snapshot.",
        help="Human-readable source note",
    )
    args = parser.parse_args()

    records = sorted((normalize_record(record) for record in load_records(args.input)), key=lambda item: item["canonical"])
    payload = {
        "metadata": {
            "source_name": "repository-maintained-ccf-official-snapshot",
            "version": args.version,
            "verified_at": args.verified_at,
            "source_note": args.source_note,
        },
        "venues": records,
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
