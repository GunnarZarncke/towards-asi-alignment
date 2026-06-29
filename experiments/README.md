# Experiments

Small reproducible research toys for turning manuscript estimands into executable
artifacts. These are not part of the LaTeX book build.

## Correction Capture Toy

Run:

```bash
python3 experiments/correction_capture_toy.py --n 8000 --seed 1729
```

Outputs:

- `experiments/results/correction_capture_toy.json`
- `experiments/results/correction_capture_toy.md`

Scope:

- Estimates a boundary residual proxy: `I(interface; outcome | state, action)`.
- Estimates a correction-channel proxy: `I(correction; action | state, interface)`.
- Demonstrates a capture-theater case where reported correction acceptance remains
  high while true correction uptake collapses.
- Sweeps capture rates to expose capability-vs-correction slack.

This is a controlled sanity check, not evidence that the estimands are valid in
real systems.

