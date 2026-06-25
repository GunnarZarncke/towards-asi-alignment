# 2026-06-25 — CCI canonical definition consolidation

## Trigger
User asked to define correction-channel integrity (CCI) only once and adapt other chapter uses to cross-reference it.

## Done
- **Canonical home:** `chapters/ch25-correction-channel-integrity.tex` — `\label{eq:cci-ch25}` on Section `\ref{sec:correction-channel-integrity-def}` only; chapter thesis and compact summary use `\eqref` instead of re-displaying.
- **ch24:** Demoted CCI functional (removed `eq:correction-channel-integrity-ch24` and `\lambda_G G`); channel remains canonical here; forward to ch25.
- **Replaced full CCI re-definitions** with cross-refs in ch02, ch03, ch14, ch21, ch23, ch26, ch27, ch29, ch31, ch34, ch35, ch36, ch37, ch38, ch42.
- **Stale MI formulas** removed from ch37/ch38; ch36 keeps `\mathcal{C}_{\text{corr}}` as diagnostic proxy for `C_{\mathrm{raw}}`.
- **Metadata:** `notation.md`, `terminology.md`, `INSTRUCTIONS.md` §6.9, `appendices/appF-glossary.tex` point to ch25 as sole manuscript definition.
- **Build:** `./build.sh` succeeded → `dist/pdf/towards-superintelligence-alignment.pdf`.

## Decisions
- ch25 owns **both** `eq:correction-bottleneck-capacity` and `eq:cci-ch25`; ch24 keeps `eq:correction-raw-capacity` for channel-view capacity only.
- Goodhart remains a failure mode (lowers capacity / raises `M`), not a separate `\lambda_G` penalty — consistent with fix-plans §C4.
- ch36 proxy `I(C^H_t;A_{t+k}\mid\cdot)` explicitly labeled as approximation when `\kappa_i` unavailable.

## Open / next
- ch24 § `\ref{sec:measuring-cci}` still lists operational audit quantities (not a second CCI definition); optional rename to avoid “Measuring CCI” confusion.
- ch11/ch12 use `C_{\mathrm{raw}}` without always cross-refing ch25 — acceptable where capacity growth is the topic.

## Key paths
- `chapters/ch25-correction-channel-integrity.tex` (`sec:correction-channel-integrity-def`, `eq:cci-ch25`, `eq:correction-bottleneck-capacity`)
- `metadata/notation.md`, `INSTRUCTIONS.md` §6.9

## Commits
- (none — user did not request commit)
