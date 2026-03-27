---
name: evidence-grading
description: Grade evidence strength for papers or claims using study-design and validation signals while reading authority-aware metadata as context. Use after authority-ranking when you need calibrated writing, and do not treat venue prestige as evidence strength.
argument-hint: [paper-db-or-claim]
---

# Evidence Grading

This skill calibrates how strongly a result should be trusted or stated in prose.

## Responsibilities

- write `evidence_score`
- write `evidence_label`
- add caution flags such as `high_authority_low_evidence`
- support claim wording in reviews, related work, and surveys

## Important Rule

Authority and evidence are not the same thing.

- `authority-ranking` uses venue and metadata signals to prioritize reading and selection
- `evidence-grading` uses design and validation signals to calibrate trust

High-prestige venues can still contain exploratory evidence. Strong evidence can also appear outside the highest-prestige venues.

## Inputs

- ranked `outputs/<topic-slug>/paper_db.jsonl`
- optional claim tables or contradiction maps

## Outputs

- `outputs/<topic-slug>/paper_db.evidence.jsonl`
- optional `outputs/<topic-slug>/analysis/evidence_summary.md`

## Script

```bash
python skills/evidence-grading/scripts/grade_evidence.py \
  --input outputs/<topic-slug>/paper_db.jsonl \
  --output outputs/<topic-slug>/paper_db.evidence.jsonl \
  --summary outputs/<topic-slug>/analysis/evidence_summary.md
```

If you want refreshed final scores that include the new `evidence_score`, run `authority-ranking` again after this step.

## Related Skills

- Upstream: [authority-ranking](../authority-ranking/), [paper-quality-filter](../paper-quality-filter/)
- Companions: [claim-tracker](../claim-tracker/), [consensus-mapping](../consensus-mapping/), [contradiction-detection](../contradiction-detection/)
- Downstream: [literature-review](../literature-review/), [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
