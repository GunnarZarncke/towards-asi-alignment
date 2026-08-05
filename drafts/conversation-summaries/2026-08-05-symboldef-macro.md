# 2026-08-05 — `\symboldef` macro + eq-chain integration

## Done

- Added `\symboldef` / `\symboldef[id]{math}` to `metadata/preamble.tex` (invisible at render; like `\leanspine`).
- Extractor: `SymbolDef` dataclass, brace-balanced parser, `canonical_symbol_id`, integration in `_compute_eq_chain_core` and eq-chain DOT builders.
- Eq-chain graph: amber `symdef:chNN:line` note nodes; purple def edges; chapter anchors can point at symdef sites.
- Extraction tweaks: `\mu_E`, `\kappa_{\mathrm{sel}}` patterns; skip bare `\mu` when `\mu_E` present.
- Pilot manuscript marks: CCI (ch26), Control (ch11), epsilon (ch07), mu_E + kappa_sel (ch34), RiskGap (ch33).
- Documented in `metadata/symbol-census/graphs/README.md`.

## Verified in regenerated `equation-chain-graph.dot`

Bridge symbols newly / better anchored via symdef: **CCI**, **Control**, **epsilon**, **mu_E**.

**2026-08-05 batch (Tier 1–3):** **RiskGap** now chains (labeled leaves ch42/ch48); **GLI** chains (`eq:gli-ch40` → `eq:gli-stop-ch40`). Added symdefs: Fit_E, ICI, SelfControlGap, BIQ, CCI_λ. **Removed** `kappa_sel` symdef — symbol appears only once (summand in `eq:deployment-mass-ch34`, ch34 prose); not a cross-chapter bridge.

**Not yet chaining:** Fit_E, ICI, SelfControlGap, BIQ, CCI_λ — def sites only (no later labeled RHS uses, or use-before-def for ICI at L153).

## Open

- `\symbolref` for explicit use sites (especially unlabeled display math).
- More `\symboldef` marks per `metadata/notation.md` (BIQ, GLI, etc.) as needed.
- Optional: symdef line number vs `\begin{equation}` line for defs inside eq blocks.

## Regenerate

```bash
python3 scripts/extract_symbol_formula_graph.py
dot -Tsvg metadata/symbol-census/graphs/equation-chain-graph.dot -o metadata/symbol-census/graphs/equation-chain-graph.svg
```
