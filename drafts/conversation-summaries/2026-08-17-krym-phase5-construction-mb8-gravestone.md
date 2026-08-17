# Session: Krym Phase 5 — Construction + MB8 gravestone

**Date:** 2026-08-17  
**Thread:** Krym architecture revision (after Phase 4)

## Goal

Add construction-vs-certification Lean interface (no `TargetRealizable` axiom); retire MB8 from live bridge path; MB8 gravestone card; remove MB8 from field matrix column.

## Shipped

- `formal/AlignmentProofSpine/AlignmentConstruction.lean` (new): `AlignmentTarget`, `Realizes`, `TargetRealizable`, `CertifiedAsRealizing`, `ConstitutionalRule`/`cevConstitution`/`constitutionalTarget`, `fin_certification_without_construction`.
- `formal/AlignmentProofSpine/Core.lean`: removed `mb8` from `BridgeAssumptions`; `MB8_cev_process_convergence` relabeled legacy/gravestone (kept for Chokepoint).
- `appendices/appG-lean-proof-spine.tex`: MB8 gravestone assumption block + construction paragraph.
- `metadata/concepts/bodies/mb8-cev-process-convergence.md`: gravestone rewrite.
- `metadata/bridges.yml`: MB8 card `status: gravestone`.
- `reference/field-agendas/data/bridges.yml`: `matrixColumn: false`, `gravestone: true`.
- `site/scripts/sync-field-agendas.mjs`: hide `matrixColumn: false` bridges from rendered matrix **and** `field-agendas.json`.
- `formal/scripts/check_axiom_budget.py`: MB8 removed from `ALL_CORE_BRIDGES`.
- `context/lean_graph_node_aliases.json`, `formal/README.md`.

## Verification

- `lake build` — pass
- `python3 scripts/check_axiom_budget.py --update` — pass; `certified_class_safety_from_spine_and_bridges` no longer lists `MB8_cev_process_convergence`

## Open / next

- **Phase 6:** Crux-as-Prop threading for remaining spine; field v1/v2 cutover.
- Run `cd site && npm run sync:field-agendas` + `npm run sync:bridges` to regenerate site JSON/cards. **Done** (MB8 column filtered from JSON).
- Optional: `alignment-construction` concept card body for site.

## Locked (unchanged)

- MB8 card slug stays; matrix column hidden, not deleted from YAML data.
