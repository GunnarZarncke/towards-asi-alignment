# 2026-08-07 — Lean Astro Unicode escape CI diagnosis

## Trigger
Site CI failed on Astro build: `Invalid Unicode escape sequence` at `site/src/pages/lean/index.astro:53:103`.

## Done
- Reproduced failure by checking out pre-fix `index.astro` (inline LaTeX in HTML bullets).
- Confirmed current `main` already fixes via `String.raw` frontmatter strings (`150f406b`).
- Verified `npm ci && CI=true npm run build` succeeds locally (865 pages).
- No code changes required this session.

## Decisions
- Root cause: inline LaTeX like `$C_{\mathrm{raw}}$` in Astro HTML compiles to JS template literals where `\r`, `\v`, `\t` in `\mathrm`, `\vec`, etc. are parsed as escapes.
- Fix pattern: keep LaTeX in frontmatter `String.raw` template literals (comment on line 20 documents why).

## Open / next
- If CI still red on a feature branch, rebase/merge `main` (includes `150f406b`).
- Avoid inline `$\\...$` LaTeX in `.astro` HTML; use `String.raw`, doubled backslashes, or a KaTeX component.

## Key paths
- `site/src/pages/lean/index.astro` (dependency spines block, lines 20–37)
- `.github/workflows/site.yml`

## Commits
- `0aa59e0b` Log Lean Astro Unicode escape CI diagnosis session.
