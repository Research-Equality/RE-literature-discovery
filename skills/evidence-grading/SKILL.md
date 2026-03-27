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

## Output Policy

After this step, re-run `authority-ranking` so `final_score`, `selection_bucket`, `ranking_report.md`, and `resolution_audit.jsonl` all reflect the new evidence score.

## Script

```bash
python skills/evidence-grading/scripts/grade_evidence.py \
  --input outputs/<topic-slug>/paper_db.jsonl \
  --output outputs/<topic-slug>/paper_db.evidence.jsonl \
  --summary outputs/<topic-slug>/analysis/evidence_summary.md
```

## Related Skills

- Upstream: [authority-ranking](../authority-ranking/), [paper-quality-filter](../paper-quality-filter/)
- Downstream: [literature-review](../literature-review/), [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
