---
name: paper-quality-filter
description: Attach quality_flags and caution_flags to a paper corpus and optionally filter by peer review, preprint status, year, or metadata completeness. Use after venue-authority-resolver and before authority-ranking.
argument-hint: [paper-db]
---

# Paper Quality Filter

Use this skill to turn authority metadata into auditable keep/drop signals before final ranking.

## Responsibilities

- add `quality_flags`
- add `caution_flags`
- optionally exclude papers by peer-review or preprint policy
- preserve records for later writing when you only want caution labels

## Script

```bash
python skills/paper-quality-filter/scripts/apply_quality_filter.py \
  --input outputs/<topic-slug>/paper_db.authority.jsonl \
  --output outputs/<topic-slug>/paper_db.filtered.jsonl
```

Optional filters:

```bash
python skills/paper-quality-filter/scripts/apply_quality_filter.py \
  --input outputs/<topic-slug>/paper_db.authority.jsonl \
  --output outputs/<topic-slug>/paper_db.filtered.jsonl \
  --peer-reviewed-only \
  --exclude-preprints
```

## Related Skills

- Upstream: [venue-authority-resolver](../venue-authority-resolver/)
- Downstream: [authority-ranking](../authority-ranking/), [evidence-grading](../evidence-grading/)
