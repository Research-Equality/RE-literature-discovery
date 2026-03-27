---
name: consensus-mapping
description: Distill what a field broadly agrees on versus what remains contested from a curated corpus. Use for background sections, survey framing, and onboarding summaries, not for paper discovery or bibliography management.
argument-hint: [topic-or-corpus]
---

# Consensus Mapping

Separate established knowledge from active debate inside a literature corpus.

## Repository Role

This is a synthesis-analysis skill.

- It helps surveys and introductions avoid overstating contested claims
- It is narrower than `literature-review` and more interpretive than `citation-graph`
- It should usually come after corpus construction and at least light synthesis

## Do Not Use This Skill For

- searching for new papers
- one-paper summaries
- generating a full manuscript end to end

## Shared Inputs and Outputs

Preferred inputs:

- `outputs/<topic-slug>/paper_db.jsonl`
- optional claim registry or contradiction report

Preferred outputs:

- `outputs/<topic-slug>/analysis/consensus_map.md`
- `outputs/<topic-slug>/analysis/contested_claims.md`

## Workflow

1. Group claims by subtopic
2. Measure how many papers support, challenge, or leave each claim unresolved
3. Weight by recency and evidence strength rather than raw citation counts alone
4. Mark each claim as consensus, emerging consensus, contested, or unclear
5. Produce prose and tables that can be reused in reviews and surveys

## Related Skills

- Upstream: [literature-review](../literature-review/), [systematic-review](../systematic-review/)
- Companion: [claim-tracker](../claim-tracker/), [contradiction-detection](../contradiction-detection/), [evidence-grading](../evidence-grading/)
- Downstream: [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
