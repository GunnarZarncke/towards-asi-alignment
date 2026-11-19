# 2026-11-02 — FutureSearch snapshots and hub forecast panels

kind: new-work
uptake: local

## Trigger
User ran FutureSearch on Markets 1 and 4, asked to archive the reports in drafts, then replace the predictions hub Metaculus placeholders for those markets with an improvised forecast panel (FutureSearch probabilities plus a compact listing-platform note). End-of-session commit.

## Done
- content: `drafts/predictions/futuresearch-market-01-2026-11-02.md` and `futuresearch-market-04-2026-11-02.md`; indexed in `drafts/predictions/README.md`.
- content: `metadata/predictions.yml` — `improvisedForecast` on markets 1 and 4 (FutureSearch URLs and YES/NO/OTHER percentages).
- content: `site/src/components/PredictionImprovisedForecast.astro`; `PredictionMarketPanel.astro` and `/predictions/` index pass improvised data when no Metaculus embed.
- housekeeping: session log, HANDOFF, INDEX.

## Decisions
- Third-party snapshots live in catalog YAML (sync regenerates gitignored `predictions.json` at build); not resolution input and not manuscript canon.

## Open / next
- When Markets 1 or 4 list on Metaculus, set `metaculusEmbedId` — embed takes precedence over improvised panel.
- Refresh `improvisedForecast` if FutureSearch re-runs on updated registry state.

## Key paths
- `metadata/predictions.yml` · `drafts/predictions/futuresearch-market-*.md` · `site/src/components/PredictionImprovisedForecast.astro`

## Verification
- `cd site && npm run sync:predictions` — exit 0, "wrote 20 cards and predictions.json".
- `cd site && npm run build` — exit 0, 1200 pages.

## Commits
- `4789b2e94b` Show FutureSearch snapshots on predictions hub for Markets 1 and 4.
