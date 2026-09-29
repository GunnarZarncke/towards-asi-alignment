# 2026-09-22 — Predictions funding gate

## Trigger

Continue the assurance-risk plan after an intervening editorial review pass. Preserve the reviewed Appendix P as the new baseline.

## Done

- Published a funding card for independent evaluation of the 2027 bridge contracts, with USD 50k / 120k / 250k bands, independence rules, milestones, null publication, and scoped success criteria.
- Added the frozen listing-status vocabulary and resolution reason codes to `metadata/predictions.yml`.
- Classified the 18 candidates as seven `draft` and eleven `funding-gated`; none is `ready-to-list`.
- Added generated-card frontmatter, validation, badges, hub labels, funding links, and explanatory copy that funding-gated does not mean technically false.
- Reconciled Markets 7 and 13 question strings with the reviewed Appendix P source.
- Regenerated prediction cards/data and card redirects.

## Decisions

- Generic card maturity is `framework`; prediction listing status is a separate field.
- Funding buys a credible resolution route, not a YES.
- The first proposed evaluation substrates are Markets 4, 8, and 15, with final selection frozen only after independent protocol review.
- External grant submission and evaluator commitments remain open, so no market advances to ready-to-list.

## Verification

- `npm --prefix site run build` passed.
- `make check` passed.
- Prediction sync emitted no question mismatch warnings.
- Browser check passed for `/predictions/` and `/cards/funding/prediction-evaluation-program/`.
- IDE lints reported no errors.

## Open / next

- Choose and submit to an external funding target; obtain funding or evaluator commitments before listing.
- Phase 3: freeze the assurance model unit and typed manifest; design Markets 19–20 and the user-parameter site demo. Do not list Markets 19–20 yet.

## Key paths

- `site/src/content/cards/funding/prediction-evaluation-program.md`
- `metadata/predictions.yml`
- `drafts/plans/predictions/assurance-risk-modelling.md`

## Commits

- none
