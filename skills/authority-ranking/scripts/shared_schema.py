#!/usr/bin/env python3
"""Shared paper-schema helpers for authority-aware literature workflows."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from datetime import datetime, timezone
from typing import Any

SCHEMA_VERSION = "authority-paper-v2"

REQUIRED_FIELDS = [
    "paper_id",
    "title",
    "authors",
    "year",
    "venue",
    "venue_type",
    "doi",
    "citation_count",
    "peer_reviewed",
    "is_preprint",
    "ccf_rank",
    "core_rank",
    "jcr_quartile",
    "impact_factor",
    "cas_quartile",
    "authority_score",
    "relevance_score",
    "citation_score",
    "recency_score",
    "evidence_score",
    "final_score",
    "selection_bucket",
    "ranking_reason",
    "caution_flags",
    "quality_flags",
    "source_of_truth",
    "source_version",
    "resolved_from",
    "match_confidence",
    "authority_reason",
    "ranking_components",
    "ranking_profile",
    "last_verified_at",
]

PREPRINT_HINTS = ("arxiv", "biorxiv", "medrxiv", "preprint")
JOURNAL_HINTS = ("journal", "transactions", "review", "letters", "annals")
WORKSHOP_HINTS = ("workshop", "symposium")
CONFERENCE_HINTS = (
    "conference",
    "proceedings",
    "neurips",
    "icml",
    "iclr",
    "aaai",
    "ijcai",
    "acl",
    "emnlp",
    "naacl",
    "eacl",
    "coling",
    "cvpr",
    "iccv",
    "eccv",
    "kdd",
    "sigir",
    "www",
    "corl",
    "aistats",
    "uai",
    "ccs",
    "ndss",
    "sp",
    "usenix security",
)
STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "from",
    "in",
    "of",
    "on",
    "the",
    "to",
    "towards",
    "using",
    "with",
}


def utc_now_iso() -> str:
    """Return a stable UTC ISO-8601 timestamp."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_list(value: Any) -> list[str]:
    """Normalize a list-like field into a clean list of strings."""
    if value is None:
        return []
    if isinstance(value, list):
        items = value
    elif isinstance(value, str):
        if not value.strip():
            return []
        parts = re.split(r";|\band\b|\n", value)
        items = [part.strip() for part in parts if part.strip()]
    else:
        items = [str(value)]

    cleaned = []
    for item in items:
        text = str(item).strip()
        if text and text not in cleaned:
            cleaned.append(text)
    return cleaned


def ensure_mapping(value: Any) -> dict[str, Any]:
    """Normalize mapping-like fields."""
    if isinstance(value, dict):
        return dict(value)
    return {}


def merge_mappings(existing: Any, incoming: Any) -> dict[str, Any]:
    """Merge two shallow mappings."""
    merged = ensure_mapping(existing)
    merged.update(ensure_mapping(incoming))
    return merged


def normalize_text(value: Any) -> str:
    """Normalize scalar text fields."""
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def normalize_doi(value: Any) -> str:
    """Strip DOI prefixes and normalize casing."""
    doi = normalize_text(value)
    if doi.lower().startswith("https://doi.org/"):
        doi = doi[16:]
    elif doi.lower().startswith("http://doi.org/"):
        doi = doi[15:]
    return doi


def coerce_bool(value: Any) -> bool | None:
    """Coerce common truthy/falsy representations into bool."""
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"true", "yes", "y", "1"}:
        return True
    if text in {"false", "no", "n", "0"}:
        return False
    return None


def coerce_float(*values: Any) -> float | None:
    """Return the first parseable float value."""
    for value in values:
        if value is None or value == "":
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return None


def coerce_int(*values: Any) -> int | None:
    """Return the first parseable integer value."""
    for value in values:
        if value is None or value == "":
            continue
        try:
            return int(float(value))
        except (TypeError, ValueError):
            continue
    return None


def parse_year(*values: Any) -> int | None:
    """Extract a 4-digit year from candidate values."""
    for value in values:
        if value is None or value == "":
            continue
        text = str(value).strip()
        match = re.search(r"(19|20)\d{2}", text)
        if match:
            return int(match.group(0))
    return None


def normalize_rank(value: Any, *, allowed: tuple[str, ...]) -> str | None:
    """Normalize rank-like categorical values."""
    text = normalize_text(value).upper()
    if not text:
        return None
    if text in allowed:
        return text
    return None


def slugify(text: str, *, max_length: int = 24) -> str:
    """Build a filesystem- and citation-safe slug."""
    parts = re.findall(r"[a-z0-9]+", text.lower())
    slug = "-".join(parts[:6])[:max_length].strip("-")
    return slug or "paper"


def sanitize_citation_key(text: str) -> str:
    """Build a LaTeX-safe provisional citation key."""
    cleaned = re.sub(r"[^a-zA-Z0-9:_-]+", "", text)
    return cleaned[:64] or "paper"


def provisional_citation_key(record: dict[str, Any]) -> str:
    """Generate a stable provisional citation key from metadata."""
    authors = ensure_list(record.get("authors"))
    first_author = slugify(authors[0].split()[-1], max_length=16) if authors else "anon"
    year = str(parse_year(record.get("year")) or "nd")
    title_tokens = [
        token
        for token in re.findall(r"[a-z0-9]+", normalize_text(record.get("title")).lower())
        if token not in STOPWORDS
    ]
    focus = title_tokens[0] if title_tokens else "paper"
    return sanitize_citation_key(f"{first_author}{year}{focus}")


def infer_venue(record: dict[str, Any]) -> str:
    """Resolve a usable venue name from mixed-source records."""
    for key in ("venue", "venue_normalized", "journal", "booktitle"):
        value = normalize_text(record.get(key))
        if value:
            return value
    return ""


def infer_venue_type(record: dict[str, Any], venue: str, source: str) -> str:
    """Infer the publication venue type."""
    explicit = normalize_text(record.get("venue_type")).lower()
    if explicit:
        return explicit

    work_type = normalize_text(record.get("type")).lower()
    venue_lower = venue.lower()
    source_lower = source.lower()

    if any(token in venue_lower or token in source_lower for token in PREPRINT_HINTS):
        return "preprint"
    if work_type in {"journal-article", "article"}:
        return "journal"
    if work_type in {"proceedings-article", "inproceedings"}:
        return "conference"
    if any(token in venue_lower for token in JOURNAL_HINTS):
        return "journal"
    if any(token in venue_lower for token in WORKSHOP_HINTS):
        return "workshop"
    if any(token in venue_lower for token in CONFERENCE_HINTS):
        return "conference"
    return "other"


def infer_is_preprint(record: dict[str, Any], venue_type: str, source: str, venue: str) -> bool:
    """Infer whether the record is a preprint."""
    explicit = coerce_bool(record.get("is_preprint"))
    if explicit is not None:
        return explicit
    if venue_type == "preprint":
        return True
    lowered = " ".join([source.lower(), venue.lower()])
    return any(token in lowered for token in PREPRINT_HINTS)


def infer_peer_reviewed(record: dict[str, Any], venue_type: str, is_preprint: bool) -> bool:
    """Infer peer-review status conservatively."""
    explicit = coerce_bool(record.get("peer_reviewed"))
    if explicit is not None:
        return explicit
    if is_preprint:
        return False
    return venue_type in {"conference", "journal"}


def canonical_paper_id(record: dict[str, Any]) -> str:
    """Generate a stable canonical paper ID."""
    for key in ("paper_id", "paperId"):
        value = normalize_text(record.get(key))
        if value:
            return value

    doi = normalize_doi(record.get("doi"))
    if doi:
        return f"doi:{doi.lower()}"

    arxiv_id = normalize_text(record.get("arxiv_id"))
    if arxiv_id:
        return f"arxiv:{arxiv_id}"

    openalex_id = normalize_text(record.get("openalex_id") or record.get("openalexId"))
    if openalex_id:
        return openalex_id

    title = normalize_text(record.get("title"))
    year = parse_year(record.get("year")) or 0
    digest = hashlib.sha1(f"{title}|{year}".encode("utf-8")).hexdigest()[:12]
    return f"title:{digest}"


def merge_text(existing: Any, incoming: Any) -> str:
    """Prefer the longer non-empty text value."""
    old = normalize_text(existing)
    new = normalize_text(incoming)
    if not old:
        return new
    if not new:
        return old
    return new if len(new) > len(old) else old


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Clamp a numeric value to a range."""
    return max(minimum, min(maximum, value))


def load_jsonl(path: str) -> list[dict[str, Any]]:
    """Load JSONL records from disk."""
    records: list[dict[str, Any]] = []
    if not os.path.exists(path):
        return records
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def save_jsonl(records: list[dict[str, Any]], path: str):
    """Write JSONL records to disk."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def normalize_paper(record: dict[str, Any], default_source: str | None = None) -> dict[str, Any]:
    """Normalize arbitrary paper metadata into the shared authority schema."""
    normalized = dict(record)
    source = normalize_text(normalized.get("source")) or normalize_text(default_source) or "unknown"
    venue = infer_venue(normalized)
    year = parse_year(
        normalized.get("year"),
        normalized.get("publicationDate"),
        normalized.get("publication_date"),
        normalized.get("published"),
        normalized.get("updated"),
    )
    citation_count = coerce_int(
        normalized.get("citation_count"),
        normalized.get("citationCount"),
        normalized.get("cited_by"),
        normalized.get("cited_by_count"),
    )
    venue_type = infer_venue_type(normalized, venue, source)
    is_preprint = infer_is_preprint(normalized, venue_type, source, venue)
    peer_reviewed = infer_peer_reviewed(normalized, venue_type, is_preprint)

    normalized.update(
        {
            "schema_version": normalized.get("schema_version") or SCHEMA_VERSION,
            "paper_id": canonical_paper_id(normalized),
            "title": normalize_text(normalized.get("title")),
            "authors": ensure_list(normalized.get("authors")),
            "year": year,
            "venue": venue,
            "venue_type": venue_type,
            "doi": normalize_doi(normalized.get("doi")),
            "citation_count": citation_count or 0,
            "peer_reviewed": peer_reviewed,
            "is_preprint": is_preprint,
            "ccf_rank": normalize_rank(normalized.get("ccf_rank"), allowed=("A", "B", "C")),
            "core_rank": normalize_rank(normalized.get("core_rank"), allowed=("A*", "A", "B", "C")),
            "jcr_quartile": normalize_rank(normalized.get("jcr_quartile"), allowed=("Q1", "Q2", "Q3", "Q4")),
            "impact_factor": coerce_float(normalized.get("impact_factor")),
            "cas_quartile": normalize_rank(normalized.get("cas_quartile"), allowed=("Q1", "Q2", "Q3", "Q4")),
            "authority_score": coerce_float(normalized.get("authority_score")),
            "relevance_score": coerce_float(normalized.get("relevance_score"), normalized.get("affinity_score")),
            "citation_score": coerce_float(normalized.get("citation_score")),
            "recency_score": coerce_float(normalized.get("recency_score")),
            "evidence_score": coerce_float(normalized.get("evidence_score")),
            "final_score": coerce_float(normalized.get("final_score")),
            "selection_bucket": normalize_text(normalized.get("selection_bucket")) or "unranked",
            "ranking_reason": normalize_text(normalized.get("ranking_reason")),
            "caution_flags": ensure_list(normalized.get("caution_flags")),
            "quality_flags": ensure_list(normalized.get("quality_flags")),
            "source_of_truth": ensure_mapping(normalized.get("source_of_truth")),
            "source_version": ensure_mapping(normalized.get("source_version")),
            "resolved_from": ensure_mapping(normalized.get("resolved_from")),
            "match_confidence": ensure_mapping(normalized.get("match_confidence")),
            "authority_reason": normalize_text(normalized.get("authority_reason")),
            "ranking_components": ensure_mapping(normalized.get("ranking_components")),
            "ranking_profile": ensure_mapping(normalized.get("ranking_profile")),
            "last_verified_at": ensure_mapping(normalized.get("last_verified_at")),
            "source": source,
            "sources": ensure_list(normalized.get("sources") or [source]),
            "citation_key": sanitize_citation_key(
                normalize_text(normalized.get("citation_key")) or provisional_citation_key(normalized)
            ),
            "abstract": normalize_text(normalized.get("abstract")),
            "publication_date": normalize_text(
                normalized.get("publication_date") or normalized.get("publicationDate") or normalized.get("published")
            ),
            "url": normalize_text(normalized.get("url")),
            "pdf_url": normalize_text(normalized.get("pdf_url")),
            "ccf_match_type": normalize_text(normalized.get("ccf_match_type")),
            "ccf_match_confidence": coerce_float(normalized.get("ccf_match_confidence")),
            "ccf_source": normalize_text(normalized.get("ccf_source")),
            "ccf_version": normalize_text(normalized.get("ccf_version")),
            "ccf_verified_at": normalize_text(normalized.get("ccf_verified_at")),
            "ccf_warnings": ensure_list(normalized.get("ccf_warnings")),
            "metric_source": normalize_text(normalized.get("metric_source")),
            "metric_year": coerce_int(normalized.get("metric_year")),
            "metric_license_note": normalize_text(normalized.get("metric_license_note")),
            "is_official_metric": bool(coerce_bool(normalized.get("is_official_metric")) or False),
            "journal_metric_warnings": ensure_list(normalized.get("journal_metric_warnings")),
            "journal_metric_match_type": normalize_text(normalized.get("journal_metric_match_type")),
            "journal_metric_match_confidence": coerce_float(normalized.get("journal_metric_match_confidence")),
        }
    )

    return normalized


def merge_records(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    """Merge duplicate records without losing metadata."""
    base = normalize_paper(existing)
    other = normalize_paper(incoming)
    merged = dict(base)

    for key in ("title", "venue", "abstract", "publication_date", "url", "pdf_url", "ranking_reason", "authority_reason"):
        merged[key] = merge_text(merged.get(key), other.get(key))

    for key in ("doi", "paper_id", "citation_key", "ccf_rank", "core_rank", "jcr_quartile", "cas_quartile"):
        if not merged.get(key):
            merged[key] = other.get(key)

    if merged.get("year") is None:
        merged["year"] = other.get("year")
    if not merged.get("venue_type") or merged.get("selection_bucket") == "unranked":
        merged["venue_type"] = other.get("venue_type") or merged.get("venue_type")
        merged["selection_bucket"] = other.get("selection_bucket") or merged.get("selection_bucket")

    merged["authors"] = sorted(set(ensure_list(merged.get("authors")) + ensure_list(other.get("authors"))))
    merged["caution_flags"] = sorted(set(ensure_list(merged.get("caution_flags")) + ensure_list(other.get("caution_flags"))))
    merged["quality_flags"] = sorted(set(ensure_list(merged.get("quality_flags")) + ensure_list(other.get("quality_flags"))))
    merged["ccf_warnings"] = sorted(set(ensure_list(merged.get("ccf_warnings")) + ensure_list(other.get("ccf_warnings"))))
    merged["journal_metric_warnings"] = sorted(
        set(ensure_list(merged.get("journal_metric_warnings")) + ensure_list(other.get("journal_metric_warnings")))
    )
    merged["sources"] = sorted(set(ensure_list(merged.get("sources")) + ensure_list(other.get("sources"))))
    merged["source"] = merged["sources"][0] if merged["sources"] else merge_text(merged.get("source"), other.get("source"))
    merged["peer_reviewed"] = bool(merged.get("peer_reviewed") or other.get("peer_reviewed"))
    merged["is_preprint"] = bool(merged.get("is_preprint") or other.get("is_preprint"))
    merged["citation_count"] = max(merged.get("citation_count") or 0, other.get("citation_count") or 0)

    for key in ("impact_factor", "authority_score", "relevance_score", "citation_score", "recency_score", "evidence_score", "final_score"):
        values = [value for value in (merged.get(key), other.get(key)) if value is not None]
        merged[key] = max(values) if values else None

    for key in ("source_of_truth", "source_version", "resolved_from", "match_confidence", "ranking_components", "ranking_profile", "last_verified_at"):
        merged[key] = merge_mappings(merged.get(key), other.get(key))

    for key in ("ccf_match_confidence", "journal_metric_match_confidence"):
        values = [value for value in (merged.get(key), other.get(key)) if value is not None]
        merged[key] = max(values) if values else None

    for key in ("ccf_match_type", "ccf_source", "ccf_version", "ccf_verified_at", "metric_source", "metric_license_note", "journal_metric_match_type"):
        if not normalize_text(merged.get(key)):
            merged[key] = normalize_text(other.get(key))

    if merged.get("metric_year") is None:
        merged["metric_year"] = other.get("metric_year")
    merged["is_official_metric"] = bool(merged.get("is_official_metric") or other.get("is_official_metric"))

    merged["paper_id"] = canonical_paper_id(merged)
    if not merged.get("citation_key"):
        merged["citation_key"] = provisional_citation_key(merged)
    return normalize_paper(merged)


def token_overlap_score(query: str, title: str, abstract: str = "") -> float:
    """Rough lexical relevance score for early triage."""
    query_tokens = {token for token in re.findall(r"[a-z0-9]+", query.lower()) if token not in STOPWORDS}
    if not query_tokens:
        return 0.5
    text_tokens = set(re.findall(r"[a-z0-9]+", f"{title} {abstract}".lower()))
    overlap = len(query_tokens & text_tokens) / len(query_tokens)
    title_bonus = 0.2 if query_tokens and query_tokens <= set(re.findall(r"[a-z0-9]+", title.lower())) else 0.0
    return clamp(overlap + title_bonus)


def log_normalize(value: int | float, upper: int | float) -> float:
    """Log-normalize a count into [0, 1]."""
    if upper <= 0:
        return 0.0
    return clamp(math.log1p(max(value, 0)) / math.log1p(max(upper, 1)))
