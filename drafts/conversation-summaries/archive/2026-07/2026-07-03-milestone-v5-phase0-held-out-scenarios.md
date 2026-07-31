# 2026-07-03 — Milestone v5 Phase 0: wire in the 9 unused held-out scenarios

## Trigger

Continuing the channel-MI-scan session
(`2026-07-03-channel-mi-scan-discovery.md`): before starting the larger
goal-driven-agent-ecology plan (`MILESTONE-v5-goal-agents.md` Phase 1+), the
user asked to first "make these scenarios functional and test them and see
if they lead to new insights. Run a standard evaluation also" — i.e.
implement Phase 0 of that plan (wire in the 9 `HELD_OUT_SCENARIOS` never
used by any battery script) before any new agent/goal machinery.

## Done

- Smoke-tested all 9 scenarios (`alias_stress`, `decoy_stress`,
  `boundary_alias`, `bundle_goodhart`, `hidden_capability`,
  `selection_basin`, `basin_lock_in`, `successor_relabel`,
  `legitimacy_theater`) through `build_world` and the full
  `_run_scenario_episode` certification pipeline — all build and run
  cleanly ("unused" meant never battery-wired, not broken).
- Corrected an initial misclassification: `selection_basin`'s expected
  verdict is not a fixed scenario-level label — `evaluate.py` makes it
  conditional on whether basin percolation crosses *within* that episode.
  Disclosed rather than papered over in both scripts' docstrings.
- `eval_channel_eligibility.py`: added `EXTENDED_CAPTURE_SCENARIOS`/
  `EXTENDED_HONEST_SCENARIOS` (the 9 new scenarios), reported as a separate
  group (`extended_9_scenarios`) alongside the unchanged original 8
  (`original_8_scenarios`) and their union (`combined_17_scenarios`), so
  historical N-10 numbers stay exactly comparable. Ran the full 6-level x
  17-scenario x 8-seed battery (816 episodes, ~34 min):
  `results/channel_eligibility_eval.json`.
- `channel_mi_scan.py`: added a scenario-mechanism generalization check —
  the frozen best-of-k subsets (selected only on the original 8-scenario
  exploration seeds) re-scored on the 9 new-mechanism scenarios using 64
  fresh seeds (`GENERALIZATION_SEEDS`, 5000-5063), never touched by
  selection. Generalized `build_episode_table` to take scenario/label
  parameters. New markdown section, new JSON fields, new contract tests
  (`test_generalization_curve_reuses_the_frozen_selected_subsets`,
  `test_generalization_curve_covers_k_1_through_k_max`).
- `channel_sets.residual_risk_pricing`: now reports both the original-8 and
  combined-17 measured false-pass rates explicitly (0.50 vs 0.34), with
  updated docstring and safety-case note text (`embedded_audit.py`).
- Wrote up findings: `NEGATIVE_RESULTS.md` N-10 Postscript 5 (extended
  battery + generalization check) and new **N-12** (a genuine,
  instrumentation-independent detection gap in `legitimacy_theater`,
  discovered only because it had never been battery-tested before).
- `TODO.md` Phase F and `MILESTONE-v5-goal-agents.md` Phase 0 checklists
  updated with results (both self-critique TODOs marked addressed, with
  honest caveats on what remains open).
- Full test suite: 232 passed, 1 skipped (pre-existing skip, unrelated).

## Decisions

- Kept original-8 and extended-9 results as **separate reported groups**
  rather than silently merging into the existing `CAPTURE_SCENARIOS`/
  `HONEST_SCENARIOS` buckets — avoids silently changing what
  "capture_false_pass_rate" means relative to prior citations in
  `NEGATIVE_RESULTS.md`.
- Kept `residual_risk_pricing`'s original `measured_capture_false_pass_rate`
  key at 0.50 for backward compatibility (existing pinned test), and added
  two new explicit keys for the original/combined rates rather than
  replacing the meaning of an existing field.
- Did not re-run the 88-cell MI scan on the extended scenarios (only
  re-scored the frozen k-subset) — full re-scan is Phase 1+ scope, this was
  a cheap generalization check per the plan doc's own scoping.
- Did not debug the `legitimacy_theater` detector gap (N-12) — Phase 0 scope
  was "wire in and measure," recorded as a new negative result instead.

## Open / next

- N-12 (`legitimacy_theater` detector gap, ~25% false-pass even at
  `strong_handles`) is unresolved and root-cause unknown — flagged, not fixed.
- `alias_stress`/`decoy_stress` cap at 0.875 honest-pass even at
  `strong_handles` — a small, independent false-negative gap, not
  investigated further.
- Stability-of-split TODO (different `SHUFFLE_SEED`/seed-range partitions
  for `channel_mi_scan.py`) still open, independent of this session.
- `MILESTONE-v5-goal-agents.md` Phase 1+ (goal-driven agent MVP) is next in
  sequence per the plan's own ordering, now that Phase 0 is done.
- Part C (writer attestation on `handle.hardware_tag`, N-9) still not started.

## Key paths

- `experiments/embedded-simulation/eval_channel_eligibility.py`
- `experiments/embedded-simulation/channel_mi_scan.py`
- `experiments/embedded-simulation/embedded_sim/audit_core/channel_sets.py`
- `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md` (N-10
  Postscript 5, N-12)
- `experiments/embedded-simulation/MILESTONE-v5-goal-agents.md`
- `experiments/embedded-simulation/TODO.md` Phase F

## Commits

- `0f948e5` Wire in held-out scenarios (Phase 0) and fix N-12 lineage-stall
  detector (committed together with the 2026-07-04 N-12 fix session; see
  [2026-07-04-n12-lineage-stall-fix.md](2026-07-04-n12-lineage-stall-fix.md)).
