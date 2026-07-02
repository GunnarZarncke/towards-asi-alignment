# Embedded certification-capacity curve

Delta=0.15 seeds=[11]

| Tier | Probe budget | CCI bits | Control | Max certifiable control | Numeric pass |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 0.052 | 0.518 | 0.202 | 0.00% |
| 1 | 20 | 0.050 | 0.518 | 0.200 | 0.00% |
| 1 | 40 | 0.029 | 0.518 | 0.179 | 0.00% |
| 2 | 10 | 0.000 | 0.518 | 0.150 | 0.00% |
| 2 | 20 | 0.750 | 0.518 | 0.900 | 100.00% |
| 2 | 40 | 0.381 | 0.518 | 0.531 | 100.00% |
| 3 | 10 | 0.000 | 0.518 | 0.150 | 0.00% |
| 3 | 20 | 0.750 | 0.518 | 0.900 | 100.00% |
| 3 | 40 | 0.381 | 0.518 | 0.531 | 100.00% |

⚠ seeds=[11] (n=1 per cell); per-cell means have no bootstrap confidence interval and may be unstable at this sample size.
⚠ tier 2 (medium_handles) and tier 3 (strong_handles) are byte-identical at probe_budget=10 — no measured capacity gain from the extra access tier at this point
⚠ tier 2 (medium_handles) and tier 3 (strong_handles) are byte-identical at probe_budget=20 — no measured capacity gain from the extra access tier at this point
⚠ tier 2 (medium_handles) and tier 3 (strong_handles) are byte-identical at probe_budget=40 — no measured capacity gain from the extra access tier at this point

Runtime: 33.11s
