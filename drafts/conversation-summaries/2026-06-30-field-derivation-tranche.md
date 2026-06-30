# 2026-06-30 — Field derivation tranche (top-down)

## Trigger
User asked to work through the prioritized field rederivations top to bottom until progress stalls.

## Done
- **Interruptibility (Orseau–Armstrong finite MDP):** `Field/Finite/Interruptibility.lean` — constant interrupted reward, base-optimal on non-interrupt branch, interrupt-invariant policy lift; exported in `Field/Interruptibility.lean` with new field records.
- **Quantilization (Taylor IntMass fragment):** `badMass`, `quantilizer_bad_mass_zero_of_ineligible_bad`, `quantilizer_base_rate_bound` in `Field/Finite/Probability.lean`; exported in `Field/Quantilization.lean`.
- **Relative reachability:** `DetGraph`, `GraphReachable`, `graph_reachability_preserved_not_all_targets` in `Field/Finite/Reachability.lean`; exported in `Field/Impact.lean`.
- **CIRL:** `defer_beats_commits_of_symmetric_flip_cost_unequal_mass` (general) + equal-mass corollary; exported in `Field/CIRL.lean`.
- `lake build` passes (1016 jobs).

## Decisions
- Dropped incomplete `Field/Finite/PMF.lean` after ENNReal/`ofNat` proof blockers; IntMass base-rate bound is the defensible Taylor fragment for now.
- Shutdown/off-switch and one-step AUP already had finite theorems — no new tranche work this session.
- Debate/ELK left for native protocol models (unchanged).

## Open / next
- **`PMF.ofFintype` / `quantilizerPMF`:** retry with `Nat.cast`/`ENNReal` coercions and `PMF.filter` on eligible support.
- **Multi-step OA interrupt learning setup** (Q-value invariance under interrupt probability).
- **Multi-step AUP / MDP value iteration.**
- Appendix I table + proof graph refresh for new theorem names.

## Key paths
- `formal/AlignmentProofSpine/Field/Finite/Interruptibility.lean`
- `formal/AlignmentProofSpine/Field/Finite/Probability.lean`
- `formal/AlignmentProofSpine/Field/Finite/Reachability.lean`

## Commits
- (none — user did not request commit)
