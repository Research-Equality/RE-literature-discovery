---
name: claim-tracker
description: Track specific claims across a literature corpus over time, including supporting, challenging, and superseding papers. Use when verifying whether an important premise still stands or when maintaining claim provenance across a review.
argument-hint: [claim-or-topic]
---

# Claim Tracker

Track the lifecycle of important claims rather than treating every citation as equally stable.

## Repository Role

This skill is for claim-level provenance.

- Use it when a survey or paper relies on a few critical premises
- Use it after you already have a corpus and want claim-level status, not just paper-level summaries
- It works especially well with `contradiction-detection` and `evidence-grading`

## Do Not Use This Skill For

- broad topic discovery
- generic literature review drafting
- BibTeX maintenance

## Shared Inputs and Outputs

Preferred inputs:

- `outputs/<topic-slug>/paper_db.jsonl`
- a list of claims to track

Preferred outputs:

- `outputs/<topic-slug>/analysis/claim_registry.md`
- `outputs/<topic-slug>/analysis/claim_timelines.md`

## Workflow

1. Register the exact claim text, scope, and source paper
2. Find follow-up papers that support, refine, challenge, or refute the claim
3. Track whether the claim status is standing, contested, or obsolete
4. Separate claim status from paper prestige: a famous paper can still support a weak claim
5. Record the evidence chain so future writing can cite the right state of knowledge

## Related Skills

- Upstream: [literature-search](../literature-search/), [systematic-review](../systematic-review/)
- Companion: [contradiction-detection](../contradiction-detection/), [evidence-grading](../evidence-grading/), [consensus-mapping](../consensus-mapping/)
- Downstream: [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
