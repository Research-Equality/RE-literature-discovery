---
name: citation-graph
description: Build citation-network views from a curated paper set to identify foundational works, bridge papers, and reading gaps. Use after initial corpus construction when influence structure matters, not for raw search or final prose writing.
argument-hint: [topic-or-seed-corpus]
---

# Citation Graph

Analyze citation structure around a paper set rather than reading papers one by one in isolation.

## Repository Role

This is an analysis skill that sits after corpus collection.

- It helps expand or reorganize a corpus by citation structure
- It does not replace `literature-search` or source-specific retrieval
- It is especially useful before `related-work-writing`, `survey-generation`, and `gap-detection`

## Do Not Use This Skill For

- one-off title or DOI lookup
- bibliography cleanup
- drafting a full review directly

## Shared Inputs and Outputs

Preferred inputs:

- `outputs/<topic-slug>/paper_db.jsonl`
- optional seed DOIs, arXiv IDs, or OpenAlex / Semantic Scholar identifiers

Preferred outputs:

- `outputs/<topic-slug>/analysis/citation_graph.md`
- `outputs/<topic-slug>/analysis/citation_graph.json`
- `outputs/<topic-slug>/analysis/reading_gaps.md`

## Workflow

1. Start from a curated seed set rather than the entire internet
2. Expand citations and references using structured metadata sources
3. Identify highly central, bridge, and under-covered papers
4. Separate foundational papers from recent cluster-defining papers
5. Feed missing-but-important papers back into `paper_db.jsonl`

## Output

A good citation graph report should include:

- core papers everyone cites
- bridge papers connecting clusters
- cluster labels or thematic communities
- missing papers worth reading next

## Related Skills

- Upstream: [literature-search](../literature-search/), [systematic-review](../systematic-review/), [openalex-database](../openalex-database/)
- Downstream: [gap-detection](../gap-detection/), [related-work-writing](../related-work-writing/), [survey-generation](../survey-generation/)
