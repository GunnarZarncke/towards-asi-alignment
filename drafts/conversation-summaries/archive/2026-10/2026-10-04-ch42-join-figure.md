# 2026-10-04 — Ch. 42 join figure in chapter

kind: new-work
uptake: local

## Trigger
Add the reviewed safety-case join Graphviz figure to Chapter 42.
Prompts: none resolved (paraphrase-only)

## Done
- content: `figures/ch42-safety-case-join.dot` (canonical), `.pdf`/`.png` renders; included as `fig:ch42-safety-case-join` in `chapters/ch42-safety-case.tex`.
- content: Plain-Language Model walks the join instead of the eight-item layer list; Formal Model longtable removed; `LayeredAlignedDef` is the join; `MB6` lands on join conjuncts, not as a cycle into the correction box.
- bookkeeping: extract records whose quotes were deleted dropped; `python3 scripts/check_claim_extract.py` → `ch42.jsonl: 0 error(s)`.
- bookkeeping: `drafts/plans/claim-extract/claim-extract.md` points at `figures/`.

## Decisions
- Caption carries title and arrow key; no legend on the graph.
- PDF include for print (`figures/ch42-safety-case-join.pdf`).

## Open / next
- Summary still says seven layers; opening artifact list still seven names; worked-example bullets not retold from the figure (plan item 1 remainder).
- Remaining P1 table items (root naming, G0 paragraph, etc.).

## Key paths
- `chapters/ch42-safety-case.tex`
- `figures/ch42-safety-case-join.dot`

## Commits
- none
