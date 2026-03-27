---
name: venue-authority-resolver
description: Resolve venue authority metadata such as venue_type, peer_reviewed, preprint status, CCF rank, and journal metrics before final ranking. Use after search/merge/triage and before authority-ranking.
argument-hint: [paper-db]
---

# Venue Authority Resolver

Use this skill to enrich paper metadata without assigning final scores.

## Responsibilities

- normalize venue metadata into the shared paper schema
- call CCF and journal metrics resolvers
- mark preprints and peer-reviewed venues consistently
- add authority-related flags for downstream ranking and writing

## Do Not Use This Skill For

- final ranking
- evidence grading
- drafting prose

## Script

```bash
python skills/venue-authority-resolver/scripts/resolve_authority.py \
  --input outputs/<topic-slug>/paper_db.triaged.jsonl \
  --output outputs/<topic-slug>/paper_db.authority.jsonl
```

## Related Skills

- Upstream: [literature-search](../literature-search/), [ccf-ranking](../ccf-ranking/), [journal-metrics](../journal-metrics/)
- Next layer: [paper-quality-filter](../paper-quality-filter/), [authority-ranking](../authority-ranking/)
