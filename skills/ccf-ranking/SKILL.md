---
name: ccf-ranking
description: Resolve bundled or custom CCF-style venue ranks for CS literature review corpora. Use when conference hierarchy is an important authority signal, especially before authority-ranking.
argument-hint: [paper-db-or-venue]
---

# CCF Ranking

Use this skill to attach `ccf_rank` and `core_rank` for CS-centric corpora.

## Notes

- the bundled JSON is a starter mapping, not a claim of complete official coverage
- prefer the `cs` field-ranking-profile when this metadata drives ranking
- this skill resolves metadata only; it does not write `final_score`

## Scripts

Resolve a whole corpus:

```bash
python skills/ccf-ranking/scripts/resolve_ccf.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.ccf.jsonl
```

Resolve a single venue:

```bash
python skills/ccf-ranking/scripts/resolve_ccf.py --venue "NeurIPS"
```

## Related Skills

- Upstream: [field-ranking-profile](../field-ranking-profile/)
- Downstream: [venue-authority-resolver](../venue-authority-resolver/), [authority-ranking](../authority-ranking/)
