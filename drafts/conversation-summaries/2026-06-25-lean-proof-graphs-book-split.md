# 2026-06-25 — Lean proof graphs book split

## Trigger
User wanted the dependency diagram split for the book: 3–4 sub-diagrams plus an overview showing composition into the top certification assertion.

## Done
- Added `context/lean_proof_graphs/` with five Graphviz sources:
  - `01-boundary-measurement.dot` (Spine I)
  - `02-value-transport.dot` (Spine II)
  - `03-correction-successors.dot` (Spine III)
  - `04-selection-limits.dot` (Spine IV)
  - `00-overview.dot` (composition into P02/P30/P30T)
- Added `scripts/render_lean_graphs.sh` → `figures/lean_proof/*.png`
- Added Appendix I § Proof dependency structure with five `[p]` figures
- Updated `formal/README.md`, `metadata/source-canon.md`
- Fixed MB7a→MB7b→MB7c chain in full graph (prior session fix retained)
- PDF build succeeds

## Decisions
- Sub-spines follow book parts: discovery/measurement, value transport, correction/successors, selection/limits.
- Overview uses four summary nodes (Spines I–IV) feeding P02/P30/P30T; MB6 and MB7 shown as bridge chains.
- Full `lean_proof_dependency_graph.dot` kept as developer reference.

## Open / next
- Tune figure sizing if appendix pages still feel tight (currently `width=\textwidth` on `[p]` floats).

## Key paths
- `context/lean_proof_graphs/`
- `figures/lean_proof/`
- `appendices/appI-lean-proof-spine.tex` (`sec:appi-proof-dependency`)

## Commits
- (none this session)
