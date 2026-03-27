#!/usr/bin/env python3
"""Normalize source-specific search outputs into the shared JSONL paper schema.

Usage:
    python normalize_search_results.py \
      --source arxiv-database \
      --input raw_arxiv.json \
      --output arxiv.jsonl

    python normalize_search_results.py \
      --source biorxiv-database \
      --input raw_biorxiv.json \
      --output biorxiv.jsonl
"""

import argparse
import json
import os
import sys
from pathlib import Path

AUTHORITY_SCRIPTS = Path(__file__).resolve().parents[2] / "authority-ranking" / "scripts"
if str(AUTHORITY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AUTHORITY_SCRIPTS))

from shared_schema import normalize_paper


def load_any_json(path: str):
    """Load JSON or JSONL from a file path."""
    with open(path, encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        return []

    if content[0] in "[{":
        return json.loads(content)

    records = []
    for line in content.splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records


def split_authors(value) -> list[str]:
    """Normalize author fields to a list of names."""
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]

    if not value:
        return []

    text = str(value).strip()
    separators = [";", " and ", "\n"]
    parts = [text]
    for sep in separators:
        if sep in text:
            parts = [p.strip() for p in text.split(sep)]
            break
    return [p for p in parts if p]


def extract_records(data) -> list[dict]:
    """Extract the list of records from common wrapper shapes."""
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("results"), list):
            return [item for item in data["results"] if isinstance(item, dict)]
        return [data]
    return []


def parse_year(*values) -> int | None:
    """Extract a 4-digit year from candidate values."""
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if len(text) >= 4 and text[:4].isdigit():
            return int(text[:4])
    return None


def normalize_arxiv_database(record: dict) -> dict:
    """Map arxiv-database JSON records into the shared paper schema."""
    published = record.get("published", "")
    year = parse_year(record.get("year"), published)
    return normalize_paper(
        {
            "paper_id": f"arxiv:{record.get('arxiv_id', '')}" if record.get("arxiv_id") else "",
            "arxiv_id": record.get("arxiv_id", ""),
            "doi": record.get("doi", ""),
            "title": record.get("title", ""),
            "authors": split_authors(record.get("authors", [])),
            "abstract": record.get("abstract", ""),
            "year": year,
            "published": published,
            "updated": record.get("updated", ""),
            "venue": record.get("journal_ref") or "arXiv",
            "venue_normalized": record.get("journal_ref") or "arXiv",
            "venue_type": "preprint",
            "peer_reviewed": False,
            "is_preprint": True,
            "citationCount": 0,
            "citation_count": 0,
            "categories": record.get("categories", []),
            "primary_category": record.get("primary_category", ""),
            "comment": record.get("comment", ""),
            "url": record.get("abs_url", ""),
            "pdf_url": record.get("pdf_url", ""),
            "source": "arxiv",
        }
    )


def normalize_biorxiv_database(record: dict) -> dict:
    """Map biorxiv-database JSON records into the shared paper schema."""
    publication_date = record.get("date", "") or record.get("published", "")
    year = parse_year(record.get("year"), publication_date)
    doi = record.get("doi", "")
    url = record.get("html_url", "")
    if not url and doi:
        url = f"https://doi.org/{doi}"
    return normalize_paper(
        {
            "paper_id": f"doi:{doi.lower()}" if doi else "",
            "doi": doi,
            "title": record.get("title", ""),
            "authors": split_authors(record.get("authors", "")),
            "abstract": record.get("abstract", ""),
            "year": year,
            "published": publication_date,
            "publicationDate": publication_date,
            "venue": "bioRxiv",
            "venue_normalized": "bioRxiv",
            "venue_type": "preprint",
            "peer_reviewed": False,
            "is_preprint": True,
            "citationCount": 0,
            "citation_count": 0,
            "category": record.get("category", ""),
            "version": record.get("version", ""),
            "url": url,
            "pdf_url": record.get("pdf_url", ""),
            "source": "biorxiv",
        }
    )


NORMALIZERS = {
    "arxiv-database": normalize_arxiv_database,
    "biorxiv-database": normalize_biorxiv_database,
}


def normalize_records(source: str, records: list[dict]) -> list[dict]:
    """Normalize all records for the selected source."""
    normalize = NORMALIZERS[source]
    normalized = []
    for record in records:
        item = normalize(record)
        if item.get("title"):
            normalized.append(item)
    return normalized


def save_jsonl(records: list[dict], path: str):
    """Write records as JSONL."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Normalize source-specific search outputs into shared JSONL paper records"
    )
    parser.add_argument(
        "--source",
        choices=sorted(NORMALIZERS),
        required=True,
        help="Source skill output format to normalize",
    )
    parser.add_argument("--input", required=True, help="Input JSON or JSONL file")
    parser.add_argument("--output", "-o", required=True, help="Output JSONL file")
    args = parser.parse_args()

    data = load_any_json(args.input)
    records = extract_records(data)
    normalized = normalize_records(args.source, records)
    save_jsonl(normalized, args.output)
    print(
        f"Normalized {len(records)} records from {args.source} -> {len(normalized)} records written to {args.output}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
