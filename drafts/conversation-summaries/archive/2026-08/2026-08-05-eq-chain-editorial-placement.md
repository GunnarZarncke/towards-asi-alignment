# Session: eq-chain editorial placement (2026-08-05)

## Shipped

- **Extractor:** font-wrapped `B` + subscript → `B_{race}` etc. (not bare `B`).
- **Control:** `\symboldef` moved to early ch11 (~L172); `\symbolref` at spine eq.
- **Basins:** `\mathbb{B}_{\mathrm{race}}`, `\mathbb{B}_{\mathrm{certified}}` in ch38/ch44/appF; `\mathsf{VB}_i` in ch19; `\mathbb{B}_{\mathrm{bearer}}` in ch47.
- **Moves:** responsibility eqs ch08→ch09; `D_G` + signature ch10→ch40; audit-gap ch22→ch32 forward ref.
- **ch26:** CCI section split into validity / vector / scalar subsections.
- **Laundering spine:** `\symboldef` for `D_G`, `Omega_Q`; GLI unchanged in ch40.
- **notation.md:** intro homes aligned to graph; basin rows; regenerate Appendix A.
- **Site:** four dependency spines blurb on `/lean/`; intro pointer.
- **Instructions:** `drafts/editorial-guidance-eq-chain-placement.md`.

## Verification

- 13 `\symboldef`, 12 `\symbolref`; `B_{race}` / `B_{i}` separate in eq-chain core.
- Graphs regenerated; chapters SVG rendered (co-occur off by default).

## Graph cleanup (same session)

- Layout: `ranksep` / `nodesep` / `sep` on eq-chain graphs.
- Co-occur edges gated behind `--cooccur` (default off).
- Single canonical `C_t` (ch25); `\mathcal{C}_t` boundary in ch08; `\theta_{\mathrm{reach}}` in ch12.

## Open

- Propagate `\mathbb{B}` in any remaining concept bodies / open-problems prose grep hits.
- ch19 `\mathsf{VB}_i` if cited elsewhere in prose.
