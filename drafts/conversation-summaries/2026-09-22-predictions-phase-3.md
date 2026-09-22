# 2026-09-22 — Predictions Phase 3

## Trigger

Continue the assurance-risk plan with Phase 3 after the editorial review pass and Phase 2b funding gate.

## Done

- Added `metadata/assurance-model.yml` with shared nodes, relation types, dependence warnings, and Phase 3 market metadata.
- Added `site/scripts/sync-assurance-model.mjs` with Lean identifier drift check against `Evidence.lean`.
- Draft Markets 19 and 20 in Appendix P (cross-cutting section): integrated transfer tournament and open-world coverage challenge.
- Extended assurance section with unit of analysis, Market 19/20 mapping notes, one-attempt consequence parameters, and site demo pointer.
- Shipped `/predictions/assurance/` sensitivity demo with assurance update, consequence step, and illustrative per-attempt tree.
- Linked demo from predictions hub; wired sync into site `npm run sync`.
- Added unit tests for assurance demo math.

## Decisions

- Markets 19–20 stay draft in the appendix and manifest; catalog sync remains at 18 markets until Phase 4 approval.
- Market prices and YES/NO outcomes never populate demo parameters; preset slots stay empty until qualifying artifacts exist.
- κ remains a sensitivity input; Market 20 informs ranges only.

## Verification

- `npm --prefix site run sync:assurance-model` passed.
- `make check` passed (including assurance demo tests).
- `npm --prefix site run build` passed; `/predictions/assurance/index.html` generated.

## Open / next

- Phase 4: pilot Markets 19–20, secure evaluators/funding, approve catalog expansion to `market-19` / `market-20`.
- External funding submission for prediction-evaluation program.
- Add versioned presets when qualifying tournament/challenge artifacts resolve.

## Key paths

- `metadata/assurance-model.yml`
- `appendices/appP-bridge-predictions.tex` (Markets 19–20, extended assurance)
- `site/src/pages/predictions/assurance/index.astro`

## Commits

- none
