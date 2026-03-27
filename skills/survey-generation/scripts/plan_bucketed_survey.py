#!/usr/bin/env python3
"""Generate bucket-aware survey writing guidance from a ranked corpus."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
if str(AUTHORITY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AUTHORITY_SCRIPTS))

from shared_schema import ensure_list, load_jsonl, normalize_paper


def choose(records: list[dict], bucket: str, limit: int) -> list[dict]:
    """Select the top N records from a bucket."""
    chosen = [normalize_paper(record) for record in records if normalize_paper(record).get("selection_bucket") == bucket]
    chosen.sort(key=lambda record: (-(record.get("final_score") or 0.0), -(record.get("authority_score") or 0.0)))
    return chosen[:limit]


def summarize(records: list[dict]) -> list[str]:
    """Summarize records into short bullet-like lines."""
    lines = []
    for record in records:
        caution = ",".join(ensure_list(record.get("caution_flags")))
        caution_text = f" cautions={caution}" if caution else ""
        lines.append(
            f"- {record.get('title')} ({record.get('year')}, {record.get('venue')}) score={record.get('final_score', 0):.3f}{caution_text}"
        )
    return lines


def build_guidance(topic: str, records: list[dict]) -> str:
    """Build a survey writing plan."""
    core = choose(records, "core", 8)
    supporting = choose(records, "supporting", 8)
    background = choose(records, "background", 5)
    frontier = choose(records, "frontier", 5)
    lines = [
        "# Bucket-Aware Survey Guidance",
        "",
        f"Topic: {topic}",
        "",
        "## Writing Rules",
        "",
        "- core papers: canonical / backbone treatment",
        "- supporting papers: comparative / supportive treatment",
        "- frontier papers: cautious / tentative treatment",
        "- frontier papers must never be written as established consensus",
        "",
        "## Core Backbone",
        "",
        *summarize(core),
        "",
        "## Supporting Comparison Layer",
        "",
        *summarize(supporting),
        "",
        "## Background and Historical Context",
        "",
        *summarize(background),
        "",
        "## Frontier and Tentative Signals",
        "",
        *summarize(frontier),
    ]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate bucket-aware survey writing guidance")
    parser.add_argument("--topic", required=True, help="Survey topic")
    parser.add_argument("--input", required=True, help="Input ranked JSONL paper DB")
    parser.add_argument("--output", "-o", required=True, help="Output markdown path")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    markdown = build_guidance(args.topic, records)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
