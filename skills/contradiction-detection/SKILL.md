---
name: contradiction-detection
description: Detect and organize conflicting findings across papers in a curated corpus. Use when literature appears inconsistent or when writing discussion, limitations, or survey sections that must address disagreement.
argument-hint: [topic-or-corpus]
---

# Contradiction Detection

Find where papers disagree, why they disagree, and whether the disagreement is superficial or fundamental.

## Repository Role

This is a disagreement-analysis skill.

- It should consume a real corpus, not a vague topic prompt
- It helps downstream writing stay honest about contested results
- It complements `consensus-mapping` by focusing on the disagreement surface

## Do Not Use This Skill For

- initial retrieval
- bibliography formatting
- full survey drafting without prior corpus work

## Shared Inputs and Outputs

Preferred inputs:

- `outputs/<topic-slug>/paper_db.jsonl`
- optional full-paper notes from `systematic-review`

Preferred outputs:

- `outputs/<topic-slug>/analysis/contradictions.md`
- `outputs/<topic-slug>/analysis/resolution_hypotheses.md`

## Workflow

1. Extract comparable claims, results, and methodological assumptions
2. Detect papers that make incompatible statements or report materially different outcomes
3. Classify contradictions as empirical, methodological, interpretive, or benchmark-specific
4. Propose likely causes such as data differences, metrics, scope mismatch, or evaluation leakage
5. Route the result into review, discussion, or future-work writing

## Related Skills

- Upstream: [systematic-review](../systematic-review/), [literature-review](../literature-review/)
- Companion: [consensus-mapping](../consensus-mapping/), [evidence-grading](../evidence-grading/), [claim-tracker](../claim-tracker/)
- Downstream: [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
