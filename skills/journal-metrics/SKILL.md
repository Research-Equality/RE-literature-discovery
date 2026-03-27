---
name: journal-metrics
description: Resolve auditable journal metrics through source-of-record, open fallback, and local override layers before authority-aware ranking. Use when journal authority matters and missing or stale metrics must be surfaced explicitly.
argument-hint: [paper-db]
---

# Journal Metrics

Use this skill to attach auditable journal metrics rather than opaque quartile values.

## Resolution Layers

1. source of record: licensed or manually maintained authoritative export
2. open fallback: lower-trust open metric source
3. local override: operator-supplied CSV or JSON

Override data takes precedence when present, but the chosen source is always written into the record.

## Output Fields

- `jcr_quartile`
- `impact_factor`
- `cas_quartile`
- `metric_source`
- `metric_year`
- `metric_license_note`
- `is_official_metric`
- `journal_metric_warnings`

Missing, stale, ambiguous, or low-confidence metrics must emit warnings.

## Script

```bash
python skills/journal-metrics/scripts/resolve_journal_metrics.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.journal.jsonl
```

With a local override:

```bash
python skills/journal-metrics/scripts/resolve_journal_metrics.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.journal.jsonl \
  --local-override path/to/journal_override.csv
```

## Related Skills

- Upstream: [field-ranking-profile](../field-ranking-profile/)
- Downstream: [venue-authority-resolver](../venue-authority-resolver/), [authority-ranking](../authority-ranking/)
