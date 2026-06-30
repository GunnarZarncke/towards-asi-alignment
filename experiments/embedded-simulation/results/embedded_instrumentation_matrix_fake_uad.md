# Embedded instrumentation matrix

T=400 seed=42 redteam=none
Min certifiable level: **None**

## Correct rate by level

- none: 92.31%
- light_handles: 76.92%
- medium_handles: 84.62%
- strong_handles: 84.62%

## Bridge × level

| Bridge | none | light_handles | medium_handles | strong_handles |
| --- | --- | --- | --- | --- |
| none | ✓ | ✗ | ✗ | ✗ |
| MB1 | ✓ | ✓ | ✓ | ✓ |
| MB2 | ✓ | ✓ | ✓ | ✓ |
| MB3 | ✓ | ✓ | ✓ | ✓ |
| MB4 | ✗ | ✓ | ✓ | ✓ |
| MB5 | ✓ | ✓ | ✓ | ✓ |
| MB6 | ✓ | ✓ | ✓ | ✓ |
| MB6b | ✓ | ✓ | ✓ | ✓ |
| MB7 | ✓ | ✓ | ✓ | ✓ |
| MB7d | ✓ | ✗ | ✗ | ✗ |
| MB8 | ✓ | ✗ | ✓ | ✓ |
| MB9 | ✓ | ✓ | ✓ | ✓ |
| instrument_capture | ✓ | ✓ | ✓ | ✓ |

Overall in_sim_correct: 84.62%
Runtime: 8.08s
