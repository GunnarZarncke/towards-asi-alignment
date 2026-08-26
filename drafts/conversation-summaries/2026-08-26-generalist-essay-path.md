# 2026-08-26 — Generalist essay path

## Trigger
User asked for a Paul Graham-style general-audience start: catch, essay spine, optional tangents; then implement including writing the essays. Nav must not change. Essays most prominent on Start Here, also linked from homepage and Guided Tour. Park Guided Tour “read next” from last book page.

## Done
- New `essay` card type and `/essay/[slug]/` layout (asides, branch chips, Next/Back, precise-version footer). `/cards/{slug}/` 301s to `/essay/` for essay types.
- Wrote 7 spine/closer essays and 4 branch essays. *Align* / *alignment* first appears in the closer (*A map, not a certificate*).
- `/essay/` 301s to the first essay (no hub hop). **Start Here** prints the opening paragraphs plus **Continue reading**.
- Homepage, Guided Tour, generalist path, FAQ, search index script, README, `llms.txt`, About; visit-history `essay` type. Main nav unchanged.
- Parked on Site board: Guided Tour continue from last book page.
- Late pass: unpacked the helper-email paragraph in *The copy did not inherit the listening*.

## Decisions
- Essays are hand-authored cards (`type: essay`), not a second collection and not generated from `concepts.yml`.
- Homepage stays a mode picker; essays are a door, not a nav item.
- Chapter-card related lists skip essay `bookChapters` so sync does not churn chapter cards.

## Open / next
- Guided Tour “read next” from last visited book page (TODO Site board). Do not build yet.
- Essay prose can be revised for voice; first pass is site paratext, not PDF canon.

## Key paths
- `site/src/content/cards/the-chatbot-passed-the-test.md` (and sibling essay cards)
- `site/src/pages/essay/`
- `site/src/pages/start/index.astro`

## Commits
- `ca5c9026` — Add general-audience essay spine with Start Here teaser.
