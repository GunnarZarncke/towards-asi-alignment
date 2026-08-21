# 2026-08-18 — Field v2 split + stance SVG icons

## Trigger
Split `/field/v2/` into a slim hub with coverage on a subpage; fix fragile Unicode stance marks by replacing them with seven generated monochrome SVG icons (stacked +/−, ± unclear).

## Done
- **Hub split:** `/field/v2/` intro + nav only; matrix + evidence catalog on `/field/coverage/`.
- **Components:** `FieldLifecycleAxis`, `FieldSpecifyConstructTable`, `FieldAdjacentWork`, `FieldBridgeGraphSection`, `FieldHubNav`, `StanceMark`.
- **Concept cards:** `alignment-lifecycle`, `field-coverage`, `bearer-admission-adjacent`; embeds on `bridge-assumptions`, `alignment-target`.
- **Stance icons:** `reference/field-agendas/scripts/stance-icons.mjs` → `site/public/icons/stance/*.svg`; `sync:stance-icons` in site sync chain.
- **Removed:** Unicode combining-mark logic, CSS glyph stacking, colored support/challenge matrix styling.
- **Plain-text marks:** `+`/`−`/`±` in `meta.yml`, generated index, validators, tests.
- **Middleware:** trailing-slash redirect for field routes.

## Decisions
- Icons use `currentColor` stroke (monochrome); no green/red stance coloring on matrix cells.
- Markdown/sync layer uses ASCII marks, not icon filenames, for agent-readable index.

## Open / next
- Deploy to fix production 404s on new routes.
- `frontmatter/introduction.tex` has an unstaged Part I blurb removal (not in this commit).

## Key paths
- `site/src/pages/field/coverage/`, `site/public/icons/stance/`
- `reference/field-agendas/scripts/stance-icons.mjs`, `site/src/lib/field-matrix-cell.ts`

## Commits
- `e524459d` Split field v2 hub and replace Unicode stance marks with SVG icons.
