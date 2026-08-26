# 2026-08-26 — Site nav landings remainder

## Trigger
Finish the remaining nav landing splits after header/home/Field (Cards, Book, News, Tour, Lean, Experiments, Demos, folded-URL crumbs).

## Done
- `/cards/` leads with Highlights (top 3, rest folded) plus compact topic groups (glossary early, references last); full inventory at `/cards/browse/`.
- `/book/` is PDF + compact linked part list (first viewport was empty because of stacked hero padding); chapter tables at `/book/map/`.
- `/news/` has two one-row unfolds (field news + releases); `/updates/` kept with crumb.
- `/paths/` is chapter-graph CTA + six path cards (FAQ hero and graph essay removed).
- `/lean/`, `/experiments/`, `/demos/` are short landings; dense bodies at `/lean/spine/`, `/experiments/coverage/`, `/demos/all/`.
- Parent crumb “You are in …” on folded and child routes. About unchanged.
- `llms.txt` pointers updated. Astro build 200 on the new routes.

## Decisions
- Featured demo is the value-bundle simulator (plan). In-repo experiment lines only on the Experiments landing (siblings stay on coverage).
- Shared `card-catalog.ts` so browse matches landing groups. No `NavLanding` wrapper (pages already share the skeleton).
- End-of-session commit covers nav landings only. Unstaged leftovers: chapter-reading-graph sync; in-progress essay type (`/essay/`, essay cards, homepage/Start Here tiles).

## Open / next
None for this landing pass. Ask before committing graph sync or the essay entry layer.

## Key paths
- `site/src/pages/cards/index.astro`, `site/src/pages/book/index.astro`, `site/src/pages/news/index.astro`
- `site/src/pages/lean/index.astro`, `site/src/pages/experiments/index.astro`, `site/src/pages/demos/index.astro`
- `site/src/components/ParentCrumb.astro`, `site/src/lib/card-catalog.ts`

## Commits
- `a19e90c8` Slim remaining site landings so first visits show an offer, not a catalog.
