---
name: literature-review
description: Synthesize an already collected, authority-aware paper corpus into a focused literature review. Use after discovery and ranking when the goal is thematic review writing, evidence-aware synthesis, and gap analysis rather than raw search or full survey-manuscript generation.
argument-hint: [topic]
---

# Literature Review

This skill turns a ranked corpus into a coherent review bundle.

## Recommended Inputs

- `outputs/<topic-slug>/paper_db.jsonl` or `paper_db.evidence.jsonl`
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
- mention `watchlist` papers only when frontier context matters, especially for preprints

Do not treat high authority as a substitute for evidence. When authority is high but evidence is exploratory, write with caution.

## Outputs

- `outputs/<topic-slug>/review/review_outline.md`
- `outputs/<topic-slug>/review/review.md`
- `outputs/<topic-slug>/review/evidence_table.md`
- `outputs/<topic-slug>/review/gaps.md`

## Related Skills

- Upstream: [literature-search](../literature-search/), [authority-ranking](../authority-ranking/), [evidence-grading](../evidence-grading/), [systematic-review](../systematic-review/)
- Downstream: [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
