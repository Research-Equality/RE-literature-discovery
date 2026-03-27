# venue-authority-resolver

Resolve venue authority metadata before ranking.

This skill standardizes `venue_type`, `peer_reviewed`, `is_preprint`, `ccf_rank`, `core_rank`, `jcr_quartile`, `impact_factor`, and `cas_quartile`. It does not write `final_score`.

```bash
python skills/venue-authority-resolver/scripts/resolve_authority.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.authority.jsonl
```
