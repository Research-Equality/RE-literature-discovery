---
name: survey-generation
description: Generate a full survey manuscript from a curated authority-aware corpus with bucket-aware writing rules. Use when the deliverable is an end-to-end survey paper and frontier papers must remain tentative rather than presented as consensus.
argument-hint: [topic]
---

# Survey Generation

This is the repository's full-manuscript writing skill.

## Section Planning Policy

- `core`: canonical / backbone treatment
- `supporting`: comparative / supportive treatment
- `background`: historical framing
- `frontier`: cautious / tentative treatment

Frontier papers must never be described as established consensus, especially when caution flags include `preprint_only`, `high_authority_low_evidence`, or `weak_metadata`.

## Planning Helper

```bash
python skills/survey-generation/scripts/plan_bucketed_survey.py \
  --topic "TOPIC" \
  --input outputs/<topic-slug>/paper_db.evidence.jsonl \
  --output outputs/<topic-slug>/survey/writing_guidance.md
```

## Related Skills

- Upstream: [systematic-review](../systematic-review/), [literature-review](../literature-review/), [authority-ranking](../authority-ranking/), [evidence-grading](../evidence-grading/)
- Final validation: [citation-management](../citation-management/)
- See also: [related-work-writing](../related-work-writing/)
