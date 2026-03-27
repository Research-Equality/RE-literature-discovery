#!/usr/bin/env python3
"""Resolve auditable CCF ranks from a maintained snapshot."""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
if str(AUTHORITY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AUTHORITY_SCRIPTS))

from shared_schema import ensure_list, ensure_mapping, load_jsonl, normalize_paper, save_jsonl

DEFAULT_SNAPSHOT = Path(__file__).resolve().parent.parent / "data" / "ccf_official_snapshot.json"
DEFAULT_ALIASES = Path(__file__).resolve().parent.parent / "data" / "ccf_aliases.json"
ABBR_STOPWORDS = {"of", "the", "and", "on", "for", "in", "international", "conference", "symposium"}


def normalize_key(text: str) -> str:
    """Normalize venue text for matching."""
    return " ".join("".join(ch.lower() if ch.isalnum() else " " for ch in text).split())


def abbreviation(text: str) -> str:
    """Generate a normalized abbreviation."""
    raw = text.strip()
    if raw.isupper() and len(raw) <= 12:
        return raw
    parts = [part for part in normalize_key(raw).split() if part and part not in ABBR_STOPWORDS]
    return "".join(part[0].upper() for part in parts if part)


def load_snapshot(snapshot_file: str | None = None) -> tuple[dict, list[dict]]:
    """Load snapshot metadata and venue rows."""
    path = Path(snapshot_file) if snapshot_file else DEFAULT_SNAPSHOT
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload.get("metadata", {}), payload.get("venues", [])


def load_aliases(aliases_file: str | None = None) -> tuple[dict, list[dict]]:
    """Load alias metadata and rows."""
    path = Path(aliases_file) if aliases_file else DEFAULT_ALIASES
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload.get("metadata", {}), payload.get("aliases", [])


def build_indexes(venues: list[dict], aliases: list[dict]) -> tuple[dict, dict, dict, list[tuple[str, dict]]]:
    """Build exact, alias, abbreviation, and fuzzy indexes."""
    exact_index: dict[str, dict] = {}
    alias_index: dict[str, dict] = {}
    abbreviation_index: dict[str, list[dict]] = {}
    fuzzy_candidates: list[tuple[str, dict]] = []
    canonical_set = {entry["canonical"] for entry in venues}

    for entry in venues:
        canonical = entry["canonical"]
        names = [canonical, entry.get("official_name", canonical)]
        for name in names:
            key = normalize_key(name)
            if key:
                exact_index[key] = entry
                fuzzy_candidates.append((key, entry))
        for short in entry.get("abbreviations", []):
            key = abbreviation(short)
            if key:
                abbreviation_index.setdefault(key, []).append(entry)
                fuzzy_candidates.append((normalize_key(short), entry))

    for alias in aliases:
        key = normalize_key(alias.get("alias", ""))
        canonical = alias.get("canonical", "")
        if key and canonical and canonical in canonical_set:
            alias_index[key] = {"canonical": canonical, "note": alias.get("note", "")}
            fuzzy_candidates.append((key, {"canonical": canonical, "official_name": canonical}))

    return exact_index, alias_index, abbreviation_index, fuzzy_candidates


def venue_by_canonical(venues: list[dict]) -> dict[str, dict]:
    """Build a canonical entry lookup."""
    return {entry["canonical"]: entry for entry in venues}


def resolve_ccf_venue(venue: str, *, snapshot_file: str | None = None, aliases_file: str | None = None) -> dict:
    """Resolve one venue into auditable CCF metadata."""
    snapshot_meta, venues = load_snapshot(snapshot_file)
    _, aliases = load_aliases(aliases_file)
    exact_index, alias_index, abbreviation_index, fuzzy_candidates = build_indexes(venues, aliases)
    canonical_index = venue_by_canonical(venues)

    query = venue.strip()
    query_key = normalize_key(query)
    result = {
        "ccf_rank": None,
        "core_rank": None,
        "ccf_match_type": "unresolved",
        "ccf_match_confidence": 0.0,
        "ccf_source": snapshot_meta.get("source_name", "ccf_official_snapshot"),
        "ccf_version": snapshot_meta.get("version", ""),
        "ccf_verified_at": snapshot_meta.get("verified_at", ""),
        "ccf_warnings": [],
        "resolved_from": {"ccf": query},
        "source_of_truth": {"ccf": snapshot_meta.get("source_name", "ccf_official_snapshot")},
        "source_version": {"ccf": snapshot_meta.get("version", "")},
        "match_confidence": {"ccf": 0.0},
        "last_verified_at": {"ccf": snapshot_meta.get("verified_at", "")},
    }

    entry = None
    matched_on = query

    if query_key in exact_index:
        entry = exact_index[query_key]
        result["ccf_match_type"] = "exact"
        result["ccf_match_confidence"] = 1.0
        matched_on = entry.get("canonical", query)
    elif query_key in alias_index:
        alias = alias_index[query_key]
        entry = canonical_index.get(alias["canonical"])
        result["ccf_match_type"] = "alias"
        result["ccf_match_confidence"] = 0.98
        matched_on = alias["canonical"]
    else:
        abbr = abbreviation(query)
        candidates = abbreviation_index.get(abbr, [])
        if len(candidates) == 1:
            entry = candidates[0]
            result["ccf_match_type"] = "normalized_abbreviation"
            result["ccf_match_confidence"] = 0.94
            matched_on = abbr
            result["ccf_warnings"].append("ccf_non_exact_match")
        elif len(candidates) > 1:
            result["ccf_warnings"].append("ccf_ambiguous_abbreviation_match")

    if entry is None:
        scored = []
        for candidate_key, candidate_entry in fuzzy_candidates:
            ratio = difflib.SequenceMatcher(None, query_key, candidate_key).ratio()
            if ratio >= 0.84:
                scored.append((ratio, candidate_key, candidate_entry))
        scored.sort(reverse=True)
        if scored:
            best_ratio, best_key, best_entry = scored[0]
            second_ratio = scored[1][0] if len(scored) > 1 else 0.0
            if best_ratio >= 0.88 and best_ratio - second_ratio >= 0.03:
                entry = canonical_index.get(best_entry.get("canonical"), best_entry)
                result["ccf_match_type"] = "fuzzy"
                result["ccf_match_confidence"] = round(best_ratio, 4)
                matched_on = best_key
                result["ccf_warnings"].extend(["ccf_fuzzy_match", "ccf_manual_review_recommended"])
            else:
                result["ccf_warnings"].append("ccf_ambiguous_fuzzy_match")
        else:
            result["ccf_warnings"].append("ccf_unresolved")

    if entry:
        result["ccf_rank"] = entry.get("rank")
        result["core_rank"] = "A" if entry.get("rank") == "A" else entry.get("rank")
        result["resolved_from"]["ccf"] = matched_on
        result["match_confidence"]["ccf"] = result["ccf_match_confidence"]
        if result["ccf_match_type"] in {"alias", "normalized_abbreviation"}:
            result["ccf_warnings"].append("ccf_non_exact_match")
    else:
        result["match_confidence"]["ccf"] = 0.0

    result["ccf_warnings"] = sorted(set(result["ccf_warnings"]))
    return result


def enrich_ccf_records(records: list[dict], *, snapshot_file: str | None = None, aliases_file: str | None = None) -> list[dict]:
    """Enrich a corpus with auditable CCF metadata."""
    enriched = []
    for record in records:
        paper = normalize_paper(record)
        match = resolve_ccf_venue(paper.get("venue", ""), snapshot_file=snapshot_file, aliases_file=aliases_file)
        paper["ccf_rank"] = match.get("ccf_rank")
        if not paper.get("core_rank"):
            paper["core_rank"] = match.get("core_rank")
        paper["ccf_match_type"] = match.get("ccf_match_type")
        paper["ccf_match_confidence"] = match.get("ccf_match_confidence")
        paper["ccf_source"] = match.get("ccf_source")
        paper["ccf_version"] = match.get("ccf_version")
        paper["ccf_verified_at"] = match.get("ccf_verified_at")
        paper["ccf_warnings"] = sorted(set(ensure_list(paper.get("ccf_warnings")) + ensure_list(match.get("ccf_warnings"))))
        paper["source_of_truth"] = {**ensure_mapping(paper.get("source_of_truth")), **ensure_mapping(match.get("source_of_truth"))}
        paper["source_version"] = {**ensure_mapping(paper.get("source_version")), **ensure_mapping(match.get("source_version"))}
        paper["resolved_from"] = {**ensure_mapping(paper.get("resolved_from")), **ensure_mapping(match.get("resolved_from"))}
        paper["match_confidence"] = {**ensure_mapping(paper.get("match_confidence")), **ensure_mapping(match.get("match_confidence"))}
        paper["last_verified_at"] = {**ensure_mapping(paper.get("last_verified_at")), **ensure_mapping(match.get("last_verified_at"))}
        enriched.append(normalize_paper(paper))
    return enriched


def main():
    parser = argparse.ArgumentParser(description="Resolve auditable CCF ranks")
    parser.add_argument("--input", help="Input JSONL paper DB")
    parser.add_argument("--output", "-o", help="Output JSONL paper DB")
    parser.add_argument("--snapshot", help="Optional snapshot JSON")
    parser.add_argument("--aliases", help="Optional aliases JSON")
    parser.add_argument("--venue", help="Resolve one venue and print full JSON")
    args = parser.parse_args()

    if args.venue:
        print(json.dumps(resolve_ccf_venue(args.venue, snapshot_file=args.snapshot, aliases_file=args.aliases), indent=2, ensure_ascii=False))
        return

    if not args.input or not args.output:
        raise SystemExit("--input and --output are required unless --venue is used")

    records = load_jsonl(args.input)
    enriched = enrich_ccf_records(records, snapshot_file=args.snapshot, aliases_file=args.aliases)
    save_jsonl(enriched, args.output)


if __name__ == "__main__":
    main()
