# 2026-08-05 — Equation-chain chapters variant

## Trigger
Add a chapter-aware variant of the equation-chain graph: link each chapter to symbol definitions, without inter-chapter edges. Fix layout and ch08 fan-out after first pass.

## Done
- `build_eq_chain_chapters_dot()` in `scripts/extract_symbol_formula_graph.py` — refactored shared `EqChainCore` / `_compute_eq_chain_core` / `_append_eq_chain_nodes_edges`.
- Emits `equation-chain-graph-chapters.dot`: one amber **unit:chNN → eq** edge per chapter (earliest first-def equation in that chapter, `constraint=true` for layout).
- Dropped chapter→symbol fan-out (was 59 edges; ch08 alone had 18) — symbol defs remain purple eq→sym.
- Updated `metadata/symbol-census/graphs/README.md` (output table + render command).

## Decisions
- Chapter anchor = earliest kept eq in chapter that first-defines a bridge symbol (manuscript order), not every symbol first-defined there.
- Rejected `constraint=false` ch→sym (left all chapters on global left edge).

## Open / next
- Optional: semantic anchor (e.g. prefer `eq:identity-vector` over heuristic `eq:blanket-leakage` for ch08).
- Optional: `--eq-chain-only` to skip Lean/combined regen.

## Key paths
- `scripts/extract_symbol_formula_graph.py` — `build_eq_chain_chapters_dot`, `_chapter_anchor_eq`
- `metadata/symbol-census/graphs/equation-chain-graph-chapters.dot` (gitignored; regen locally)

## Commits
- (this session)
