# authority-ranking examples

Use the offline sample workflow in [`/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/examples/authority-aware-minimal/README.md`](/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/examples/authority-aware-minimal/README.md).

Minimal standalone command:

```bash
python skills/authority-ranking/scripts/rank_papers.py \
  --input examples/authority-aware-minimal/paper_db.authority.jsonl \
  --output examples/authority-aware-minimal/paper_db.ranked.jsonl \
  --query "language model reasoning agents" \
  --profile cs
```
