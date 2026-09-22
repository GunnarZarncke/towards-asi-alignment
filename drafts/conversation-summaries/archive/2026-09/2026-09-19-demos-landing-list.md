# 2026-09-19 — Demos landing list

## Trigger
User asked to replace the minimal `/demos/` landing (two buttons) with a list page in general language and a call to action. Follow-up: drop the separate full inventory; link to the badge index instead.

## Done
- **`site/src/pages/demos/index.astro`** — Hero lede + CTAs (Try a demo, Badge index, Source on GitHub) and a 7-item demo list with plain-language blurbs and anchor ids.
- **Removed `site/src/pages/demos/all/index.astro`** — Detailed inventory page retired.
- **`site/astro.config.mjs`** — Redirect `/demos/all/` → `/demos/`.
- **`site/src/pages/cards/[...slug].astro`** — Demo sidebar links point to `/demos/#id` (“All demos”).
- Site build verified (`npm run build` in `site/`).

## Decisions
- Single demos surface at `/demos/`; no second inventory page.
- Secondary nav goes to `/badges/` (badge index), not a demos-specific index.
- Blurbs live inline on the landing page (not synced from README excerpts).

## Open / next
- **`metadata/predictions.yml`** has unstaged copy edits (market titles/questions) — not part of this commit; user may commit separately.
- **`site/src/data/chapter-reading-graph.json`** timestamp-only change from an unrelated sync — left unstaged.
- Re-run `cd site && npm run sync:predictions` if predictions.yml edits should flow to site cards.

## Key paths
- `site/src/pages/demos/index.astro`
- `site/astro.config.mjs`
- `site/src/pages/cards/[...slug].astro`

## Commits
- `0cd23936` Consolidate demos into a single landing list page.
