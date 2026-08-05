# 2026-08-05 — Iliad / Textbook from the Future field agenda

## Trigger
User asked which agenda and team owns [textbookfromthefuture.org/faq.html](https://textbookfromthefuture.org/faq.html), then requested adding it to the field-agendas reference: new off-matrix agenda, TSA contrast, field hub bullet, Resolution cross-link only — no manuscript changes.

## Done
- Added `reference/field-agendas/data/agendas/iliad-textbook-from-the-future.yml` (field-building / theory-synthesis megaproject; empty `bookBridges`).
- Registered in `roster.yml` (order 35, `inMatrix: false`) and `clustering.yml` (Iliad, Textbook from the Future, ILIAD Conference).
- Extended TSA `bookSeparates` with breadth-first communal TOC vs depth-first typed bridges contrast.
- Extended Resolution `contributes` with Iliad/TftF + Timaeus lineage overlap link.
- Field hub bullet in `site/src/content/field/intro.md`.
- Bumped agenda count in `meta.yml` (31 records).
- Ran `npm run sync:field-agendas` (new card + index + JSON).

## Decisions
- Classify as off-matrix field-building / synthesis megaproject (like CAIS/Kairos), not a bridge-discharge agenda.
- Cross-link only Resolution among sibling agendas (Timaeus/Iliad founder overlap); no App B or other manuscript prose.
- Deferred App B “coordination instruments vs typed bridges” paragraph.

## Open / next
- Optional App B one-paragraph mention of synthesis/coordination artifacts vs bridge typing (`metadata/TODO.md` if tracked).
- Iliad projects page lists many chapter leads as TBD — revisit when names stabilize.

## Key paths
- `reference/field-agendas/data/agendas/iliad-textbook-from-the-future.yml`
- `site/src/content/cards/field-agendas/iliad-textbook-from-the-future.md`
- `site/src/content/field/intro.md`

## Commits
- (this session)
