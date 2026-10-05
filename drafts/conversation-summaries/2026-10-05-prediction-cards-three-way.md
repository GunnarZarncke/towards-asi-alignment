# 2026-10-05 — Prediction cards YES/NO/OTHER

kind: correction
uptake: status

## Trigger
The overview card still said a NO is everything else (missing evals, missing publication, missed requirements). That is outdated under three-way resolution.

Prompts: (paraphrase — this session)

## Done
- content: `metadata/predictions.yml` purpose now maps missed bars to NO and missing qualification to OTHER.
- content: Regenerated prediction cards and the App P chapter card; funding-card success criteria no longer treat missing reporting as NO.
- housekeeping: Card listing badge includes resolved-other; search index rebuilt.
- bookkeeping: Field/predictions plans that still said “binary contracts” or “refuse → NO” updated to three-way.

## Decisions
- Hub lede states the split in one paragraph so the catalog card matches Appendix P reading rules.

## Open / next
- Markets 19–21 remain outside the eighteen-card catalog (Market 20 stays YES/OTHER in the appendix).

## Key paths
- `metadata/predictions.yml`
- `site/scripts/sync-predictions.mjs`
- `site/src/content/cards/predictions/overview.md`
- `site/src/content/cards/chapters/appP.md`

## Commits
- none
