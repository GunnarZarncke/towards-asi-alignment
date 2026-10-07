# 2026-10-07 — Appendix P after the split

kind: new-work
uptake: status

## Trigger
User: the registry site is https://aintelope.github.io/ai-safety-claims/ ; do “Appendix P after the split” from `eval-registry-split.md`.
Prompts: paraphrase only (no prompt id).

## Done
- content: `appendices/appP-bridge-predictions.tex`: how-to-read and how-a-market-can-resolve point at the claims registry; each market keeps property + box + registry pointer + closest work; Market 14 keeps YES requires; dropped YES lists, Common rules, and fine print.
- content: `INSTRUCTIONS.md` Appendix H scope: bars live in the registry; appendix keeps property and pointer.
- bookkeeping: `metadata/predictions.yml`: `registryRepo` / `registrySite`; dropped all `bars:`; `registryContractPublished` on Markets 1 and 4.
- bookkeeping: `site/scripts/sync-predictions.mjs`: no Common-rules copy assert; cards are property + registry link.
- bookkeeping: predictions hub listing note, Claims registry button, per-panel registry line (Market 14 excepted).
- bookkeeping: `eval-registry-split.md` status step 5 of 7.
- bookkeeping: `cd site && npm run sync:predictions` → `sync-predictions: wrote 20 cards and predictions.json`.
- bookkeeping: `make check` → 14 pass rows (`## Check — pass`).

## Decisions
- Markets without a published registry contract (other than 14) stay not listable; the appendix says that in the pointer.
- No `snapshotTag` until an independent host tags `snapshot-0`.
- Remaining contracts are not copied in this pass; Metaculus listing is not started.

## Open / next
- Independent host, then tag a snapshot, then list frozen contracts on Metaculus.
- Copy remaining contracts into `ai-safety-claims` when asked.

## Key paths
- `appendices/appP-bridge-predictions.tex`
- `drafts/plans/predictions/eval-registry-split.md`
- `https://aintelope.github.io/ai-safety-claims/`

## Commits
- none
