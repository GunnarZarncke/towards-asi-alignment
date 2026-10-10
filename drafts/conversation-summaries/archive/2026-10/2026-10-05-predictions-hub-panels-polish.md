# 2026-10-05 — Predictions hub panels polish

kind: new-work
uptake: status

## Trigger
Continue predictions hub work: merge external factors into related-forecast panels (Metaculus links), widen embed layout, fix card short/long title rendering, contextual panel notes, and render resolution `\textbf{YES requires}` / `Output` blocks on market cards.

Prompts: (paraphrase — continuation after commit `9f0dbfcc4`)

## Done
- content: Related forecasts hub section now includes external pause factor; all use `PredictionMarketPanel` with direct Metaculus links and embeds.
- content: Panel grid uses full page width, two columns from 960px; Metaculus `layout="panel"` with ~50% taller embed min-height for desktop charts.
- content: Related/external panel notes in `metadata/predictions.yml` add catalog context only (no restatement of embed titles).
- content: Market cards — title uses short title; lede shows long title; sync extracts `predictionbackground` and all `\textbf{…}` resolution blocks as `###` subheadings with paragraph breaks.
- housekeeping: Updated `sync-predictions.mjs` overview related-forecast list and YAML comment on panel notes.

## Decisions
- Cap hub panel grid at two columns so Metaculus iframes stay wide enough for chart UI (not mobile embed).
- Rename card section from “Performance bars” to “Resolution criteria” with per-block labels preserved from Appendix H (`YES requires`, `Output`, etc.).

## Open / next
- Populate `metaculusEmbedId` on catalog markets when questions go live.
- Phase 4 pilot/listing for Markets 19–21 unchanged.

## Key paths
- `site/src/pages/predictions/index.astro`
- `site/scripts/sync-predictions.mjs`
- `site/src/components/PredictionMarketPanel.astro`
- `site/src/components/MetaculusEmbed.astro`
- `metadata/predictions.yml`

## Verification
- `npm run sync:predictions` → `sync-predictions: wrote 20 cards and predictions.json`

## Commits
- `63bb15e20` Predictions hub: related Metaculus panels, card resolution blocks.
