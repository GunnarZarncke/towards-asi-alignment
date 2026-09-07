# 2026-09-07 — Claim ID renumber + ledger freshness

## What changed

- **Renumber:** `C-004a` → `C-012` (grounding); `C-044` → `C-013` (synthesis tracking). Updated ledgers, concepts, LaTeX tables, backtest artifacts/plans, `drafts/claim-spine.md`, site sync sources.
- **Claims ledger:** numbering scheme note; W-* backtest bullets on C-003–C-007, C-012, C-010; C-013 gap updated (App N shipped; adversarial M / M8 remains).
- **Uncertainty ledger:** `Treated in` dedupe; SharedInstrumentHypothesis note on U-03/U-05/U-14/U-16; Bears-on IDs updated.
- **Voice lane:** marked claims-ledger freshness + U-ledger reconciliation done in `drafts/plans/voice.md`.

## Verification

- `rg 'C-004a|C-044'` outside archive → only intentional “was …” notes in ledger headers.
- `cd site && npm run sync:experiments && npm run sync:concepts` — pass.

## Open

- WWCTV → chokepoint forward refs — moved to optional TODO in `metadata/TODO.md` (may drop).

## Closed this session

- Voice lane (`drafts/plans/voice.md`).
- Claim renumber C-012/C-013 + ledger freshness.
