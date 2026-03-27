#!/usr/bin/env python3
"""Generate a minimal related-work draft from ranked literature metadata."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
if str(AUTHORITY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AUTHORITY_SCRIPTS))

from shared_schema import load_jsonl, normalize_paper


def format_citation(record: dict) -> str:
    """Format a provisional citation token."""
    return f"\\cite{{{record.get('citation_key', record.get('paper_id', 'paper'))}}}"


def pick(records: list[dict], bucket: str, limit: int) -> list[dict]:
    """Select the top N records from one bucket."""
    selected = [normalize_paper(record) for record in records if normalize_paper(record).get("selection_bucket") == bucket]
    selected.sort(key=lambda record: (-(record.get("final_score") or 0.0), -(record.get("authority_score") or 0.0)))
    return selected[:limit]


def build_paragraph(topic: str, records: list[dict], *, opener: str) -> str:
    """Render one prose paragraph from selected records."""
    if not records:
        return ""
    mentions = []
    for record in records:
        venue = record.get("venue") or record.get("source") or "unknown venue"
        caution = ""
        if record.get("is_preprint"):
            caution = " (preprint)"
        mentions.append(
            f"{record.get('title')} {format_citation(record)} ({record.get('year')}, {venue}{caution})"
        )
    lead = opener.format(topic=topic)
    return lead + " " + "; ".join(mentions) + "."


def draft_related_work(topic: str, records: list[dict]) -> str:
    """Generate a structured markdown draft."""
    core = pick(records, "core", 5)
    supporting = pick(records, "supporting", 5)
    background = pick(records, "background", 3)
    watchlist = pick(records, "watchlist", 2)

    paragraphs = [
        build_paragraph(
            topic,
            background + core[:2],
            opener="Early work on {topic} established the main problem framing through",
        ),
        build_paragraph(
            topic,
            core,
            opener="The strongest peer-reviewed line of work in {topic} is represented by",
        ),
        build_paragraph(
            topic,
            supporting,
            opener="A complementary supporting line explores adjacent design choices, including",
        ),
    ]

    if watchlist:
        paragraphs.append(
            build_paragraph(
                topic,
                watchlist,
                opener="Recent frontier signals should be discussed more cautiously, especially for",
            )
        )

    lines = [
        "# Related Work Draft",
        "",
        f"Topic: {topic}",
        "",
        "## Draft",
        "",
    ]
    lines.extend([paragraph for paragraph in paragraphs if paragraph])
    lines.extend(
        [
            "",
            "## Selection Notes",
            "",
            f"- core papers: {len(core)}",
            f"- supporting papers: {len(supporting)}",
            f"- background papers: {len(background)}",
            f"- frontier watchlist papers: {len(watchlist)}",
            "- preprints should be framed as emerging evidence rather than settled consensus.",
            "- if provisional cite keys differ from the final BibTeX keys, reconcile them with citation-management before submission.",
        ]
    )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate a related-work draft from ranked papers")
    parser.add_argument("--topic", required=True, help="Topic or contribution framing")
    parser.add_argument("--input", required=True, help="Input ranked JSONL paper DB")
    parser.add_argument("--output", "-o", required=True, help="Output markdown file")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    markdown = draft_related_work(args.topic, records)
    Path(args.output).write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
