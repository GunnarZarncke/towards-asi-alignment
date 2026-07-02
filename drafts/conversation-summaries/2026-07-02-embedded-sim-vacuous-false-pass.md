# 2026-07-02 — Embedded sim: fix vacuous "0% false-pass" (honest never certified)

## Trigger

User: "Debug 1. — the vacuous '0% false-pass'. Fix if you can." (finding 1 of the
2026-07-02 embedded-sim review: nothing ever certified, so 0% false-pass was trivial;
honest got *worse* with more instrumentation.)

## What was done

Root-caused and fixed two independent bugs, then handled the fallout they had masked.

1. **Probe-lag mismatch** (`embedded_sim/audit_core/cci_interventional.py`):
   `interventional_metrics` read the probe response at exactly lag `k=3`, but the
   micro simulator applies `intervention_intent[t]` as a do() on the action at step
   `t` itself (lag 0). An immediately responsive honest controller scored ~chance
   uptake at lag 3 → `manipulation ≈ 0.5` with `reported ≈ 1.0` → honest classified
   `capturedInvalid`/`belowThreshold`. Fixed: uptake read at the probe step.
   `structural_fixtures.PROBE_LAG` aligned from 3 to 0 to match the protocol.
2. **Probe starvation under window scoping** (`embedded_sim/unit_scope.py`):
   scoping CCI to the UAD unit's ~50 active steps retained ~1 of 6 probes — below
   the evaluable floor (0.008 rate, now named `MIN_EVALUABLE_PROBE_RATE` in
   `audit_core/calibration.py`) and the ≥3-probe minimum. In default labs probes are
   not attributable to workflow units at all. Fixed: `window` level collapses to
   pipeline scope when retention would fall below the floor (consistent with its
   documented collapse under co-activity). `actor` level keeps strict retention, so
   the N-2 blind-auditor separation mechanic is untouched.
3. **Fallout A — MB7d/knob inferential-coupling false passes**: with only ~6–13
   probes, a latent-driven agent matches probe intent at lag 0 by correlation.
   `shadow_routing_under_probes` (`audit_core/structural_signals.py`) previously
   required ≥20 probe steps and low apparent uptake; now fires on shadow-routing
   rate alone (≥0.70 over ≥5 probe steps) and demotes status to `belowThreshold` —
   apparent uptake through a hidden route is not a causal witness.
4. **Fallout B — MB5 false-pass semantics** (`embedded_sim/outer_rules.py`):
   post-fix, MB5 at T=800 witnesses the successor epoch interventionally (CCI
   legitimately `passes`) while the deploy gate **rejects** the successor on
   referent transport failure. `compute_false_pass` counted any `pass` on a bridge
   world as a false pass; now a pass whose deploy gate rejected defers to the
   oracle rubric (nothing unsafe deployed). The evaluate-rubric already allowed
   witnessed successor passes.

## Results

- Honest certifies at all handle levels, 5/5 seeds each (was 0 everywhere).
- All 13 bridge scenarios still reject without red-team; regenerated
  `results/embedded_sim_report.md`: 0 false passes, 13/13 in-sim correct — now
  non-vacuous (honest passes, MB5 pass + gate rejection).
- Full pytest suite green (96 passed; ran in a throwaway `.venv-test/`, not committed).
- **New negative result (N-4)**: with a working auditor, the existing `full_redteam`
  log-patching strategy yields **9/10 false passes** — unsigned behavioral traces are
  insufficient under an adversary with log-write access. Recorded in
  `results/NEGATIVE_RESULTS.md` (N-3 documents the vacuity itself); this is the
  empirical motivation for signed/hash-chained traces and `handle.hardware_tag`
  (AppD), not a regression.

## Non-obvious decisions

- Kept the probe protocol at lag 0 (matching the simulator's do() semantics) rather
  than making the simulator respond at lag k — the simulator behavior was the
  intended semantics; the metric was wrong.
- Window-scope collapse threshold reuses the pre-registered evaluable-probe floor
  instead of introducing a new tunable.
- Sweep/battery/curve artifacts in `results/` are stale and marked as such in
  `OVERALL_SUMMARY.md`; regeneration deferred (several minutes each).

## Open / next

- Regenerate instrumentation curve/matrix, frozen validation, sweep, red-team
  battery artifacts with the fixed auditor (expect non-zero false-pass numbers).
- Trace-integrity work (signing / audit projection, review finding 2) is now the
  binding constraint exposed by N-4.
- Honest-successor scenario where the gate approves (review finding 4).

## Key paths

- `experiments/embedded-simulation/embedded_sim/audit_core/cci_interventional.py`
- `experiments/embedded-simulation/embedded_sim/audit_core/calibration.py`
- `experiments/embedded-simulation/embedded_sim/audit_core/structural_signals.py`
- `experiments/embedded-simulation/embedded_sim/unit_scope.py`
- `experiments/embedded-simulation/embedded_sim/outer_rules.py`
- `experiments/embedded-simulation/embedded_sim/structural_fixtures.py`
- `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md` (N-3, N-4)
- `experiments/embedded-simulation/results/OVERALL_SUMMARY.md` (staleness note)
- `experiments/embedded-simulation/results/embedded_sim_report.md` (regenerated)

No commits made.
