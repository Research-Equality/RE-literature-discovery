---
name: survey-generation
description: Generate a full survey manuscript from a curated authority-aware corpus, outline, and synthesis notes. Use when the deliverable is an end-to-end survey paper rather than quick review writing or bibliography cleanup.
argument-hint: [topic]
---

# Survey Generation

This is the repository's full-manuscript writing skill.

## Recommended Inputs

- `outputs/<topic-slug>/paper_db.evidence.jsonl` or ranked `paper_db.jsonl`
- `outputs/<topic-slug>/phase5_synthesis/synthesis.md` or `outputs/<topic-slug>/review/review.md`
- optional `references.bib`

## Section Planning Policy

- `core` papers define the main section backbone
- `supporting` papers extend comparisons and breadth
- `background` papers cover classic framing and historical transitions
- `watchlist` papers belong only in frontier, outlook, or cautionary sections unless you manually promote them

Use `authority_score` to decide which papers structure the survey. Use `evidence_score` and `caution_flags` to control claim strength and caveats.

## Citation Policy

- never fabricate citations
- if a record is unresolved, keep an explicit placeholder
- if provisional cite keys differ from final BibTeX keys, reconcile them with `citation-management`

## Related Skills

- Upstream: [systematic-review](../systematic-review/), [literature-review](../literature-review/), [authority-ranking](../authority-ranking/), [evidence-grading](../evidence-grading/)
- Final validation: [citation-management](../citation-management/)
- See also: [related-work-writing](../related-work-writing/)
