# related-work-writing

Draft one Related Work section from an authority-aware ranked corpus.

Use `selection_bucket` to decide what enters the section:
- `core`: anchor paragraphs
- `supporting`: breadth and comparison
- `background`: historical framing
- `watchlist`: frontier or preprint discussion only

```bash
python skills/related-work-writing/scripts/draft_related_work.py \
  --topic "TOPIC" \
  --input outputs/<topic-slug>/paper_db.evidence.jsonl \
  --output outputs/<topic-slug>/writing/related_work.md
```
