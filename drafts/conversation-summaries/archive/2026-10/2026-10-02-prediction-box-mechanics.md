# 2026-10-02 — Prediction box mechanics and plain terms

kind: correction
uptake: local

## Trigger
Finish the missing scoring mechanics, put Market 13's conditions inside its own box, make Markets 19 and 20 bracket templates, and replace private terms in the question boxes.
Prompts: paraphrase

## Done
- content: Appendix P boxes now name the statistics. A 95% upper bound on a rate is the Clopper-Pearson one-sided bound after shared trials collapse to one unit. A lower 95% AUROC bound is DeLong's one-sided bound. Markets 1, 2, 5, 6, 7, 12, and 14 freeze the list, the statistic, or the dated record before scoring.
- content: Market 13 states the seven checks in the box and does not cite Market 6. Markets 19 and 20 are templates; a question that still contains a bracket is not the listed contract. The freeze order sits in the prose around those boxes.
- content: Box titles and leads for Markets 16 and 17, and the catalog question column, use the plain names. Bridge card slugs are unchanged.
- content: `metadata/predictions.yml` leads and bars match the new box wording. All 18 `marketQuestion` strings match the appendix lead sentences.
- bookkeeping: `npm run sync:predictions` wrote 20 cards and `predictions.json` with no lead-mismatch warning. `npm run sync:chapters` wrote 56 book pages. Local `astro sync` reported "Synced content".

## Decisions
- Effect sizes that were missing are frozen per evaluation, not invented as a target result. Rates already in the catalog stay: 90/80 correction, and a 20-percentage-point drop or gap.
- Market 2's pair class is new: same choice on at least 90% of at least 20 frozen ordinary tasks. Distinguishing uses at least 50 pairs, direction at least 100 novel conflicts, intervention at least 50 interventions.
- A false-safe result, defined once in the common box, is a failing case labeled as passing.
- Date format ("December 31, 2027" plus a timezone) and title-versus-criteria overclaim were left as they are.

## Open / next
- Markets 19–21 are still unlisted until the Phase 4 gates. Filling the brackets is part of posting, not of this appendix.
- None of the proposed advisors are confirmed.

## Key paths
- `appendices/appP-bridge-predictions.tex`
- `metadata/predictions.yml`

## Commits
- none
