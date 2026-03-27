#!/usr/bin/env python3
"""Resolve auditable journal metrics across source-of-record, fallback, and override layers."""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import sys
from datetime import datetime
from pathlib import Path

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
if str(AUTHORITY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AUTHORITY_SCRIPTS))

from shared_schema import ensure_list, ensure_mapping, load_jsonl, normalize_paper, save_jsonl

DEFAULT_SOURCE_OF_RECORD = Path(__file__).resolve().parent.parent / "data" / "journal_source_of_record.json"
DEFAULT_OPEN_FALLBACK = Path(__file__).resolve().parent.parent / "data" / "journal_open_fallback.json"


def normalize_key(text: str) -> str:
    """Normalize journal text for matching."""
    return " ".join("".join(ch.lower() if ch.isalnum() else " " for ch in text).split())


def load_json_source(path: Path) -> tuple[dict, list[dict]]:
    """Load a metrics JSON source."""
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload.get("metadata", {}), payload.get("journals", [])


def load_local_override(path: str | None) -> tuple[dict, list[dict]]:
    """Load local override data from JSON or CSV."""
    if not path:
        return {}, []
    override_path = Path(path)
    if override_path.suffix.lower() == ".csv":
        with open(override_path, encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = [dict(row) for row in reader]
        metadata = {
            "source_name": "local_override",
            "version": override_path.stem,
            "metric_year": None,
            "verified_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "license_note": "Local override supplied by the operator.",
            "is_official_metric": False,
        }
        return metadata, rows
    with open(override_path, encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, dict):
        return payload.get("metadata", {}), payload.get("journals", payload.get("records", []))
    return {
        "source_name": "local_override",
        "version": override_path.stem,
        "metric_year": None,
        "verified_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "license_note": "Local override supplied by the operator.",
        "is_official_metric": False,
    }, list(payload)


def build_index(rows: list[dict]) -> tuple[dict[str, dict], list[tuple[str, dict]]]:
    """Build exact and fuzzy indexes."""
    exact: dict[str, dict] = {}
    fuzzy: list[tuple[str, dict]] = []
    for row in rows:
        names = [row.get("canonical", ""), *row.get("aliases", [])]
        if isinstance(row.get("aliases"), str):
            names = [row.get("canonical", "")] + [part.strip() for part in row["aliases"].split(";") if part.strip()]
        for name in names:
            key = normalize_key(str(name))
            if key:
                exact[key] = row
                fuzzy.append((key, row))
    return exact, fuzzy


def resolve_from_source(venue: str, metadata: dict, rows: list[dict]) -> dict:
    """Resolve one venue against one metric source."""
    exact, fuzzy = build_index(rows)
    key = normalize_key(venue)
    result = {
        "matched": None,
        "match_type": "unresolved",
        "match_confidence": 0.0,
        "warnings": [],
        "source_name": metadata.get("source_name", ""),
        "version": metadata.get("version", ""),
        "metric_year": metadata.get("metric_year"),
        "license_note": metadata.get("license_note", ""),
        "verified_at": metadata.get("verified_at", ""),
        "is_official_metric": bool(metadata.get("is_official_metric")),
    }

    if key in exact:
        result["matched"] = exact[key]
        result["match_type"] = "exact"
        result["match_confidence"] = 1.0
        return result

    scored = []
    for candidate_key, candidate in fuzzy:
        ratio = difflib.SequenceMatcher(None, key, candidate_key).ratio()
        if ratio >= 0.84:
            scored.append((ratio, candidate_key, candidate))
    scored.sort(reverse=True)
    if scored:
        best_ratio, best_key, best = scored[0]
        second_ratio = scored[1][0] if len(scored) > 1 else 0.0
        if best_ratio >= 0.89 and best_ratio - second_ratio >= 0.03:
            result["matched"] = best
            result["match_type"] = "fuzzy"
            result["match_confidence"] = round(best_ratio, 4)
            result["warnings"].append("journal_metric_fuzzy_match")
        else:
            result["warnings"].append("journal_metric_ambiguous_match")
    else:
        result["warnings"].append("journal_metric_missing")

    if not result["is_official_metric"]:
        result["warnings"].append("journal_metric_unofficial_source")
    metric_year = result.get("metric_year")
    if metric_year and metric_year < datetime.utcnow().year - 1:
        result["warnings"].append("journal_metric_stale")
    return result


def select_metric_match(venue: str, *, source_of_record_file: str | None = None, open_fallback_file: str | None = None, local_override_file: str | None = None) -> dict:
    """Resolve metrics across local override, source of record, then open fallback."""
    source_meta, source_rows = load_json_source(Path(source_of_record_file) if source_of_record_file else DEFAULT_SOURCE_OF_RECORD)
    fallback_meta, fallback_rows = load_json_source(Path(open_fallback_file) if open_fallback_file else DEFAULT_OPEN_FALLBACK)
    override_meta, override_rows = load_local_override(local_override_file)

    candidates = []
    if override_rows:
        candidates.append(resolve_from_source(venue, override_meta, override_rows))
    candidates.append(resolve_from_source(venue, source_meta, source_rows))
    candidates.append(resolve_from_source(venue, fallback_meta, fallback_rows))

    for candidate in candidates:
        if candidate.get("matched"):
            return candidate
    return candidates[-1]


def resolve_journal_metric_record(
    paper: dict,
    *,
    source_of_record_file: str | None = None,
    open_fallback_file: str | None = None,
    local_override_file: str | None = None,
) -> dict:
    """Resolve one journal record into auditable metric metadata."""
    record = normalize_paper(paper)
    if record.get("venue_type") != "journal":
        return record

    match = select_metric_match(
        record.get("venue", ""),
        source_of_record_file=source_of_record_file,
        open_fallback_file=open_fallback_file,
        local_override_file=local_override_file,
    )
    matched = match.get("matched") or {}

    warnings = ensure_list(record.get("journal_metric_warnings")) + ensure_list(match.get("warnings"))
    record["jcr_quartile"] = record.get("jcr_quartile") or matched.get("jcr_quartile")
    record["impact_factor"] = record.get("impact_factor") if record.get("impact_factor") is not None else matched.get("impact_factor")
    record["cas_quartile"] = record.get("cas_quartile") or matched.get("cas_quartile")
    record["metric_source"] = match.get("source_name", "")
    record["metric_year"] = match.get("metric_year")
    record["metric_license_note"] = match.get("license_note", "")
    record["is_official_metric"] = bool(match.get("is_official_metric"))
    record["journal_metric_warnings"] = sorted(set(warnings))
    record["journal_metric_match_type"] = match.get("match_type", "unresolved")
    record["journal_metric_match_confidence"] = match.get("match_confidence", 0.0)
    record["source_of_truth"] = {**ensure_mapping(record.get("source_of_truth")), "journal_metrics": match.get("source_name", "")}
    record["source_version"] = {**ensure_mapping(record.get("source_version")), "journal_metrics": match.get("version", "")}
    record["resolved_from"] = {**ensure_mapping(record.get("resolved_from")), "journal_metrics": matched.get("canonical", record.get("venue", ""))}
    record["match_confidence"] = {**ensure_mapping(record.get("match_confidence")), "journal_metrics": match.get("match_confidence", 0.0)}
    record["last_verified_at"] = {**ensure_mapping(record.get("last_verified_at")), "journal_metrics": match.get("verified_at", "")}
    return normalize_paper(record)


def enrich_journal_metric_records(
    records: list[dict],
    *,
    source_of_record_file: str | None = None,
    open_fallback_file: str | None = None,
    local_override_file: str | None = None,
) -> list[dict]:
    """Resolve journal metrics for a whole corpus."""
    return [
        resolve_journal_metric_record(
            record,
            source_of_record_file=source_of_record_file,
            open_fallback_file=open_fallback_file,
            local_override_file=local_override_file,
        )
        for record in records
    ]


def main():
    parser = argparse.ArgumentParser(description="Resolve auditable journal metrics")
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
