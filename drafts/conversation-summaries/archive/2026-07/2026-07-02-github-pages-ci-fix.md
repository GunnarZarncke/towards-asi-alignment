# 2026-07-02 — GitHub Pages CI fix

## Trigger
Site workflow failed on first push; user enabled GitHub Actions Pages and asked for end-of-session commit.

## Done
- **CI build fix:** install `src/` demo deps (`esbuild` for `build-demos.mjs`) before `site` build.
- **Node:** workflow uses Node 24 (GitHub runner alignment; Astro needs `>=22.12.0`).
- **`site/package.json`:** added `engines.node`.
- **`src/package-lock.json`:** added for reproducible demo builds in CI.

## Open / next
- Push commit and confirm **Actions → Site** shows green **Build site** + **Deploy to GitHub Pages**.
- Live URL: `https://towards-alignment.com/`
- Unrelated dirty tree: embedded-sim results, ch09 demo HTML, older untracked conversation logs.

## Commits
- `66f7019` — Fix GitHub Pages site build: install demo deps and use Node 24.
