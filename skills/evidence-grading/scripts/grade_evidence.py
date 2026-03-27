#!/usr/bin/env python3
"""Attach evidence scores without collapsing evidence into venue prestige."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
if str(AUTHORITY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AUTHORITY_SCRIPTS))

from shared_schema import ensure_list, ensure_mapping, load_jsonl, log_normalize, normalize_paper, save_jsonl, utc_now_iso

DESIGN_KEYWORDS = {
    "systematic review": 0.95,
    "meta-analysis": 0.95,
    "benchmark": 0.82,
    "leaderboard": 0.8,
    "replication": 0.78,
    "ablation": 0.72,
    "comprehensive evaluation": 0.76,
    "randomized": 0.88,
    "case study": 0.45,
    "position paper": 0.35,
    "opinion": 0.3
}


def infer_design_score(text: str) -> float:
    """Infer evidence-design quality from lexical signals."""
    lowered = text.lower()
    score = 0.55
    for phrase, candidate in DESIGN_KEYWORDS.items():
        if phrase in lowered:
            score = max(score, candidate)
    if "theorem" in lowered or "proof" in lowered:
        score = max(score, 0.68)
    if "dataset" in lowered or "evaluation" in lowered:
        score = max(score, 0.64)
    return score


def evidence_label(score: float) -> str:
    """Map evidence scores to writing labels."""
    if score >= 0.8:
        return "strong"
    if score >= 0.6:
        return "moderate"
    if score >= 0.45:
        return "exploratory"
    return "weak"


def grade_records(records: list[dict]) -> list[dict]:
    """Attach evidence score and writing label."""
    max_citations = max((normalize_paper(record).get("citation_count", 0) for record in records), default=0)
    graded = []
    verified_at = utc_now_iso()
    for record in records:
        paper = normalize_paper(record)
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
        design_score = infer_design_score(text)
        citation_context = log_normalize(paper.get("citation_count", 0), max_citations) * 0.08
        peer_review_bonus = 0.08 if paper.get("peer_reviewed") else 0.0
        preprint_penalty = 0.08 if paper.get("is_preprint") else 0.0
        caution_penalty = min(len(ensure_list(paper.get("caution_flags"))) * 0.03, 0.15)
        score = max(0.0, min(1.0, design_score + citation_context + peer_review_bonus - preprint_penalty - caution_penalty))
        paper["evidence_score"] = round(score, 4)
        paper["evidence_label"] = evidence_label(score)

        quality_flags = ensure_list(paper.get("quality_flags"))
        quality_flags.append(f"evidence:{paper['evidence_label']}")
        paper["quality_flags"] = sorted(set(quality_flags))

        caution_flags = ensure_list(paper.get("caution_flags"))
        if paper.get("authority_score", 0) >= 0.75 and score < 0.55:
            caution_flags.append("high_authority_low_evidence")
        paper["caution_flags"] = sorted(set(caution_flags))
        paper["last_verified_at"] = {**ensure_mapping(paper.get("last_verified_at")), "evidence": verified_at}
        graded.append(paper)
    return graded


def write_summary(records: list[dict], output_path: str):
    """Write a simple markdown summary for evidence grading."""
    counts = {}
    caution_counts = {}
    for record in records:
        label = record.get("evidence_label", "unknown")
        counts[label] = counts.get(label, 0) + 1
        for flag in ensure_list(record.get("caution_flags")):
            caution_counts[flag] = caution_counts.get(flag, 0) + 1
    lines = [
        "# Evidence Grading Summary",
        "",
        "| Label | Count |",
        "| --- | ---: |",
    ]
    for label in ("strong", "moderate", "exploratory", "weak"):
        if label in counts:
            lines.append(f"| {label} | {counts[label]} |")
    if caution_counts:
        lines.extend(["", "## Caution Flags", "", "| Flag | Count |", "| --- | ---: |"])
        for flag, count in sorted(caution_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {flag} | {count} |")
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Grade evidence strength in a paper corpus")
    parser.add_argument("--input", required=True, help="Input JSONL paper DB")
    parser.add_argument("--output", "-o", required=True, help="Output JSONL paper DB")
    parser.add_argument("--summary", help="Optional markdown summary path")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    graded = grade_records(records)
    save_jsonl(graded, args.output)
    if args.summary:
        write_summary(graded, args.summary)


if __name__ == "__main__":
    main()
