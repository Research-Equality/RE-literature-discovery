# paper-quality-filter

Metadata-only quality gating and caution flagging layer.

This skill flags missing abstracts, missing venue/year, preprints, and other review-salient quality issues. It can optionally filter out records before final ranking.

```bash
python skills/paper-quality-filter/scripts/apply_quality_filter.py \
  --input outputs/<topic-slug>/paper_db.authority.jsonl \
  --output outputs/<topic-slug>/paper_db.filtered.jsonl
```
