---
name: journal-metrics
description: Enrich journal papers with pluggable quartile and impact-factor metadata before authority-aware ranking. Use when journal authority matters and you want a source that can be swapped without changing the rest of the workflow.
argument-hint: [paper-db]
---

# Journal Metrics

Use this skill to attach `jcr_quartile`, `impact_factor`, `cas_quartile`, and optional `core_rank`.

## Design Rule

Keep journal metrics pluggable. The rest of the repository should depend on the fields, not on one specific metric source.

## Script

```bash
python skills/journal-metrics/scripts/enrich_journal_metrics.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.journal.jsonl
```

With a custom metrics file:

```bash
python skills/journal-metrics/scripts/enrich_journal_metrics.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.journal.jsonl \
  --metrics-file path/to/current_journal_metrics.json
```

## Related Skills

- Upstream: [field-ranking-profile](../field-ranking-profile/)
- Downstream: [venue-authority-resolver](../venue-authority-resolver/), [authority-ranking](../authority-ranking/)
