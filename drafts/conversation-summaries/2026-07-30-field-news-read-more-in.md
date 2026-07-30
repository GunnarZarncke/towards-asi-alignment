# 2026-07-30 — Field news “Read more in” rollout

## Trigger
User asked to finish the stalled task: replace terse “Read in book” / chapter-id lines with **Read more in** plus expanded chapter and appendix titles across all field-news entries, including the `/news/` index list.

## Done
- Added `site/scripts/lib/chapter-links.mjs` (titles from `book.json`, appendix map, markdown footer formatter, `chapterRefs` for the index).
- Updated `sync-field-news.mjs` to strip legacy footers from bodies, append auto-generated **Read more in** lines from `bookChapters`, emit `chapterRefs` in `field-news.json`, and keep dates as `YYYY-MM-DD`.
- Updated `/news/` index to render `Read more in: Ch. N, Title; … and Appendix X, Title.`
- Aligned `bookChapters` in `field-news.yml` for ET-2 (`appN`), pacing (`appC`), insurance (`appC`, `appM`).
- Removed hand-maintained footers from all 15 body files; regenerated all cards.

## Decisions
- Footers are generated at sync time from YAML `bookChapters` + `book.json` titles — bodies stay prose-only.
- ET-3 keeps its separate “not rewritten from this experiment” note above the auto footer.

## Open / next
- None requested.

## Key paths
- `site/scripts/lib/chapter-links.mjs`
- `site/scripts/sync-field-news.mjs`
- `site/src/pages/news/index.astro`
- `metadata/field-news.yml`, `metadata/field-news/bodies/`

## Commits
- None.
