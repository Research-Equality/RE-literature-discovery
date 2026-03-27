# paper-quality-filter

Metadata-only quality gating and caution flagging layer.

This skill flags:
- `preprint_only`
- `weak_metadata`
- missing abstract/year/venue
- other review-salient quality issues

`weak_metadata` is reserved for structurally weak records. It is not triggered merely because one authority source, such as CCF, does not cover the venue.

It can optionally filter records before final ranking, but it is also valid to keep them and pass the warnings downstream.

```bash
python skills/paper-quality-filter/scripts/apply_quality_filter.py \
  --input outputs/<topic-slug>/paper_db.authority.jsonl \
  --output outputs/<topic-slug>/paper_db.filtered.jsonl
```
