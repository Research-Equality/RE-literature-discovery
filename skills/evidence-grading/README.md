# evidence-grading

Evidence calibration layer for downstream writing.

This skill reads authority-aware metadata but does not equate venue prestige with evidence strength. It writes:
- `evidence_score`
- `evidence_label`
- caution flags such as `high_authority_low_evidence`

It should usually be followed by a second `authority-ranking` pass so `final_score` and `selection_bucket` reflect the new evidence score.

```bash
python skills/evidence-grading/scripts/grade_evidence.py \
  --input outputs/<topic-slug>/paper_db.jsonl \
  --output outputs/<topic-slug>/paper_db.evidence.jsonl \
  --summary outputs/<topic-slug>/analysis/evidence_summary.md
```
