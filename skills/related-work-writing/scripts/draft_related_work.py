#!/usr/bin/env python3
"""Generate a bucket-aware related-work draft from ranked literature metadata."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
if str(AUTHORITY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AUTHORITY_SCRIPTS))

from shared_schema import ensure_list, load_jsonl, normalize_paper


def format_citation(record: dict) -> str:
    """Format a provisional citation token."""
    return f"\\cite{{{record.get('citation_key', record.get('paper_id', 'paper'))}}}"


def pick(records: list[dict], bucket: str, limit: int) -> list[dict]:
    """Select the top N records from one bucket."""
    selected = [normalize_paper(record) for record in records if normalize_paper(record).get("selection_bucket") == bucket]
    selected.sort(key=lambda record: (-(record.get("final_score") or 0.0), -(record.get("authority_score") or 0.0)))
    return selected[:limit]


def build_mentions(records: list[dict], *, tone: str) -> str:
    """Render one phrase bundle with tone-specific qualifiers."""
    mentions = []
    for record in records:
        venue = record.get("venue") or record.get("source") or "unknown venue"
        caution = set(ensure_list(record.get("caution_flags")))
        qualifier = ""
        if tone == "canonical":
            qualifier = "a canonical backbone reference"
        elif tone == "supportive":
            qualifier = "a useful comparative reference"
        elif tone == "tentative":
            qualifier = "an emerging result that should be treated cautiously"

        if "high_authority_low_evidence" in caution:
            qualifier += ", despite stronger venue placement than underlying evidence"
        elif "preprint_only" in caution:
            qualifier += ", currently available only as a preprint"
        elif "weak_metadata" in caution:
            qualifier += ", with weak supporting metadata"

        mentions.append(
            f"{record.get('title')} {format_citation(record)} ({record.get('year')}, {venue}) as {qualifier}"
        )
    return "; ".join(mentions)


def draft_related_work(topic: str, records: list[dict]) -> str:
    """Generate a structured markdown draft."""
    background = pick(records, "background", 2)
    core = pick(records, "core", 5)
    supporting = pick(records, "supporting", 5)
    frontier = pick(records, "frontier", 3)

    lines = [
        "# Related Work Draft",
        "",
        f"Topic: {topic}",
        "",
        "## Draft",
        "",
    ]

    if background:
        lines.append(
            "Historical framing for "
            f"{topic} can start with {build_mentions(background, tone='canonical')}."
        )
    if core:
        lines.append(
            "The canonical backbone of the literature on "
            f"{topic} is built around {build_mentions(core, tone='canonical')}."
        )
    if supporting:
        lines.append(
            "Comparative and supportive context comes from "
            f"{build_mentions(supporting, tone='supportive')}."
        )
    if frontier:
        lines.append(
            "Frontier work should be described cautiously rather than as established consensus, especially for "
            f"{build_mentions(frontier, tone='tentative')}."
        )

    lines.extend(
        [
            "",
            "## Selection Notes",
            "",
            f"- core papers: {len(core)}",
            f"- supporting papers: {len(supporting)}",
            f"- background papers: {len(background)}",
            f"- frontier papers: {len(frontier)}",
            "- core papers should be written as canonical or backbone references.",
            "- supporting papers should be written comparatively and supportively.",
            "- frontier papers must be framed as tentative, emerging, or incomplete rather than settled consensus.",
            "- if provisional cite keys differ from the final BibTeX keys, reconcile them with citation-management before submission.",
        ]
    )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate a bucket-aware related-work draft from ranked papers")
    parser.add_argument("--topic", required=True, help="Topic or contribution framing")
    parser.add_argument("--input", required=True, help="Input ranked JSONL paper DB")
    parser.add_argument("--output", "-o", required=True, help="Output markdown file")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    markdown = draft_related_work(args.topic, records)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
