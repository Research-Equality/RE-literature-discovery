# ccf-ranking examples

Snapshot files:
- [`/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/skills/ccf-ranking/data/ccf_official_snapshot.json`](/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/skills/ccf-ranking/data/ccf_official_snapshot.json)
- [`/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/skills/ccf-ranking/data/ccf_aliases.json`](/Users/mingxinyang/Documents/GitHub/RE-literature-discovery/skills/ccf-ranking/data/ccf_aliases.json)

Resolve a single venue with audit metadata:

```bash
python skills/ccf-ranking/scripts/resolve_ccf_rank.py --venue "Oakland"
python skills/ccf-ranking/scripts/resolve_ccf_rank.py --venue "USENIX Security Symposium"
python skills/ccf-ranking/scripts/resolve_ccf_rank.py --venue "International Conference on Automated Planning and Scheduling"
python skills/ccf-ranking/scripts/resolve_ccf_rank.py --venue "ICLR"
```

`ICLR` is a useful negative check for the current offline subset: it should stay unresolved unless the maintained official snapshot is explicitly extended.
