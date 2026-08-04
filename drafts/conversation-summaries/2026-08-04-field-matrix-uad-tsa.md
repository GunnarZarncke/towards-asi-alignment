# 2026-08-04 — Field matrix UAD → TSA row

## Trigger
User asked whether coverage matrix entry **#82** (UAD / agency-detect, MB1 support) still listed under **Neglected approaches** rather than **TSA**; confirmed yes, then requested move to TSA.

## Done
- `reference/field-agendas/data/matrix.yml` — added #82 to TSA `MB1` (type S, alongside #81); Neglected `MB1` already empty in YAML.
- Re-synced `reference/field-agendas/field-agenda-index.md` and `site/src/data/field-agendas.json`.
- Note: `reference/field-agendas/data/evidence.yml` already had `agenda: TSA` for #82 in HEAD; only matrix placement + generated artifacts were stale.

## Decisions
- Move matrix cell only; leave Neglected approaches portfolio agenda card prose mentioning UAD as historical portfolio context (UAD originated in that portfolio).

## Open / next
- None for this change. Rebuild site if a deploy is pending so `/field/` picks up JSON.

## Key paths
- `reference/field-agendas/data/matrix.yml`
- `reference/field-agendas/data/evidence.yml` (#82)
- `site/src/data/field-agendas.json`

## Commits
- `a1cfeff6` Move field matrix evidence #82 (UAD/agency-detect) to the TSA row.
