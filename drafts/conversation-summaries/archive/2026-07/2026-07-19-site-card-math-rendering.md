# 2026-07-19 — Site card math rendering

## Trigger
Formulas on concept cards (e.g. `/cards/goodhart-as-selector/`, `/cards/certification-under-manipulation/`) showed raw `(M)`, `\mathrm{Corr}`, etc. instead of KaTeX output.

## Done
- Converted LaTeX-style delimiters `\(...\)` / `\[...\]` to remark-math `$...$` / `$$...$$` in three concept bodies:
  - `metadata/concepts/bodies/goodhart-as-selector.md`
  - `metadata/concepts/bodies/certification-under-manipulation.md`
  - `metadata/concepts/bodies/anti-capture-correction-validity.md`
- Added `normalizeMarkdownMath()` in `site/scripts/lib/concepts-yaml.mjs` so future `\(...\)` / `\[...\]` in body text is converted at sync time.
- Ran `npm run sync:concepts` and `npm run build` in `site/`; verified KaTeX HTML in `dist/cards/goodhart-as-selector/` and `dist/cards/certification-under-manipulation/`.

## Decisions
- Root cause: CommonMark strips `\(` and `\[` before remark-math runs; book sync already uses `$` delimiters. Fix at source + defensive normalizer in sync pipeline rather than a custom remark plugin.

## Open / next
- Deploy site (push to `main` or manual gh-pages build) for live fix.
- Optional: grep other metadata sources (bridges/projections bodies) if LaTeX delimiters are added there later.

## Key paths
- `metadata/concepts/bodies/*.md`
- `site/scripts/lib/concepts-yaml.mjs`
- `site/astro.config.mjs` (remark-math + rehype-katex)

## Commits
- `39015af` Fix concept card math rendering on the companion site.
