# 2026-07-19 — Site bot orientation, search index, mobile search fix

## Trigger
Fix mobile search dropdown clipping; improve companion-site interpretability for bots by reusing repo-root orientation files; expose the search JSON index for programmatic lookup without promoting it in the human UI.

## Done
- **Mobile search:** `SiteSearch.astro` — full-width search row on mobile; dropdown `left: 0` so results do not extend past the viewport left edge.
- **Bot orientation:** extended repo-root `llms.txt` with Companion site URLs; `site/scripts/sync-bot-orientation.mjs` copies `llms.txt`, `REVIEWING_FOR_AGENTS.md` → `reviewing-for-agents.md`, and builds `llms-full.txt` at site sync/build.
- **Discovery:** `robots.txt` pointer to `/llms.txt`; `<link rel="alternate">` for `llms.txt` and `search-index.json`; JSON-LD `WebSite` in `SiteLayout`; sitemap custom pages for bot assets.
- **Search index:** `build-search-index.mjs` emits versioned JSON (`entries` + metadata); `/search-index/` docs page; header search reads wrapped or legacy flat format.
- **Human UI:** no footer link to search index (bots only via llms.txt / head alternate / direct URL).
- Pointers in `README.md`, `REVIEWING_FOR_AGENTS.md`, `site/README.md`.

## Decisions
- Repo-root `llms.txt` remains source of truth; site copies are generated (gitignored in `public/`).
- Search index docs page stays reachable but not linked from footer/nav.
- Wrapped JSON keeps backward-compatible parsing in `SiteSearch`.

## Open / next
- Deploy and verify live `/llms.txt`, `/search-index.json`, `/search-index/`.
- Optional: `noindex` on `/search-index/` if it appears in human-facing search results.

## Key paths
- `llms.txt`, `REVIEWING_FOR_AGENTS.md`
- `site/scripts/sync-bot-orientation.mjs`, `site/scripts/build-search-index.mjs`
- `site/src/components/SiteSearch.astro`, `site/src/pages/search-index/index.astro`
- `site/src/layouts/SiteLayout.astro`, `site/src/lib/seo.ts`

## Commits
- (this session)
