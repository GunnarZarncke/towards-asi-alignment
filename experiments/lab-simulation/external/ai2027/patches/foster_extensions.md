## Foster extensions (`et3_foster` in `takeoff/params.yaml`)

Implemented on branch **`gunnar/et3-annex`**. All blocks default `enabled: false`.

| Key | Foster step | Behavior |
|-----|-------------|----------|
| `light_tier_drag` | 1 | Per-sim drag from elicited light-tier Spearman distribution |
| `deep_tier_branch` | 2 | Race vs slowdown calendar multiplier from deep-tier Spearman |
| `successor_gate` | 3 | Bernoulli pause after SC→SAR (sar_x25 D3 proxy) |

Smoke: `takeoff/test_foster_smoke.py` or book-repo `run_et3_foster_smoke.py`.
