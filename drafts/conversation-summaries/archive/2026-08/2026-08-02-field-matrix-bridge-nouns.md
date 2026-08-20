# 2026-08-02 — Field matrix bridge nouns

## Trigger

Replace opaque `MB*` matrix column headers with field-facing nouns plus semantic crux wording; rename MB bridge card titles; defer field–book crux divergence to a Track 2 plan.

## Done

- Added [`reference/field-agendas/data/bridges.yml`](../../reference/field-agendas/data/bridges.yml) — locked nouns (Embedded Agency … Deployment Safety; MB10 **Successor Gaming**, MB9 **Grounding Drift**), crux wording, Lean handles, legend notes.
- Updated [`metadata/bridges.yml`](../../metadata/bridges.yml) — MB1–MB10 card titles + `fieldCrux` aligned to nouns (site cards regenerated via `sync:bridges`; card files gitignored).
- Extended [`site/scripts/sync-field-agendas.mjs`](../../site/scripts/sync-field-agendas.mjs) — crux legend + `Noun (MB*)` matrix headers; exports `bridges` in `field-agendas.json`.
- Field hub: [`FieldCruxLegend.astro`](../../site/src/components/FieldCruxLegend.astro), noun headers in [`FieldAgendaMatrix.astro`](../../site/src/components/FieldAgendaMatrix.astro).
- Updated [`bridge-crosswalk.json`](../../site/src/data/bridge-crosswalk.json) — MB4/MB4a/MB8 split, MB11 row, `noun` + crux columns on App B table.
- Track 2: [`drafts/field-crux-divergence-plan.md`](../../drafts/field-crux-divergence-plan.md); open item in [`metadata/TODO.md`](../../metadata/TODO.md).

## Decisions

- **Two layers:** matrix **noun** (field label) + **crux wording** (semantic bridge bet); `MB*` stays as spine keys only.
- **MB10 noun:** Successor Gaming (not Deceptive Alignment / Alignment Transport) — successor checklist gaming, distinct from MB7 inner alignment.
- **Track 2 deferred:** Lean field-local models + App B/manuscript pickup per divergence plan; no spine axiom renames in Track 1.

## Open / next

- Execute Track 2 per [`drafts/field-crux-divergence-plan.md`](../../drafts/field-crux-divergence-plan.md) (P1: MB4/MB4a, MB5/MB10, MB9).
- Optional: sync App B longtable `fieldCrux` strings to `bridges.yml` crux wording (secondary App B item in TODO).
