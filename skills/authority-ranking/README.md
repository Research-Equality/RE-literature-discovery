# authority-ranking

Final authority-aware ranking layer for this repository.

Use this skill after search, merge, dedup, venue-authority resolution, and optional evidence grading. It is the only layer that should write `final_score` and `selection_bucket`.

Inputs:
- `outputs/<topic-slug>/paper_db.raw.jsonl` or `paper_db.triaged.jsonl`
- optional authority-enriched or evidence-enriched JSONL

Outputs:
- canonical `outputs/<topic-slug>/paper_db.jsonl`
- optional ranking summary markdown

Core command:

```bash
python skills/authority-ranking/scripts/rank_papers.py \
  --input outputs/<topic-slug>/paper_db.authority.jsonl \
  --output outputs/<topic-slug>/paper_db.jsonl \
  --query "QUERY" \
  --profile cs \
  --summary outputs/<topic-slug>/analysis/ranking_summary.md
```
