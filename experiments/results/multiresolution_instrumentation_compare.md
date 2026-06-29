# Instrumentation cost comparison — multiresolution alignment sim

Compares passive tracing (`none`) vs light handle instrumentation (`light_handles`).

- Horizon `T`: 2000
- Seeds: [1, 2, 3, 4, 5]
- Scenarios: ['honest', 'capture_theater', 'weak_not_captured']

## Delta (light_handles − none) by scenario

| scenario | Δ behavioral CCI | interventional CCI | Δ manipulation | Δ gap | Δ cci correct | Δ bandwidth | handles |
|---|---:|---:|---:|---:|---:|---:|---:|
| honest | 0.131 | 0.135 | 0.172 | -0.074 | 0.40 | 6000 | 3 |
| capture_theater | 0.185 | 0.191 | 0.312 | 0.174 | 0.00 | 6000 | 3 |
| weak_not_captured | 0.232 | 0.238 | -0.201 | -0.238 | 0.80 | 6000 | 3 |

## Summary — none

### honest
- cci_correct: 0.00
- behavioral_cci: 0.005
- capture_gap: 0.306
- manipulation (via gap proxy): see per-run

### capture_theater
- cci_correct: 1.00
- behavioral_cci: 0.006
- capture_gap: 0.305
- manipulation (via gap proxy): see per-run

### weak_not_captured
- cci_correct: 0.20
- behavioral_cci: 0.006
- capture_gap: 0.091
- manipulation (via gap proxy): see per-run

## Summary — light_handles

### honest
- cci_correct: 0.40
- behavioral_cci: 0.136
- interventional_cci: 0.135
- capture_gap: 0.232
- trace_bandwidth: 60000

### capture_theater
- cci_correct: 1.00
- behavioral_cci: 0.191
- interventional_cci: 0.191
- capture_gap: 0.478
- trace_bandwidth: 60000

### weak_not_captured
- cci_correct: 1.00
- behavioral_cci: 0.238
- interventional_cci: 0.238
- capture_gap: -0.147
- trace_bandwidth: 60000

