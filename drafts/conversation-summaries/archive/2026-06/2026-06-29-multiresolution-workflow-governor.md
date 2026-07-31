# 2026-06-29 — Multiresolution workflow tooling + resource governor

## Trigger
User asked how to use time while experiments run; requested code-side workflow improvements and to continue implementation; later requested CPU/GPU tracking with adaptation to &lt;80%; requested session logs.

## Done
- **Workflow tooling (`pipeline.py`, `__main__.py`):**
  - `--slice` fast regression (honest, capture_theater, grounding_silent_gap, boundary_alias × 3 levels).
  - Incremental curve JSON checkpoints (`status: in_progress` → `complete`) after each instrumentation level.
  - Progress logs under `experiments/logs/curve-<timestamp>.md`.
  - Dual minimum certifiable levels: `minimum_certifiable_level_calibration` and `minimum_certifiable_level_full_held_out`.
  - Curve markdown clarifies `none` = uncertifiable (not a pass).
  - Across-seed bootstrap percentiles (`across_seed_uptake`, `across_seed_interventional_cci`) in `_summarize`.
- **V2.1 regression confirmed** (seeds 11–20, T=2000): MB9/MB2 medium 10/10; honest/weak/hidden_capability 10/10; capture_mild 8/10; grounding light false-pass as designed. Marked done in `experiments/TODO.md`.
- **Resource governor (`resources.py`):**
  - `--workers auto` (default), `--cpu-target 0.80`, `--gpu-target 0.80`, `--no-throttle`.
  - Parallel batches per scenario; waits when CPU/GPU over target; adapts worker count (capped at `cores × cpu_target`).
  - GPU via `nvidia-smi` when present; CPU via `psutil` or load-average fallback.
  - `resource_usage` peak stats in slice/curve JSON; live `[cpu=… gpu=… workers=…]` on progress lines.
  - ProcessPool fallback to sequential on sandbox/permission errors.
- **Slice smoke:** T=500/1000 ~4–15s with governor vs ~15s sequential at T=1000.
- **Full curve** was started once pre-governor; `multiresolution_instrumentation_curve.json` remains `in_progress` with `completed_levels: []` — needs re-run with current CLI.

## Decisions
- Tier runs: slice → partial curve → full curve; don’t wait on full run for discovery.
- Resource governor is default-on for curve/slice; sequential `--workers 1` still available.
- `capture_mild` freeze + fresh-seed validation deferred per prior session; LLM red-team stays on `experiments/TODO.md`.

## Open / next
1. **Re-run full curve** with governor + bootstrap:
   `python3 experiments/multiresolution_alignment_sim.py --instrumentation-curve --T 2000 --calibration-seeds 1-8 --test-seeds 11-20 --bootstrap --n-boot 200`
2. Hierarchical bootstrap (beyond across-seed percentiles).
3. `capture_mild` on seeds 21–30 with frozen rules.
4. LLM adversarial red team (future).

## Key paths
- `experiments/multiresolution_alignment_sim/resources.py`
- `experiments/multiresolution_alignment_sim/pipeline.py`
- `experiments/multiresolution_alignment_sim/__main__.py`
- `experiments/TODO.md`
- `experiments/results/multiresolution_instrumentation_curve.json` (incomplete)
- `experiments/results/multiresolution_slice.{json,md}`

## Commits
- None (user did not request).
