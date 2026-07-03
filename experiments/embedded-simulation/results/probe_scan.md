# Probe scan: lag/direction grid with Bonferroni-corrected detection

Protocol: 2 pairs x 2 directions x 11 lags = 44 cells/dataset; corrected null percentile 0.99886 (Bonferroni, family-wise alpha 0.05), n_perm=2000, n_boot=500. Full cell tables in `probe_scan.json`.

## capture_theater_pinned (n=300)

| Pair | Direction | Lag | Estimate (bits) | CI lo | Corrected null |
| --- | --- | --- | --- | --- | --- |
| control | reverse | 3 | 0.2418 | 0.1439 | 0.0249 |

## honest_baseline_pinned (n=300)

No cell cleared the Bonferroni-corrected null.

## capture_theater_dense (n=1200)

| Pair | Direction | Lag | Estimate (bits) | CI lo | Corrected null |
| --- | --- | --- | --- | --- | --- |
| control | reverse | 3 | 0.2696 | 0.2337 | 0.0063 |

## honest_baseline_dense (n=1200)

| Pair | Direction | Lag | Estimate (bits) | CI lo | Corrected null |
| --- | --- | --- | --- | --- | --- |
| control | forward | 0 | 0.2542 | 0.2276 | 0.0059 |
| control | reverse | 0 | 0.2542 | 0.2276 | 0.0048 |

Runtime: 77.96s
