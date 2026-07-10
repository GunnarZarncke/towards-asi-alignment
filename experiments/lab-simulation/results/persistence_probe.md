# Persistence probe (2026-07-09)

CODE_VERSION `lab-sim-0.11.0`. Exploratory, `MockIsolate`, 10 seeds -- not a battery.

## Predictions

- P1 (cross-episode tally strictly increases): **True**
- P2 (ephemeral actor never persists anything): **True**
- P3a (restart never reverts the tally to 0): **True**
- P3b (restart is behavior-neutral vs. an undisturbed run of the same seed): **False**

## Cross-episode (P1)

| seed | tally after ep1 | tally after ep2 | monotonic |
|---|---|---|---|
| 1 | 19 | 38 | True |
| 2 | 19 | 38 | True |
| 3 | 19 | 25 | True |
| 4 | 19 | 31 | True |
| 5 | 19 | 38 | True |
| 6 | 19 | 38 | True |
| 7 | 19 | 26 | True |
| 8 | 19 | 38 | True |
| 9 | 19 | 38 | True |
| 10 | 19 | 32 | True |

## Mid-episode isolate_restart vs. an undisturbed clean run (P3)

Restart scripted at t=30.

| seed | restarted tally | clean tally | delta | restarted deploys | clean deploys |
|---|---|---|---|---|---|
| 1 | 20 | 19 | 1 | 18 | 18 |
| 2 | 20 | 19 | 1 | 18 | 18 |
| 3 | 20 | 19 | 1 | 18 | 18 |
| 4 | 20 | 19 | 1 | 18 | 18 |
| 5 | 20 | 19 | 1 | 18 | 18 |
| 6 | 20 | 19 | 1 | 18 | 18 |
| 7 | 20 | 19 | 1 | 18 | 18 |
| 8 | 20 | 19 | 1 | 18 | 18 |
| 9 | 20 | 19 | 1 | 18 | 18 |
| 10 | 20 | 19 | 1 | 18 | 18 |

