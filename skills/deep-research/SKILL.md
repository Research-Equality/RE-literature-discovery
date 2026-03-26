---
name: deep-research
description: Conduct systematic academic literature reviews in 6 phases, producing structured notes, a curated paper database, and a synthesized final report. Output is organized by phase for clarity.
argument-hint: [topic]
---

# Deep Research

Run a six-phase literature review pipeline that moves from frontier discovery to a compiled report.

Command examples assume you are running from the repository root.

## Trigger

Activate this skill when the user wants to:
- research a topic in depth
- understand the state of the art in an area
- build a structured literature review or survey backbone
- collect papers, read them systematically, and synthesize conclusions

## Overview

This skill writes all artifacts under `outputs/{topic-slug}/` and enforces a strict phase order:

1. Frontier
2. Survey
3. Deep Dive
4. Code & Tools
5. Synthesis
6. Compilation

Do not skip phases. A final report built only from titles and abstracts is not acceptable.

## Phase Gate Protocol

Before starting Phase N+1, confirm Phase N already produced its required files.

| Phase | Required outputs before continuing |
|-------|------------------------------------|
| 1 -> 2 | `phase1_frontier/frontier.md` with >=10 papers |
| 2 -> 3 | `phase2_survey/survey.md` and `paper_db.jsonl` with 35-80 papers |
| 3 -> 4 | `phase3_deep_dive/selection.md` and `phase3_deep_dive/deep_dive.md` with detailed notes for >=8 papers |
| 4 -> 5 | `phase4_code/code_repos.md` with >=3 repositories |
| 5 -> 6 | `phase5_synthesis/synthesis.md` and `phase5_synthesis/gaps.md` |

After each phase, print a checkpoint:

```text
Phase N complete. Output: ...
```

## Source Quality Policy

Peer-reviewed conference and journal papers take priority over preprints.

Source priority:
1. Top conferences: NeurIPS, ICLR, ICML, ACL, EMNLP, NAACL, AAAI, IJCAI, CVPR, ICCV, ECCV, KDD, SIGIR, WWW, CoRL
2. Peer-reviewed journals: JMLR, TACL, Nature, Science, and domain journals
3. Workshops
4. arXiv preprints with clear impact
5. very recent preprints that have no reviewed version yet

When citing a non-peer-reviewed paper, mark it as `(preprint)`.

## Tools

Primary scripts in this repository:

- `skills/deep-research/scripts/search_semantic_scholar.py`
- `skills/deep-research/scripts/search_arxiv.py`
- `skills/literature-search/scripts/search_openalex.py`
- `skills/deep-research/scripts/paper_db.py`
- `skills/deep-research/scripts/download_papers.py`
- `skills/deep-research/scripts/extract_pdf.py`
- `skills/deep-research/scripts/bibtex_manager.py`
- `skills/deep-research/scripts/compile_report.py`

Optional helper:

- `paper_finder`, if you already maintain a local installation or wrapper for venue-specific scraping. Treat it as optional acceleration, not a hard dependency.

If Semantic Scholar rate limits matter, pass `--api-key "$S2_API_KEY"` to the relevant commands.

## 6-Phase Workflow

### Phase 1: Frontier

Goal: understand the newest directions in the area.

1. Create `outputs/{slug}/phase1_frontier/search_results/`
2. Search recent conference papers and preprints
3. Record frontier signals, notable papers, and active themes
4. Write `phase1_frontier/frontier.md`

Useful commands:

```bash
python skills/deep-research/scripts/search_semantic_scholar.py \
  --query "TOPIC" \
  --year-range 2024-2026 \
  --max-results 30 \
  --peer-reviewed-only \
  --api-key "$S2_API_KEY" \
  -o outputs/{slug}/phase1_frontier/search_results/s2_frontier.jsonl

python skills/deep-research/scripts/search_arxiv.py \
  --query "TOPIC" \
  --max-results 20 \
  -o outputs/{slug}/phase1_frontier/search_results/arxiv_frontier.jsonl
```

### Phase 2: Survey

Goal: build the broad paper landscape and curate a stable paper database.

1. Search across Semantic Scholar, arXiv, and OpenAlex
2. Merge results into one `paper_db.jsonl`
3. Filter to 35-80 papers
4. Cluster them by theme and write `phase2_survey/survey.md`

Useful commands:

```bash
python skills/literature-search/scripts/search_openalex.py \
  --query "TOPIC" \
  --year-range 2020-2026 \
  --max-results 40 \
  -o outputs/{slug}/phase2_survey/search_results/openalex.jsonl

python skills/deep-research/scripts/paper_db.py merge \
  --inputs \
  outputs/{slug}/phase1_frontier/search_results/s2_frontier.jsonl \
  outputs/{slug}/phase1_frontier/search_results/arxiv_frontier.jsonl \
  outputs/{slug}/phase2_survey/search_results/openalex.jsonl \
  --output outputs/{slug}/paper_db.jsonl

python skills/deep-research/scripts/paper_db.py filter \
  --input outputs/{slug}/paper_db.jsonl \
  --output outputs/{slug}/paper_db.jsonl \
  --min-score 0.80 \
  --max-papers 70
```

### Phase 3: Deep Dive

Goal: read 8-15 representative papers in detail.

1. Select papers and justify the selection in `phase3_deep_dive/selection.md`
2. Download PDFs
3. Read full papers, not just abstracts
4. Write structured notes covering problem, method, experiments, limitations, and links
5. Save everything to `phase3_deep_dive/deep_dive.md`

Useful commands:

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

### Phase 4: Code & Tools

Goal: map the implementation ecosystem around the papers you read.

1. Extract GitHub and benchmark links from Phase 3 notes
2. Search for repositories, datasets, and evaluation toolchains
3. Record repository quality, maintenance status, and relevance
4. Write `phase4_code/code_repos.md`

At least 3 concrete repositories should be captured.

### Phase 5: Synthesis

Goal: connect the papers into a coherent taxonomy.

Produce:
- `phase5_synthesis/synthesis.md`
- `phase5_synthesis/gaps.md`

Required content:
- taxonomy of approaches
- comparative discussion across papers
- contradictions or unresolved questions
- open problems and future directions

This phase must build on full-paper reading from Phase 3 and repo mapping from Phase 4.

### Phase 6: Compilation

Goal: assemble the final report and bibliography.

Useful commands:

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

## Output Structure

```text
outputs/{topic-slug}/
├── paper_db.jsonl
├── phase1_frontier/
│   ├── search_results/
│   └── frontier.md
├── phase2_survey/
│   ├── search_results/
│   └── survey.md
├── phase3_deep_dive/
│   ├── papers/
│   ├── texts/
│   ├── selection.md
│   └── deep_dive.md
├── phase4_code/
│   └── code_repos.md
├── phase5_synthesis/
│   ├── synthesis.md
│   └── gaps.md
└── phase6_report/
    ├── report.md
    └── references.bib
```

## Key Conventions

- Prefer `arxiv_id` when available, otherwise use `paperId`
- Use `[@key]` citations while drafting notes
- Mark non-peer-reviewed evidence as `(preprint)`
- Save after each phase rather than keeping work only in chat
- Keep the final `paper_db.jsonl` curated; bigger is not always better

## References

- `references/workflow-phases.md` — detailed phase guide
- `references/note-format.md` — note templates and report structure
- `references/api-reference.md` — API usage and retrieval patterns

## Related Skills

- Downstream: [literature-search](../literature-search/), [literature-review](../literature-review/), [citation-management](../citation-management/)
- See also: [survey-generation](../survey-generation/)
