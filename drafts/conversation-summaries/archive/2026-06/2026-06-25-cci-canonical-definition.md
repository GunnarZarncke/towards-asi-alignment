# 2026-06-25 — CCI canonical definition consolidation

## Trigger
User asked to define correction-channel integrity (CCI) only once and adapt other chapter uses to cross-reference it.

## Done
- **Canonical home:** `chapters/ch26-correction-channel-integrity.tex` — `\label{eq:cci-ch46}` on Section `\ref{sec:correction-channel-integrity-def}` only; chapter thesis and compact summary use `\eqref` instead of re-displaying.
- **ch46:** Demoted CCI functional (removed `eq:correction-channel-integrity-ch46` and `\lambda_G G`); channel remains canonical here; forward to ch46.
- **Replaced full CCI re-definitions** with cross-refs in ch02, ch03, ch14, ch46, ch46, ch46, ch48, ch48, ch48, ch46, ch48, ch46, ch48, ch45, ch46.
- **Stale MI formulas** removed from ch48/ch45; ch46 keeps `\mathcal{C}_{\text{corr}}` as diagnostic proxy for `C_{\mathrm{raw}}`.
- **Metadata:** `notation.md`, `terminology.md`, `INSTRUCTIONS.md` §6.9, `appendices/appE-glossary.tex` point to ch46 as sole manuscript definition.
- **Build:** `./build.sh` succeeded → `dist/pdf/towards-superintelligence-alignment.pdf`.

## Decisions
- ch46 owns **both** `eq:correction-bottleneck-capacity` and `eq:cci-ch46`; ch46 keeps `eq:correction-raw-capacity` for channel-view capacity only.
- Goodhart remains a failure mode (lowers capacity / raises `M`), not a separate `\lambda_G` penalty — consistent with fix-plans §C4.
- ch46 proxy `I(C^H_t;A_{t+k}\mid\cdot)` explicitly labeled as approximation when `\kappa_i` unavailable.

## Open / next
- ch46 § `\ref{sec:measuring-cci}` still lists operational audit quantities (not a second CCI definition); optional rename to avoid “Measuring CCI” confusion.
- ch11/ch12 use `C_{\mathrm{raw}}` without always cross-refing ch46 — acceptable where capacity growth is the topic.

## Key paths
- `chapters/ch26-correction-channel-integrity.tex` (`sec:correction-channel-integrity-def`, `eq:cci-ch46`, `eq:correction-bottleneck-capacity`)
- `metadata/notation.md`, `INSTRUCTIONS.md` §6.9

## Commits
- `a800909` Ground correction in handle control and consolidate CCI in ch46.
