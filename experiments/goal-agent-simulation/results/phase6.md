# Phase 6 — responses-side twin, certifier capture, adversarial search

Protocol pre-registered in `run_phase6.py` docstring.

## Part A — round 4 escalation, fixed responses-side twin

| version | agent verdict-true rate | twin verdict-true rate | twin disclosed/queried |
| --- | --- | --- | --- |
| v1 | 0.0 | 0.0 | 0/0 |
| v2 | 0.0583 | 0.4083 | 294/294 |

Frozen GA-20 (old twin rule) v2 twin verdict-true rate: 0.0708. Prediction (fixed twin's v2 rate <= agent's v2 rate) holds: False.

## Part B — certifier capture (legacy, capture_start=150)

| board | n | mean sign-offs/ep | D5 fire rate | mean severity | full composite | light composite |
| --- | --- | --- | --- | --- | --- | --- |
| honest | 240 | 0.8625 | 0.15 | 0.2079 | 0.126 | 0.1181 |
| captured | 240 | 0.8625 | 0.15 | 0.1889 | 0.1144 | 0.1198 |

## Part C — adversarial weight search vs. uniform sampling (lambda=1.0, budget=205 evals each)

| repertoire | search score | baseline score | search >= baseline | search severity | baseline severity |
| --- | --- | --- | --- | --- | --- |
| legacy | 0.3322 | 0.331 | True | 0.8258 | 0.823 |
| round3 | 0.4596 | 0.4484 | True | 0.8646 | 0.8479 |

