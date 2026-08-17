# Session: Krym Phase 3b — MB2 checkable Props

**Date:** 2026-08-17  
**Thread:** Krym architecture revision (Harfe review triage of Phase 3 `3f664d28`)

## Goal

Make MB2 non-vacuous: concrete finite evidence types, `MB2a`/`MB2b`/`MB2c1` as `Prop` cruxes (not global axioms), split gradient from causal control, consumer theorem, shrink certification axiom footprint.

## Shipped

- `formal/AlignmentProofSpine/Bundles.lean`: `BundleExperiment` / `BundleModel`, `CompatibleWithEvidence`, `BundleIdentifiable`, `FinBundleAudit`, gradient/geometry/causal/tradeoff finite `def`s; `P15_observed_policy_not_fin_identifiable` on canonical `2×2×2` domain.
- `formal/AlignmentProofSpine/MB2Identifiability.lean`: `MB2aCrux` / `MB2bCrux` / `MB2c1Crux` / `MB2Crux`; `bundle_aligned_from_mb2_chain`; `fin_policy_only_refutes_mb2a`; `fin_gradient_without_causal_control`.
- `formal/AlignmentProofSpine/Core.lean`: removed `MB2_bundle_identifiability`, `BundleAligned` axiom trio, and `BridgeAssumptions.mb2`.
- `formal/AlignmentProofSpine/SpineModel.lean`: `MB2_independently_load_bearing` via finite gradient-without-causal-control witness.
- `appendices/appG-lean-proof-spine.tex`: MB2 block matches finite-layer Props + split MB2c1.
- `formal/axiom-ledger.json` + `metadata/axiom-budget-index.tex`: regenerated — `MB2_bundle_identifiability` and bundle-alignment vocabulary axioms gone from certification footprint.
- Metadata: `mb2-bundle-identifiability.md`, `bridges.yml`, `lean_graph_node_aliases.json`, `formal/README.md`, `check_axiom_budget.py` (MB2 not in `ALL_CORE_BRIDGES`).

## Verification

- `lake build` — pass
- `python3 scripts/check_axiom_budget.py --update` — pass

## Open / next

- **Phase 4:** MB4 uptake vs legitimacy; rename `MB4_correction_legitimacy` → `MB4_correction_integrity`.
- Site card body may need `npm run sync` from metadata if publishing MB2 card lean node text.
- `site/src/data/lean-spine.json` / `field-agendas.json` still reference old `MB2_bundle_identifiability` until site sync.

## Locked (unchanged)

- Public MB2 matrix noun: Value Learning; no MB2a/b/c site cards.
- Certification spine still uses `BundleTransport` directly; MB2 chain is parallel finite layer.
