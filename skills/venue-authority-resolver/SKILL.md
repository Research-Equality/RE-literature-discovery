---
name: venue-authority-resolver
description: Resolve auditable venue authority metadata such as venue_type, peer_reviewed, CCF rank, and journal metrics before final ranking. Use after search/merge/triage and before paper-quality-filter or authority-ranking.
argument-hint: [paper-db]
---

# Venue Authority Resolver

Use this skill to enrich paper metadata without assigning final scores.

## Responsibilities

- normalize venue metadata into the shared paper schema
- call the CCF and journal metric resolvers
- write shared audit fields such as `source_of_truth`, `resolved_from`, and `match_confidence`
- add authority-related caution flags for downstream ranking and writing

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
