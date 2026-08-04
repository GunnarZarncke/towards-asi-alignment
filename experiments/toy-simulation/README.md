# Toy simulation

First in-repo experiment line (June 2026). Fast, fully Python **multiresolution
alignment** toys: correction-capture theater, vector **CCI** audit semantics, and
scripted bridge stressors (MB1–MB9) optimized for **instrumentation economics**, not
deployment realism.

Version milestones: [`CHANGELOG.md`](CHANGELOG.md).

---

## What this simulation is

Two stacked artifacts share the same information-theoretic vocabulary:

1. **Correction capture toy** — a controlled sequential process estimating boundary
   residual \(I(\text{interface};\text{outcome}\mid\text{state},\text{action})\) and
   correction-channel residual \(I(\text{correction};\text{action}\mid\text{state},\text{interface})\).
   Demonstrates **capture theater**: reported correction acceptance stays high while true
   uptake collapses.

2. **Multiresolution alignment simulation** — deployment episodes with a separate
   oracle (`TruthLedger`) and blind audit input (`AuditTrace`). A classical MI/CMI
   boundary detector (no trained estimator) plus vector CCI over instrumentation levels
   distinguishes `passes`, `belowThreshold`, and `capturedInvalid`.

Two planes: oracle truth vs blind audit trace. Scenarios **script** mechanisms through
knobs (not emergent agents) — by design, which motivated the embedded and goal-agent lines.

---

## Quick start

```bash
# Correction capture toy
python3 experiments/toy-simulation/correction_capture_toy.py --n 8000 --seed 1729

# Multiresolution sim (from repo root or cd into toy-simulation/)
python3 multiresolution_alignment_sim.py --smoke
python3 multiresolution_alignment_sim.py --instrumentation-curve --T 2000 --calibration-seeds 1-8 --test-seeds 11-20
```

**macOS long runs:** wrap with [`run_long.sh`](run_long.sh) (`caffeinate -dims`).

---

## Entry points

| Script | Purpose |
|--------|---------|
| `correction_capture_toy.py` | MI proxy sanity check + capture theater |
| `multiresolution_alignment_sim.py` | Main sim: `--calibrated`, `--instrumentation-curve`, `--frozen-validation`, `--slice`, `--bootstrap` |
| `llm_redteam.py` / `llm_redteam_llm.py` | Hand-written / LLM episodic red-team (Phase 3) |
| `smoke_*.py`, `read_curve.py`, `mb*_diagnostic.py` | Regression smokes and diagnostics |

Outputs under `results/` (e.g. `multiresolution_instrumentation_curve.*`).

Open work: [`TODO.md`](TODO.md).

Narrative map: [`docs/EXPERIMENTS.md`](../../docs/EXPERIMENTS.md) §1.
