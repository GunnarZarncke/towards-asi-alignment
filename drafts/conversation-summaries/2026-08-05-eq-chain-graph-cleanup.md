# 2026-08-05 — Eq-chain graph cleanup

## Trigger

Continue eq-chain editorial pass: reduce graph noise (layout, dashed co-occur edges), disambiguate overloaded symbols (`C_t`, `\theta`), single canonical defs.

## Done

- **Layout:** `ranksep=1.4`, `nodesep=0.45`, `sep=+24` on eq-chain `dot` graphs.
- **Co-occurrence:** sym↔sym co-occur edges optional; **`--cooccur` flag** (off by default). README updated.
- **`C_t`:** canonical `\symboldef[C_t]` in ch25; tuple decompositions use `\symbolref` (ch25/ch26/ch28); boundary partition renamed `\mathcal{C}_t` in ch08; extractor emits `mathcal_C_{t}` distinct from correction `C_t`.
- **`\theta`:** reach cutoff → `\theta_{\mathrm{reach}}` in ch12 (`eq:predictive-reach`, `eq:control-reach`); MI/correction threshold keeps bare `\theta`.
- **Manuscript (continued from editorial pass):** Control/basin notation, chapter moves (responsibility, D_G, CCI split), `\symboldef`/`\symbolref`, notation.md, site dependency spines — see `2026-08-05-eq-chain-editorial-placement.md` and `drafts/editorial-guidance-eq-chain-placement.md`.
- **Extractor:** normalize_chain_sym_id, symref labels, co-occur gating, mathcal disambiguation.
- Graphs regenerated (`.dot`/`.svg` gitignored).

## Decisions

- Co-occur is editorial overlay only; def/use chain is default view.
- Rarer reach parameter gets new symbol (`\theta_{\mathrm{reach}}`), not the widely reused MI threshold.

## Open / next

- `\theta` still collides with latent-model `p_\theta` in ch16/ch22 eq-chain hub — separate pass if still noisy.
- ch11/ch09 prose still use bare `C_t` for boundary in places (not eq-chain defs).
- Propagate `\mathbb{B}` basin notation in concept bodies grep hits.
