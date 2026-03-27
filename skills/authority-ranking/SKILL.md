---
name: authority-ranking
description: Compute the repository's single auditable authority-aware final_score and selection_bucket after metadata enrichment. Use when ranking a corpus for review writing or systematic review curation, and when you need explainable score components and analysis artifacts.
argument-hint: [paper-db]
---

# Authority Ranking

This is the only final ranking layer in the repository.

## Responsibilities

- write `final_score`
- assign `selection_bucket`
- write `authority_reason`
- write `ranking_components`
- write `ranking_profile`
- emit `ranking_report.md`
- emit `resolution_audit.jsonl`

## Inputs

- authority-enriched `paper_db.authority.jsonl`
- optional evidence-enriched corpus

## Outputs

- `outputs/<topic-slug>/paper_db.jsonl`
- `outputs/<topic-slug>/analysis/ranking_report.md`
- `outputs/<topic-slug>/analysis/resolution_audit.jsonl`

## Script

```bash
python skills/authority-ranking/scripts/rank_papers.py \
  --input outputs/<topic-slug>/paper_db.authority.jsonl \
  --output outputs/<topic-slug>/paper_db.jsonl \
  --query "QUERY" \
  --profile cs
```

If `evidence_score` is missing, the script uses the profile fallback. Re-run it after `evidence-grading` when you want refreshed final scores.

## Related Skills

- Upstream: [literature-search](../literature-search/), [venue-authority-resolver](../venue-authority-resolver/), [paper-quality-filter](../paper-quality-filter/), [field-ranking-profile](../field-ranking-profile/)
- Metadata companions: [ccf-ranking](../ccf-ranking/), [journal-metrics](../journal-metrics/)
- Downstream: [literature-review](../literature-review/), [systematic-review](../systematic-review/), [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
