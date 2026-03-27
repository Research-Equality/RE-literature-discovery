# journal-metrics examples

Bundled starter metrics file:
- [`/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/skills/journal-metrics/references/journal_metrics.sample.json`](/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/skills/journal-metrics/references/journal_metrics.sample.json)

Minimal command:

```bash
python skills/journal-metrics/scripts/enrich_journal_metrics.py \
  --input examples/authority-aware-minimal/paper_db.triaged.jsonl \
  --output examples/authority-aware-minimal/paper_db.journal.jsonl
```
