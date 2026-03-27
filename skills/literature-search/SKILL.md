---
name: literature-search
description: Default discovery skill for academic search, merge, deduplication, and early triage. Use it to build a reusable paper corpus from search results, then hand the corpus to the authority-aware ranking layer. Do not use it as the final ranking or writing stage.
argument-hint: [search-query]
---

# Literature Search

This is the repository's discovery entry point.

## Responsibilities

- search external sources
- normalize source outputs into shared JSONL
- merge and deduplicate records
- do early relevance triage
- hand the corpus to the authority layer

This skill no longer owns final ranking logic. `authority-ranking` is the only layer that writes `final_score` and `selection_bucket`.

## Canonical Outputs

- `outputs/<topic-slug>/search_results/<source>.jsonl`
- `outputs/<topic-slug>/paper_db.raw.jsonl`
- `outputs/<topic-slug>/paper_db.triaged.jsonl`
- initial authority-ranked `outputs/<topic-slug>/paper_db.jsonl`

After `evidence-grading`, re-run `authority-ranking` to refresh the canonical `paper_db.jsonl`.

## Recommended Flow

1. search one or more sources
2. normalize wrapped JSON if needed
3. merge and deduplicate
4. apply rough lexical triage
5. call `venue-authority-resolver`
6. call `paper-quality-filter`
7. call `authority-ranking`
8. later, after `evidence-grading`, refresh ranking again

## Scripts

Search:

```bash
python skills/systematic-review/scripts/search_semantic_scholar.py \
  --query "QUERY" \
  --max-results 30 \
  --output outputs/<topic-slug>/search_results/s2.jsonl
```

Normalize source-specific JSON:

```bash
python skills/literature-search/scripts/normalize_search_results.py \
  --source arxiv-database \
  --input raw.json \
  --output outputs/<topic-slug>/search_results/arxiv.jsonl
```

Prepare the corpus and hand it to the authority layer:

```bash
python skills/literature-search/scripts/prepare_corpus.py \
  --query "QUERY" \
  --inputs outputs/<topic-slug>/search_results/*.jsonl \
  --merged-output outputs/<topic-slug>/paper_db.raw.jsonl \
  --triaged-output outputs/<topic-slug>/paper_db.triaged.jsonl \
  --authority-output outputs/<topic-slug>/paper_db.jsonl \
  --profile cs
```

## Related Skills

- Source companions: [arxiv-database](../arxiv-database/), [biorxiv-database](../biorxiv-database/), [openalex-database](../openalex-database/), [pubmed-database](../pubmed-database/)
- Authority layer: [venue-authority-resolver](../venue-authority-resolver/), [paper-quality-filter](../paper-quality-filter/), [authority-ranking](../authority-ranking/), [field-ranking-profile](../field-ranking-profile/)
- Downstream: [literature-review](../literature-review/), [systematic-review](../systematic-review/)
