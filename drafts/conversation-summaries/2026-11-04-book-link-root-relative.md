# 2026-11-04 — Book sync links: root-relative URLs

kind: correction
uptake: local

## Trigger

Google Search Console 404s from depth-relative links in synced book markdown; user asked to investigate link generation, then implement root-relative URLs and `/full/` consolidation.

## Done

- **`site/scripts/lib/book-site-paths.mjs`:** `bookUnitSitePath` / `bookUnitSiteHref`; dedicated paths for appA/appE/appG → `/notation/`, `/glossary/`, `/lean/`.
- **`site/scripts/lib/tex-convert.mjs`:** Book, card, citation, and illustration hrefs emit root-relative `/cards/…` and `/illustrations/…`.
- **`site/scripts/lib/card-urls.mjs`:** `bookPublicHref` uses `bookUnitSitePath` (fixes reference-card “Cited in appG”).
- **`site/src/lib/site-urls.ts`:** `bookFullHref` → hub except `appM`; `BOOK_CHAPTER_PDF_HREF` root-relative.
- **`site/src/pages/cards/[...slug].astro`:** Non–overview-hub `/full/` routes 301 to chapter card URL.
- **`site/astro.config.mjs`:** Sitemap excludes `/book/ch*`, `/book/app*`, and duplicate `/full/` (keeps `appM/full`).
- Regenerated **`site/src/content/book/`** and **`site/src/content/cards/chapters/appM.md`** via `sync:chapters` + `sync:chapter-cards`.
- **`npm run build`** in `site/` succeeded (1205 pages).

## Verification

- `dist/cards/chapter/ch48/full/index.html` → redirect stub to `/cards/chapter/ch48/`.
- Hub ch48 HTML cites `/cards/reference/casper2023rlhflimits/`, `/cards/chapter/ch38/#…`.

## Open / next

- Deploy site; GSC recrawl should drop malformed `/cards/chapter/chapter/…` URLs.
- Optional: safety-net redirects for legacy malformed paths (not added).

## Commits

- (this session)
