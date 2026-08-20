# 2026-08-05 — Chapter symbol dependency DAG

## Trigger
After preferring the vertical (TB) eq-chain layout, extract a chapter-level prerequisite DAG from eq-chain bridge symbols for coherent reading paths; then thin transitive edges for a scroll-friendly concept graph.

## Done
- **Vertical eq-chain outputs:** `equation-chain-graph-vertical.dot` and `equation-chain-graph-chapters-vertical.dot` (`rankdir=TB`) from `extract_symbol_formula_graph.py`.
- **Chapter symbol dependency builder:** `scripts/build_chapter_symbol_dependency.py` — aggregates cross-chapter def→use edges; outputs `metadata/concept-graph/chapter-symbol-dependency.dot` (gitignored) + `chapter-symbol-dependency.md` (topo layers, edge table, reading-path notes).
- **Transitive reduction:** drop `A→C` when a longer path exists (69 → 26 edges; 24 chapters).
- **Auto-hook:** eq-chain extractor calls chapter DAG builder at end of run.
- **Docs:** `metadata/concept-graph/README.md`, `metadata/symbol-census/graphs/README.md`.

## Decisions
- Chapter DAG semantics: **provider→consumer** on bridge symbols (defined-then-used), not prose `\ref{ch:…}` cites — complements `section-reference-graph-units.dot`.
- Default layout **TB** for scroll/book friendliness (same as vertical eq-chain).
- Transitive thinning on by default (same policy as section-reference back-ref ranks).

## Open / next
- **C12 basin operationalization** — basins island still isolated (5 nodes); ch38 TODO only.
- Optional: companion-site reading paths from `chapter-symbol-dependency.md` layers.
- Regenerate SVG locally: `dot -Tsvg metadata/concept-graph/chapter-symbol-dependency.dot -o …svg`.

## Key paths
- `scripts/build_chapter_symbol_dependency.py`
- `metadata/concept-graph/chapter-symbol-dependency.md`
- `scripts/extract_symbol_formula_graph.py` (vertical variants + hook)

## Commits
- `b4926095` Add chapter symbol-prerequisite DAG and vertical eq-chain layouts.
