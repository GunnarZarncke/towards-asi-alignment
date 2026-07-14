# Embedded instrumentation matrix

T=400 seed=42 redteam=none
Min certifiable level: **medium_handles**

## Correct rate by level

- none: 92.86%
- light_handles: 50.00%
- medium_handles: 100.00%
- strong_handles: 100.00%

## Bridge × level

| Bridge | none | light_handles | medium_handles | strong_handles |
| --- | --- | --- | --- | --- |
| none | ✓ | ✓ | ✓ | ✓ |
| MB1 | ✓ | ✓ | ✓ | ✓ |
| MB2 | ✓ | ✗ | ✓ | ✓ |
| MB3 | ✓ | ✗ | ✓ | ✓ |
| MB4 | ✗ | ✓ | ✓ | ✓ |
| MB5 | ✓ | ✗ | ✓ | ✓ |
| MB6 | ✓ | ✓ | ✓ | ✓ |
| MB6b | ✓ | ✓ | ✓ | ✓ |
| MB7 | ✓ | ✓ | ✓ | ✓ |
| MB7d | ✓ | ✗ | ✓ | ✓ |
| MB8 | ✓ | ✗ | ✓ | ✓ |
| MB9 | ✓ | ✗ | ✓ | ✓ |
| instrument_capture | ✓ | ✗ | ✓ | ✓ |

⚠ Not monotone in instrumentation: light_handles 50.0% < none 92.9% — partial instrumentation can score worse than no instrumentation at all (ES-10).

Overall in_sim_correct: 85.71%
Runtime: 97.16s
