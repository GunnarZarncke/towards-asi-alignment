# 2026-10-02 — Predictions three-way and loopholes

kind: correction
uptake: rule

## Trigger
User asked to apply four market comments: three-way YES/NO/OTHER; self-contained Markets 4 and 6; close Market 8/13 loopholes (Market 15 as the pattern); site leftover chapter-reference TeX.

## Done
- content: Appendix P common rule and resolution stack now three-way. Qualifying attempt vs performance bars. Unresolved residual calls resolve OTHER, not NO.
- content: Markets 4 and 6 boxes no longer depend on chapter `\ref` for scoring; seven properties have operational tests in the box.
- content: Market 8 requires per-family coverage, complete-interface negative controls, and an 80% true-complete floor. Market 13 requires an 80% true-pass floor and the successor-gaming family.
- content: Prediction sync strips `\ref`, fails leftover TeX, restores "Closest existing work" on cards, and no longer warns on extra draft appendix markets.
- content: Listing questions are three-outcome: "which outcome will hold ... YES, NO, or OTHER?" Copy as multiple choice; do not list a binary "Will there be" plus annulment.
- bookkeeping: YAML listing status `resolved-other`; contractVersion 2 on markets 4, 6, 8, 13. Plans and TODO updated.

## Decisions
- OTHER is no qualifying attempt, not a platform refund.
- \(P(\mathrm{YES})/(P(\mathrm{YES})+P(\mathrm{NO}))\) is the attempt-success ratio; it is not a deployment probability.
- Desk disagreement and unresolved judgment are OTHER.

## Open / next
- Phase 4 listing still gated.

## Key paths
- `appendices/appP-bridge-predictions.tex`
- `metadata/predictions.yml`
- `site/scripts/sync-predictions.mjs`

## Commits
- none
