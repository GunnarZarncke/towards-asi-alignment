# 2026-06-19 — Chapter demos scaffold (value bundle simulator)

## Trigger
User asked to turn a toy value-bundle HTML demo into a working mini app served by Python, then restructure for multiple chapter demos (one per chapter) with folder documentation only—experimental, not referenced in the book.

## Done
- Added `src/` experimental demo area: Python `serve.py`, landing `index.html`, shared `package.json` / `build-demos.mjs` / `tsconfig.json`.
- Moved value bundle simulator to `src/demos/ch16-value-bundle-simulator/` (TS, compiled JS, tests, page).
- Documented conventions in `src/README.md`, demo README, and `AGENTS.md` § Chapter demos.
- Verified server routes: `/` index and `/demos/ch16-value-bundle-simulator/`.

## Decisions
- **One folder per chapter** at `demos/chNN-short-slug/`; each must have `index.html`; main module is `app.ts` or sole non-test `.ts`.
- **Not in manuscript** — no `book.tex` / chapter `.tex` links; docs live under `src/` and `AGENTS.md` only.
- **Committed compiled `.js`** so `python3 serve.py` works without Node when JS is fresh; auto-rebuild via `npx esbuild` when TS is newer.

## Open / next
- Run `npm install` in `src/` before `npm test` or `npm run build` (esbuild not installed until then).
- Add new demos: create `demos/chNN-slug/`, link from `src/index.html`.
- Optional: vitest config if test discovery needs tuning as demo count grows.

## Key paths
- `src/README.md` — layout, run, add-demo instructions
- `src/serve.py` — dev server
- `src/demos/ch16-value-bundle-simulator/` — first demo

## Commits
- (pending this session end)
