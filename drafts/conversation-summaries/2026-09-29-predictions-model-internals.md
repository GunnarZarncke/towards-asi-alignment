# 2026-09-29 — Predictions and model internals

kind: feedback
uptake: local

## Trigger
User: for the predictions, TSA excludes model internals, but alignment within the models is a real effort that influences the safety and research readiness the forecasts discuss.
Prompts: `4b3368f5-5ade-4bd4-83ad-848f918e856f`

## Done
- content: Draft Market 21, "Alignment inside the model," marked outside the book. Catch-all for the excluded internals cluster. Price is research readiness; certificate is the assurance interface for leaving \(U\).
- content: Aggregation, \(S_U=1\) floor, hub blurb, assurance manifest (`m21`, dependence with Markets 8/9/13), and assurance-demo note updated to match.
- bookkeeping: `npm run sync:assurance-model` — "Lean identifier check passed"; wrote `assurance-model.json` (22 nodes).

## Decisions
- The eighteen catalog rows still follow the book's exclusion. Market 21 is the wrapper, not a book object and not an MB* discharge.
- YES is a frozen internal-object / behavioral-counterpart / intervention package, not "the model is internally aligned."
- The price \(P(\mathrm{YES}_{21})\) does not enter the odds update. The certificate, after scope and transfer, is what can change \(\kappa\), and only inside its declared scope.
- Same Phase 4 listing gates as Markets 19–20. Resolve-by 31 December 2027.

## Open / next
- Phase 4 pilot/listing of Markets 19–20 remains gated on funding or an external evaluator.

## Key paths
- `appendices/appP-bridge-predictions.tex`
- `metadata/predictions.yml`
