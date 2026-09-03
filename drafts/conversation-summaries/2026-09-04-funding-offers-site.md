# 2026-09-04 — Funding opportunities site offer

## Trigger
Implement the TSA funding-opportunity plan: nine public funding cards from existing application wording, `/funding/` overview with HTML dependency diagram, and entry points from About and funder-policy path.

## Done
- Added `funding` card type: `badges.ts`, `card-urls.mjs`, `content.config.ts` (fundingState, doneState, costs, dependsOn, roles).
- Card chrome: `FundingCardChrome.astro`, `FundingStateIcon.astro`; side panel roles/dependsOn on funding card pages.
- Nine cards under `site/src/content/cards/funding/` (UAD, TSA writing, Practical UAD, observability platform, corrigibility, multi-principal testbed, competitive labs, crux map, attractor hub).
- `/funding/` overview page with legend, CSS grid diagram, and card list.
- Catalog section “Funding opportunities” in `card-catalog.ts`.
- Links: About → `/funding/`; funder-policy path step + body link; **Guided Tour funder card** via `companionLink` on `/paths/`.
- Fixed `funding/index.astro` compile error (`const diagramNodes` typo).
- `npm run build` in `site/` succeeds.

## Decisions
- UAD card shows asked $60k, granted $10k, remaining ~$30k (work-weighted finish cost, not $50k accounting leftover).
- Attractor hub distinct from observability platform; no staffing/capacity edges on diagram.
- Raw applications in `funding/` and sibling repo stay unpublished; cards use roles only.

## Open / next
- User may want primary-nav link to `/funding/` (plan said no).
- Regenerate card redirects if bookmark migration needed: `cd site && npm run generate:card-redirects`.
- Commit when asked.
