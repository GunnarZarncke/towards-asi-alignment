# 2026-08-17 — Krym Phase 3 MB2 Lean chain

## Trigger

Continue Krym architecture revision Phase 3: expose evidence→identifiability→gradient→`BundleAligned` in Lean; de-opaque `BundleAligned`.

## Done

- `formal/AlignmentProofSpine/Core.lean`: `BundleAligned` is now a `def` (geometry correspondence ∧ causal policy control ∧ tradeoff direction); `MB2_bundle_identifiability` relabeled MB2c (gradient → aligned).
- `formal/AlignmentProofSpine/MB2Identifiability.lean` (new): `BundleExperiment` / `BundleModel`, `BundleIdentifiable`, axioms **MB2a** (evidence → identifiability) and **MB2b** (identifiability → gradient), `MB2Crux` packaging.
- `formal/AlignmentProofSpine/Bundles.lean`: `P15_observed_policy_not_fin_identifiable` — finite counterexample that policy-only evidence is not identifiable (MB2a crux shape).
- `appendices/appG-lean-proof-spine.tex`: MB2 assumption block split into eqs mb2a/b/c + `BundleAligned` conjunction note.
- `formal/AlignmentProofSpine/Defeaters.lean`: MB2 row cites finite toy.
- `metadata/concepts/bodies/mb2-bundle-identifiability.md`: lean node summary + module path.
- `lake build` passed; `check_axiom_budget.py --update` refreshed ledger.
- Site `sync:bridges`, `sync:concepts`.

## Decisions

- Public MB2 stays one bridge in `BridgeAssumptions`; MB2a/b are Lean-visible sub-cruxes only (no MB2a/b/c site cards).
- `BundleCausallyControlsPolicy` remains an abstract `axiom` on `System` (exact operational def deferred per plan).

## Open / next

- **Phase 4:** Lean MB4 — correction uptake vs legitimacy; rename `MB4_correction_legitimacy` → `MB4_correction_integrity`.
- Phases 5–6 per `drafts/krym-architecture-revision-plan.md`.

## Key paths

- `formal/AlignmentProofSpine/MB2Identifiability.lean`
- `formal/AlignmentProofSpine/Core.lean` (`BundleAligned` def)
- `appendices/appG-lean-proof-spine.tex` (`appi:eq:mb2a`–`c`)

## Commits

- (none — user did not request commit)
