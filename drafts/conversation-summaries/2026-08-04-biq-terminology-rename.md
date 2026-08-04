# 2026-08-04 — B-IQ → BIQ terminology rename

## Trigger
User asked to replace **B-IQ** with **BIQ** throughout book and site.

## Done
- Replaced `B-IQ` → `BIQ` in appendices (App B/E/G), metadata (concepts, bridges, assumptions ledger, TODO), formal spine comments/docs, reference field-agenda glossary + index, site JSON + lean-spine sync script, Lean proof-graph DOT files, and embedded-simulation trace-BIQ calibration docs.
- Regenerated site artifacts: `sync-field-agendas.mjs`, `sync-concepts.mjs`, `sync-bridges.mjs`, `sync-lean-spine.mjs` (51 concept cards, 14 bridge cards, field-agendas.json).
- Left **`context/extracts/*`** unchanged (source-paper spelling); **`drafts/*`** archive logs untouched.

## Decisions
- Scope = reader-facing book + site + formal spine cross-refs; not external extract canon.
- Did **not** stage `reference/field-agendas/data/evidence.yml` or `matrix.yml` in this commit — both had pre-existing unstaged field-matrix work mixed with the single ev-96 BIQ line; commit those separately when ready.

## Open / next
- Stage and commit remaining `evidence.yml` / `matrix.yml` field-matrix prune when that thread is closed (ev-96 line already reads BIQ on disk).
- Optional: grep `drafts/` and `review/attic/` if internal working docs should follow the new spelling.

## Key paths
- `appendices/appE-glossary.tex` — homograph note (experimental BIQ vs hidden productive BIQ bound)
- `reference/field-agendas/inter-agenda-term-glossary.md`
- `metadata/concepts.yml` — glossary term `Hidden productive BIQ bound`

## Commits
- `9044dd6b` Rename B-IQ to BIQ across book and companion site.
