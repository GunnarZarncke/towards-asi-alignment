# 2026-07-25 — RSS feed and news posting dates

## Trigger
Add a combined RSS feed for news and releases, an RSS icon in the footer, and fix chronological ordering so news posting dates are not before the first release (v1.0.0, 2026-06-30).

## Done
- Added `site/scripts/build-feed.mjs` — merges release cards + field news into `public/feed.xml` (RSS 2.0); wired into `npm run sync` and `check:concepts`.
- Added `<link rel="alternate" type="application/rss+xml">` in `SiteLayout.astro` and footer **RSS** link with new `LinkIndicator` `rss` kind.
- Added `FEED_XML_URL` to `seo.ts`; included `/feed.xml` in sitemap `customPages`.
- Split field-news dates: `eventDate` (when the incident happened) vs `date` (site posting date). Six pre-release items backfilled to 2026-07-01 … 2026-07-06; July items unchanged.
- News index shows event date + “posted …” when they differ; list sorted by event date; RSS uses posting date interleaved with releases.
- `eventDate` added to card schema and sync pipeline.

## Decisions
- Posting dates for backfilled news: one day each from 2026-07-01 through 2026-07-06, preserving incident order and staying after v1.0.0 (2026-06-30) and before v1.1.0 (2026-07-08).
- Feed is build-time static asset (like `search-index.json`), not an Astro endpoint.

## Open / next
- None for this task.

## Key paths
- `site/scripts/build-feed.mjs`
- `site/src/layouts/SiteLayout.astro`
- `metadata/field-news.yml`
- `site/scripts/sync-field-news.mjs`

## Commits
- (none — user did not request commit)
