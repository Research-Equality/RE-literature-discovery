---
name: ccf-ranking
description: Resolve auditable CCF ranks for CS, AI, and security literature review corpora using an official snapshot, alias layer, and explicit match diagnostics. Use before venue-authority-resolver or authority-ranking when conference authority matters.
argument-hint: [paper-db-or-venue]
---

# CCF Ranking

Use this skill to attach auditable CCF metadata, not just a bare rank.

## Data Layers

1. `data/ccf_official_snapshot.json` is the in-repo source of truth, curated from official CCF AI and NIS pages
2. `data/ccf_aliases.json` supports abbreviations, historical names, and shorthand
3. `scripts/resolve_ccf_rank.py` computes the final match result

This repository currently maintains an auditable offline subset for CS / AI / security review, not the entire CCF catalog. If a venue falls outside the maintained subset, the resolver should return `unresolved` with warnings rather than invent a rank.

## Output Fields

- `ccf_rank`
- `ccf_match_type`
- `ccf_match_confidence`
- `ccf_source`
- `ccf_version`
- `ccf_verified_at`
- `ccf_warnings`

Non-exact and uncertain matches must never be silent. They must emit warnings.

## Scripts

Resolve a whole corpus:

```bash
python skills/ccf-ranking/scripts/resolve_ccf_rank.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.ccf.jsonl
```

Resolve one venue with full audit output:

```bash
python skills/ccf-ranking/scripts/resolve_ccf_rank.py --venue "USENIX Security Symposium"
```

Update the maintained snapshot:

```bash
python skills/ccf-ranking/scripts/update_ccf_snapshot.py \
  --input path/to/curated_ccf_export.json \
  --version 2026-03-27 \
  --verified-at 2026-03-27T00:00:00Z
```

## Related Skills

- Upstream: [field-ranking-profile](../field-ranking-profile/)
- Downstream: [venue-authority-resolver](../venue-authority-resolver/), [authority-ranking](../authority-ranking/)
