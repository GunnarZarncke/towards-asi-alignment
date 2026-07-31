# 2026-07-15 — Symbol–formula Graphviz graph

## Trigger
User requested full chapter symbol coverage with symbol→formula mapping in Graphviz format for reachability tracing.

## Done
- Added `scripts/extract_symbol_formula_graph.py` (parses `equation`/`align`/… blocks + prose `\eqref`).
- Generated `drafts/symbol-formula-graph.dot` (646 formula nodes, 740 symbols, 32 chapters with display math).
- Generated `drafts/symbol-formula-coverage.md` (per-chapter symbol→formula tables).
- Generated `drafts/symbol-formula-graph-ch14.dot` + `symbol-formula-graph-ch14.svg`.
- Wrote `drafts/symbol-formula-graph-README.md` (semantics, render, reachability CLI).

## Decisions
- Three node kinds: labeled eq, unlabeled display block (`chNN:unlabeled:LINE`), prose ref (`chNN:prose:LINE`).
- Two edge kinds: `in` (symbol→formula), `ref` (formula→formula); external refs → dashed `ghost:` nodes.
- Inline `$...$` outside display environments not extracted (documented limitation).

## Open / next
- Extend parser for inline math if needed; 16 chapters currently have zero display blocks in scan.
- Optional: JSON adjacency export; merge ghost nodes for full cross-chapter reachability queries.

## Key paths
- `scripts/extract_symbol_formula_graph.py`
- `drafts/symbol-formula-graph.dot`
- `drafts/symbol-formula-coverage.md`
- `drafts/symbol-formula-graph-README.md`

## Commits
- None

## Update (same day, follow-up): added Lean spine layer

### Trigger
User noticed the generated graph had "very short chains and no Lean symbols," suspecting the extraction was missing real depth.

### Root cause (confirmed, not a false alarm)
1. The manuscript-only graph only chains through `\eqref`/`\ref{eq:...}` — genuinely sparse (69 refs across 646 formula nodes) because the book cross-references at chapter/section granularity in prose, not per-equation.
2. The script never parsed `formal/AlignmentProofSpine/**/*.lean` at all, so no Lean node could ever appear, even though the Lean spine (1016 declarations, 37 files) has far deeper import/proof-term dependency chains.
3. The actual manuscript↔Lean crosswalk anchor, `\leanspine{kind}{node}{gloss}` (69 occurrences, 22 chapters), was also never parsed.

### Done
- `parse_lean_files()`: parses `formal/AlignmentProofSpine/**/*.lean` top-level declarations (theorem/lemma/def/structure/axiom/inductive/instance) and their import statements; `strip_lean_comments()` strips `--`/`/- -/`/`/-- -/` comments first — doc-comment prose (e.g. `/-! ## Section -/` headers) was previously false-matching the decl-start regex and truncating bodies, which had suppressed most real `uses` edges (100 → 2751 after the fix, same 1016-decl count both times).
- `parse_leanspine_refs()` + `resolve_lean_alias()` + `expand_leanspine_node()`: parses `\leanspine{}` anchors, resolves short proof-spine ids (`P13`, `MB8`) to full Lean names (`P13_risk_gap_bounded_by_cci_slack`, `MB1_estimator_soundness`) via prefix match, and expands ranges (`MB7a--MB7d`, `MB1--MB9`) into individual nodes.
- New outputs: `drafts/lean-dependency-graph.dot` (Lean-only, 1016 nodes/2751 edges) and `drafts/manuscript-lean-crosswalk-graph.dot` (symbol → formula → leanspine anchor → Lean declaration, full chain). Both render only with `sfdp`, not `dot` (`dot`'s layered ranking algorithm hangs/spews `trouble in init_rank` on a graph this large and cyclic).
- `symbol-formula-coverage.md` gained a "Lean spine coverage" section: per-anchor resolution table, chapters with zero `\leanspine{}` anchors (17: ch02/ch04/ch12/ch13/ch14/ch16/ch22/ch23/ch24/ch32/ch34/ch36/ch37/ch38/ch40/ch44/ch46), and 5 unresolved anchors (`P34A`, `P34K`, `P35M`, `P38H`, `inferential-ici`).
- `symbol-formula-graph-README.md` updated with the root-cause explanation, new node/edge semantics, verified example chain, and `sfdp` render instructions.

### Decisions
- `uses` edges are heuristic whole-word token matching against a declaration's body text, not Lean's elaborated term graph — documented as a coverage limit; authoritative dependency checks should use `#print axioms` per `formal/README.md`.
- Did not touch `context/lean_proof_dependency_graph.dot` (the existing hand-curated "conjectured" Lean graph) — the new `lean-dependency-graph.dot` is a separate, source-parsed cross-check, not a replacement.

### Open / next
- 17 chapters have zero `\leanspine{}` anchors — real gap, not a script bug; adding anchors there is manuscript work, not extraction work.
- 5 unresolved anchor names (`P34A`/`P34K`/`P35M`/`P38H`/`inferential-ici`) should be checked against `metadata/TODO.md`'s Lean proof-spine gap list — either not yet formalized under that name, or need a resolver rule.

### Key paths (additional)
- `drafts/lean-dependency-graph.dot` / `.svg`
- `drafts/manuscript-lean-crosswalk-graph.dot` / `.svg`
