[English](README.md) | [简体中文](README.zh.md)

# RE-literature-discovery

An authoritative skills repository for literature discovery, authority-aware ranking, evidence synthesis, and survey writing.

The repository is organized around one synchronized workflow:

`literature-search -> venue-authority-resolver -> paper-quality-filter -> authority-ranking -> evidence-grading -> authority-ranking -> literature-review/systematic-review -> related-work-writing/survey-generation`

## Positioning

- keep only literature-review-related skills
- harden the authority layer around data source quality, auditability, and maintainability
- normalize all outputs into a shared paper schema
- keep ranking explainable instead of hiding it inside one search script
- support ResearchClaw-compatible loading from `skills/`

## Authority-Aware Workflow

### 1. Discovery

`literature-search` performs search, merge, deduplication, and early triage.

### 2. Venue and Metric Resolution

- `venue-authority-resolver` attaches authority metadata
- `ccf-ranking` uses `data/ccf_official_snapshot.json` and `data/ccf_aliases.json`
- `journal-metrics` resolves source-of-record, open fallback, and local override layers

### 3. Ranking and Audit

`authority-ranking` is the only layer that writes:
- `final_score`
- `selection_bucket`
- `authority_reason`
- `ranking_components`
- `ranking_profile`

It also writes:
- `outputs/<topic-slug>/analysis/ranking_report.md`
- `outputs/<topic-slug>/analysis/resolution_audit.jsonl`

### 4. Evidence, Reranking, and Writing

- `evidence-grading` reads authority metadata but does not equate venue prestige with evidence strength
- after `evidence-grading`, re-run `authority-ranking` so `final_score` and `selection_bucket` stay canonical
- `related-work-writing` and `survey-generation` use bucket-aware tone control:
  - `core`: canonical / backbone
  - `supporting`: comparative / supportive
  - `frontier`: cautious / tentative

Frontier papers must never be written as established consensus.

## Included Skills

Recommendation scale:
- `5/5`: default or critical for most literature-review workflows
- `4/5`: strong companion, commonly useful
- `3/5`: specialized or optional

### Discovery and Workflow

| Skill | Function | Reference Repo | Recommended |
| --- | --- | --- | --- |
| `literature-search` | Default entry point for search, merge, deduplication, and early triage | `agent-research-skills` | `5/5` |
| `evidence-grading` | Calibrate evidence strength without collapsing it into venue prestige | `PaperClaw` | `5/5` |
| `literature-review` | Turn a ranked corpus into a focused review bundle with built-in analysis modes | `agent-research-skills` | `5/5` |
| `systematic-review` | Run the end-to-end review workspace from search to compiled report | `agent-research-skills + AI-research-SKILLs` | `5/5` |
| `related-work-writing` | Draft one Related Work section with bucket-aware tone control | `agent-research-skills + AI-research-SKILLs` | `4/5` |
| `survey-generation` | Plan and draft a full survey manuscript from the canonical corpus | `agent-research-skills + AI-research-SKILLs` | `4/5` |

### Authority and Ranking

| Skill | Function | Reference Repo | Recommended |
| --- | --- | --- | --- |
| `venue-authority-resolver` | Normalize venue metadata and attach auditable authority provenance | `repository-native` | `5/5` |
| `authority-ranking` | Compute the repository's single canonical `final_score` and `selection_bucket` | `repository-native` | `5/5` |
| `ccf-ranking` | Resolve auditable CCF ranks for CS, AI, and security venues | `repository-native` | `5/5` |
| `journal-metrics` | Resolve journal quartiles and impact metrics through layered sources | `repository-native` | `4/5` |
| `paper-quality-filter` | Add quality and caution flags before final ranking | `repository-native` | `4/5` |
| `field-ranking-profile` | Switch ranking weights and thresholds by field | `repository-native` | `3/5` |

### Databases and Reference Management

| Skill | Function | Reference Repo | Recommended |
| --- | --- | --- | --- |
| `arxiv-database` | Run arXiv-specific search and retrieval workflows | `claude-scientific-skills` | `4/5` |
| `biorxiv-database` | Run bioRxiv-specific preprint search workflows | `claude-scientific-skills` | `3/5` |
| `openalex-database` | Query OpenAlex for source, author, and citation metadata | `claude-scientific-skills` | `4/5` |
| `pubmed-database` | Run PubMed and MEDLINE-specific biomedical search workflows | `claude-scientific-skills` | `4/5` |
| `citation-management` | Validate, repair, and generate BibTeX and cite keys | `agent-research-skills + AI-research-SKILLs` | `4/5` |
| `pyzotero` | Sync curated corpora with Zotero libraries and exports | `claude-scientific-skills` | `3/5` |

## Embedded Analysis Modes

This repository no longer keeps doc-only analysis skills as separate top-level routes.

The following capabilities are now embedded into `literature-review` and `systematic-review` as built-in analysis modes:

- comparison tables and cross-paper synthesis
- consensus versus contested-claim mapping
- contradiction and claim tracking
- gap detection and positioning
- citation-graph expansion and ongoing arXiv monitoring

See [`skills/README.md`](skills/README.md) for the catalog.

## Shared Paper Schema

The canonical corpus file is `outputs/<topic-slug>/paper_db.jsonl`.

Each paper record contains at least:

- bibliographic fields: `paper_id`, `title`, `authors`, `year`, `venue`, `venue_type`, `doi`, `citation_count`
- authority fields: `peer_reviewed`, `is_preprint`, `ccf_rank`, `core_rank`, `jcr_quartile`, `impact_factor`, `cas_quartile`
- score fields: `authority_score`, `relevance_score`, `citation_score`, `recency_score`, `evidence_score`, `final_score`
- writing-control fields: `selection_bucket`, `ranking_reason`, `caution_flags`, `quality_flags`
- audit fields: `source_of_truth`, `source_version`, `resolved_from`, `match_confidence`, `authority_reason`, `ranking_components`, `ranking_profile`, `last_verified_at`

The full JSON schema lives in [`skills/authority-ranking/schemas/paper_record.schema.json`](skills/authority-ranking/schemas/paper_record.schema.json).

## Shared Artifacts

- `outputs/<topic-slug>/search_results/*.jsonl`
- `outputs/<topic-slug>/paper_db.raw.jsonl`
- `outputs/<topic-slug>/paper_db.triaged.jsonl`
- `outputs/<topic-slug>/paper_db.jsonl`
- `outputs/<topic-slug>/paper_db.evidence.jsonl`
- `outputs/<topic-slug>/analysis/ranking_report.md`
- `outputs/<topic-slug>/analysis/resolution_audit.jsonl`
- `outputs/<topic-slug>/analysis/evidence_summary.md`
- `outputs/<topic-slug>/research_log.md`
- `outputs/<topic-slug>/findings.md`
- `references.bib`
- `outputs/<topic-slug>/review/`
- `outputs/<topic-slug>/phase*/`
- `outputs/<topic-slug>/survey/`

## Minimal Workflow Example

See [`examples/authority-aware-minimal/README.md`](examples/authority-aware-minimal/README.md).

## Environment and API Keys

Skills that benefit from external credentials now declare them in `SKILL.md` frontmatter under `requires.env`.

Suggested shared variables:

| Variable | Used By | Required | Purpose |
| --- | --- | --- | --- |
| `S2_API_KEY` | `literature-search`, `systematic-review`, `citation-management` | No | Higher Semantic Scholar rate limits |
| `OPENALEX_EMAIL` | `literature-search`, `openalex-database` | No | OpenAlex polite-pool email |
| `CROSSREF_EMAIL` | `literature-search` | No | Crossref User-Agent contact email |
| `NCBI_API_KEY` | `pubmed-database` | No | Higher PubMed E-utilities rate limits |
| `NCBI_EMAIL` | `pubmed-database` | No | Contact email for traceable PubMed automation |
| `ZOTERO_LIBRARY_ID` | `pyzotero` | Yes | Zotero target library id |
| `ZOTERO_API_KEY` | `pyzotero` | Yes | Zotero API key |
| `ZOTERO_LIBRARY_TYPE` | `pyzotero` | Yes | Zotero library type |

Copy [`.env.example`](.env.example) into your own local environment file or mirror these keys into your ResearchClaw env store.

## ResearchClaw

This repository can be used as an external skills source for [ResearchClaw](https://github.com/ymx10086/ResearchClaw).

When loading it there, treat this repository's [`skills/`](skills/) directory as the authoritative loadable skill set. The root README and skill catalog define routing rules, shared artifacts, and role boundaries.

For ResearchClaw integration, the key contract is:

- each skill exposes `requires.env` in `SKILL.md`
- ResearchClaw should read that metadata from `/api/skills`
- missing required or recommended variables should be surfaced before or immediately after enabling the skill

## Curation Rules

- a skill must directly support literature discovery, authority-aware ranking, evidence synthesis, citation work, or survey writing
- analysis patterns that do not need independent scripts should live inside `literature-review` or `systematic-review` references rather than as separate top-level skills
- experiment, implementation, formatting, or presentation skills should not live here
- prefer scriptable and auditable workflows
