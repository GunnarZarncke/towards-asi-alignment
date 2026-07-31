# 2026-07-17 — Symbol census promoted to `metadata/symbol-census/`

## Trigger

User: "Make this census of symbols a proper element of the book including proper rendering of the graph in its own subfolder and mentioned in the README." Asked via `AskQuestion` for scope; user chose: (1) repo-level permanent artifact (not a new LaTeX appendix, not the site), (2) keep the large graphs as browser-viewable SVGs only (no attempt at print-legible figures), (3) keep the contribution audit and the coverage report as separate documents, updating the audit's action list to reflect the reduce/remove pass applied earlier this session.

## Done

- Created `metadata/symbol-census/` as the permanent home, moving (not copying) the previously ad hoc `drafts/` artifacts:
  - `symbol-contribution-audit-2026-07-15.md` → `metadata/symbol-census/symbol-contribution-audit.md` — added an "Applied 2026-07-17" note at the top pointing at the reduce/remove pass log, without rewriting the rest of the hand-written audit.
  - `symbol-formula-coverage.md` → `metadata/symbol-census/symbol-formula-coverage.md` (regenerated fresh, see below).
  - `symbol-formula-graph-README.md` → `metadata/symbol-census/graphs/README.md` — updated all `drafts/`-relative paths, updated the render instructions (see below), fixed hardcoded counts to match regeneration.
  - `symbol-formula-graph.dot/.svg`, `symbol-formula-graph-ch14.dot/.svg`, `lean-dependency-graph.dot/.svg`, `manuscript-lean-crosswalk-graph.dot/.svg` → `metadata/symbol-census/graphs/`.
- Updated `scripts/extract_symbol_formula_graph.py` default output paths (`--out`, `--coverage`) and the hardcoded path string inside `build_coverage_md()` to point at the new location; updated the module docstring's usage example.
- Regenerated the coverage report and all three script-generated `.dot` files from the current manuscript state (which now includes this session's ch13/ch14/ch15/ch19/ch35 edits): 637 formula nodes / 719 symbols in the manuscript-only graph (down slightly from 646/740, consistent with the reductions applied earlier this session); Lean-spine stats unchanged (1016 declarations, 68 `\leanspine{}` anchors, 5 unresolved, 17 chapters with none).
- Re-rendered all four SVGs. Discovered that `dot` now hangs (`trouble in init_rank`) on the full manuscript-only graph too, not just the two Lean graphs — it has grown past `dot`'s practical layered-ranking limit. Rendered all three large graphs (`symbol-formula-graph.svg`, `lean-dependency-graph.svg`, `manuscript-lean-crosswalk-graph.svg`) with `sfdp` instead; only the small `symbol-formula-graph-ch14.svg` still renders fine with `dot`. Updated `graphs/README.md`'s render section accordingly.
- Wrote `metadata/symbol-census/README.md` as the top-level overview: what the three pieces (audit / coverage / graphs) each answer, why they're kept as separate documents (hand-maintained judgment vs. machine-regenerated), regenerate instructions, and a "known open items" section (notation-index drift, unresolved leanspine anchors, chapters with no leanspine anchors, most audit rows still open).
- Added a "Symbol census" row to the main `README.md`'s "Manuscript at a glance" table, next to the existing "Formal spine" row.
- Verified: `python3 scripts/check_bibliography_summaries.py` still passes; no remaining `drafts/symbol-*` or `drafts/lean-dependency-graph`/`drafts/manuscript-lean-crosswalk-graph` references outside historical conversation logs (left untouched — they are a record of what was true at the time).

## Decisions

- **Not a new LaTeX appendix.** The graphs are thousands of nodes (`manuscript-lean-crosswalk-graph.dot` alone is ~7.9k lines) and illegible as static print figures; embedding a distilled version would require curatorial work (choosing which ~20 spine symbols to show) that wasn't requested. Per the user's explicit choice, this stays a repo-level artifact referenced from the README rather than compiled into the PDF.
- **`metadata/` over a new top-level folder.** `metadata/` already holds the manuscript's other hand+machine-maintained ledgers/indexes (`notation.md`, `claims-ledger.md`, `TODO.md`, etc.); the symbol census is the same kind of artifact, just larger, hence its own subfolder rather than loose files.
- **Audit and coverage stay separate files**, per the user's explicit choice, rather than merging "should we keep it" judgment with "where is it used" mechanics into one table — the audit is hand-edited over time as actions are applied; the coverage/graphs are fully regenerated and would lose hand-edits on the next run.
- **Minimal-touch update to the audit file**: rather than rewriting all five affected rows (some duplicated across the Executive Summary and Part B tables), added one "Applied" callout at the top pointing to the session log, leaving the original per-row text as a historical record of the review that motivated the edit.

## Open / next

- The audit's remaining ~40 `reduce`/`remove` rows and the notation-index-drift list (`metadata/notation.md` ch46/ch48 homes) are still open — not touched this session beyond the one `ICI_ij` row fixed earlier.
- `graphs/README.md` point 2 ("some chapters have zero display blocks") and point 6/7 (leanspine coverage gaps) are unchanged and still open; see `metadata/symbol-census/README.md`'s "Known open items."
- No LaTeX build was run — this was a repo-organization task, not a manuscript-content task (beyond the already-logged ch13/14/15/19/35 edits).

## Key paths

- `metadata/symbol-census/README.md` — start here.
- `metadata/symbol-census/symbol-contribution-audit.md`, `symbol-formula-coverage.md`, `graphs/` — the three pieces.
- `scripts/extract_symbol_formula_graph.py` — regeneration script, paths updated.
- `README.md` — one new table row ("Symbol census").

## Commits

- None (no commit requested this session).
