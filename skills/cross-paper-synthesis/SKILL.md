---
name: cross-paper-synthesis
description: Produce structured multi-paper synthesis outputs such as comparative tables, narrative through-lines, and temporal evolution summaries from an existing corpus. Use when the task is analytical synthesis across papers, not initial search or full survey-manuscript generation.
argument-hint: [topic-or-corpus]
---

# Cross-Paper Synthesis

Generate comparison-heavy synthesis artifacts from a curated set of papers.

## Repository Role

This skill is a focused synthesis utility.

- `literature-review` is the broader review-drafting skill
- `cross-paper-synthesis` is better when the deliverable is a comparison table, timeline, or structured through-line
- It is a good intermediate step before `related-work-writing` or `survey-generation`

## Do Not Use This Skill For

- raw paper search
- bibliography repair
- end-to-end survey generation without prior corpus curation

## Shared Inputs and Outputs

Preferred inputs:

- `outputs/<topic-slug>/paper_db.jsonl`
- optional deep-dive notes or review drafts

Preferred outputs:

- `outputs/<topic-slug>/analysis/comparison_table.md`
- `outputs/<topic-slug>/analysis/timeline.md`
- `outputs/<topic-slug>/analysis/synthesis.md`

## Workflow

1. Choose the synthesis mode: narrative, comparison table, timeline, or method taxonomy
2. Limit the corpus to a coherent subset when necessary
3. Extract comparable dimensions such as methods, data, assumptions, metrics, and limitations
4. Write the synthesis so that it reveals patterns across papers, not just isolated summaries
5. Hand the result to `related-work-writing`, `survey-generation`, or `gap-detection`

## Related Skills

- Upstream: [literature-review](../literature-review/), [systematic-review](../systematic-review/)
- Companion: [consensus-mapping](../consensus-mapping/), [contradiction-detection](../contradiction-detection/)
- Downstream: [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
