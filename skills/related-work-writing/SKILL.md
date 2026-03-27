---
name: related-work-writing
description: Write or revise the Related Work section of a specific paper from an existing corpus, notes, and bibliography. Use for positioning one contribution against prior work, not for initial discovery, full literature review synthesis, or full survey generation.
argument-hint: [paper-draft]
---

# Related Work Writing

Generate publication-quality Related Work sections with proper citations and thematic organization.

Command examples assume you are running from the repository root.

## Repository Role

This skill is a narrow writing-stage skill.

- It assumes discovery and synthesis have already happened
- It should consume `review.md`, `phase5_synthesis/synthesis.md`, or similar curated notes
- It should output one section, not a full survey manuscript

## Do Not Use This Skill For

- collecting papers from scratch
- fixing bibliography inconsistencies
- generating an entire survey paper

## Shared Inputs and Outputs

Preferred inputs:

- current paper draft
- `outputs/<topic-slug>/review/review.md` or `outputs/<topic-slug>/phase5_synthesis/synthesis.md`
- `references.bib`

Preferred output:

- `outputs/<topic-slug>/writing/related_work.md`

## Input

- `$0` — Current paper draft or method description
- `$1` — Collected literature (BibTeX entries, paper summaries, or literature review notes)

## References

- Related work writing prompts and strategies: `references/related-work-prompts.md`

## Workflow

### Step 1: Analyze the Paper's Contributions
- Read the current paper draft (especially Methods and Introduction)
- Identify the key contributions and novelty claims
- List the technical components that need literature context

### Step 2: Organize Literature by Theme
Group related papers into thematic clusters:
- Each cluster should represent a research direction or technique
- Common themes: problem formulation, methodology family, application domain, evaluation approach
- Order themes from most to least relevant to your work

### Step 3: Write Each Theme Paragraph
For each thematic group:
1. **Topic sentence** — Introduce the research direction
2. **Describe key works** — Summarize 2-5 representative papers
3. **Compare and contrast** — How does each approach differ from yours?
4. **Transition** — Connect to the next theme or to your contribution

### Step 4: Refine
- Ensure every cited paper has a clear reason for inclusion
- Check that your work's novelty is clear from the comparisons
- Verify all `\cite{}` keys exist in the `.bib` file
- Aim for 1-2 pages (single column) or 0.5-1 page (double column)
- If a citation cannot be verified, keep an explicit placeholder and resolve it through `citation-management` rather than inventing a reference

## Rules

- **Compare and contrast, don't just describe** — "Unlike [X] which assumes..., our method..."
- **Organize by theme, not chronologically** — Group by research direction
- **Cite broadly** — Not just the most popular papers; include recent and diverse work
- **Be fair** — Acknowledge strengths of prior work before stating limitations
- **Explain inapplicability** — If a method could apply to your setting, explain why you don't compare experimentally, or add it to experiments
- **Use present tense for established facts** — "Smith et al. propose..." or "This approach uses..."
- **End with positioning** — The final paragraph should clearly position your work relative to all discussed prior work

## Related Skills
- Upstream: [literature-review](../literature-review/), [systematic-review](../systematic-review/), [citation-management](../citation-management/)
- Analysis companions: [cross-paper-synthesis](../cross-paper-synthesis/), [consensus-mapping](../consensus-mapping/), [contradiction-detection](../contradiction-detection/), [evidence-grading](../evidence-grading/), [gap-detection](../gap-detection/)
- See also: [survey-generation](../survey-generation/)
