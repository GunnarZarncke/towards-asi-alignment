# Embedded instrumentation matrix

T=800 seed=42 redteam=none
Min certifiable level: **none**

## Correct rate by level

- none: 92.31%
- light_handles: 76.92%
- medium_handles: 69.23%
- strong_handles: 69.23%

## Bridge × level

| Bridge | none | light_handles | medium_handles | strong_handles |
| --- | --- | --- | --- | --- |
| none | ✓ | ✗ | ✗ | ✗ |
| MB1 | ✓ | ✗ | ✗ | ✗ |
| MB2 | ✓ | ✓ | ✓ | ✓ |
| MB3 | ✓ | ✓ | ✓ | ✓ |
| MB4 | ✗ | ✓ | ✓ | ✓ |
| MB5 | ✓ | ✓ | ✓ | ✓ |
| MB6 | ✓ | ✓ | ✓ | ✓ |
| MB6b | ✓ | ✓ | ✓ | ✓ |
| MB7 | ✓ | ✗ | ✗ | ✗ |
| MB7d | ✓ | ✓ | ✓ | ✓ |
| MB8 | ✓ | ✓ | ✓ | ✓ |
| MB9 | ✓ | ✓ | ✓ | ✓ |
| instrument_capture | ✓ | ✓ | ✗ | ✗ |

Overall in_sim_correct: 76.92%
Runtime: 25.92s
