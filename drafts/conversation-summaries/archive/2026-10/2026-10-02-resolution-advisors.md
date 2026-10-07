# 2026-10-02 — Resolution advisors off the public contracts

kind: correction
uptake: local

## Trigger
Proposed resolvers and the judge panel were for other platforms, and for later advice. Remove them from the manuscript and the site.
Prompts: paraphrase

## Done
- content: Appendix P no longer appoints a desk, a panel, or named judges. An unsettled load-bearing call is OTHER. Markets 3 and 17 score only cases with mechanical ground truth. Markets 19 and 20 no longer freeze a named resolver.
- content: `metadata/predictions.yml` dropped `resolvers` and `resolverStatus` (18 markets). Prediction-card sync no longer prints a resolver line.
- content: Funding card asks for an independent review memo. The host platform adjudicates.
- bookkeeping: Names, the desk protocol, and the five-judge panel live in `drafts/predictions/resolution-advisors.md`. Not linked from the manuscript or the site.
- bookkeeping: `npm run sync:predictions` wrote 20 cards and `predictions.json`. `npm run sync:chapters` wrote 56 book pages. Local `astro sync` content store has no "independent judges", "Dan MacKinlay", or "Resolver (proposed)".

## Decisions
- The published contracts do not name who resolves them. The host platform does.
- Without a panel, Markets 3 and 17 do not score cases that lack mechanical ground truth. Those cases do not count toward the sample size or the rates.
- Debate-judge and correction-channel uses of "judge" stay. They are not these resolvers.

## Open / next
- None of the proposed advisors are confirmed. Asking any of them is a separate step, and only for a venue that requires an external judge or for advice.

## Key paths
- `drafts/predictions/resolution-advisors.md`
- `appendices/appP-bridge-predictions.tex`
- `metadata/predictions.yml`

## Commits
- none
