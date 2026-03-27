---
name: field-ranking-profile
description: Resolve field-specific ranking profiles that control authority-aware scoring weights, bucket thresholds, and recency policy. Use when ranking logic should differ between CS, biomedical, or general literature review workflows.
argument-hint: [field-name]
---

# Field Ranking Profile

Use this skill to decide how authority-aware ranking should behave for one field.

## Bundled Profiles

- `cs`: conference-heavy, CCF-first
- `biomedicine`: journal-heavy, quartile-first
- `general`: balanced mixed-domain profile

## Script

```bash
python skills/field-ranking-profile/scripts/get_profile.py --profile cs
```

You can also pass a custom `--profile-file` to `authority-ranking`.

## Related Skills

- Upstream: [literature-search](../literature-search/)
- Downstream: [authority-ranking](../authority-ranking/), [ccf-ranking](../ccf-ranking/), [journal-metrics](../journal-metrics/)
