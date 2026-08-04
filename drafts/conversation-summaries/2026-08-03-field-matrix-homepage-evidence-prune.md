# 2026-08-03 — Field matrix homepage evidence prune

## Trigger
Reviewer feedback: matrix citations accurate but ~dozen cells use org landing pages as evidence; user agreed — remove generic entries, move org links to agenda cards, add concrete papers where missing.

## Done
- Removed evidence catalog entries **12, 30, 32, 37, 44, 71** from `reference/field-agendas/data/evidence.yml` and pruned matching ids from `matrix.yml`.
- Added **ev-150** (Orthogonal MB1): Demski & Garrabrant 2019 embedded agency — replaces orxl.org homepage cell.
- Enriched agenda `links` in YAML for Redwood, Anthropic, DeepMind, METR, Orthogonal, CLR (papers + org hubs on cards, not matrix).
- Regenerated `field-agenda-index.md`, site agenda cards, `field-agendas.json`.

## Not in this pass (similar pattern)
Apollo **33** / Truthful **72** homepages; Anthropic cluster tool homepages **74–76**; CAIF **69** — still in matrix as O/D/E types. User may want a follow-up pass.

## Key paths
- `reference/field-agendas/data/evidence.yml`
- `reference/field-agendas/data/matrix.yml`
- `reference/field-agendas/data/agendas/*.yml`
