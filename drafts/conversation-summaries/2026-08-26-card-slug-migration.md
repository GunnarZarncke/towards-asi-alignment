# 2026-08-26 — Card slug migration

## Trigger
User asked for slug migration so card type appears in URLs (fix continue-reading grouping and make paths legible).

## Done
- **`site/scripts/lib/card-urls.mjs`** — canonical `/cards/{type}/{local}/` builder; essays stay on `/essay/`.
- **`cardHref` / `getStaticPaths`** — typed routes; content ids unchanged (`chapters/ch07`, flat slugs).
- **`generate-card-redirects.mjs`** → **`card-redirects.json`** (684 rules) wired in **`astro.config.mjs`**.
- Sync scripts + search/feed index emit new URLs; tex-convert relative links updated; card index stores `{slug, type}`.
- **Continue reading** — `latestByKind` groups by card type (Chapter, Concept, Bridge, …); skips nav landings.
- **Path read-next** — shared `read-next-core` + `PathReadNext.astro`; chapter URLs use `/cards/chapter/…`.
- **`/book/`** — appendix rows without letter initials (same session tail).
- Field-agenda + field-news card bodies partially regenerated with typed links; remaining old `/cards/chapters/` in bodies still redirect.

## Decisions
- Physical card file paths unchanged; URL layer only.
- `frontmatter` is a single segment: `/cards/frontmatter/`.
- Legacy flat URLs redirect; no dual canonical paths.

## Open / next
- Re-run full sync when convenient so all field-news bodies pick up typed chapter links in source (redirects cover gaps).
- Optional: bump `VISIT_HISTORY_KEY` if old localStorage rows feel noisy (not required — kind derived from path when typed).

## Key paths
- `site/scripts/lib/card-urls.mjs`, `site/src/lib/site-urls.ts`, `site/src/data/card-redirects.json`
- `site/src/lib/visit-history.ts`, `site/src/components/ContinueReading.astro`

## Commits
- (pending)
