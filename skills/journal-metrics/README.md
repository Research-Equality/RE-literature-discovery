# journal-metrics

Pluggable journal metric resolver for quartiles, impact factor, and generic journal core rank.

The bundled metrics file is intentionally a starter sample for wiring and local tests. Replace it with a current licensed export or internal source when accuracy matters.

```bash
python skills/journal-metrics/scripts/enrich_journal_metrics.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.journal.jsonl
```
