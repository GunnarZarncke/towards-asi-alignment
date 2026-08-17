# Site card notes Phase 5 — sync/math (B1, B4, B5, A12)

**Date:** 2026-08-17  
**Scope:** `site/scripts/lib/tex-convert.mjs`, `site/src/styles/global.css`, regenerated `site/src/content/book/`.

## Done

- **B1/B5:** `\symboldef` / `\symbolref` inline handlers + `preprocessMathMacros` inside display math blocks.
- **B4:** `align` / `gather` / `multline` envs emit `\begin{env}...\end{env}` inside `$$` so KaTeX renders multi-line blocks (ch10 three goal layers).
- **Labels in math:** `\label{...}` stripped from KaTeX input; emitted as `<span id="...">` anchors outside math.
- **A12:** Horizontal scroll on `.katex-display` inside `.content-card` and `.readable`.
- **Sync:** `npm run sync:chapters` — no raw `symboldef`/`symbolref` left in book markdown.

## Next

Phase 6 mobile (A7–A11): figure caching, panel icons, highlight tap, expand drawer.
