# 2026-10-08 — External-services claims registry card

kind: new-work
uptake: local

## Trigger
User asked for a site card for ai-safety-claims.com as a related card from predictions (not replacing market registry links). Iterated away from sync-generated card and `predictions/` placement; settled on hand-authored `external-services/` card type.

## Done
- content: `site/src/content/cards/external-services/ai-safety-claims.md` — explanatory companion for the claims registry (resolution layer, outcomes, scope).
- content: New card type `external-service` / URL segment `external-services` (`badges.ts`, `card-urls.mjs`, `card-catalog.ts`, `visit-history.ts`).
- content: Related links on predictions overview sync, Appendix H chapter card source, evaluation funding card.
- bookkeeping: `sync-predictions.mjs` — overview `related:` plus inline **Claims registry** paragraph and companion-card external link.
- content: `site/src/pages/cards/[...slug].astro` — primary CTA button on `external-service` cards (hostname + secondary GitHub buttons).

## Decisions
- Hand-authored card outside gitignored `predictions/` (like funding cards); market cards keep direct `external:` links to ai-safety-claims.com.
- Card slug `ai-safety-claims` under `external-services/` rather than a prediction-type card.

## Open / next
- None for this card. Metaculus listing and independent host transfer remain on eval-registry-split lane.

## Key paths
- `site/src/content/cards/external-services/ai-safety-claims.md`
- `site/scripts/sync-predictions.mjs` (overview related line)

## Verification
- `cd site && npm run sync:predictions && npm run sync:chapter-cards` → exit 0; `sync-predictions: wrote 20 cards and predictions.json`.
- `cd site && npm run sync:predictions` (follow-up) → exit 0.

## Commits
- `565150402` Add external-services card for ai-safety-claims registry.
- `362c85f71` Polish claims registry card discovery on predictions overview.
