# Systematic Review Corpus Maintenance

This reference folds the old monitoring and citation-expansion patterns into `systematic-review`.

## Citation Expansion

Use this mode when the current corpus is coherent but still missing bridge papers or foundational references.

Recommended outputs:
- `outputs/{topic-slug}/analysis/citation_expansion.md`
- `outputs/{topic-slug}/analysis/reading_gaps.md`

Checklist:
- start from the current `paper_db.jsonl`
- inspect citations around the top `core` and `supporting` papers
- add only papers that materially change coverage, not every neighbor in the graph
- route accepted additions back through `venue-authority-resolver -> paper-quality-filter -> authority-ranking -> evidence-grading -> authority-ranking`

## Ongoing Monitoring

Use this mode when the topic is already defined and you want to keep the corpus current.

Recommended outputs:
- `outputs/{topic-slug}/monitoring/recent_digest.md`
- `outputs/{topic-slug}/monitoring/recent_candidates.jsonl`

Checklist:
- focus on recent months, not the full history
- prefer reviewed venues first, then a small number of relevant preprints
- deduplicate against the current corpus before reading
- new additions must still pass the full authority-aware workflow before entering the canonical `paper_db.jsonl`
