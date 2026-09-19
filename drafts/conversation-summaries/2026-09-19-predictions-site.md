# 2026-09-19 — Predictions site hub

## Trigger
User asked to continue with the site phase after Appendix H shipped.

## Done
- `metadata/predictions.yml` — P1 catalog (18 markets + bridge tags).
- `site/scripts/sync-predictions.mjs` — extracts `predictionbox` + prior-test text from `appP`; writes `predictions.json` and 19 cards under `src/content/cards/predictions/`.
- `/predictions/` hub (`site/src/pages/predictions/index.astro`); nav item; Gauss bell icon; coming-soon offsite graph placeholder.
- `prediction` card type plumbing: `badges.ts`, `content.config.ts`, `card-urls.mjs`, `visit-history.ts`, `card-catalog.ts`, search index, card chrome.
- `appP` chapter card `related` includes `predictions/overview`.
- `prediction-interface.md` site phase marked done.

## Verification
- `npm run sync:predictions` — 19 cards.
- `npm run build` (site) — `/predictions/index.html` + prediction card routes.
- `make check` — pass.

## Open / next
1. Spine `Evidence.lean` adapters.
2. Q1/Q2/Q6 listing (platform, desk, claim-strength on host).
3. Embed live prices when a platform is chosen.

## Commits
- (pending)
