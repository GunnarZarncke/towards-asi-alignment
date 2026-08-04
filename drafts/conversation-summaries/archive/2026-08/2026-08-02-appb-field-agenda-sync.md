# 2026-08-02 — App B field agenda core sync

## Trigger
User: fix headline App B ↔ field agenda gap (MB4a/MB11 missing); defer secondary prose items as TODO.

## Done
- [`appendices/appB-bridge-crosswalk.tex`](../../appendices/appB-bridge-crosswalk.tex): intro range **MB1–MB11** incl. **MB4a**; **Field agenda index** paragraph (repo path + `/field/` URL + spine-translation caveat); crosswalk table split **MB4 / MB4a / MB8** + new **MB11** row; notes paragraphs for MB4, MB4a, MB8, MB11 (one-way MB4a direction, CompositePathBypass, MB11 packaging vs bridge).
- [`reference/field-agendas/field-agenda-index.md`](../../reference/field-agendas/field-agenda-index.md): remove "App B deferred" lines; bridge-map line now MB1–MB11 incl. MB4a.
- [`metadata/TODO.md`](../../metadata/TODO.md): mark core sync done; add **App B ↔ field agenda sync (deferred secondary)** bucket.
- [`drafts/field-claim-formalization-and-bridge-review-plan.md`](../field-claim-formalization-and-bridge-review-plan.md): status line updated.

## Decisions
- Split MB4/MB8 table row into three rows (MB4, MB4a, MB8) rather than sub-label only — matches field-index matrix columns.
- Spine-translation rules stay primary in field index; App B gets a short caveat paragraph, not the full table (deferred).
- Intervention map unchanged this pass (infra-Bayesianism / IASR deferred).

## Open / next
- See `metadata/TODO.md` § **App B ↔ field agenda sync (deferred secondary)**.
- Rebuild PDF / sync site appB card when convenient (`node scripts/sync-chapters.mjs`).

## Key paths
- [`appendices/appB-bridge-crosswalk.tex`](../../appendices/appB-bridge-crosswalk.tex)
- [`reference/field-agendas/field-agenda-index.md`](../../reference/field-agendas/field-agenda-index.md)
