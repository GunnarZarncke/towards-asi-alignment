# 2026-08-02 — Site Field hub and agenda restructure

## Trigger
User requested site nav changes (Field before Cards, Book before PDF, Badges after Cards), a Field hub with the coverage matrix and evidence catalog, agenda cards linked from matrix rows, MB column headers linked to bridge cards, and restructuring `field-agenda-index.md` into individual YAML files to avoid duplication.

## Done
- Split `reference/field-agendas/field-agenda-index.md` into structured YAML under `reference/field-agendas/data/` (32 agendas, matrix, 132 evidence rows, clustering).
- Added `reference/field-agendas/scripts/extract-from-index.mjs` (markdown → YAML import) and `site/scripts/sync-field-agendas.mjs` (YAML → agenda cards, `field-agendas.json`, regenerated index markdown).
- New `/field/` page with coverage matrix, evidence catalog, agenda list, map clustering; components `FieldAgendaMatrix.astro`, `FieldEvidenceCatalog.astro`.
- 32 agenda cards at `site/src/content/cards/field-agendas/*.md` (type `agenda`) with intro, links, clustering roll-ups.
- Nav order: Start Here, Guided Tour, **Field**, Cards, **Badges**, **Book**, …, **PDF**, Glossary.
- MB columns link to bridge cards; matrix row headers link to agenda cards.
- Wired `sync:field-agendas` into `npm run sync`; search index includes Field hub and agenda cards.
- Updated `reference/field-agendas/README.md`, `site/README.md`, `badges.ts` (agenda type).
- Canonical matrix cells in YAML (`{ type, ids[] }`); `matrix-cell.mjs` normalizes legacy markdown on sync; `MAINTAINER.md` documents agent editing rules.
- Matrix cells chunk to **≤3 catalog IDs per type letter** (`chunkMatrixCellGroups`) so wide superscript runs (e.g. CIRIS MB4 D54–111) wrap in narrow columns; site renders grouped tags (`D`<sup>54,55,56</sup> + `D`<sup>109,110,111</sup>).
- Public Field intro (`site/src/content/field/intro.md`); trimmed hub (no inclusion test / spine translation on public page).

## Decisions
- **Source of truth:** `reference/field-agendas/data/` — `field-agenda-index.md` is generated output, not edited by hand.
- **MB4a / MB7d / MB11** map to existing cards (`mb4-correction-legitimacy`, `mb7-hidden-capability-and-access`, `dynamical-guarantee`).
- Training/meta agendas (BlueDot, MATS, CAIS, etc.) get cards but are excluded from matrix per existing index policy.

## Open / next
- Hand-edit YAML for future agenda/matrix updates; run `npm run sync:field-agendas`.
- Optional: richer agenda card matrix slice (per-agenda evidence subset) on card pages.
- `inter-agenda-term-glossary.md` still monolithic — deferred.

## Verify
- `cd site && npm run sync:field-agendas && npm run build` — 841 pages, `/field/` and `/cards/field-agendas/miri/` present.

## Commits
- (this session)
