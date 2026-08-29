# 2026-08-29 — Continuity & drift catalog precision

## Trigger
Orchestrator follow-up: log isolated precisioner packets until the union catalog was complete, then report usable counts by domain.

## Done
- Logged all **366** in-union names in `drafts/continuity-drift-study/phase1/precision/results.tsv` (plus 4 extra non-union firm rows, not counted).
- Domain usable counts in `phase1/precision/wave1.md`. Congregation of the Mission / Vincentians logged from replacement packet `64fd9688` (prior spawn produced no output).
- Hub `README.md` and `metadata/TODO.md` note catalog precision complete.

## Decisions
- Usable = `earliest_own_aim` yes (quoted/paraphrased own earliest-period aims with citation). Persistence alone is not usable.
- First complete packet wins on duplicate catalog names (unchanged).

## Open / next
- Gate remaining packets (other fact/episode logs, judge); holdout / Phase 2. Do not deploy `packets/bundle-*.md`.

## Key paths
- `drafts/continuity-drift-study/phase1/precision/results.tsv`
- `drafts/continuity-drift-study/phase1/precision/wave1.md`
- `drafts/continuity-drift-study/README.md`

## Commits
- none
