---
name: gap-detection
description: Identify open questions, blind spots, and novelty opportunities from a curated literature corpus. Use after synthesis when positioning future work, related work, or survey conclusions, not for collecting papers from scratch.
argument-hint: [topic-or-corpus]
---

# Gap Detection

Find what the literature still does not explain, compare, validate, or settle.

## Repository Role

This is a post-corpus analysis skill.

- It consumes an existing corpus or synthesis notes
- It complements `systematic-review` phase-5 gaps, but works as a focused standalone analysis skill
- It is useful for introductions, future-work sections, survey conclusions, and project positioning

## Do Not Use This Skill For

- initial literature search
- citation-format repair
- full manuscript generation

## Shared Inputs and Outputs

Preferred inputs:

- `outputs/<topic-slug>/paper_db.jsonl`
- `outputs/<topic-slug>/review/review.md` or `outputs/<topic-slug>/phase5_synthesis/synthesis.md`
- optional contradiction or evidence reports

Preferred outputs:

- `outputs/<topic-slug>/analysis/gap_map.md`
- `outputs/<topic-slug>/analysis/novelty_checks.md`

## Workflow

1. Inspect explicit limitations, future work, and unresolved comparisons in the corpus
2. Cluster gaps into empirical, methodological, theoretical, dataset, or application gaps
3. Check whether an apparent gap has already been addressed in recent literature
4. Rank gaps by novelty confidence and practical relevance
5. Produce actionable directions rather than vague "more work is needed" statements

## Related Skills

- Upstream: [literature-review](../literature-review/), [systematic-review](../systematic-review/), [citation-graph](../citation-graph/)
- Companion: [contradiction-detection](../contradiction-detection/), [consensus-mapping](../consensus-mapping/), [evidence-grading](../evidence-grading/)
- Downstream: [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
