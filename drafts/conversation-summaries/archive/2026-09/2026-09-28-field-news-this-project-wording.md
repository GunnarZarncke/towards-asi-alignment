# 2026-09-28 — Field news: “this project” wording

## Trigger
User asked to replace “this book” with “this project” in field-news posts and `metadata/field-news.yml`.

## Done
- Bulk replace in 11 canonical bodies and five YAML summaries (`This project’s cut`, legend swatch, quote attributions, prose).
- `npm run sync:field-news` — 30 cards regenerated.
- Separate commits: embedded-evaluators remember-one-thing card sync; UAD `open-problems.md` link path kept at repo root (`../../../../`).
- `make check` passed.

## Decisions
- Leave `bookChapters`, `book-figure` CSS, and YAML header comment unchanged.

## Open / next
- None.

## Key paths
- `metadata/field-news.yml`
- `metadata/field-news/bodies/*.md`
