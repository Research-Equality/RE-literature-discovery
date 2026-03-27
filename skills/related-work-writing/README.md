# related-work-writing

Bucket-aware Related Work drafting from an authority-aware corpus.

Writing tones:
- `core`: canonical / backbone
- `supporting`: comparative / supportive
- `frontier`: cautious / tentative

Caution flags matter:
- `high_authority_low_evidence`
- `preprint_only`
- `weak_metadata`

Frontier papers must not be written as established consensus.

```bash
python skills/related-work-writing/scripts/draft_related_work.py \
  --topic "TOPIC" \
  --input outputs/<topic-slug>/paper_db.evidence.jsonl \
  --output outputs/<topic-slug>/writing/related_work.md
```
