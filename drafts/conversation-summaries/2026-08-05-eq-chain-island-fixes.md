# 2026-08-05 — Eq-chain island fixes

## Trigger
Continue eq-chain editorial pass: tighten loose basin defs (TODO only), repair K_coll / ICI / 𝓡_i / CCI_λ / SelfControlGap graph islands, end session with commit.

## Done
- **ch38:** `% TODO[formalize]` on `\mathbb{B}_{\mathrm{race}}` / `\mathbb{B}_{\mathrm{certified}}`; track rows in `metadata/TODO.md` and `metadata/notation.md` (C12 operationalization).
- **ch13:** K_coll spine — `\symboldef[B_i]`, `K_i := B_i`, `\symboldef[K_coll]` / `G_coord` / `Omega_coord`, `\partial K_{\mathrm{coll}}/\partial B_i`, labeled `eq:reversibility-correction-coupling-ch13` with `\symbolref[C_raw]`.
- **ch35:** ICI block moved before `eq:uad-inferential-kappa-ch35` (def-before-use in prose order).
- **ch09 + ch11:** `\symboldef[mathcal_R_i]`, `\symboldef[K_X]` on `eq:biq`, `eq:responsibility-gap-bridge-ch11` (labeled use of both); `\symbolref` on `eq:responsibility-gap`.
- **ch33:** `\symbolref[SelfControlGap]` on `eq:risk-gap`.
- **ch10/ch14/ch25/ch40:** `\symbolref` bridges for `Omega_Q`, `C_raw`, `D_G` (GLI four-term preserved).
- **C_raw spelling:** `\text{raw}` → `\mathrm{raw}` in ch03, ch19, ch41, ch45, `INSTRUCTIONS.md`, `metadata/notation.md`.
- **Extractor:** `\symboldef` LHS override (`CCI_lambda`); `\symbolref` canonical ids merged into equation `used_symbols`.
- Regenerated eq-chain graphs locally (gitignored `.dot`/`.svg`); **5 components**, main spine **199 nodes**.

## Decisions
- Basins stay expositional until percolation / `\mu_E` machinery exists — no forced inequalities or fake graph edges.
- ch13→ch35 κ prose cross-ref skipped (user).
- GLI stays four-term; `D_G` linked via `cf.` in `eq:gli-ch40`, not as summand.
- ICI remains a small ch35-local island (3 nodes) — no external deps yet; ordering fix is sufficient for now.

## Open / next
- Operationalize macro basins (C12); concept cards for `\mathbb{B}_{\mathrm{race}}` / `\mathbb{B}_{\mathrm{certified}}`.
- Remaining islands: basins (4), ICI cluster (3), plus any ch08 split-transport locals.
- Forward-ref policy: ch09 `eq:responsibility-gap` still uses `K_X` before ch11 in PDF order (bridge eq is the post-def spine link).
- Untracked drafts in tree (`lw-*`, `TSA.png`, etc.) — not part of this commit.

## Key paths
- `scripts/extract_symbol_formula_graph.py`
- `chapters/ch13-coordination-bottleneck.tex`, `ch35-multi-agent-strategic-coupling.tex`, `ch09-composite-agent.tex`, `ch11-capability-without-task-ontology.tex`
- `metadata/TODO.md`, `metadata/notation.md`
- `drafts/editorial-guidance-eq-chain-placement.md`

## Commits
- (this session)
