# 2026-06-30 — Mathlib spine broadening

## Trigger
User asked whether other existing proofs can and should use Mathlib; implement where yes.

## Done
- Expanded `AlignmentProofSpine/Mathlib.lean`:
  - `not_exists_injective_of_fin_card_lt` (P34 pigeonhole wrapper)
  - `listIntAllNonnegative`, `listIntSum_nonneg`, `listIntSum_nonneg_of_mem`
- `Adversarial.lean`: `P34` delegates to shared pigeonhole lemma.
- `Correction.lean`: imports Mathlib hub; `P24_chain_capacity_le_each_edge` uses `min_le_left` / `min_le_right` instead of `omega`.
- `Field/Finite/Basic.lean` + `Weights.lean`: share list-sum nonnegativity from Mathlib hub (removed duplicate induction proofs).
- `Field/Finite/MDP.lean`: dropped private `finUnivNonempty`; uses `Finset.univ_nonempty` like `Probability.lean`.
- Minor proof cleanups exposed by Mathlib import chain (`Capability.Control_le_IctrlSys`, `trajectory_cci_implies_impact_bound`).

## Decisions
- Keep `ChainCapacity` as a custom list min (not `List.foldl min`) — empty/singleton semantics differ from a generic fold.
- Did not bulk-replace `omega` with `linarith` in Capability/Boundaries/CooperationGraph — cosmetic only, no shared lemma gain.
- Left `iterateN` in `Core.lean` self-contained (low priority per prior log).

## Open / next
- Optional: `Function.iterate` from Mathlib for `Certification` induction proofs.
- Optional: graph reachability in `CooperationGraph` if a Mathlib fragment matches the custom UAD graph API.
- Commit `formal/` Mathlib broadening when user asks.

## Key paths
- `formal/AlignmentProofSpine/Mathlib.lean`
- `formal/AlignmentProofSpine/Adversarial.lean`
- `formal/AlignmentProofSpine/Correction.lean`
- `formal/AlignmentProofSpine/Field/Finite/Basic.lean`
- `formal/AlignmentProofSpine/Field/Finite/Weights.lean`
- `formal/AlignmentProofSpine/Field/Finite/MDP.lean`

## Commits
- None.

## Verification
- `lake -d formal build` passed (1719 jobs).
