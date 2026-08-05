# Symbol census

A permanent, regeneratable audit of every symbol, formula, and Lean declaration in
**towards-asi-alignment**: which ones pay rent toward the thesis, where each one is used, and
how far its dependency chain reaches into the Lean proof spine.

This started as an ad hoc review in `drafts/` (2026-07-15/16) and was promoted here on
2026-07-17 once the first reduce/remove pass was applied, per
[`drafts/conversation-summaries/archive/2026-07/2026-07-17-symbol-audit-reduce-remove-pass.md`](../../`drafts/conversation-summaries/archive/2026-07/2026-07-17-symbol-audit-reduce-remove-pass.md`).

## Contents

| File | Answers | Generated? |
|------|---------|------------|
| [`symbol-contribution-audit.md`](symbol-contribution-audit.md) | *Should we keep this symbol?* — per-symbol action (keep / reduce / remove / footnote / appendix-future / lean-demo-exp / optional-md / expand), reasoning, source chapter, line numbers | No — hand-written review, updated by hand as actions are applied |
| [`symbol-formula-coverage.md`](symbol-formula-coverage.md) | *Where is this symbol used?* — per-chapter symbol → formula tables, plus a Lean-spine crosswalk coverage section | Yes — `scripts/extract_symbol_formula_graph.py` |
| [`graphs/`](graphs/) | *What does it reach?* — Graphviz `.dot` sources and rendered `.svg` graphs tracing symbol → formula → `\leanspine{}` anchor → Lean declaration dependency chains | Yes — same script |

The contribution audit (*should we keep it*) and the coverage/graph outputs (*where is it used,
what does it reach*) are complementary and deliberately kept as separate documents: the audit
is editorial judgment that gets updated by hand as actions are applied to chapters; the coverage
and graphs are mechanically regenerated from the current state of `chapters/*.tex` and
`formal/AlignmentProofSpine/**/*.lean` and would be overwritten by hand-edits.

## Regenerate the mechanical parts

```bash
python3 scripts/extract_symbol_formula_graph.py
# then re-render the graphs (see graphs/README.md "Render" for why dot vs sfdp and why these flags):
cd metadata/symbol-census/graphs
dot  -Tsvg symbol-formula-graph-ch14.dot                                              -o symbol-formula-graph-ch14.svg
sfdp -Goverlap=prism -Gsep="+20" -GK=2   -Gmaxiter=300 -Tsvg symbol-formula-graph.dot            -o symbol-formula-graph.svg
sfdp -Goverlap=prism -Gsep="+15" -GK=1.5 -Gmaxiter=300 -Tsvg lean-dependency-graph.dot           -o lean-dependency-graph.svg
sfdp -Goverlap=prism -Gsep="+20" -GK=2   -Gmaxiter=300 -Tsvg manuscript-lean-crosswalk-graph.dot -o manuscript-lean-crosswalk-graph.svg
```

The contribution audit (`symbol-contribution-audit.md`) is not regenerated; update it by hand
when a new review pass changes a symbol's recommended action.

## Using this when writing or reviewing a chapter

1. Before adding a new symbol, check `symbol-contribution-audit.md` for a similar existing
   symbol and `metadata/notation.md` for the canonical name — avoid re-deriving something that
   already has a home elsewhere (see the audit's "symbol collisions" and "notation-index drift"
   tables for known problem spots).
2. After a substantive edit to a chapter's formalism, regenerate the coverage/graphs and skim
   `graphs/README.md`'s "coverage limits" section for what the extractor does and does not see.
3. If you add or change a `\leanspine{proof|counterexample|bridge}{node}{gloss}` anchor, check
   the regenerated "Lean spine coverage" section of `symbol-formula-coverage.md` to confirm the
   node resolves to an actual Lean declaration.

## Known open items (as of 2026-07-17)

- Notation-index drift: `metadata/notation.md` lists ch46/ch48 as home for several symbols
  (correction chain, CCI, $\Delta L_*$, $\mu_E$, $\vec\Pi$, $\kappa_{\mathrm{sel}}$, RiskGap,
  GLI, $\chi_{ij}(a)$) whose actual manuscript home moved to ch25–ch40 — see
  `symbol-contribution-audit.md`'s "Notation-index drift" table. Only the $\mathrm{ICI}_{ij}$
  row (ch48 → ch35) has been fixed so far.
- 5 of 68 `\leanspine{}` anchors don't resolve to a parsed Lean declaration
  (`P34A`, `P34K`, `P35M`, `P38H`, `inferential-ici`) — see `graphs/README.md` point 7.
- 26 chapters have zero `\leanspine{}` anchors at all (see `graphs/README.md` point 6) — every
  formula in those chapters is a dead end in the combined graph until anchors are added.
- Chapter/section-level cross-references (`\ref{ch:...}`, `\ref{sec:...}` — the manuscript's
  dominant citation style, ~536 occurrences) live in [`metadata/concept-graph/`](../concept-graph/)
  (`section-reference-graph.dot`), not in the symbol→formula graph. See that folder's README and
  `glossary-section-audit.md`. Unresolved appendix `sec:` labels remain a parser gap.
- Most of the audit's ~42 **reduce** and ~8 **remove** rows are still open; the 2026-07-17 pass
  applied 5 of them (see the "Applied" note at the top of `symbol-contribution-audit.md`).
