# venue-authority-resolver

Resolve venue authority metadata before ranking.

This skill now delegates to:
- `ccf-ranking` for audited conference resolution
- `journal-metrics` for audited journal metric resolution

It standardizes:
- `venue_type`
- `peer_reviewed`
- `is_preprint`
- `ccf_rank`
- `jcr_quartile`
- audit fields such as `source_of_truth`, `resolved_from`, `match_confidence`, `last_verified_at`

This layer does not decide `weak_metadata` or final keep/drop policy. Those belong to `paper-quality-filter`.

```bash
python skills/venue-authority-resolver/scripts/resolve_authority.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.authority.jsonl
```
