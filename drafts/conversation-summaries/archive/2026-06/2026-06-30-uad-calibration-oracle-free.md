# UAD handle calibration → oracle-free blind auditor + negative results

**Date:** 2026-06-30
**Trigger:** User asked to "Implement" the calibrated coordination scoring +
scoped blind-auditor policy (replacing hardcoded `_COORD_WEIGHT=16` and the
vacuous `passes` override), then to reflect on the approach during long runs.

## What was done

1. **Calibrated UAD coordination (replaces hardcoded constant).**
   - `embedded_sim/handle_calibration.py` fits `coord_ref`, `coord_strong_min`,
     `coord_weight` on held-out seeds 101–110 (eval seeds 11–13), freezes
     `results/handle_calibration.json` (+`.md`).
   - **Structural fix in `uad.py`:** coordination gain is now applied only when
     the coalition passes the `is_strongly_coordinated` gate. Previously the gain
     multiplied the base score unconditionally, so loud decoy pairs grew faster
     than quiet colluders and **no finite weight** could rank colluders first
     (weight blew up to the 160 cap). With the gate, colluder norm ≈ 3.3 (strong)
     vs decoy ≈ 0.6–0.95 (not strong) on every seed; derived weight is small/stable.
   - **Binary search** (`_verify_coord_weight`) finds the minimum weight where
     `select_primary_unit(discover_units(...))` picks the colluders on every fit
     seed — matching the *actual* ranking path, not a simplified score proxy.
   - **Generalization headroom** (`COORD_WEIGHT_HEADROOM = 1.5`): the min
     separating weight is zero-margin and overfits; freezing slightly above it
     transfers to held-out seeds. Final artifact weight ≈ 21.5.

2. **Oracle-free blind-auditor policy (important correctness fix).**
   - First implementation leaked ground truth into the audit path:
     `apply_blind_auditor_policy` read `world.truth.coalition` and
     `world.truth.bound_offender_lab`. The `test_oracle_separation` contract
     caught it.
   - Removed both oracle params. The pass rule now depends only on
     auditor-observable facts (selected unit, `unit_scope_steps`,
     `intervention_level`). The `true_offender_ids` check was redundant anyway
     (a correct auditor retains probes and never reaches the vacuous branch).
   - **The separation survived oracle removal** — the false-pass gap is from
     scoping, not from peeking. Strengthens the result.

3. **Negative results documented** (`results/NEGATIVE_RESULTS.md`, new):
   - **N-1:** full == fake UAD byte-for-byte in the default ecology (the cheap
     proxy already points at the loud offender).
   - **N-2:** the separation exists only in a hand-built `misleading_top2 + bind`
     ecology at actor level, rides on one coordination gate, has a thin score
     margin (~3%), and differs only in *scoring* over the same observational log.

4. **TODOs added** (`experiments/embedded-simulation/TODO.md`):
   - **N-recover:** harvest scattered negatives from conversation summaries.
   - **R-1:** red-team the auditor with a *strong optimizer*, not a fixed
     top-2 strawman.
   - **G-1:** generalize to a *real* information boundary (Pearl ladder):
     `confounded_twin` ecology where two worlds share an identical observational
     log but different offenders, separable only by intervention — an
     observational auditor is provably at chance regardless of optimizer strength.

## Non-obvious decisions

- Coordination as a **qualitative gate**, not a tunable knob, is what makes the
  weight finite and the artifact defensible.
- Tests now evaluate the **frozen committed artifact** (freeze-then-eval), not a
  per-test refit (which produced a degenerate zero-margin 3-seed weight that
  failed to transfer to seed 11).
- Claim strength stays at **existence proof**, not general superiority. The user
  explicitly accepts negative/null results and wants the boundary made real
  (G-1) rather than chasing circular tuning against the strawman.

## Verification

- `python3 -m pytest tests/ -q` → **92 passed** (incl. oracle-separation contract).
- Artifact refit on seeds 101–110: `coord_weight ≈ 21.5`, `coord_ref ≈ 0.18`,
  `coord_strong_min = 0.99`, `blind_retained_max = 0`.

## Open / next

- G-1 (`confounded_twin`) is the principled next step for a non-circular claim.
- R-1 strong-optimizer red team before any general claim.
- Margin is thin; do not upgrade prose beyond existence-proof language.
- **Not committed** — user has not asked to commit this session's work.

## Key paths

- `embedded_sim/handle_calibration.py`, `embedded_sim/uad.py` (strong_coord gate),
  `embedded_sim/embedded_audit.py` (oracle-free policy call)
- `results/handle_calibration.json` / `.md`, `results/NEGATIVE_RESULTS.md`
- `tests/unit/test_handle_calibration.py`, `tests/unit/test_intervention.py`
- `experiments/embedded-simulation/TODO.md` (N-recover, R-1, G-1)
