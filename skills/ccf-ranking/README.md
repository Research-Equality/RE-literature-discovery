# ccf-ranking

Auditable CCF resolver for CS, AI, and security literature review.

This skill now uses a three-layer design:
- `data/ccf_official_snapshot.json` as the in-repo source of truth
- `data/ccf_aliases.json` for abbreviations, aliases, and historical names
- `scripts/resolve_ccf_rank.py` for exact, alias, normalized abbreviation, and fuzzy resolution

The snapshot is now an offline manual mirror of official CCF category pages, not a local starter map. The current maintained subset prioritizes AI and network-information-security venues used by this repository's literature-review workflows. Outside that subset, unresolved output is expected and should not be silently patched over.

Primary source pages used for this offline snapshot:
- `https://www.ccf.org.cn/Academic_Evaluation/AI/`
- `https://www.ccf.org.cn/Academic_Evaluation/NIS/`
- `https://www.ccf.org.cn/Academic_Evaluation/By_category/2024-06-28/825349.shtml`

Key output fields:
- `ccf_rank`
- `ccf_match_type`
- `ccf_match_confidence`
- `ccf_source`
- `ccf_version`
- `ccf_verified_at`
- `ccf_warnings`

Core command:

```bash
python skills/ccf-ranking/scripts/resolve_ccf_rank.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.ccf.jsonl
```
