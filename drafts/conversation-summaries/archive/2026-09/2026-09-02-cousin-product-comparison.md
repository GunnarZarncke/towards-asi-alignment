# 2026-09-02 — Cousin spec-sheet shipped

## Trigger
Cousin comparison / spec-sheet plan for Start Here; user asked to implement, then iterated UI (scroll, checkboxes, TSA column order, best-for row, header labels).

## Done
- Plan: [`drafts/plans/cousin-product-comparison.md`](../plans/cousin-product-comparison.md) (implemented). Siblings: [`iliad-communal-canon.md`](../plans/iliad-communal-canon.md), [`lw-wiki-tags.md`](../plans/lw-wiki-tags.md); pointer in [`field.md`](../plans/field.md).
- **Site:** `/start/spec-sheet/` — `SpecSheetGrid.astro`, YAML source, sync script, Start Here link, FAQ, agenda-card footers.
- **Data:** `product-comparison.yml` — 8 features × 25 roster columns; TSA first; Ships product + Communal last; Iliad always visible.
- **MIRI card:** Arbital → LW wiki as living explainer layer; clustering.yml + CAIS AISES link.
- **UI (final):** Agenda / Best for / Feature header rows; circle checkmarks (partial = half-fill); horizontal scroll + arrows + drag; disclaimer at bottom; TSA column highlight; best-for per column.

## Decisions
- Columns = roster slugs only; no Field hub tile; not a ranking.
- TSA usable product = simulations/demos (Partial), not companion site. Constructive theory = No for TSA.
- Public knowledge site row still scores companion site for TSA.

## Open / next
- Human pass on YAML marks and `because` lines.
- LW-tag pilot and Iliad communal wiki not in this commit.

## Not staged
- `drafts/alignment-crux-map/*`, `alignment-problem-alternative-decomposition.md`, conversation-log archive moves, unrelated sync drift in `experiments.json` / `card-redirects.json`.
