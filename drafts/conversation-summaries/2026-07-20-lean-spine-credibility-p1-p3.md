# 2026-07-20 — Lean spine credibility plan P1–P3 (no P4 tiling)

## Trigger

User asked to implement all of `drafts/lean-spine-credibility-plan.md` except P4 (Löbian/tiling contrast).

## Done

### P1 — Non-omega headline certification

- Added `risk_gap_bound_from_trace_calibrated_profile`, `risk_gap_bound_from_trace_vector_certificate`, and `risk_gap_bound_from_trace_profile` in `Field/Finite/TraceBIQ.lean` — route through `traceControlDiversity_le_tight_optimism` / `risk_gap_bound_from_threshold_certified_cci` rather than bare `unfold RiskGap; omega` on the conclusion alone.
- Rewired `WorkedInstance.honest_instance_risk_bound` to use `risk_gap_bound_from_trace_profile` + `honest_trace_theta_margin`.
- Added headline theorem to `formal/axiom-ledger.json` (38 theorems; regenerated `metadata/axiom-budget-index.tex`).
- Updated `Certification.lean` module docstring pointer.

### P2 — Ground tolerance by example

- New `ToyDeploymentGate.lean`: `EpisodeBatteryGate`, `frozenValidationBatteryGate` (36 runs, 3 false passes, max 5 pre-registered), `frozen_validation_battery_gate_passes` by `decide`.
- `safe_from_case_requires_mb11` shows composition pattern (case + tolerance → `Safe` only via `MB11`).
- Prose in `formal/README.md`, `metadata/assumptions-ledger.md`. **Did not** axiomatize `WithinDeploymentRiskTolerance` for a toy system.

### P3 — Consistency + bridge independence

- New `SpineModel.lean`: `spine_axioms_consistent`, `spine_axioms_nontrivial`, 18 `*_independently_load_bearing` theorems (MB1–MB9, MB4a, MB10, MB11, S10, tolerance) — lifts `Defeaters`/`Forgeability` where possible, minimal new toys for MB2/MB3/MB5/MB6a/MB7*/MB9/S10.
- New `formal/scripts/check_spine_model.py` (checklist drift guard).
- Wired imports in `AlignmentProofSpine.lean`; module map rows in `formal/README.md`.

### Not done (explicit)

- **P4 Löbian/tiling** — deferred per user request.

## Verification

- `lake build`: 2252/2252 success.
- `python3 formal/scripts/check_spine_model.py`: pass.
- `python3 formal/scripts/check_axiom_budget.py`: pass (38 theorems).
- `make check`: not run this session (user can run before commit).

## Decisions

- Dropped collective `all_bridges_independently_load_bearing` And-chain: Lean parsed theorem names in type position as proof terms (Type-level `And`). Individual independence theorems + script checklist suffice.
- Renamed S10 export to `s10_blanket_coherence_independently_load_bearing` (avoid `S10_` prefix parse issues in structures).
- Frozen-validation battery: publish 3/36 false passes against maxFailures=5 (passes with margin; thresholds chosen before inspecting result).

## Open / next

- P4 Löbian contrast (`Field/Finite/LobTiling.lean`) when requested.
- Optional: appG subsection for bridge-independence table; wire `check_spine_model.py` into CI/Makefile.
- Optional: calibrated-profile corollary on a trace where `traceDiversityTightOptimism ≤ θ.lambdaFloor`.

## Key paths

- `formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean`, `ToyDeploymentGate.lean`, `SpineModel.lean`
- `formal/scripts/check_spine_model.py`, `formal/axiom-ledger.json`
- `formal/README.md`, `metadata/assumptions-ledger.md`, `drafts/lean-spine-credibility-plan.md`

## Commits

- `ea05db30` — Lean spine credibility P1–P4 (batched with P4 session)
