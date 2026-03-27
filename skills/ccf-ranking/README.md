# ccf-ranking

CCF-style CS venue ranking companion for authority-aware literature workflows.

Use this skill when conference prestige matters, especially for CS and AI literature review. The bundled mapping is a starter local map and can be replaced with a custom JSON file.

```bash
python skills/ccf-ranking/scripts/resolve_ccf.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.ccf.jsonl
```
