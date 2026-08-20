# 2026-08-05 — Equation-chain def/use graphs

## Trigger
Build manuscript dependency graphs: section/chapter refs in `concept-graph/`, symbol→equation chains in `symbol-census/`. Fix equation-chain graph so symbols get incoming arrows via **definition vs use** (not duplicate bidirectional sym↔eq edges).

## Done
- Added `scripts/build_section_reference_graph.py` — section/chapter `\ref` DAG, unit overview, eq line-order spines, transitive thinning on back-ref ranks; outputs under `metadata/concept-graph/`.
- Extended `scripts/extract_symbol_formula_graph.py`:
  - `split_defined_used_symbols()` — LHS `=` defines, RHS uses; tuple intro via `\left(…\right)` / `(…)`; fixed LaTeX `\\` vs `\command` split bug; subscript false-positive on command tails (e.g. `\kappa_{ij}`).
  - `build_eq_chain_dot()` — purple **eq→sym** (define), blue **sym→eq** (use, after first def in manuscript order).
  - `equation-chain-graph.dot` emitted alongside existing symbol-formula outputs.
- Updated `metadata/symbol-census/graphs/README.md`, `metadata/symbol-census/README.md` (concept-graph pointer), `metadata/concept-graph/README.md`.
- Glossary section crosswalk: `metadata/concepts.yml` `bookLabels` additions; audit files in `metadata/concept-graph/`.
- `.gitignore`: symbol-census + concept-graph generated `.dot`/`.svg` and `symbol-formula-coverage.md`; removed tracked graph binaries from index.

## Decisions
- Equation chains are **def/use bipartite**, not undirected sym↔eq — user rejected duplicate reverse edges.
- Generated graph artifacts stay local (gitignored); scripts + READMEs are source of truth.

## Open / next
- Optional: first-definition-only (drop re-statement def edges like ch13 `\kappa`).
- Optional: `--eq-chain-only` flag to skip slow Lean/combined graph regen.
- Section graph still large; `sfdp` for full SVG; eq-chain graph renders with `dot`.

## Key paths
- `scripts/extract_symbol_formula_graph.py` — `split_defined_used_symbols`, `build_eq_chain_dot`
- `scripts/build_section_reference_graph.py`
- `metadata/concept-graph/README.md`
- `metadata/symbol-census/graphs/README.md`

## Commits
- `226783e9` Add def/use equation chains and section reference graph scripts.
