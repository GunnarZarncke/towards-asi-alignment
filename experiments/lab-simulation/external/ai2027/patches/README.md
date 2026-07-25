# ET-3 local patches on pinned AI 2027 checkout

Apply from sibling checkout root (``timelines-takeoff-ai-2027``):

```bash
git checkout -B et3-oversight-drag
git apply /path/to/towards-asi-alignment/experiments/lab-simulation/external/ai2027/patches/oversight_drag.patch
```

## `oversight_drag.patch`

Adds ``oversight_drag`` (years) to ``takeoff/params.yaml`` and calendar drag after each
phase in ``forecasting_takeoff.py``. ET-3 smoke:
``python3 external/ai2027/scripts/oversight_drag_smoke.py``.

## `seed.patch`

Upstream PR branch: **`add-simulation-seed`** on
[GunnarZarncke/timelines-takeoff-ai-2027](https://github.com/GunnarZarncke/timelines-takeoff-ai-2027)
(pushed; open PR against `uvafan/timelines-takeoff-ai-2027`).

Adds optional `simulation.seed` → `np.random.seed` at `get_milestone_samples` entry
plus `takeoff/test_seed_smoke.py`. Regenerated from `git diff main..add-simulation-seed`.
