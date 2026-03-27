# Literature Review Analysis Modes

Use these patterns inside `literature-review` instead of routing to a separate top-level analysis skill.

## Cross-Paper Comparison

Write `review/comparison_table.md` when the task needs:
- method-by-method comparison
- dataset or benchmark alignment
- timelines or taxonomies

Prefer `core` and `supporting` papers. Keep `frontier` rows clearly marked as tentative.

## Consensus and Contested Claims

Write `review/consensus_map.md` when the task needs:
- what the field broadly agrees on
- what remains contested
- which claims are still immature

Use `evidence_score` and `caution_flags` before citation counts when deciding whether a claim is settled.

## Contradictions and Claim Tracking

Write `review/contradictions.md` or `review/claim_registry.md` when:
- two papers make incompatible claims
- a paper's status has changed over time
- the review depends on a few critical premises

Track the exact claim text, who supports it, who challenges it, and why the disagreement may exist.

## Gap Detection

Write `review/gaps.md` when the task needs:
- open methodological gaps
- missing evaluations or datasets
- under-tested assumptions
- future-work positioning

Do not call something a gap until you check whether newer `supporting` or `frontier` papers already address it.
