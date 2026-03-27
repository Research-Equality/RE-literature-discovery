---
name: evidence-grading
description: Grade evidence strength for papers or claims based on study design, replication, venue, and recency. Use when deciding how strongly to trust a finding or how cautiously to phrase a claim, not for discovery or bibliography management.
argument-hint: [claim-or-corpus]
---

# Evidence Grading

Estimate how much confidence a reader should place in a paper or claim.

## Repository Role

This is a trust-calibration skill.

- Use it when writing needs calibrated language, not just citation counts
- Use it after you already know which papers or claims matter
- It supports both literature synthesis and final manuscript phrasing

## Do Not Use This Skill For

- searching for papers from scratch
- full review generation
- cite-key or `.bib` maintenance

## Shared Inputs and Outputs

Preferred inputs:

- `outputs/<topic-slug>/paper_db.jsonl`
- optional claim registry, contradiction report, or consensus map

Preferred outputs:

- `outputs/<topic-slug>/analysis/evidence_grades.md`
- `outputs/<topic-slug>/analysis/claim_strength.md`

## Workflow

1. Define the grading rubric appropriate to the domain
2. Grade papers or claims using design quality, replication status, recency, and venue context
3. Penalize unresolved contradictions and unsupported extrapolation
4. Map grades to writing guidance such as strong claim / cautious claim / speculative claim
5. Feed the grades into literature review and manuscript writing

## Related Skills

- Upstream: [literature-review](../literature-review/), [systematic-review](../systematic-review/)
- Companion: [claim-tracker](../claim-tracker/), [consensus-mapping](../consensus-mapping/), [contradiction-detection](../contradiction-detection/)
- Downstream: [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
