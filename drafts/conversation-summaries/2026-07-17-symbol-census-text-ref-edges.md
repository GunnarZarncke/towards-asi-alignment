# 2026-07-17 — Symbol census: make text-only cross-references discoverable

## Trigger

Follow-up on the symbol census work (see `2026-07-17-symbol-census-promoted-to-metadata.md`). The
graphs' README documented that the manuscript's dominant citation style — chapter/section-level
prose like `Chapter~\ref{ch:foo}` / `Section~\ref{sec:bar-ch15}` — was invisible to the
dependency graph, since the extractor only turned `\eqref`/`\ref{eq:...}` into edges. The user
asked to make these text-inferred edges discoverable for the parser.

## Done

- Extended `scripts/extract_symbol_formula_graph.py`:
  - New regexes `LABEL_SEC` (`\label{sec:...}`) and `TEXTREF` (`\ref{ch:...}` / `\ref{sec:...}`).
  - `parse_chapter()` now takes optional `ch_owner`/`sec_owner` dicts (mutated in place) mapping
    each `\label{ch:...}`/`\label{sec:...}` to its owning chapter, and records `Formula.text_refs`
    from both math blocks and prose lines.
  - New `resolve_text_ref()` / `emit_text_ref_edges()` helpers: for each text-ref, resolve to the
    target chapter and emit a `chref:chNN` node (cds shape, amber) plus a dashed amber `text-ref`
    edge (edge label carries the specific `sec:...` id when available). Unresolved targets get an
    octagon `textref:...` node, same convention as existing `ghost:` nodes for missing eq targets.
  - Wired through `build_dot()`, `build_combined_dot()`, and `build_coverage_md()` (new "Text
    cross-references" section with counts and the unresolved-target list).
- Regenerated `metadata/symbol-census/symbol-formula-coverage.md` and all four `.dot`/`.svg`
  graphs (`sfdp` for the three large graphs, `dot` for the ch14-only one, per existing convention).
- Updated `metadata/symbol-census/graphs/README.md` (new node/edge types, new "Text-only
  cross-references are now edges too" section, refreshed counts, new coverage-limits point 8) and
  `metadata/symbol-census/README.md` (refreshed leanspine-anchor chapter count, new open-item bullet).

## Decisions

- Section-level refs (`\ref{sec:...}`) resolve to their **owning chapter**, not a per-section node
  — modeling one node per section wasn't worth the complexity; the edge label still carries the
  specific `sec:...` id so the target is identifiable without a dedicated node.
- Text-ref edges are visually distinct (dashed amber, `chref:chNN` target) from formal `\eqref`
  edges (solid green, real formula target) so readers don't mistake chapter-granularity citations
  for equation-granularity dependencies — documented explicitly as coverage-limits point 8.

## Open / next

- 9 of 536 text-ref occurrences don't resolve (`sec:appm-*` appendix labels outside
  `chapters/*.tex`, which this script doesn't parse) — could extend to parse `appendices/*.tex`
  if that gap matters later.
- Adding `\leanspine{}` anchors to the 26 chapters that have none (this count went from 17 to 26
  because chapters with only text-refs, previously absent from the coverage report entirely, are
  now included) is still open, per the pre-existing propagation checklist in the contribution
  audit.
- The older pending items (propagation checklist, 5 unresolved leanspine anchors) are unchanged
  by this session; see `metadata/symbol-census/README.md`'s "Known open items."

## Key paths

- `scripts/extract_symbol_formula_graph.py`
- `metadata/symbol-census/graphs/README.md`
- `metadata/symbol-census/symbol-formula-coverage.md`
- `metadata/symbol-census/graphs/symbol-formula-graph.dot` / `.svg`
- `metadata/symbol-census/graphs/manuscript-lean-crosswalk-graph.dot` / `.svg`

## Commits

- None (not committed; per `AGENTS.md`, only commit when asked).
