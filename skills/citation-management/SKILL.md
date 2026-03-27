---
name: citation-management
description: Validate, generate, repair, and deduplicate BibTeX and cite keys for an existing paper draft or curated paper database. Use for bibliography hygiene and citation insertion, not for broad literature discovery or narrative synthesis.
argument-hint: [tex-or-bib-file]
---

# Citation Management

Manage the full lifecycle of citations in a LaTeX paper.

Command examples assume you are running from the repository root.

## Repository Role

This skill is the bibliography contract layer for the repository.

- It consumes a curated paper set, draft `.tex`, or existing `.bib`
- It does not replace discovery or synthesis skills
- It is the final gate before manuscript compilation

## Do Not Use This Skill For

- broad paper discovery across databases
- thematic literature synthesis
- writing Related Work or survey prose

## Shared Inputs and Outputs

Preferred shared flow:

1. `paper_db.jsonl` from `literature-search` or `systematic-review`
2. `references.bib` generated or repaired here
3. manuscript `.tex` validated against `references.bib`

If you already have a curated corpus, generate BibTeX from it before searching for new papers again.

## Non-Negotiable Rule

Never generate BibTeX from memory.

- search first
- verify existence in programmatic metadata sources
- fetch BibTeX from a verified identifier when possible
- only then add the citation

If a citation cannot be verified, keep an explicit placeholder rather than inventing a reference.

## Input

- `$0` — Action: `harvest`, `validate`, `add`, `format`
- `$1` — Path to `.tex` or `.bib` file

## Scripts

### Validate citations (check all cite keys resolve)
```bash
python skills/citation-management/scripts/validate_citations.py \
  --tex paper/main.tex --bib paper/references.bib --check-figures --figures-dir paper/figures/
```

Reports: missing citations, unused bib entries, duplicate keys, duplicate sections, duplicate labels, undefined references, missing figures.

### Generate BibTeX from paper database
```bash
python skills/systematic-review/scripts/bibtex_manager.py \
  --jsonl paper_db.jsonl --output references.bib
```

### Search for a specific paper to add
```bash
python skills/systematic-review/scripts/search_semantic_scholar.py \
  --query "attention is all you need" --max-results 5 \
  --api-key "$S2_API_KEY"
```

### Retrieve BibTeX from verified DOI
Use DOI content negotiation or another verified metadata source rather than hand-writing BibTeX entries.

### Harvest missing citations automatically
```bash
python skills/citation-management/scripts/harvest_citations.py \
  --tex paper/main.tex --bib paper/references.bib --output candidates.bib --max-rounds 10
```

Scans .tex for uncited claims, searches Semantic Scholar, outputs candidate BibTeX entries.
Key flags: `--dry-run` (preview only), `--verbose`, `--api-key`

### Auto-fix missing citation placeholders
```bash
python skills/citation-management/scripts/validate_citations.py \
  --tex paper/main.tex --bib paper/references.bib --fix
```

Generates `references_fixed.bib` with placeholder entries for all missing citation keys.

## Action: `harvest` — Iterative Citation Harvesting

Based on AI-Scientist's 20-round citation harvesting loop. For each round:

1. Read the current `.tex` draft
2. Identify the most important missing citation
3. Search Semantic Scholar via script
4. Select the most relevant paper from results
5. Extract BibTeX and generate a clean key (`lastNameYearWord`)
6. Append to `.bib` (skip if key exists)
7. Insert `\cite{key}` at the appropriate location
8. Stop when no more gaps or 20 rounds reached

**Key rules:**
- DO NOT add a citation that already exists
- Only add citations found via API — never fabricate
- Cite broadly — not just popular papers
- Do not copy verbatim from prior literature

## Action: `validate` — Pre-Compilation Check

Run `validate_citations.py` to catch all issues before compilation. Fix any reported problems.

## Action: `add` — Add Specific Paper

Search Semantic Scholar for the paper, extract BibTeX, clean the key, append to `.bib`.

BibTeX key format: `firstAuthorLastNameYearFirstContentWord` (e.g., `vaswani2017attention`)

## Action: `format` — Standardize .bib

- Sort entries alphabetically by key
- Ensure consistent indentation (2 spaces)
- Remove empty fields
- Protect proper nouns with `{Braces}` in titles
- Ensure required fields per entry type

## References

- `references/citation-verification.md` — repository-standard citation verification workflow and placeholder policy

## Related Skills
- Upstream: [literature-search](../literature-search/), [systematic-review](../systematic-review/), [pyzotero](../pyzotero/)
- Downstream: [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
