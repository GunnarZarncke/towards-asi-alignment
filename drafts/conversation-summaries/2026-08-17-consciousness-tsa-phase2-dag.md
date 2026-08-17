# 2026-08-17 — Consciousness TSA Phase 2 (DAG)

## Trigger
Finish Phase 2: add `ch07 → ch18` informal edge and regenerate dependency graphs.

## Done
- Added to `metadata/concept-graph/chapter-informal-edges.yml`:
  - `ch07 → ch18` with `[candidate-process, boundary-before-bearer]`
- Regenerated: `chapter-{symbol,informal,reading}-dependency.{dot,md}`, section-reference graphs.
- Synced site: `npm run sync:chapter-reading-graph` → JSON + SVG.

## Verification (§28.3)
- Combined graph edge table includes `ch07 → ch18` (informal).
- **ch18 moved from layer 1 to layer 3** (after ch07 in layer 2).
- ch32 still has no edge to/from ch18.
- Section cite graph: `unit:ch07 → unit:ch18` (prose `\ref`s from Phase 1).
- No ch32 ↔ ch18 edge added.

## Open / next
- Phase 3: ledgers + open problem.
- Phase 4: field v2 adjacent-work list.

## Commits
- none
