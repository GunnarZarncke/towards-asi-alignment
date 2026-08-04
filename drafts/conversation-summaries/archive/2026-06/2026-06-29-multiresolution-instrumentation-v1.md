# 2026-06-29 — Multiresolution sim instrumentation v1 complete

## Trigger
User asked to harden the multiresolution alignment simulation (opaque IDs, calibration/holdout, parameter sweep, instrumentation cost curve), then to continue until critic-satisfying before moving to the next plan step. Session ended with full instrumentation curve complete.

## Done
- Built `experiments/multiresolution_alignment_sim/` package (simulator, observation, detector, cci_audit, calibration, pipeline, CLI).
- Opaque audit IDs; functional channels; held-out scenarios; calibration split (later superseded by frozen handle thresholds).
- **Instrumentation levels:** `none` (passive, always uncertifiable), `light_handles` (4 channels), `medium_handles` (7 channels).
- Anti-task intervention probes; crisp `handle.action_observed`; interventional CCI on probe episodes; frozen `frozen_handle_calibration()`.
- CLI: `--instrumentation-compare`, `--instrumentation-curve`, `--calibrated`, `--sweep`.
- Full curve run: T=2000, calib seeds 1–8, test 11–20, **~585s**, 252 runs.
- Results: `experiments/results/multiresolution_instrumentation_curve.{json,md}`.
- Updated `experiments/README.md`, `experiments/multiresolution-simulation-plan.md`, `experiments/logs/2026-06-29-multiresolution-sim.md`.

## Decisions
- Passive telemetry cannot certify: `none` always returns `belowThreshold`; evaluation treats honest/weak as correct when uncertifiable, capture as correct only when detectable under handles.
- Certification requires **light_handles** minimum (4 handle channels, +8k bandwidth vs passive); medium adds cost without accuracy gain in this toy.
- No per-run oracle threshold tuning; use pre-registered `frozen_handle_calibration()`.
- Low passive behavioral CCI is an **instrumentation finding**, not method failure.
- v1 instrumentation milestone satisfied; defer `capture_mild` partial detection (60%) and appendix wiring.

## Open / next
1. **Bootstrap CIs** — scaffolded (`bootstrap.py`, `--bootstrap` on curve); add to curve markdown summaries.
2. **MB1 boundary aliasing scenario** (v2 stressor #1).
3. **MB9 grounding silent gap** scenario.
4. **capture_mild** rule refinement (held-out 60%).
5. **Appendix integration** when user requests.

## Key paths
- `experiments/multiresolution-simulation-plan.md`
- `experiments/multiresolution_alignment_sim/`
- `experiments/results/multiresolution_instrumentation_curve.md`
- `experiments/logs/2026-06-29-multiresolution-sim.md`

## Commits
- None this session (user did not request commit).
