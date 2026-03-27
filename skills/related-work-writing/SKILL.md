---
name: related-work-writing
description: Write or revise the Related Work section of a specific paper from an authority-aware corpus, synthesis notes, and bibliography. Use for positioning one contribution against prior work, not for initial discovery or full survey generation.
argument-hint: [paper-draft]
---

# Related Work Writing

This skill writes one section, not a full manuscript.

## Recommended Inputs

- current paper draft or contribution summary
- `outputs/<topic-slug>/paper_db.evidence.jsonl` or ranked `paper_db.jsonl`
- optional `outputs/<topic-slug>/review/review.md` or `phase5_synthesis/synthesis.md`
- optional `references.bib`

## Selection Policy

- `core`: anchor paragraphs and main comparisons
- `supporting`: widen the landscape and sharpen contrasts
- `background`: brief historical framing
- `watchlist`: frontier discussion only, usually with explicit caution for preprints

Use `authority_score` to decide what deserves space. Use `evidence_score` to decide how strongly to phrase claims.

## Script

```bash
python skills/related-work-writing/scripts/draft_related_work.py \
  --topic "TOPIC" \
  --input outputs/<topic-slug>/paper_db.evidence.jsonl \
  --output outputs/<topic-slug>/writing/related_work.md
```

## Rules

- do not cite every high-authority paper if it is not relevant to the contribution
- do not overstate weak or exploratory evidence even if venue authority is high
- if a citation key is provisional, reconcile it with `citation-management` before final submission

## Related Skills

- Upstream: [literature-review](../literature-review/), [systematic-review](../systematic-review/), [authority-ranking](../authority-ranking/), [evidence-grading](../evidence-grading/)
- Final validation: [citation-management](../citation-management/)
