---
name: systematic-review
description: Run an end-to-end systematic literature review pipeline from search to compiled report while writing durable artifacts under outputs/{topic-slug}/. Use when the user wants a managed review workspace, not only quick discovery or a single written section.
argument-hint: [topic]
---

# Systematic Review

This is the repository's heaviest orchestration skill.

## Phase Structure

1. Frontier
2. Survey
3. Deep Dive
4. Code & Tools
5. Synthesis
6. Compilation

## Authority-Aware Update

Phase 2 must now produce four canonical artifacts:

- `outputs/{topic-slug}/paper_db.raw.jsonl`
- `outputs/{topic-slug}/paper_db.triaged.jsonl`
- `outputs/{topic-slug}/paper_db.evidence.jsonl`
- canonical ranked `outputs/{topic-slug}/paper_db.jsonl`

Recommended sequence inside Phase 2:

1. search sources into `search_results/`
2. merge and deduplicate
3. early triage
4. resolve venue authority metadata
5. attach quality flags
6. rank with `authority-ranking`
7. grade evidence
8. refresh ranking with the evidence-enriched corpus

## Shared Handoff Files

- `outputs/{topic-slug}/paper_db.jsonl`
- `outputs/{topic-slug}/analysis/evidence_summary.md`
- `outputs/{topic-slug}/phase5_synthesis/`
- `outputs/{topic-slug}/phase6_report/references.bib`

## Phase Gate

Do not enter Phase 3 until `paper_db.jsonl` exists, has passed the evidence pass, and has been reranked.

## Embedded Maintenance Modes

This skill now absorbs the repository's corpus-maintenance patterns:

- citation-graph expansion and reading-gap discovery
- ongoing arXiv monitoring for a defined topic

Use `references/corpus-maintenance.md` when the task is incremental monitoring or corpus expansion rather than first-pass search.

## Core Commands

```bash
python skills/literature-search/scripts/prepare_corpus.py \
  --query "TOPIC" \
  --inputs outputs/{topic-slug}/phase2_survey/search_results/*.jsonl \
  --merged-output outputs/{topic-slug}/paper_db.raw.jsonl \
  --triaged-output outputs/{topic-slug}/paper_db.triaged.jsonl \
  --authority-output outputs/{topic-slug}/paper_db.jsonl \
  --profile cs
```

```bash
python skills/evidence-grading/scripts/grade_evidence.py \
  --input outputs/{topic-slug}/paper_db.jsonl \
  --output outputs/{topic-slug}/paper_db.evidence.jsonl
```

```bash
python skills/authority-ranking/scripts/rank_papers.py \
  --input outputs/{topic-slug}/paper_db.evidence.jsonl \
  --output outputs/{topic-slug}/paper_db.jsonl \
  --query "TOPIC" \
  --profile cs
```

## Related Skills

- Upstream/discovery: [literature-search](../literature-search/)
- Authority layer: [venue-authority-resolver](../venue-authority-resolver/), [paper-quality-filter](../paper-quality-filter/), [authority-ranking](../authority-ranking/), [evidence-grading](../evidence-grading/)
- Downstream writing: [literature-review](../literature-review/), [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
