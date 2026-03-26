# Research Workflow: Detailed Phase Guide

Execute all 6 phases in strict order: `1 -> 2 -> 3 -> 4 -> 5 -> 6`.

All outputs should live under `outputs/{topic-slug}/`.

## Phase 1: Frontier

Objective: identify the newest directions and leading papers.

Write to:
- `phase1_frontier/search_results/`
- `phase1_frontier/frontier.md`

Checklist:
- search the latest 1-2 years first
- prefer reviewed venues
- include a small number of recent preprints if the field is moving fast
- summarize trends, not just paper titles

Gate to Phase 2:
- `phase1_frontier/frontier.md` exists
- it contains at least 10 papers or signals worth tracking

## Phase 2: Survey

Objective: build a curated database of 35-80 papers spanning foundational and recent work.

Typical commands:

```bash
python skills/deep-research/scripts/search_semantic_scholar.py \
  --query "TOPIC" \
  --max-results 50 \
  --year-range 2020-2026 \
  --peer-reviewed-only \
  --api-key "$S2_API_KEY" \
  -o outputs/{slug}/phase2_survey/search_results/s2.jsonl

python skills/literature-search/scripts/search_openalex.py \
  --query "TOPIC" \
  --max-results 40 \
  --year-range 2020-2026 \
  -o outputs/{slug}/phase2_survey/search_results/openalex.jsonl
```

Then:

```bash
python skills/deep-research/scripts/paper_db.py merge \
  --inputs outputs/{slug}/phase1_frontier/search_results/s2_frontier.jsonl \
  outputs/{slug}/phase2_survey/search_results/s2.jsonl \
  outputs/{slug}/phase2_survey/search_results/openalex.jsonl \
  --output outputs/{slug}/paper_db.jsonl

python skills/deep-research/scripts/paper_db.py filter \
  --input outputs/{slug}/paper_db.jsonl \
  --output outputs/{slug}/paper_db.jsonl \
  --min-score 0.80 \
  --max-papers 70
```

Gate to Phase 3:
- `phase2_survey/survey.md` exists
- `paper_db.jsonl` is curated down to 35-80 papers

## Phase 3: Deep Dive

Objective: read 8-15 papers in detail.

Selection criteria:
- foundational impact
- recent momentum
- thematic diversity
- methodology diversity

Typical commands:

```bash
python skills/deep-research/scripts/download_papers.py \
  --jsonl outputs/{slug}/paper_db.jsonl \
  --output-dir outputs/{slug}/phase3_deep_dive/papers \
  --sort-by-citations \
  --max-downloads 15

python skills/deep-research/scripts/extract_pdf.py \
  --pdf-dir outputs/{slug}/phase3_deep_dive/papers \
  --output-dir outputs/{slug}/phase3_deep_dive/texts \
  --sections-only
```

Each paper note should include:
- problem statement
- core contribution
- methodology
- experimental evidence
- limitations
- code or data links
- connections to neighboring papers

Gate to Phase 4:
- `phase3_deep_dive/selection.md` exists
- `phase3_deep_dive/deep_dive.md` has detailed notes for at least 8 papers

## Phase 4: Code & Tools

Objective: understand the implementation ecosystem.

Write `phase4_code/code_repos.md` with:
- repository URL
- stars or activity signal
- language and framework
- last update
- documentation quality
- relation to papers in the survey

Gate to Phase 5:
- at least 3 repositories are documented

## Phase 5: Synthesis

Objective: move from notes to insight.

Write:
- `phase5_synthesis/synthesis.md`
- `phase5_synthesis/gaps.md`

Expected content:
- taxonomy of approaches
- cross-paper comparison
- historical trajectory
- contradictions or evaluation weaknesses
- gaps and open problems

Gate to Phase 6:
- both synthesis files exist and are substantive

## Phase 6: Compilation

Objective: compile the final report and bibliography.

Typical commands:

```bash
python skills/deep-research/scripts/bibtex_manager.py \
  --jsonl outputs/{slug}/paper_db.jsonl \
  --output outputs/{slug}/phase6_report/references.bib

python skills/deep-research/scripts/compile_report.py \
  --topic-dir outputs/{slug}/
```

Expected outputs:
- `phase6_report/report.md`
- `phase6_report/references.bib`

## Quality Rules

- do not synthesize from abstracts alone
- do not over-collect papers without curating them
- prefer reviewed evidence when making strong claims
- keep notes and outputs on disk phase by phase
