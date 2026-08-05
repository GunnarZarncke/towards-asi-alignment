# 2026-08-05 — Equation-chain node labels

## Trigger
Fix visible `\n` in eq-chain graph nodes; add source-locating context (chapter, line, eq label) on equation and symbol nodes.

## Done
- `dot_label()` for multi-line Graphviz labels (fixes `dot_escape` doubling `\n` into literal text).
- Equation nodes: slug, `chNN · Lline`, `eq:label`.
- Symbol nodes: name, `def <slug>`, first-def chapter and line.
- Chapter nodes (chapters variant): anchor eq slug, line, `.tex` filename.
- Updated `metadata/symbol-census/graphs/README.md` label note.

## Decisions
- Line numbers are `\label{eq:…}` line in chapter source (editor jump target), not PDF equation numbers.

## Open / next
- None for labels; optional semantic ch08 anchor remains from prior session.

## Key paths
- `scripts/extract_symbol_formula_graph.py` — `dot_label`, `_eq_chain_*_label`

## Commits
- (this session)
