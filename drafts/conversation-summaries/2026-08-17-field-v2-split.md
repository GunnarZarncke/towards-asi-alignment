# Session: Field v2 split into cards + coverage subpage

**Date:** 2026-08-17

## Goal

De-clutter `/field/v2/` by splitting content into concept cards and a coverage subpage.

## Shipped

- **Slim hub** — `/field/v2/`: intro, one bridge paragraph, Field map nav grid.
- **`/field/coverage/`** — matrix + evidence catalog (stance marks).
- **New cards:** `alignment-lifecycle`, `bearer-admission-adjacent`, `field-coverage` (pointer).
- **Extended cards:** `bridge-assumptions` (dependency graph embed), `alignment-target` (specify/construct table embed).
- **Shared components:** `FieldLifecycleAxis`, `FieldSpecifyConstructTable`, `FieldAdjacentWork`, `FieldBridgeGraphSection`, `FieldHubNav`, `StanceMark`.
- **Stance marks:** seven SVG icons (`stance-icons.mjs`, `site/public/icons/stance/`); Unicode/CSS glyph path removed (2026-08-18).
- **Deep links** updated in bodies, `sync-field-agendas.mjs`, `meta.yml`, `MAINTAINER.md`, `term-links.yml`, field intro.
- **`sync:field-v2`** and **`sync:stance-icons`** in site sync chain.
- **Build:** site `astro build` passes.

## Verify

```bash
cd site && npm run build
# Hub: /field/v2/
# Coverage: /field/coverage/
# Cards: /cards/alignment-lifecycle/, /cards/bridge-assumptions/, /cards/alignment-target/, /cards/bearer-admission-adjacent/
```
