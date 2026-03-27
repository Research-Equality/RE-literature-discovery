# literature-search

Discovery, merge, dedup, and early triage for literature corpora.

This skill no longer owns final ranking. It hands the triaged corpus to the authority layer and produces the canonical ranked `paper_db.jsonl` by calling the resolver, quality filter, and `authority-ranking`.

Treat that file as the initial ranked corpus. After `evidence-grading`, re-run `authority-ranking` to refresh the final canonical `paper_db.jsonl`.

Recommended command:

```bash
python skills/literature-search/scripts/prepare_corpus.py \
  --query "QUERY" \
  --inputs outputs/<topic-slug>/search_results/*.jsonl \
  --merged-output outputs/<topic-slug>/paper_db.raw.jsonl \
  --triaged-output outputs/<topic-slug>/paper_db.triaged.jsonl \
  --authority-output outputs/<topic-slug>/paper_db.jsonl \
  --profile cs
```
