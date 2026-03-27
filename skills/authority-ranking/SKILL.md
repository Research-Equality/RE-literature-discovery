---
name: authority-ranking
description: Compute the repository's single authority-aware final_score and selection_bucket for papers after search, merge, and metadata enrichment. Use when ranking a corpus for review writing, systematic review curation, or downstream section drafting.
argument-hint: [paper-db]
---

# Authority Ranking

This skill is the only final ranking layer in the repository.

## Use This Skill For

- writing `final_score`
- assigning `selection_bucket`
- combining relevance, authority, citation, recency, and optional evidence metadata
- producing the canonical ranked `paper_db.jsonl`

## Do Not Use This Skill For

- raw search over external databases
- resolving venue metadata such as CCF or journal quartiles
- treating venue prestige as evidence strength

## Inputs

- `outputs/<topic-slug>/paper_db.raw.jsonl`
- `outputs/<topic-slug>/paper_db.triaged.jsonl`
- optional evidence-enriched JSONL

## Outputs

- `outputs/<topic-slug>/paper_db.jsonl`
- optional `outputs/<topic-slug>/analysis/ranking_summary.md`

## Script

```bash
python skills/authority-ranking/scripts/rank_papers.py \
  --input outputs/<topic-slug>/paper_db.authority.jsonl \
  --output outputs/<topic-slug>/paper_db.jsonl \
  --query "QUERY" \
  --profile cs
```

If `evidence_score` is missing, the script uses the profile's fallback evidence value. Re-run it after `evidence-grading` when you want refreshed final scores.

## Related Skills

- Upstream: [literature-search](../literature-search/), [venue-authority-resolver](../venue-authority-resolver/), [paper-quality-filter](../paper-quality-filter/), [field-ranking-profile](../field-ranking-profile/)
- Metadata companions: [ccf-ranking](../ccf-ranking/), [journal-metrics](../journal-metrics/)
- Downstream: [literature-review](../literature-review/), [systematic-review](../systematic-review/), [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
