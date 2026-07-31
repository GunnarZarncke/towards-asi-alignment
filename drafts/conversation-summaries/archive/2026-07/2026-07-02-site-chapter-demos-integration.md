# 2026-07-02 — Site: chapter demos integrated with Astro

## Trigger
User asked to adapt chapter demos so they work both standalone (`./serve-demos.sh`) and within `./serve-site.sh` without requiring a separate server.

## Done
- `site/scripts/lib/publish-chapter-demos.mjs` — builds TS demos, copies static assets to `site/public/chapter-demos/{id}/`, writes fallback HTML for Python backend demos.
- `site/scripts/sync-demos.mjs` — calls publish on sync; adds `sitePath`, `standaloneUrl`, `requiresBackend` to `demos.json`.
- `site/src/middleware.ts` — dev: serves `index.html` for `/chapter-demos/{id}/`; proxies ch09 to uvicorn with fallback when backend unavailable.
- `scripts/demo-backends.sh` — starts ch09 uvicorn; warns if uvicorn missing.
- `serve-site.sh` — starts/stops demo backends; prints integrated demo URLs.
- Site pages (`/demos/`, book/card sidebars) link to `withBase(sitePath)` instead of localhost.
- `site/.gitignore` — `public/chapter-demos/` (generated).
- ch09 standalone landing page updated with dual-mode instructions.

## Decisions
- Static demos (ch16, ch17) are copied into `public/chapter-demos/` at sync time — works on static GitHub Pages build.
- ch09 uses Astro middleware proxy in dev (not Vite proxy) so fallback HTML is served when backend is down.
- Standalone flow unchanged: `src/serve.py` still builds TS and starts Python backends on their ports.

## Open / next
- Install uvicorn locally for full ch09 interactivity via `./serve-site.sh`: `pip install -r src/demos/ch09-uad-coalition-board/requirements.txt`.
- ch09 on GitHub Pages remains fallback-only (no hosted backend).

## Key paths
- `site/scripts/lib/publish-chapter-demos.mjs`
- `site/scripts/sync-demos.mjs`
- `site/src/middleware.ts`
- `scripts/demo-backends.sh`
- `serve-site.sh`, `serve-demos.sh`

## Commits
- (none — user did not request commit)
