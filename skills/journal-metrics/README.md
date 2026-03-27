# journal-metrics

Auditable journal metric resolver for authority-aware literature review.

This skill now uses three layers:
- `data/journal_source_of_record.json`
- `data/journal_open_fallback.json`
- `--local-override` for operator-supplied CSV/JSON overrides

Key output fields:
- `jcr_quartile`
- `impact_factor`
- `cas_quartile`
- `metric_source`
- `metric_year`
- `metric_license_note`
- `is_official_metric`
- `journal_metric_warnings`

Core command:

```bash
python skills/journal-metrics/scripts/resolve_journal_metrics.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.journal.jsonl
```
