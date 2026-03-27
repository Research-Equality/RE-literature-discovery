# Authority-Aware Minimal Workflow

This example shows the intended chain:

1. query
2. search
3. authority enrichment
4. ranking
5. evidence grading
6. related work draft

## Live Search Path

```bash
mkdir -p outputs/authority-demo/search_results outputs/authority-demo/analysis outputs/authority-demo/writing

python skills/systematic-review/scripts/search_semantic_scholar.py \
  --query "language model reasoning agents" \
  --max-results 20 \
  --output outputs/authority-demo/search_results/s2.jsonl

python skills/literature-search/scripts/prepare_corpus.py \
  --query "language model reasoning agents" \
  --inputs outputs/authority-demo/search_results/s2.jsonl \
  --merged-output outputs/authority-demo/paper_db.raw.jsonl \
  --triaged-output outputs/authority-demo/paper_db.triaged.jsonl \
  --authority-output outputs/authority-demo/paper_db.jsonl \
  --profile cs

python skills/evidence-grading/scripts/grade_evidence.py \
  --input outputs/authority-demo/paper_db.jsonl \
  --output outputs/authority-demo/paper_db.evidence.jsonl \
  --summary outputs/authority-demo/analysis/evidence_summary.md

python skills/authority-ranking/scripts/rank_papers.py \
  --input outputs/authority-demo/paper_db.evidence.jsonl \
  --output outputs/authority-demo/paper_db.jsonl \
  --query "language model reasoning agents" \
  --profile cs \
  --summary outputs/authority-demo/analysis/ranking_summary.md

python skills/related-work-writing/scripts/draft_related_work.py \
  --topic "language model reasoning agents" \
  --input outputs/authority-demo/paper_db.jsonl \
  --output outputs/authority-demo/writing/related_work.md
```

## Offline Sample Path

Use the bundled seed search results when you want a no-network smoke test:

```bash
mkdir -p outputs/authority-offline/analysis outputs/authority-offline/writing

python skills/literature-search/scripts/prepare_corpus.py \
  --query "language model reasoning agents" \
  --inputs examples/authority-aware-minimal/seed_papers.jsonl \
  --merged-output outputs/authority-offline/paper_db.raw.jsonl \
  --triaged-output outputs/authority-offline/paper_db.triaged.jsonl \
  --authority-output outputs/authority-offline/paper_db.jsonl \
  --profile cs

python skills/evidence-grading/scripts/grade_evidence.py \
  --input outputs/authority-offline/paper_db.jsonl \
  --output outputs/authority-offline/paper_db.evidence.jsonl

python skills/authority-ranking/scripts/rank_papers.py \
  --input outputs/authority-offline/paper_db.evidence.jsonl \
  --output outputs/authority-offline/paper_db.jsonl \
  --query "language model reasoning agents" \
  --profile cs

python skills/related-work-writing/scripts/draft_related_work.py \
  --topic "language model reasoning agents" \
  --input outputs/authority-offline/paper_db.jsonl \
  --output outputs/authority-offline/writing/related_work.md
```
