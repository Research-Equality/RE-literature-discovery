# authority-ranking

Final authority-aware ranking layer for this repository.

This skill is the only layer that should write:
- `final_score`
- `selection_bucket`
- `authority_reason`
- `ranking_components`
- `ranking_profile`

It also produces:
- `outputs/<topic-slug>/analysis/ranking_report.md`
- `outputs/<topic-slug>/analysis/resolution_audit.jsonl`

Core command:

```bash
python skills/authority-ranking/scripts/rank_papers.py \
  --input outputs/<topic-slug>/paper_db.authority.jsonl \
  --output outputs/<topic-slug>/paper_db.jsonl \
  --query "QUERY" \
  --profile cs
```
