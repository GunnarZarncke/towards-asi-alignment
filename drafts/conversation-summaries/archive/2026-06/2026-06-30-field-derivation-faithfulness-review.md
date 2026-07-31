# 2026-06-30 — Field derivation faithfulness review

## Trigger
User asked (as ChatGPT 5.5 reviewer): review the Mathlib-backed field derivation — any `sorry`? Is it faithful? Work on what's missing.

## Done
- Audited `formal/AlignmentProofSpine/Field/**` for `sorry`/`admit`: **none** in derivation modules; only explicit `axiom` handles in `Field/Imported.lean` for source-cited field theorems.
- **Removed misleading theorem** `aup_preserves_correction_relevant_auxiliary_actions` (tautology: only used reachability availability, ignored AUP).
- **Added honest separation** `aup_attainable_preservation_need_not_preserve_all_tracked_options` via `aupSeparationStep` / `aupSeparationInterface`.
- **Upgraded CIRL defer** from witness-only to general `defer_beats_commits_of_symmetric_flip_cost` (symmetric flip penalties, equal positive reward masses, positive defer constant); witness `cirlMismatchBelief` instantiates it.
- **Quantilization bridge:** `sampleMass` + `quantile_sample_soundness_from_distribution`; restored `quantilizer_distribution_soundness_transfers` field record.
- Updated Appendix I status table theorem names; `lake build` passes (1015 jobs).

## Decisions
- Claim strength: finite interface special cases + separations are defensible; full published CIRL/AUP/quantilization theorems remain imported axioms only.
- Equal-mass CIRL defer is the proved general theorem; unequal-mass extension left optional (brittle `nlinarith`).
- Do not reintroduce tautological AUP→correction bridges.

## Open / next
- `PMF.ofFintype` / Taylor probabilistic quantilizer bound.
- Multi-step MDP / full assistance-game deference optimality.
- Optional unequal-mass CIRL defer theorem.
- Proof graph `.dot`/PNG refresh if new theorem names should appear in figures.

## Key paths
- `formal/AlignmentProofSpine/Field/Finite/Probability.lean`
- `formal/AlignmentProofSpine/Field/CIRL.lean`, `Impact.lean`, `Quantilization.lean`
- `formal/AlignmentProofSpine/Field/Imported.lean`
- `appendices/appG-lean-proof-spine.tex`

## Commits
- (none — user did not request commit)
