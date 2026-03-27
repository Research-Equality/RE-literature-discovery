---
name: literature-review
description: Synthesize an already collected, authority-aware paper corpus into a focused literature review. Use after discovery and ranking when the goal is thematic review writing, evidence-aware synthesis, and gap analysis rather than raw search or full survey-manuscript generation.
argument-hint: [topic]
---

# Literature Review

This skill turns a ranked corpus into a coherent review bundle.

## Recommended Inputs

- canonical `outputs/<topic-slug>/paper_db.jsonl`
- optional intermediate `paper_db.evidence.jsonl` before reranking
- optional `references.bib`
- optional synthesis notes from `systematic-review`

Prefer a corpus that already includes:
- `selection_bucket`
- `authority_score`
- `evidence_score`
- `caution_flags`

## Review Policy

- use `core` papers to anchor major themes
- use `supporting` papers to widen comparisons
- use `background` papers for historical framing
- mention `frontier` papers only when emerging context matters, especially for preprints

Do not treat high authority as a substitute for evidence. When authority is high but evidence is exploratory, write with caution.

## Built-In Analysis Modes

This skill now subsumes the repo's lighter analysis patterns. Use it when you need any of the following without routing to a separate top-level skill:

- cross-paper comparison tables and synthesis notes
- consensus versus contested-claim mapping
- contradiction tracking
- claim-level provenance notes
- gap analysis and positioning

## Outputs

- `outputs/<topic-slug>/review/review_outline.md`
- `outputs/<topic-slug>/review/review.md`
- `outputs/<topic-slug>/review/evidence_table.md`
- `outputs/<topic-slug>/review/comparison_table.md`
- `outputs/<topic-slug>/review/consensus_map.md`
- `outputs/<topic-slug>/review/contradictions.md`
- `outputs/<topic-slug>/review/claim_registry.md`
- `outputs/<topic-slug>/review/gaps.md`

Read `references/analysis-modes.md` when the task is more analytical than narrative.

## Related Skills

- Upstream: [literature-search](../literature-search/), [authority-ranking](../authority-ranking/), [evidence-grading](../evidence-grading/), [systematic-review](../systematic-review/)
- Downstream: [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
