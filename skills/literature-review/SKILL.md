---
name: literature-review
description: Synthesize an already collected paper set into a focused literature review using multi-perspective dialogue and grounded note consolidation. Use for thematic review writing and gap analysis after discovery, not for raw search-only tasks or full survey-manuscript generation.
argument-hint: [topic]
---

# Literature Review

Conduct deep literature reviews through multi-perspective dialogue and systematic search.

Command examples assume you are running from the repository root.

## Repository Role

This skill sits between discovery and final writing.

- Upstream input is usually `paper_db.jsonl` from `literature-search` or `systematic-review`
- Its job is synthesis, not exhaustive search orchestration
- Its outputs should be reusable by `related-work-writing` and `survey-generation`

## Do Not Use This Skill For

- first-pass broad paper discovery across databases
- bibliography cleanup or cite-key repair
- writing a full survey manuscript from start to finish

## Shared Inputs and Outputs

Preferred inputs:

- `outputs/<topic-slug>/paper_db.jsonl`
- source notes or search-result summaries
- optional `references.bib`

Preferred outputs:

- `outputs/<topic-slug>/review/review_outline.md`
- `outputs/<topic-slug>/review/review.md`
- `outputs/<topic-slug>/review/evidence_table.md`
- `outputs/<topic-slug>/review/gaps.md`

## Input

- `$0` — Research topic or question
- `$1` — Optional: specific focus or angle

## References

- Multi-perspective dialogue prompts (STORM): `references/dialogue-prompts.md`
- Literature review workflow (AgentLaboratory): `references/review-workflow.md`

## Scripts (from literature-search skill)

```bash
# Search Semantic Scholar
python skills/systematic-review/scripts/search_semantic_scholar.py --query "topic" --max-results 20

# Search OpenAlex
python skills/literature-search/scripts/search_openalex.py --query "topic" --max-results 20

# Search arXiv
python skills/systematic-review/scripts/search_arxiv.py --query "topic" --max-results 10
```

## Workflow

### Step 1: Generate Expert Personas (from STORM)
Given the topic, create 3-5 diverse expert personas:
- Each represents a different perspective, role, or research angle
- Example: "ML systems researcher focused on efficiency", "Theoretical statistician concerned with guarantees"
- Use the persona generation prompts from references

### Step 2: Multi-Perspective Dialogue
For each persona, simulate a multi-turn Q&A conversation:
1. **Persona asks a question** from their unique angle
2. **Generate search queries** from the question
3. **Search literature** using the search scripts
4. **Synthesize an answer** grounded in retrieved papers with inline citations
5. **Record the dialogue turn** with search results
6. Repeat for 3-5 turns per persona
7. End when persona says "Thank you so much for your help!"

### Step 3: Synthesize Knowledge
- Combine all persona conversations into a unified knowledge base
- Remove redundancy across personas
- Organize by theme/subtopic
- Generate an outline based on the collected information

### Step 4: Generate Literature Review
- Write a structured review organized by the generated outline
- Every claim must be supported by a citation
- Include a summary table of key papers (method, contribution, limitations)

## Output

A structured literature review bundle:
1. **Outline** — `outputs/<topic-slug>/review/review_outline.md`
2. **Review draft** — `outputs/<topic-slug>/review/review.md`
3. **Evidence table** — `outputs/<topic-slug>/review/evidence_table.md`
4. **Knowledge gaps** — `outputs/<topic-slug>/review/gaps.md`

## Rules

- Every sentence in the review must be supported by gathered information
- If information is not found, explicitly state the gap
- Cite broadly — cover diverse approaches, not just the most popular
- Include recent papers (last 2-3 years) alongside foundational work
- Use inline citations: "Smith et al. [1] propose..."

## Related Skills
- Upstream: [literature-search](../literature-search/), [systematic-review](../systematic-review/)
- Downstream: [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
- Analysis companions: [cross-paper-synthesis](../cross-paper-synthesis/), [consensus-mapping](../consensus-mapping/), [contradiction-detection](../contradiction-detection/), [evidence-grading](../evidence-grading/), [gap-detection](../gap-detection/)
