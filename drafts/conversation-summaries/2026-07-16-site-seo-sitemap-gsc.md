# 2026-07-16 — Site SEO, sitemap, Search Console prep

## Trigger
Install `@astrojs/sitemap`, configure SEO (canonical, social, robots, unique descriptions), add OG preview image, and replace companion-site links from `gunnarzarncke.github.io/towards-asi-alignment` with `towards-alignment.com`. User added site to Google Search Console; advised deploy then submit `sitemap-index.xml`.

## Done
- `@astrojs/sitemap` in `site/astro.config.mjs` (+ PDF in `customPages`).
- `site/src/lib/seo.ts`: `HOME_DESCRIPTION`, `OG_IMAGE_*`, `truncateDescription`, canonical helpers.
- `site/src/layouts/SiteLayout.astro`: canonical, OG/Twitter (incl. `summary_large_image`), per-page descriptions.
- `site/public/robots.txt`, `site/public/og-image.png`.
- Homepage `HOME_DESCRIPTION`; card `/full/` and lean-node unique descriptions.
- Repo links updated: `README.md`, `CONTRIBUTING.md`, `docs/MANUSCRIPT.md`, `frontmatter/current-status.tex`, `metadata/TODO.md`.
- Left `site/README.md` curl examples on old github.io URLs (redirect verification).

## Decisions
- Default OG image for all pages; cards use `ogType="article"`.
- `site/public/CNAME` not added (peaceiris `cname` remains authoritative).

## Open / next
- Push/deploy; verify live `robots.txt`, `sitemap-index.xml`, `og-image.png` (404 on domain before deploy).
- GSC: submit sitemap, request indexing on homepage + key cards, enable Enforce HTTPS.
- Optional: compress `og-image.png` (~1.3 MB).

## Key paths
- `site/astro.config.mjs`, `site/src/lib/seo.ts`, `site/public/robots.txt`

## Commits
- (pending) site SEO and domain link migration
