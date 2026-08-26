# 2026-08-26 — Site nav landings steps 1–2

## Trigger
Implement the first two steps of the nav-landing plan: fold/reorder the header, split `/` vs `/start/`, record visits, then homepage tiles + Continue reading and the Field six-panel hub.

## Done
- Header is 10 items: Start Here · Guided Tour · Book · Cards · Field · Experiments · Demos · Lean · News · About. Logo still goes to `/`. Folded URLs stay live.
- `/start/` is the slower on-ramp (stake, three ways in, shared FAQ). `/faq/` uses the same `FaqList`.
- Visit history: last 100 paths in `localStorage` (`VisitRecorder` + `visit-history.ts`). Homepage Continue reading shows the last other page and More-per-type.
- `/` is the public homepage: capability lede, Start here + gems links, value tiles.
- Field preview height capped (now 20.25rem after a too-tall `1fr` stretch, then +50%).
- Footer no longer says “companion site.” `llms.txt` nav pointers updated.

## Decisions
- Field panel clicks use a sibling cover `<a>` so preview HTML is not nested inside a link.
- Continue reading runs in the page body before the recorder at the end of `body`, so this visit to `/` is not treated as the continue target.

## Open / next
Remainder shipped in `2026-08-26-site-nav-landings-remainder.md`. Not committed.

## Key paths
- `site/src/layouts/SiteLayout.astro`
- `site/src/pages/index.astro`, `site/src/pages/start/index.astro`, `site/src/pages/field/index.astro`
- `site/src/lib/visit-history.ts`

## Commits
- `3e648a95` Fold the companion-site header and land Field and Home on simpler pages.
