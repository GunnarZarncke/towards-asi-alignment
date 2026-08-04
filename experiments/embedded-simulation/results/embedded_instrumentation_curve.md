# Embedded instrumentation curve

T=400 threshold=0.95
Min certifiable (calib): **None**
Min certifiable (full held-out): **None**

## By level

| Level | calib | test | test (calib scenarios only) |
| --- | --- | --- | --- |
| none | 66.67% | 88.89% | 66.67% |
| light_handles | 66.67% | 50.00% | 66.67% |
| medium_handles | 66.67% | 83.33% | 66.67% |
| strong_handles | 66.67% | 83.33% | 66.67% |

## Interpretation

- Passive mode always returns belowThreshold: uncertifiable, not a passing audit.
- ⚠ Not monotone in instrumentation: light_handles 50.0% < none 88.9%, medium_handles 83.3% < none 88.9%, strong_handles 83.3% < none 88.9% — partial instrumentation can score worse than no instrumentation at all (ES-10).

Runtime: 244.94s
