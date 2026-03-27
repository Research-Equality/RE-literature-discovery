[English](README.md) | [简体中文](README.zh.md)

# RE-literature-discovery

An authoritative skills repository for literature discovery, authority-aware ranking, evidence synthesis, and survey writing.

This repository is organized as a layered literature workflow:
- discovery
- authority enrichment
- ranking
- evidence grading
- review writing
- survey writing

It is not a general research toolkit. It is the curated home for skills directly related to literature discovery, literature review, and survey generation.

## Positioning

- keep only literature-review-related skills
- normalize all outputs into a shared paper schema
- keep ranking auditable instead of burying logic inside one search script
- support ResearchClaw-compatible external skill loading from `skills/`

## Authority-Aware Workflow

Recommended chain:

1. `literature-search`
2. `venue-authority-resolver`
3. `paper-quality-filter`
4. `authority-ranking`
5. `evidence-grading`
6. `literature-review` or `systematic-review`
7. `related-work-writing` or `survey-generation`

`authority-ranking` is the only layer that should write `final_score`.

## Included Skills

The skill collection lives under [`skills/`](skills/).

### Discovery and Workflow

- `literature-search`
- `literature-review`
- `systematic-review`
- `citation-management`
- `related-work-writing`
- `survey-generation`

### Authority and Ranking

- `venue-authority-resolver`
- `authority-ranking`
- `ccf-ranking`
- `journal-metrics`
- `paper-quality-filter`
- `field-ranking-profile`

### Databases and Reference Management

- `arxiv-database`
- `biorxiv-database`
- `openalex-database`
- `pubmed-database`
- `pyzotero`

### Monitoring and Corpus Analysis

- `arxiv-monitor`
- `citation-graph`
- `gap-detection`
- `claim-tracker`
- `consensus-mapping`
- `contradiction-detection`
- `cross-paper-synthesis`
- `evidence-grading`

See [`skills/README.md`](skills/README.md) for the catalog.

## Shared Paper Schema

The canonical corpus file is `outputs/<topic-slug>/paper_db.jsonl`.

Each paper record should contain at least:

- `paper_id`, `title`, `authors`, `year`, `venue`, `venue_type`, `doi`, `citation_count`
- `peer_reviewed`, `is_preprint`, `ccf_rank`, `core_rank`, `jcr_quartile`, `impact_factor`, `cas_quartile`
- `authority_score`, `relevance_score`, `citation_score`, `recency_score`, `evidence_score`, `final_score`
- `selection_bucket`, `ranking_reason`, `caution_flags`, `quality_flags`

The full JSON schema lives in [`skills/authority-ranking/schemas/paper_record.schema.json`](skills/authority-ranking/schemas/paper_record.schema.json).

## Shared Artifacts

- `outputs/<topic-slug>/search_results/*.jsonl`
- `outputs/<topic-slug>/paper_db.raw.jsonl`
- `outputs/<topic-slug>/paper_db.triaged.jsonl`
- `outputs/<topic-slug>/paper_db.jsonl`
- `outputs/<topic-slug>/paper_db.evidence.jsonl`
- `outputs/<topic-slug>/research_log.md`
- `outputs/<topic-slug>/findings.md`
- `references.bib`
- `outputs/<topic-slug>/review/`
- `outputs/<topic-slug>/phase*/`
- `outputs/<topic-slug>/survey/`

## Minimal Workflow Example

See [`examples/authority-aware-minimal/README.md`](examples/authority-aware-minimal/README.md).

Offline smoke test:

```bash
python skills/literature-search/scripts/prepare_corpus.py \
  --query "language model reasoning agents" \
  --inputs examples/authority-aware-minimal/seed_papers.jsonl \
  --merged-output outputs/authority-offline/paper_db.raw.jsonl \
  --triaged-output outputs/authority-offline/paper_db.triaged.jsonl \
  --authority-output outputs/authority-offline/paper_db.jsonl \
  --profile cs
```

## ResearchClaw

This repository can be used as an external skills source for [ResearchClaw](https://github.com/ymx10086/ResearchClaw).

When loading it there, treat this repository's [`skills/`](skills/) directory as the authoritative loadable skill set. The root README and skill catalog define routing rules, shared artifacts, and role boundaries.

## Curation Rules

- a skill must directly support literature discovery, authority-aware ranking, evidence synthesis, citation work, or survey writing
- experiment, implementation, formatting, or presentation skills should not live here
- prefer scriptable and auditable workflows

## Provenance

The repository was curated and refactored from:

- `agent-research-skills/`
- `claude-scientific-skills/`
- `PaperClaw/`
- `AI-research-SKILLs/`

Only literature-review-related capabilities are retained. The normalized authoritative version is the one under [`skills/`](skills/).
