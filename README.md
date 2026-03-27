[English](README.md) | [简体中文](README.zh.md)

# RE-literature-discovery

An authoritative skills repository for literature discovery, evidence synthesis, and survey writing.

This repository focuses on the core academic literature workflow: search, reading, synthesis, citation management, database lookup, related work writing, and full survey generation. It is not a general end-to-end research toolkit. It is a curated home for skills directly related to literature discovery, literature review, and survey writing.

## Positioning

- Keep only skills related to literature research, survey writing, citation work, and scholarly source discovery
- Normalize everything into a portable repository layout without depending on one author's local machine
- Serve as the authoritative home for future literature-review-related skills

## Included Skills

The skill collection lives under [`skills/`](skills/).

### Workflow Skills

- `literature-search`: multi-source academic search with structured JSONL and BibTeX output
- `literature-review`: multi-perspective review and knowledge synthesis
- `systematic-review`: a six-phase systematic literature review pipeline
- `citation-management`: BibTeX harvesting, validation, deduplication, and repair
- `related-work-writing`: Related Work writing workflows
- `survey-generation`: full survey paper generation

### Database and Reference Skills

- `arxiv-database`: arXiv preprint search and PDF retrieval
- `biorxiv-database`: bioRxiv preprint search for life-science literature
- `openalex-database`: OpenAlex queries for scholarly search and bibliometrics
- `pubmed-database`: direct PubMed query construction and E-utilities workflows
- `pyzotero`: Zotero library automation and reference management integration

### Monitoring and Analysis Skills

- `arxiv-monitor`: recurring arXiv surveillance and digest generation
- `citation-graph`: citation-network analysis for foundational and bridge papers
- `gap-detection`: open-question and novelty-opportunity analysis
- `claim-tracker`: claim-level provenance and status tracking
- `consensus-mapping`: mapping settled versus contested claims
- `contradiction-detection`: identifying and structuring conflicting findings
- `cross-paper-synthesis`: comparison tables, timelines, and through-line synthesis
- `evidence-grading`: grading claim and paper strength for calibrated writing

See [`skills/README.md`](skills/README.md) for the skill catalog.

## Skill Routing

To avoid overlap, the repository uses a layered workflow:

- `literature-search` is the default entry point for multi-source paper discovery
- `arxiv-database`, `biorxiv-database`, `openalex-database`, and `pubmed-database` are source-specific companions for advanced database tasks
- `arxiv-monitor` is the recurring watch layer after topic definition
- `systematic-review` is the end-to-end systematic review pipeline
- `literature-review` is the synthesis layer for an already collected corpus
- `citation-graph`, `gap-detection`, `claim-tracker`, `consensus-mapping`, `contradiction-detection`, `cross-paper-synthesis`, and `evidence-grading` are corpus-analysis companions
- `citation-management` and `pyzotero` are bibliography and library-management utilities
- `related-work-writing` writes one paper section
- `survey-generation` writes a full survey manuscript

Shared artifact conventions:

- `outputs/<topic-slug>/search_results/*.jsonl` for raw retrieval results
- `outputs/<topic-slug>/paper_db.jsonl` for the shared paper corpus
- `outputs/<topic-slug>/research_log.md` and `outputs/<topic-slug>/findings.md` for long-running review state
- `references.bib` for the active bibliography
- `outputs/<topic-slug>/review/`, `outputs/<topic-slug>/phase*/`, and `outputs/<topic-slug>/survey/` for downstream writing artifacts

## Repository Layout

```text
skills/
  arxiv-monitor/
  arxiv-database/
  biorxiv-database/
  citation-graph/
  claim-tracker/
  consensus-mapping/
  contradiction-detection/
  cross-paper-synthesis/
  openalex-database/
  pubmed-database/
  pyzotero/
  evidence-grading/
  gap-detection/
  literature-search/
  literature-review/
  systematic-review/
  citation-management/
  related-work-writing/
  survey-generation/
```

## Usage

Command examples assume you run them from the repository root.

```bash
python skills/systematic-review/scripts/search_semantic_scholar.py \
  --query "long-context reasoning agents" \
  --max-results 20 \
  --api-key "$S2_API_KEY"
```

Recommended environment:

- Python 3.10+
- Optional environment variable: `S2_API_KEY`
- Optional dependency: `PyMuPDF` for PDF extraction

Systematic review outputs are recommended to live under `outputs/<topic-slug>/` so the skill directories remain clean.

## ResearchClaw

This repository can also be used as an external skills source for [ResearchClaw](https://github.com/ymx10086/ResearchClaw).

When loading it there, treat this repository's [`skills/`](skills/) directory as the authoritative loadable skill set. The root README and skill catalog define the routing rules, shared artifacts, and role boundaries between skills.

## Curation Rules

- A skill must directly support literature discovery, reading, synthesis, citation work, or related work writing
- Skills for experiments, code implementation, paper formatting, or presentation should not live here
- Prefer skills that are scriptable, reusable, and auditable

## Provenance

The current skill set was curated and refactored from four local source snapshots:

- `agent-research-skills/`: workflow-oriented academic research skills
- `claude-scientific-skills/`: scientific database, citation, and scholarly tooling skills
- `PaperClaw/`: literature monitoring and corpus-analysis skills for research teams
- `AI-research-SKILLs/`: AI research orchestration and paper-writing skills

Only literature-review-related skills are retained. Overlapping capabilities were merged into the existing mainline skills instead of duplicated one-to-one. The normalized authoritative version is the one under [`skills/`](skills/).

Examples of merged overlaps:

- `PaperClaw/living-review` -> covered by `literature-review` plus `systematic-review`
- `PaperClaw/semantic-scholar` -> covered by `literature-search` and `systematic-review` search tooling
- `PaperClaw/zotero-integration` -> covered by `pyzotero` plus `citation-management`
- `AI-research-SKILLs/autoresearch` -> distilled into `systematic-review` workspace discipline and resumable review templates
- `AI-research-SKILLs/ml-paper-writing` -> distilled into `citation-management`, `related-work-writing`, and `survey-generation` citation-verification rules
