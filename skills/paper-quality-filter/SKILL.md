---
name: paper-quality-filter
description: Attach quality_flags and caution_flags such as preprint_only and weak_metadata, and optionally filter by peer review, preprint status, year, or metadata completeness. Use after venue-authority-resolver and before authority-ranking.
argument-hint: [paper-db]
---

# Paper Quality Filter

Use this skill to turn authority metadata into auditable keep/drop signals before final ranking.

## Responsibilities

- add `quality_flags`
- add `caution_flags`
- surface `preprint_only` and `weak_metadata`
- optionally exclude papers by peer-review or preprint policy
- preserve records for later writing when you only want caution labels

`weak_metadata` means structural metadata weakness such as missing abstract/year/venue or a near-total lack of authority signals. It must not be used as a synonym for "one authority resolver did not match".

## Script

```bash
python skills/paper-quality-filter/scripts/apply_quality_filter.py \
  --input outputs/<topic-slug>/paper_db.authority.jsonl \
  --output outputs/<topic-slug>/paper_db.filtered.jsonl
```

## Related Skills

- Upstream: [venue-authority-resolver](../venue-authority-resolver/)
- Downstream: [authority-ranking](../authority-ranking/), [evidence-grading](../evidence-grading/)
