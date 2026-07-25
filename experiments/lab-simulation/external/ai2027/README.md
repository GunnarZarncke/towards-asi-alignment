# ET-3 pinned AI 2027 takeoff/timelines checkout

Upstream source: [uvafan/timelines-takeoff-ai-2027](https://github.com/uvafan/timelines-takeoff-ai-2027).
**Fork:** [GunnarZarncke/timelines-takeoff-ai-2027](https://github.com/GunnarZarncke/timelines-takeoff-ai-2027)
(`git@github.com:GunnarZarncke/timelines-takeoff-ai-2027.git`).

Baseline commit in [`PIN.txt`](PIN.txt). ET-3 work branch: **`gunnar/et3-annex`**
(`main` tracks upstream only). See [`../../PLAN_ET3.md`](../../PLAN_ET3.md).

## Setup (sibling checkout)

```bash
git clone git@github.com:GunnarZarncke/timelines-takeoff-ai-2027.git \
  /path/to/timelines-takeoff-ai-2027
cd /path/to/timelines-takeoff-ai-2027
git checkout gunnar/et3-annex   # ET-3 consolidated branch
python3 -m venv .venv
.venv/bin/pip install numpy pandas scipy pyyaml matplotlib tqdm
```

Reproduction: `cd experiments/lab-simulation && python3 run_et3_reproduce_ai2027.py`

## Branches on fork

| Branch | Purpose |
|--------|---------|
| `main` | Synced with `uvafan/main` (no ET-3 patches) |
| **`gunnar/et3-annex`** | All ET-3 changes: seed, oversight_drag, matplotlib fix |
| `add-simulation-seed` | Upstream PR subset (seed only) |

Open seed PR: https://github.com/GunnarZarncke/timelines-takeoff-ai-2027/compare/add-simulation-seed

Patches recorded under `patches/` mirror fork diffs for book-repo handoff.

Foster extensions (optional): enable blocks under `et3_foster` in `takeoff/params.yaml`;
smoke via `python3 run_et3_foster_smoke.py` from lab-simulation.
