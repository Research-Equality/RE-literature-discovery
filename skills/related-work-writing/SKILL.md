---
name: related-work-writing
description: Write or revise the Related Work section of a specific paper from an authority-aware corpus with bucket-aware tone control. Use when you need canonical, comparative, and cautious writing modes based on selection_bucket and caution_flags.
argument-hint: [paper-draft]
---

# Related Work Writing

This skill writes one section, not a full manuscript.

## Writing Policy

- `core`: canonical / backbone language
- `supporting`: comparative / supportive language
- `frontier`: cautious / tentative language

Use caution flags to further soften claims:
- `high_authority_low_evidence`
- `preprint_only`
- `weak_metadata`

Frontier papers must not be written as established consensus.

## Script

```bash
python skills/related-work-writing/scripts/draft_related_work.py \
  --topic "TOPIC" \
  --input outputs/<topic-slug>/paper_db.jsonl \
  --output outputs/<topic-slug>/writing/related_work.md
```

## Related Skills

- Upstream: [literature-review](../literature-review/), [systematic-review](../systematic-review/), [authority-ranking](../authority-ranking/), [evidence-grading](../evidence-grading/)
- Final validation: [citation-management](../citation-management/)
