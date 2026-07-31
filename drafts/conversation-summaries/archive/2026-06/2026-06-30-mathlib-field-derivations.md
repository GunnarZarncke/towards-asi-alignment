# 2026-06-30 — Mathlib field derivations

## Trigger
User asked to continue the Mathlib-backed field rederivation tranche (CIRL, AUP/RR, quantilization) after Mathlib adoption and the field-formalization gem naming.

## Done
- Added `formal/AlignmentProofSpine/Field/Finite/Probability.lean`:
  - `IntMass`, `expect`, `quantilizerMass`, `quantilizer_soundness_transfers`
  - `AUPOneStep`, `AUPAttainableUtilityPreserved`, `aup_preserves_optimal_auxiliary_actions`
  - `ScalarAssistanceBelief`, `cirlMismatchBelief`, `cirl_defer_beats_commit_under_reward_uncertainty`
  - `scalarBeliefAsBundle` / `scalar_belief_embeds_as_k1_bundle`
- Exported public theorems in `Field/CIRL.lean`, `Field/Impact.lean`, `Field/Quantilization.lean` with new field result records.
- Wired `Probability.lean` through `Field.lean`.
- Updated Appendix I status table, `formal/README.md`, and `metadata/TODO.md`.

## Decisions
- Used integer-weighted `Finset.sum` expectations rather than `PMF.ofFintype` (lighter, computable, matches existing spine style).
- AUP fragment proves before-state optimal utility stays below after-state attainable maximum (honest finite analogue of non-decreasing attainable utility).
- CIRL defer theorem uses explicit two-point belief with costly commit mismatch (`native_decide` witness).

## Open / next
- `PMF.ofFintype` / ENNReal layer for Taylor-style probabilistic quantilizer risk bound.
- Multi-step MDP value iteration and full assistance-game deference optimality.
- Native Debate/ELK models (unchanged deferral).

## Key paths
- `formal/AlignmentProofSpine/Field/Finite/Probability.lean`
- `formal/AlignmentProofSpine/Field/CIRL.lean`
- `formal/AlignmentProofSpine/Field/Impact.lean`
- `formal/AlignmentProofSpine/Field/Quantilization.lean`
- `appendices/appG-lean-proof-spine.tex`

## Commits
- None.

## Verification
- `lake build` in `formal/` passed (799 jobs).
