# venue-authority-resolver examples

Offline demo input lives in [`/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/examples/authority-aware-minimal/paper_db.triaged.jsonl`](/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/examples/authority-aware-minimal/paper_db.triaged.jsonl).

```bash
python skills/venue-authority-resolver/scripts/resolve_authority.py \
  --input examples/authority-aware-minimal/paper_db.triaged.jsonl \
  --output examples/authority-aware-minimal/paper_db.authority.jsonl
```
