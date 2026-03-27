---
name: arxiv-monitor
description: Monitor arXiv on a recurring basis for new papers, authors, or categories and produce ranked digests or watchlists. Use for ongoing literature surveillance after the topic is already defined, not for one-off broad discovery or full review synthesis.
argument-hint: [topic-or-watch-profile]
---

# arXiv Monitor

Monitor new arXiv activity for an established topic, author set, or category watchlist.

Command examples assume you are running from the repository root.

## Repository Role

This is a monitoring skill, not the repository's default discovery entry point.

- Use `literature-search` for the first-pass corpus build
- Use `arxiv-database` for one-off arXiv-only querying or PDF retrieval
- Use this skill when the task is continuous watch, weekly digest, or "what changed recently?"

## Do Not Use This Skill For

- full multi-source paper discovery
- thematic synthesis or survey writing
- bibliography validation

## Shared Inputs and Outputs

Preferred inputs:

- topic keywords or watch profile
- optional author names or arXiv categories
- optional existing `outputs/<topic-slug>/paper_db.jsonl` for deduplication

Preferred outputs:

- `outputs/<topic-slug>/monitoring/arxiv_digest.md`
- `outputs/<topic-slug>/monitoring/arxiv_recent.jsonl`

## Workflow

1. Define the watch scope: topic keywords, categories, authors, or competitor labs
2. Query recent arXiv papers with `arxiv-database` or the lighter arXiv search tooling
3. Deduplicate against the current corpus if `paper_db.jsonl` already exists
4. Score papers by relevance, novelty, and likely downstream importance
5. Produce a ranked digest with short reasons to read each paper
6. Hand selected papers to `literature-search`, `systematic-review`, or `literature-review`

## Output

Each digest entry should include:

- title
- authors
- arXiv ID
- date
- why it matters
- recommended next action: ignore / monitor / read / add to corpus

## Related Skills

- Upstream or companion: [arxiv-database](../arxiv-database/), [literature-search](../literature-search/)
- Downstream: [systematic-review](../systematic-review/), [literature-review](../literature-review/), [gap-detection](../gap-detection/)
