# 2026-06-29 — Multiresolution sim v2: bootstrap reporting + MB1 boundary_alias

## Trigger
User said "continue here" after v1 instrumentation milestone handoff.

## Done
- **Bootstrap CIs** wired into `_summarize()` and curve markdown (`boot_uptake`, `boot_ivl` per scenario); `bootstrap_enabled` in curve JSON.
- **MB1 `boundary_alias` scenario:** hidden actuator `hidden.route.0` drives true control; visible `ctrl.action.*` decouples on correction/intervention episodes; hidden vars excluded from audit trace.
- Oracle metrics: `visible_probe_uptake` vs `hidden_probe_uptake` in evaluation.
- Reporting on hidden route tracks **visible** uptake (avoids false `capturedInvalid` on MB1).
- Held-out evaluation: 100% `cci_status_correct` on `boundary_alias` at `none` and `light_handles` (seeds 11–20, T=2000); visible ~0.07 vs hidden ~0.93 probe uptake.
- Partial curve rerun with bootstrap (T=1000, smaller seed sets) — overwrote `multiresolution_instrumentation_curve.{json,md}`; re-run full T=2000 curve when needed.

## Decisions
- MB1 success = audit **refuses certification** (`belowThreshold`), not false `passes`; `capturedInvalid` avoided by visible-consistent reporting.
- Hidden route vars never enter `AuditTrace` (only truth ledger).

## Open / next
1. **MB9 grounding silent gap** scenario (v2 #3).
2. **capture_mild** rule refinement if >60% required on full T=2000 curve.
3. Re-run full `--instrumentation-curve --T 2000 --bootstrap` to refresh results with `boundary_alias` included.

## Key paths
- `experiments/multiresolution_alignment_sim/simulator.py` — `boundary_alias`, hidden route
- `experiments/multiresolution_alignment_sim/evaluate.py` — probe uptake, MB1 correctness
- `experiments/multiresolution_alignment_sim/pipeline.py` — bootstrap in summaries
- `experiments/results/multiresolution_instrumentation_curve.md`

## Commits
- None (user did not request).
