# 2026-09-04 — Funding opportunities site offer

## Trigger
Implement the TSA funding-opportunity plan: nine public funding cards from existing application wording, `/funding/` overview with dependency diagram, and entry points from About and funder-policy path.

## Done
- Added `funding` card type: `badges.ts`, `card-urls.mjs`, `content.config.ts` (fundingState, doneState, costs, fte, dependsOn, roles).
- Card chrome: `FundingCardChrome.astro`, `FundingStateIcon.astro`; team size + roles in meta; dependsOn in side panel.
- Nine cards under `site/src/content/cards/funding/` with rounded asks (2 sig fig), FTE headcounts, roles.
- `/funding/` overview: Cytoscape+dagre interactive dependency graph (`FundingDependencyGraph.astro`); compact inline legend under graph; CTA hero (what funds buy + Calendly + funder path).
- Amount rounding via `roundFundingAmount` / `formatFte` in `funding-state.ts`.
- Fixed funded/done icon fill (explicit `--funding-icon-fill`, not `currentColor` + white text).
- TSA card: site homepage summary, $10k microgrant ask.
- Crux map: `dependsOn` TSA.
- Catalog section “Funding opportunities”; About + funder-policy + Guided Tour `companionLink`.
- `npm run build` in `site/` succeeds.

## Decisions
- UAD: asked $60k, granted $10k, remaining ~$30k.
- Graph shows name + status icons only (no headcount on diagram blocks).
- Team size + roles on card chrome and `/funding/` list entries only.
- Attractor hub distinct from observability platform; no staffing edges on diagram.
- Raw applications in `funding/` stay unpublished.

## Open / next
- Primary-nav link to `/funding/` (optional).
- Unrelated working tree: alignment-crux-map drafts, conversation-summary archive moves, `experiments.json` sync.
