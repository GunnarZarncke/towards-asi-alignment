# 2026-10-05 — Market short/long titles and panels

kind: new-work
uptake: status

## Trigger
Metaculus wants a short title and a long title. Hub markets should be panels that later show the Metaculus forecast, using the short title.

Prompts: (paraphrase — this session)

## Done
- content: Catalog markets in `metadata/predictions.yml` now have `shortTitle` (question, Metaculus short) and `longTitle` (listing question).
- content: `/predictions/` renders each catalog market as a panel with the short title and a forecast slot (embed when `metaculusEmbedId` is set).
- content: Prediction cards label both titles; embed uses the same iframe as external-factor cards.
- verification: `npm run sync:predictions` (run in this session).

## Decisions
- Short titles are the existing catalog nouns with a question mark, matching the Metaculus form.
- Forecast iframe stays empty until a question id is listed.

## Open / next
- Fill `metaculusEmbedId` when questions are posted.

## Key paths
- `metadata/predictions.yml`
- `site/src/components/PredictionMarketPanel.astro`
- `site/src/pages/predictions/index.astro`

## Commits
- none
