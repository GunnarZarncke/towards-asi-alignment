# 2026-08-02 — Field crux on bridge cards

## Trigger

Remove the Field hub crux legend; fold agree/differ/homograph clarifications from `bridges.yml` onto each individual MB bridge card instead.

## Done

- Removed [`FieldCruxLegend.astro`](../../site/src/components/FieldCruxLegend.astro) and its use on [`site/src/pages/field/index.astro`](../../site/src/pages/field/index.astro).
- Removed `renderCruxLegend()` from [`site/scripts/sync-field-agendas.mjs`](../../site/scripts/sync-field-agendas.mjs); regenerated [`field-agenda-index.md`](../../reference/field-agendas/field-agenda-index.md) and [`field-agendas.json`](../../site/src/data/field-agendas.json).
- Updated matrix intro in [`meta.yml`](../../reference/field-agendas/data/meta.yml) and [`FieldAgendaMatrix.astro`](../../site/src/components/FieldAgendaMatrix.astro).
- Added **Where agendas agree / diverge** (and homograph splits where needed) to MB1–MB10 bodies under [`metadata/concepts/bodies/`](../../metadata/concepts/bodies/); MB11 on [`dynamical-guarantee.md`](../../metadata/concepts/bodies/dynamical-guarantee.md).
- Regenerated site bridge cards via `npm run sync:bridges`.

## Decisions

- Hub matrix stays noun + MB* headers; clarifications live on linked cards only (no duplicate legend table).
- MB4 card covers MB4a split inline; MB7 card covers MB7d acausal coordination inline.

## Open / next

- Track 2 field–book crux divergence (Lean + App B) per [`drafts/field-crux-divergence-plan.md`](../../drafts/field-crux-divergence-plan.md).
