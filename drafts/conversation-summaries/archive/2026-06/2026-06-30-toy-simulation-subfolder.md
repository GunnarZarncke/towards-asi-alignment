# 2026-06-30 — Toy simulation subfolder

## Trigger
User asked to move the existing experiment into a `toy-simulation` subfolder so more experiments can be added under `experiments/`.

## Done
- Moved the current experiment bundle under `experiments/toy-simulation/`:
  - multiresolution simulation package and CLI wrappers
  - LLM red-team harness and cost tracking
  - diagnostics, logs, results, local TODO, and simulation plan
- Added root `experiments/README.md` and `experiments/TODO.md` as lightweight indexes for future experiments.
- Updated current docs and command examples to use `experiments/toy-simulation/...`.
- Smoke-tested moved entry points:
  - `python3 experiments/toy-simulation/multiresolution_alignment_sim.py --smoke`
  - `python3 experiments/toy-simulation/mb5_mb6_diagnostic.py --T 80 --seeds 11 --out ...`

## Caveats
- Historical conversation logs still contain old `experiments/...` paths in some entries; these are archival and were not mass-edited.
- The main next experiment gap remains `instrument_capture` / handle-protection stress.

## Key paths
- `experiments/README.md`
- `experiments/TODO.md`
- `experiments/toy-simulation/README.md`
- `experiments/toy-simulation/TODO.md`

