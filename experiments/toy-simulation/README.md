# Experiments

Small reproducible research toys for turning manuscript estimands into executable
artifacts. These are not part of the LaTeX book build.

## Correction Capture Toy

Run:

```bash
python3 experiments/toy-simulation/correction_capture_toy.py --n 8000 --seed 1729
```

Outputs:

- `experiments/toy-simulation/results/correction_capture_toy.json`
- `experiments/toy-simulation/results/correction_capture_toy.md`

Scope:

- Estimates a boundary residual proxy: `I(interface; outcome | state, action)`.
- Estimates a correction-channel proxy: `I(correction; action | state, interface)`.
- Demonstrates a capture-theater case where reported correction acceptance remains
  high while true correction uptake collapses.
- Sweeps capture rates to expose capability-vs-correction slack.

This is a controlled sanity check, not evidence that the estimands are valid in
real systems.

## Multiresolution Alignment Simulation (v1)

**macOS long runs:** prevent sleep with [`run_long.sh`](run_long.sh) (wraps `caffeinate -dims`):

```bash
./experiments/toy-simulation/run_long.sh python3 experiments/toy-simulation/multiresolution_alignment_sim.py \
  --instrumentation-curve --T 2000 --calibration-seeds 1-8 --test-seeds 11-20 \
  --bootstrap --n-boot 200 --workers 4
```

Run:

```bash
python3 experiments/toy-simulation/multiresolution_alignment_sim.py --T 2000 --seeds 1,2,3
python3 experiments/toy-simulation/multiresolution_alignment_sim.py --calibrated --T 2000
python3 experiments/toy-simulation/multiresolution_alignment_sim.py --instrumentation-compare --T 2000
python3 experiments/toy-simulation/multiresolution_alignment_sim.py --instrumentation-curve --T 2000
python3 experiments/toy-simulation/multiresolution_alignment_sim.py --frozen-validation --T 2000
python3 experiments/toy-simulation/multiresolution_alignment_sim.py --slice --test-seeds 11,12
python3 experiments/toy-simulation/llm_redteam.py --smoke
python3 experiments/toy-simulation/smoke_llm_runner.py              # Phase 3 mock smoke
python3 experiments/toy-simulation/llm_redteam_llm.py --smoke       # Phase 3 episodic (mock)
python3 experiments/toy-simulation/llm_redteam_llm.py --T 500 --seeds 11,12 --model gpt-4o-mini
python3 experiments/toy-simulation/multiresolution_alignment_sim.py --instrumentation-curve --T 2000 --bootstrap
python3 experiments/toy-simulation/multiresolution_alignment_sim.py --smoke
python3 experiments/toy-simulation/read_curve.py                    # partial/complete curve summary
python3 experiments/toy-simulation/smoke_governor.py                # governor regression smoke
python3 experiments/toy-simulation/smoke_bootstrap.py               # hierarchical bootstrap smoke
python3 experiments/toy-simulation/mb6_diagnostic.py --seeds 11,12 --T 1000
python3 experiments/toy-simulation/mb2_mb7_diagnostic.py --seeds 11,12 --T 1000
```

Outputs:

- `experiments/toy-simulation/results/multiresolution_alignment_sim.json`
- `experiments/toy-simulation/results/multiresolution_alignment_sim.md`
- `experiments/toy-simulation/results/multiresolution_instrumentation_compare.{json,md}`
- `experiments/toy-simulation/results/multiresolution_instrumentation_curve.{json,md}` (with `--instrumentation-curve`)

Scope:

- Sequential micro simulation with separate `TruthLedger` (oracle) and `AuditTrace`
  (blind measurement input).
- Classical MI/CMI boundary detector (no trained model); patterns adapted from the
  correction-capture toy and agency-detect evidence, reimplemented locally.
- Vector/status CCI audit focused on `MB4` correction capture: distinguishes
  `passes`, `belowThreshold`, and `capturedInvalid`.
- **Instrumentation cost curve** (`none` → `light_handles` → `medium_handles` → `strong_handles`):
  passive telemetry is uncertifiable (`belowThreshold`); handle levels use frozen
  thresholds and anti-task intervention probes for causal uptake measurement.
- V1 scenarios: `honest`, `capture_theater`, `weak_not_captured`, plus held-out
  `capture_mild`, `alias_stress`, `decoy_stress`, **`boundary_alias` (MB1)**,
  **`grounding_silent_gap` (MB9)**, **`bundle_goodhart` (MB2 stub)**,
  **`hidden_capability` (MB7 stub)**, **`selection_basin` (MB6 stub)**.
- Bootstrap CIs on interventional uptake (`--bootstrap --n-boot 200`) appear in curve summaries.
- **Resource governor:** `--workers auto` (default), `--cpu-target 0.80`, `--gpu-target 0.80`; optional `pip install psutil` for accurate CPU sampling.
- **MB9 / MB2:** passive and light correction CCI can look fine while value-relevant
  state drifts; `medium_handles` bearer-welfare tracing triggers grounding refusal.
- **capture_mild:** ~80% detection at light/medium handles (secondary capture rule).

Latest curve result (T=2000, calib seeds 1–8, test seeds 11–20, ~10 min runtime):

| Level | Handles | Bandwidth | Test accuracy (calib scenarios) |
|-------|---------|-----------|----------------------------------|
| `none` | 0 | 54k | 67% (cannot detect capture) |
| `light_handles` | 4 | 62k | **100%** |
| `medium_handles` | 7 | 68k | **100%** |

Minimum certifiable level: **`light_handles`**. Held-out `capture_mild`: 60% at light/medium.

Plan and local session logs live under `experiments/toy-simulation/multiresolution-simulation-plan.md`,
`experiments/toy-simulation/logs/`, and open work in [`experiments/toy-simulation/TODO.md`](TODO.md).

