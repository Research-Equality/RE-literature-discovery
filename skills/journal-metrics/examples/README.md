# journal-metrics examples

Bundled metric layers:
- [`/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/skills/journal-metrics/data/journal_source_of_record.json`](/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/skills/journal-metrics/data/journal_source_of_record.json)
- [`/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/skills/journal-metrics/data/journal_open_fallback.json`](/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/skills/journal-metrics/data/journal_open_fallback.json)

Resolve one corpus:

```bash
python skills/journal-metrics/scripts/resolve_journal_metrics.py \
  --input examples/authority-aware-minimal/paper_db.triaged.jsonl \
  --output examples/authority-aware-minimal/paper_db.journal.jsonl
```
