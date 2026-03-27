# Citation Verification Workflow

This note defines the repository-standard rule for citation hygiene:

**Never generate BibTeX from memory. Always verify programmatically.**

## Why This Matters

Common AI citation failures include:

- fabricated titles with real-looking author names
- wrong year or venue
- fake DOI or arXiv identifiers
- plausible but nonexistent papers

For literature reviews and surveys, these errors are especially costly because one bad citation can contaminate multiple sections.

## Verification Priority

1. Search for the paper with Semantic Scholar or another scholarly index
2. Confirm the paper exists in at least one independent metadata source such as CrossRef, OpenAlex, or arXiv
3. Prefer DOI-based BibTeX retrieval when DOI is available
4. Verify that the cited paper actually supports the intended claim
5. Only then add it to the bibliography

## Recommended Source Routing

- ML / AI search: Semantic Scholar
- DOI lookup and BibTeX retrieval: CrossRef / DOI content negotiation
- preprints: arXiv
- broad open metadata cross-check: OpenAlex

## Safe Fallback

If you cannot verify a citation:

- do not fabricate the BibTeX
- keep a clear placeholder in the draft
- tell the user which citations still require manual verification

Example placeholder policy:

- `\\cite{PLACEHOLDER_verify_this_reference}`
- comment or note explaining what still needs verification

## Claim Validation

Existence is not enough. Before citing a paper for a specific statement:

- check the abstract, result section, or relevant note
- make sure the paper really supports the sentence you are attaching it to
- do not use a nearby or thematically similar paper as a substitute for a missing citation

## Integration Points

- `citation-management`: citation repair, validation, and harvesting
- `survey-generation`: end-stage bibliography validation
- `related-work-writing`: section-level support checking
