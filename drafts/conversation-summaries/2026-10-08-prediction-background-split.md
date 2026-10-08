# 2026-10-08 — Prediction background field split

kind: new-work
uptake: status

## Trigger
Apply the book/Metaculus background split and trimmed listing titles to bridge prediction markets 1–18 except 14.

## Done
- content: Appendix P — `predictionbackground` blocks and Metaculus short titles on `predictionbox` for markets 1–13 and 15–18; market 14 unchanged.
- content: `metadata/predictions.yml` — `metaculusShortTitle` and trimmed `longTitle` (no YES/NO/OTHER gloss) for markets 1–13 and 15–18.
- content: Fixed plain-language card links for markets 7, 11, 16 (`the-environment-picks-the-winner`, `intervention-supported-unit-discovery`).
- housekeeping: `site/scripts/sync-predictions.mjs` already converts `predictionbackground` via card fragment converter.
- gate: `npm run sync:predictions` → `sync-predictions: wrote 20 cards and predictions.json`; `./build.sh` → `Built dist/pdf/towards-superintelligence-alignment.pdf`.

## Decisions
- Markets 7 and 16 link to essay card `the-environment-picks-the-winner` (no `alignment-regime` card).
- Market 11 links to concept card `intervention-supported-unit-discovery` (coordination detection fit).

## Open / next
- Update `ai-safety-claims/listing-template.md` with the three-title split and Market 1 example.
- Refresh `drafts/predictions/metaculus-all-markets.md` if listing on Metaculus.
- Delete or attic one-off `scripts/patch_prediction_backgrounds.py`.

## Key paths
- `appendices/appP-bridge-predictions.tex`
- `metadata/predictions.yml`
- `site/scripts/sync-predictions.mjs`

## Commits
- (none — user did not request commit)
