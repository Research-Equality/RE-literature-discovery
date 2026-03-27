---
name: literature-search
description: Default multi-source discovery skill for building an initial paper set across Semantic Scholar, arXiv, OpenAlex, and CrossRef. Produces normalized search results and bibliography candidates. Use for discovery and triage, not for full synthesis, systematic phase management, or final writing.
argument-hint: [search-query]
---

# Literature Search

Search multiple academic databases to find relevant papers.

Command examples assume you are running from the repository root.

## Repository Role

This is the default entry point for discovery in this repository.

- Use it first when the task is "find the important papers on X"
- Use it to build or expand a reusable `paper_db.jsonl`
- Prefer source-specific skills only when you need source-specific syntax or filters

Prefer these alternatives when needed:
- `arxiv-database`: advanced arXiv-only querying and PDF retrieval
- `biorxiv-database`: bioRxiv-only preprint search
- `openalex-database`: author / institution / citation / bibliometric analysis
- `pubmed-database`: PubMed query design and biomedical systematic search
- `systematic-review`: full end-to-end review pipeline after discovery

## Do Not Use This Skill For

- full multi-phase systematic review execution
- bibliography validation or BibTeX cleanup
- writing a Related Work section or a full survey manuscript

## Shared Inputs and Outputs

Preferred shared artifact layout:

- Raw source results: `outputs/<topic-slug>/search_results/<source>.jsonl`
- Merged corpus: `outputs/<topic-slug>/paper_db.jsonl`
- Optional bibliography seed: `references.bib`

If a source-specific skill outputs wrapped JSON instead of JSONL, normalize it before merging.

## Input

- `$ARGUMENTS` — The search query (natural language)

## Scripts

### Semantic Scholar (primary — best for ML/AI, has BibTeX)
```bash
python skills/systematic-review/scripts/search_semantic_scholar.py \
  --query "QUERY" --max-results 20 --year-range 2022-2026 \
  --api-key "$S2_API_KEY" \
  -o results_s2.jsonl
```

Key flags: `--peer-reviewed-only`, `--top-conferences`, `--min-citations N`, `--venue NeurIPS ICML`

### arXiv (latest preprints)
```bash
python skills/systematic-review/scripts/search_arxiv.py \
  --query "QUERY" --max-results 10 -o results_arxiv.jsonl
```

### OpenAlex (broadest coverage, free, no API key)
```bash
python skills/literature-search/scripts/search_openalex.py \
  --query "QUERY" --max-results 20 --year-range 2022-2026 \
  --min-citations 5 -o results_openalex.jsonl
```

### Merge & Deduplicate
```bash
python skills/systematic-review/scripts/paper_db.py merge \
  --inputs results_s2.jsonl results_arxiv.jsonl results_openalex.jsonl \
  --output merged.jsonl
```

### CrossRef (DOI-based lookup, broadest type coverage)
```bash
python skills/literature-search/scripts/search_crossref.py \
  --query "QUERY" --rows 10 --output results_crossref.jsonl
```

Key flags: `--bibtex` (output .bib format), `--rows N`

### Download arXiv Source (get .tex files)
```bash
python skills/literature-search/scripts/download_arxiv_source.py \
  --title "Paper Title" --output-dir arxiv_papers/
```

Key flags: `--arxiv-id 1706.03762`, `--metadata`, `--max-results N`

### Generate BibTeX from results
```bash
python skills/systematic-review/scripts/bibtex_manager.py \
  --jsonl merged.jsonl --output references.bib
```

### Normalize source-specific search outputs into shared JSONL
```bash
python skills/literature-search/scripts/normalize_search_results.py \
  --source arxiv-database \
  --input raw_arxiv.json \
  --output outputs/<topic-slug>/search_results/arxiv.jsonl
```

```bash
python skills/literature-search/scripts/normalize_search_results.py \
  --source biorxiv-database \
  --input raw_biorxiv.json \
  --output outputs/<topic-slug>/search_results/biorxiv.jsonl
```

## Workflow

1. Expand the user's query into 2-4 complementary search queries
2. Run Semantic Scholar search (primary) with expanded queries
3. Run arXiv for very recent preprints (< 3 months)
4. Optionally run OpenAlex for broader coverage
5. Merge and deduplicate results
6. Rank by: citations (0.3) + recency (0.3) + venue quality (0.2) + relevance (0.2)
7. Present structured results table

## Venue Quality Tiers

**Tier 1:** NeurIPS, ICML, ICLR, ACL, EMNLP, NAACL, CVPR, ICCV, ECCV, KDD, AAAI, IJCAI, SIGIR, WWW
**Tier 2:** AISTATS, UAI, COLT, COLING, EACL, WACV, JMLR, TACL
**Tier 3:** Workshops, arXiv preprints — mark with `(preprint)`

## Output Format

Present results as a table + detailed entries with BibTeX keys. Always note preprint status.

## Related Skills
- Downstream: [literature-review](../literature-review/), [systematic-review](../systematic-review/), [citation-management](../citation-management/)
- See also: [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
- Source-specific companions: [arxiv-database](../arxiv-database/), [biorxiv-database](../biorxiv-database/), [openalex-database](../openalex-database/), [pubmed-database](../pubmed-database/)
- Monitoring and analysis companions: [arxiv-monitor](../arxiv-monitor/), [citation-graph](../citation-graph/)
