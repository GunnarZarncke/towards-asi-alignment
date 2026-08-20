# Session: Krym Phase 4 — MB4 uptake vs legitimacy

**Date:** 2026-08-17  
**Thread:** Krym architecture revision (after Phase 3b)

## Goal

Separate reference legitimacy from causal correction uptake on measured paths; rename `MB4_correction_legitimacy` → `MB4_correction_integrity`; package MB4 cruxes as checkable `Prop`s.

## Shipped

- `formal/AlignmentProofSpine/Correction.lean`: `ReferenceLegitimacyOnPath`, `CorrectionUptakeOnPath`, `CorrectionPersistenceOnPath`; `correction_path_legitimate_iff_components`.
- `formal/AlignmentProofSpine/MB4CorrectionIntegrity.lean` (new): `MB4aReferenceLegitimacyCrux`, `MB4UptakeCrux`, `MB4PersistenceCrux`, `MB4Crux`, `MB4DecomposedCrux`; `preserves_correction_from_mb4_chain`; finite witness independence theorems.
- `formal/AlignmentProofSpine/Core.lean`: `MB4_correction_legitimacy` renamed → `MB4_correction_integrity`.
- `formal/AlignmentProofSpine/SpineModel.lean`: `MB4_uptake_separate_from_reference_legitimacy`.
- `appendices/appG-lean-proof-spine.tex`: MB4 block documents decomposition + global bridge.
- Metadata: `mb4-correction-legitimacy.md`, `bridges.yml`, `lean_graph_node_aliases.json`, `formal/README.md`.

## Verification

- `lake build` — pass
- `python3 scripts/check_axiom_budget.py --update` — pass (ledger shows `MB4_correction_integrity`)

## Open / next

- **Phase 5:** Construction Lean model (no MB*); MB8 gravestone.
- Site sync for MB4 lean node rename (`field-agendas.json` still has old name until `npm run sync:field-agendas`).

## Locked (unchanged)

- MB4a remains sibling bridge for measured-path legitimacy; card slug unchanged (`mb4-correction-legitimacy`).
