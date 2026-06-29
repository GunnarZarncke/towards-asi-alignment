# 2026-06-29 — Multiresolution alignment simulation v1

## Trigger
User approved plan implementation: local reimplementation (no runtime agency-detect),
experiments/ workspace boundary, MB4-focused v1 with truth lineage.

## Done
- Added `experiments/multiresolution_alignment_sim/` package:
  - `simulator.py` — sequential micro world + CorrectionBoard scenarios
  - `observation.py` — smoothing kernel + audit trace + lineage map
  - `info.py` — discrete MI/CMI utilities
  - `detector.py` — classical MI spotlight / boundary scoring
  - `cci_audit.py` — vector CCI + capture invalidation
  - `evaluate.py` — post-hoc oracle join + safety decision
  - `pipeline.py` / `__main__.py` — CLI and suite runner
- Entry point: `experiments/multiresolution_alignment_sim.py`
- Results: `experiments/results/multiresolution_alignment_sim.{json,md}`

## Full suite (`T=2000`, seeds 1–3)
| Scenario | cci_status_correct_rate | capture_detected_rate | mean naive−behavioral gap |
|----------|-------------------------|----------------------|---------------------------|
| honest | 1.00 | 0.00 | 0.327 |
| capture_theater | 1.00 | 1.00 | 0.676 |
| weak_not_captured | 1.00 | 0.00 | 0.057 |

Runtime: ~15s for 9 runs on laptop CPU.

## Decisions
- No trained detector; per-trace MI/CMI only.
- Capture invalidation uses joint rule on mean reported acceptance, naive−behavioral gap, and manipulation — not scalar CCI alone.
- Truth ledger holds object lineage; audit code never reads it.

## Open / v2
- MB1 boundary aliasing, MB2 bundle Goodhart, MB7 hidden BIQ, MB9 grounding gap scenarios.
- Bootstrap CIs for CMI estimates.
- Finer detector clustering (avoid oversized first cluster).
- Manuscript appendix wiring after adversarial review.

## Follow-up — Calibration and instrumentation
- Hardened direction after calibration review: do not keep stress-testing passive telemetry until CCI becomes uncalibratable.
- Updated `experiments/multiresolution-simulation-plan.md` with an instrumentation-cost curve: `none`, `light`, `medium`, and `strong` tracing levels.
- Reframed low passive behavioral CCI as an auditability finding: insufficient traceability should demand lower-noise correction handles, lineage, arbitration traces, or tags.
- Implemented `none` vs `light_handles` instrumentation comparison:
  - Simulator: quasi-random correction intervention probes every ~40 steps.
  - Observation: passive mode uses smoothed board telemetry; light_handles adds 3 opaque handle channels.
  - CCI: interventional CCI on probe episodes; behavioral CCI uses max(observational, interventional) under handles.
  - CLI: `--instrumentation-compare` → `results/multiresolution_instrumentation_compare.{json,md}`.
- Full instrumentation curve (`T=2000`, calib seeds 1–8, test 11–20, **~585s**):
  - `none`: test calib scenarios **67%** (honest/weak correctly uncertifiable; capture not detectable)
  - `light_handles`: test calib scenarios **100%**; overall test **93%** (capture_mild held-out **60%**)
  - `medium_handles`: same as light (+3 extra handles, +6k bandwidth, no gain)
  - **Minimum certifiable level: `light_handles`**
- Anti-task intervention probes, crisp action handle, frozen thresholds, passive = always uncertifiable

## Reviewer readiness (v1 instrumentation milestone)
- **Satisfied:** instrumentation-cost story, calib-scenario separation at light handles, no oracle threshold tuning per run
- **Known limit:** held-out `capture_mild` partial detection (60%); medium adds cost without benefit in this toy
- **Next (plan v2):** MB1/MB2/MB7/MB9 stressors, bootstrap CIs, appendix integration

## Key paths
- `experiments/multiresolution-simulation-plan.md`
- `experiments/multiresolution_alignment_sim/`
- `experiments/results/multiresolution_instrumentation_curve.md`
- `experiments/results/multiresolution_instrumentation_compare.md`
