# Editorial guidance: eq-chain placement (2026-08-05)

Durable instructions for manuscript moves driven by the revised equation-chain graph.

## Goals

- Align symbol **first-definition** order with dependency spines (boundary, correction, laundering, selection).
- Disambiguate basin vs bundle notation using **subscript truth** (extractor emits `B_{race}`, not font).
- Move graph-isolated clusters to natural chapter homes without full Part reorder.

## Non-goals

- No ch11 BIQ cluster move.
- No wholesale rename of generic ch03 `\mathcal{B}` safety basins.
- No `\symboldef` for basins when subscript extraction suffices.

## Extractor rule (basins)

In `scripts/extract_symbol_formula_graph.py`, font-wrapped identifiers with subscripts map to subscripted hub ids:

- `\mathbb{B}_{\mathrm{race}}` → `B_{race}`
- `\mathcal{B}_{\mathrm{safe}}` → `B_{safe}`
- Bare `\mathcal{B}` (no subscript) → `B`
- Bundle `B_i` → `B_{i}` (distinct from `B_{race}`)

## Chapter edit recipes

### ch11 — Control

- **First `\symboldef[Control]`** after `eq:ctrl-info-int` (~L170).
- **`\symbolref[Control]`** at `eq:control-capacity-spine` (~L671).

### Basins vs bundles

- **Race/certified:** `\mathbb{B}_{\mathrm{race}}`, `\mathbb{B}_{\mathrm{certified}}` in ch38; echoes in ch44, appF, concept cards.
- **ch19 pair:** `\mathsf{VB}_i = (B_i,\Phi_i)` — not `\mathcal{B}_i`.
- **ch47 bearers:** `\mathbb{B}_{\mathrm{bearer}}`.

### ch08 → ch09 — Responsibility

- **Move:** `eq:responsibility-capacity`, `eq:responsibility-gap`, prose → ch09 `sec:composite-responsibility`.
- **Leave in ch08:** 2–4 sentence pointer after Merging.
- **Keep:** Split/merge eqs at head of `sec:splitting`.

### ch10 → ch40 — Goal divergence

- **Move:** `eq:goal-divergence`, `eq:goal-laundering-signature` → ch40 `sec:problem-ch40` with `\symboldef[D_G]`.
- **Leave in ch10:** opacity→laundering stub; `\symboldef[Omega_Q]` on selective-opacity score.
- **Remove from ch10:** full `D_G` definition block.

### ch22 → ch32 — Audit gap

- **Remove** labeled `eq:self-control-audit-gap` from ch22; forward ref to ch32 `sec:core-failure-condition-ch32`.
- **Do not move** `eq:bundle-conservation-ch22`.

### ch26 — Split CCI section

Subsections under `sec:correction-channel-integrity-def`:

1. `sec:cci-validity` — ValidRef / invalidation
2. `sec:cci-vector` — `\vec{CCI}` vector certificate
3. `sec:cci-scalar` — `CCI_\lambda` projection
4. `sec:coerced-correction` — existing

Seam sentence to `sec:value-bundle-correction` (bundle geometry cluster).

## Notation.md

- **Home column = first formal definition** (not ch46/ch48 capstone roster).
- Add rows: `B_{race}`, `B_{certified}`, `D_G`, `Omega_Q`, `mathsf{VB}_i`.
- Regenerate: `python3 scripts/generate_notation_appendix.py`.

## Four dependency spines (reading guide)

**Site:** `site/src/pages/lean/index.astro` § dependency-spines.

**Manuscript pointer:** `frontmatter/introduction.tex` § How to Read.

**Phrasing:**

> Four dependency spines run through the book's formal vocabulary. **Boundary** asks whether the system is carved so leakage and partition are measurable. **Correction** asks whether a legitimate channel can still change the system. **Laundering** asks whether goals, bundles, or bearers are being rewritten under stakes and opacity. **Selection** asks whether the deployment environment grows what the certificates claim to bound. These spines are reading order for symbols and chapters; they are related to, but not identical with, the Lean proof spines in Appendix G.

Distinct from Lean Spine I–IV (`context/lean_proof_graphs/00-overview.dot`).

## Verification

```bash
python3 scripts/extract_symbol_formula_graph.py
dot -Tsvg metadata/symbol-census/graphs/equation-chain-graph-chapters.dot \
  -o metadata/symbol-census/graphs/equation-chain-graph-chapters.svg
python3 scripts/generate_notation_appendix.py
make check
```

Confirm: Control first-def early ch11; `B_{race}` ≠ `B_{i}`; `D_G`/`GLI`/`Omega_Q` in chain; responsibility eqs in ch09; ch32 owns audit-gap story.
