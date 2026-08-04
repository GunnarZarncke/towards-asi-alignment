# 2026-08-02 — Field agenda restructure and merges

## Trigger
Restructure field agendas from neglected-approaches report review: rename AE Studio row, add Safeguarded AI and MAI+CIP, fold satellite listings into existing rows, merge non-independent agendas where bridge unions stay clean, improve Neglected approaches card from AE Studio essay, shorten long matrix row headers.

## Done
- **Neglected approaches portfolio** replaces AE Studio (`neglected-approaches-portfolio.yml`); rich `overview` from AE alignment agenda essay; ev-41 sources updated.
- **New agendas:** `safeguarded-ai-aria-zeroth-heron`, `mai-cip-institutional-alignment` (+ evidence ev-134–149 folded items).
- **TSA:** restored matrix row with `matrixLink` → companion home; `generateCard: false` (no agenda card).
- **Independence merges (4 rows → 25 matrix rows):** GovAI+UK AISI, Apollo+Truthful AI, CHAI+FAR.AI, Anthropic+Goodfire; deleted absorbed YAML/cards.
- **Left separate:** AI Futures vs METR; Conjecture carrier expanded (EleutherAI) only.
- **Sync:** `overview` optional field in `sync-field-agendas.mjs`; matrix `matrixLink` row headers in `FieldAgendaMatrix.astro`.
- **Matrix labels:** `Neglected approaches`, `Safeguarded AI` (short row headers).
- Ran `npm run sync:field-agendas`.

## Decisions
- Portfolio breadth is one matrix row; satellite neglected listings fold into existing rows rather than new rows.
- Merged rows use union of bridge cells without mixing incompatible crux coverage (per prior independence review).
- Card titles stay descriptive; matrix row headers may be shorter.

## Open / next
- Full site build to refresh `search-index.json` (stale URLs for deleted agenda cards).
- App B crosswalk prose still deferred for new/merged agenda names.
- `metadata/TODO.md` unchanged this session.

## Key paths
- `reference/field-agendas/data/` (YAML source of truth)
- `site/scripts/sync-field-agendas.mjs`
- `reference/field-agendas/field-agenda-index.md` (generated)

## Commits
- `5c3170e7` Restructure field agenda matrix after neglected-approaches review.
