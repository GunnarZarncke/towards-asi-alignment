# 2026-08-17 — Specify / construct instances (field v2 + Lean)

## Trigger

Continue prior thread: typed specify/construct instance catalog with Lean names, concept cards, and `/field/v2/` table linking each constitutional approach to its construction bet.

## Done

- **Lean** (`AlignmentConstruction.lean`): extended `ConstitutionalRule` (`openWorldCoverage`, `institutional`); `SpecWellFormedness` / `SpecifyCrux` placeholder; named instances (`cevConstitution`, `caiConstitution`, `gsaiConstitution`, `institutionalConstitution`); `ConstructionBet`, `SpecifyConstructPair`, pairing theorems; `fin_claimed_builder_without_realization`.
- **Data:** `reference/field-agendas/data/specify-construct-instances.yml` (4 schema instances + PreDCA peer row).
- **Cards:** 9 new concept cards (`alignment-target`, `specify-*`, `construct-*`) via `metadata/concepts.yml` + bodies.
- **Site:** `/field/v2/#specify-construct-instances` table with parameters, Lean names, correspondence prose, references; peer-target subsection.
- **Checks:** `check_specify_construct_instances.py`; wired into `make check` with `sync:field-v2 --check` and `check_open_spine_interfaces.py`.
- **Docs:** `MAINTAINER.md`, `formal/README.md`; open-spine `alignment-target` card → `/cards/alignment-target/`.

## Decisions

- Field programs are **instances** of one schema, not new MB columns.
- `SpecifyCrux` stays uninterpreted / never axiomatized (out of scope).
- PreDCA/Kosoy listed as **peer outer target**, not `ConstitutionalRule` filling.

## Open / next

- Optional: CIRL/assistance-games instance row; legal examples beyond App C analogue.
- App G prose pass for new Lean names (deferred).

## Key paths

- `formal/AlignmentProofSpine/AlignmentConstruction.lean`
- `reference/field-agendas/data/specify-construct-instances.yml`
- `site/src/pages/field/v2/index.astro`

## Verification

- `lake build` — pass
- `check_open_spine_interfaces.py`, `check_specify_construct_instances.py` — pass
- `npm run sync:concepts`, `sync:field-v2`, `npm run build` — pass (905 pages)
