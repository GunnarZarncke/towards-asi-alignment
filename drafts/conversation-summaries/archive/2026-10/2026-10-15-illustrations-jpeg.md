# 2026-10-15 — Chapter illustrations: PNG → JPEG masters

kind: correction
uptake: local

## Trigger

User asked to convert bloated chapter-opening illustration PNGs to a suitable format and update LaTeX `\includegraphics` paths.

Prompts: (paraphrase-only)

## Done

- content: Converted 16 `figures/illustrations/ch*.png` to JPEG (Q90, same dimensions); removed PNGs (~48 MiB → ~7.5 MiB masters).
- Regenerated `figures/illustrations/web/*.jpg` and synced to `site/public/figures/illustrations/web/`.
- Updated `chapters/ch01–ch16` `.tex` includes, `site/src/content/illustrations/*.md`, `drafts/illustrations/prompts/*.md`, `scripts/generate_web_illustrations.py`, `site/scripts/lib/tex-convert.mjs`, `site/src/pages/illustrations/[id].astro`.
- `make check`: pass (including site lib tests).

## Decisions

- Book and site canonical masters are JPEG at full pixel size; web copies remain downscaled Q82 via existing script (still accepts `.png` in `webIllustrationPath` for legacy paths).

## Commits

- `acb69ba71` Convert chapter-opening illustrations from PNG to JPEG masters.
