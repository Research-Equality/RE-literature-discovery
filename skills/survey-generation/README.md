# survey-generation

Bucket-aware survey manuscript planning from an authority-aware corpus.

Writing tones:
- `core`: canonical / backbone
- `supporting`: comparative / supportive
- `frontier`: cautious / tentative

Frontier papers must never be written as established consensus.

Planning helper:

```bash
python skills/survey-generation/scripts/plan_bucketed_survey.py \
  --topic "TOPIC" \
  --input outputs/<topic-slug>/paper_db.jsonl \
  --output outputs/<topic-slug>/survey/writing_guidance.md
```
