---
name: survey-generation
description: Generate a full survey manuscript from a curated corpus, outline, and synthesis notes. Use when the deliverable is an end-to-end survey paper, not just a Related Work section, quick review, or citation cleanup.
argument-hint: [topic]
---

# Survey Generation

Generate complete academic survey papers with structured outline, RAG-based writing, and citation validation.

Command examples assume you are running from the repository root.

## Repository Role

This is the final manuscript-generation skill in the repository.

- Prefer `systematic-review` as the upstream producer of the corpus and synthesis notes
- `literature-review` can also act as a lighter upstream input
- `citation-management` should be used before finalizing the manuscript

## Do Not Use This Skill For

- first-pass paper discovery
- bibliography-only repair
- writing only a single Related Work section

## Shared Inputs and Outputs

Preferred inputs:

- `outputs/<topic-slug>/paper_db.jsonl`
- `outputs/<topic-slug>/phase5_synthesis/synthesis.md` or `outputs/<topic-slug>/review/review.md`
- optional `references.bib`

Preferred output root:

- `outputs/<topic-slug>/survey/`

## Input

- `$0` — Survey topic or research area

## Scripts

### Literature search
```bash
python skills/systematic-review/scripts/search_semantic_scholar.py \
  --query "relevant search query" --max-results 50
```

## References

- Survey prompts (outline, writing, citation, coherence): `references/survey-prompts.md`

## Workflow (from AutoSurvey)

### Step 1: Collect Papers
1. Search Semantic Scholar / arXiv for papers on the topic
2. Collect 50-200 relevant papers with titles and abstracts
3. Filter by relevance and citation count

### Step 2: Generate Outline (Multi-LLM Parallel)
1. Generate N rough outlines independently (parallel)
2. Merge outlines into a single comprehensive outline
3. Expand each section into subsections
4. Edit final outline to remove redundancies

### Step 3: Write Subsections (RAG-Based)
For each subsection:
1. Retrieve relevant papers for the subsection topic
2. Generate content with inline citations `[paper_title]`
3. Enforce minimum word count per subsection
4. Only cite papers from the provided list

### Step 4: Validate Citations
For each subsection:
1. Check that cited paper titles are correct
2. Verify citations support the claims made
3. Remove or correct unsupported citations
4. Use NLI (Natural Language Inference) for claim-source faithfulness

### Step 5: Enhance Local Coherence
For each subsection:
1. Read previous and following subsections
2. Refine transitions and flow
3. Preserve core content and citations
4. Ensure smooth reading experience

### Step 6: Convert Citations to BibTeX
1. Replace `[paper_title]` with `\cite{key}`
2. Generate BibTeX entries for all cited papers
3. Validate all citation keys exist in .bib file
4. If any paper cannot be verified, keep an explicit placeholder and resolve it before final output

## Output Structure

```
outputs/<topic-slug>/survey/
├── main.tex          # Complete survey paper
├── references.bib    # All citations
├── outline.json      # Survey outline
└── sections/         # Individual section files
```

## Rules

- Only cite papers from the collected paper list — never hallucinate citations
- Each subsection must meet minimum word count
- No duplicate subsections across sections
- Citation validation is mandatory before final output
- If a citation cannot be verified programmatically, keep a visible placeholder instead of fabricating a BibTeX entry
- Local coherence enhancement must preserve all citations
- The survey should be comprehensive and logically organized

## Related Skills
- Upstream: [systematic-review](../systematic-review/), [literature-review](../literature-review/), [literature-search](../literature-search/)
- Analysis companions: [cross-paper-synthesis](../cross-paper-synthesis/), [consensus-mapping](../consensus-mapping/), [contradiction-detection](../contradiction-detection/), [evidence-grading](../evidence-grading/), [gap-detection](../gap-detection/)
- Final validation: [citation-management](../citation-management/)
- See also: [related-work-writing](../related-work-writing/)
