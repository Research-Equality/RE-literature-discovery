# systematic-review

End-to-end multi-phase review workspace.

Within this repository, Phase 2 should now produce:
- `paper_db.raw.jsonl`
- `paper_db.triaged.jsonl`
- `paper_db.evidence.jsonl`
- canonical ranked `paper_db.jsonl`
- `analysis/evidence_summary.md`

Recommended pattern:
1. search
2. merge and initial triage
3. venue authority resolution
4. quality filtering
5. authority-aware ranking
6. evidence grading
7. reranking
8. writing handoff

This skill also absorbs citation-graph expansion and ongoing monitoring as built-in maintenance modes. See `references/corpus-maintenance.md`.
