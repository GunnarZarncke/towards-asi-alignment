# Phase 7 battery report

CODE_VERSION `lab-sim-0.5.0`.

## 1. Escalation ladder (`lab_sim/escalation.py`)

- 135 episodes, 132 escalated (screen score in the gated band), 75 with a true (oracle-side) report divergence.
- confusion matrix (ground truth = `severity.report_divergence > 0.1`): {'tp': 65, 'fp': 2, 'tn': 58, 'fn': 10}
- precision 0.9701, recall 0.8667

## 2. Red-team search (`lab_sim/redteam.py`)

| repertoire | search best (search seeds) | uniform-baseline mean | found (report seeds) | baseline-best (report seeds) | search >= baseline |
|---|---|---|---|---|---|
| baseline | 0.0347 | 0.002 | 0.0326 | 0.0326 | True |
| generated | 0.0352 | 0.0146 | 0.0326 | 0.0326 | True |

## 3. Capture grid (independent board/admin capture channels)

Regime: `build_params={'scale': 0.95, 'safety_effort': 0.05}` (crosses `ontology.REVIEW_HAZARD_THRESHOLD`), conscientious reviewer weights, 10 seeds/cell.

| cell | board capture | admin capture | mean severity composite | mean n deploys |
|---|---|---|---|---|
| neither | None | None | 0.0055 | 0.0 |
| board_only | 0 | None | 0.0235 | 22.0 |
| admin_only | None | 0 | 0.0055 | 0.0 |
| both | 0 | 0 | 0.0235 | 22.0 |

## Isolate cost ledger

This run: 525 isolate lifetimes, 13.019717s total (0.0248s/isolate-lifetime).

