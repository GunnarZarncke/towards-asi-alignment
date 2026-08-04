# Phase 5 — GA-16/GA-17 follow-ups

Protocol pre-registered in `run_phase5_followups.py` docstring. 30 configs x 8 seeds per repertoire. Gates: {'low_gate': 0.15, 'high_gate': 0.55, 'k_queries': 3, 'disclose_fraction_gate': 0.5}.

## Part A — per-detector honest-twin gap decomposition (agent minus twin)

| repertoire | n | d1 gap (frac>0) | d1b gap (frac>0) | d2 gap (frac>0) | light_deception gap (frac>0) |
| --- | --- | --- | --- | --- | --- |
| legacy | 240 | 0.0663 (0.2208) | 0.0509 (0.2208) | -0.068 (0.0708) | 0.0586 (0.2208) |
| round1 | 240 | 0.0065 (0.0583) | 0.0113 (0.1708) | -0.04 (0.0583) | 0.0089 (0.1708) |
| round2 | 240 | 0.0093 (0.0792) | 0.0107 (0.1833) | -0.1679 (0.0292) | 0.01 (0.1833) |
| round3 | 240 | 0.0104 (0.0958) | 0.0426 (0.5542) | -0.4546 (0.0125) | 0.0265 (0.5542) |

## Part B — escalation v1 vs v2, queryability diagnostic

| repertoire | n | frac queryable v1 | frac queryable v2 |
| --- | --- | --- | --- |
| legacy | 240 | 0.25 | 0.525 |
| round1 | 240 | 0.2292 | 1.0 |
| round2 | 240 | 0.2958 | 0.9708 |
| round3 | 240 | 0.8708 | 1.0 |
| round4 | 240 | 0.0125 | 1.0 |

| repertoire | version | verdict-true rate | escalated rate | mean queried | mean disclose frac | sev\|True | sev\|False | Spearman(sev,verdict) | twin verdict-true rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| legacy | v1 | 0.0542 | 0.2417 | 1.1034 | 0.0 | 0.8157 | 0.173 | 0.3937 | 0.0 |
| legacy | v2 | 0.0542 | 0.2417 | 2.9828 | 0.0 | 0.8157 | 0.173 | 0.3937 | 0.0 |
| round1 | v1 | 0.0 | 0.1208 | 1.7931 | 0.0 | None | 0.1857 | 0.0 | 0.0 |
| round1 | v2 | 0.0 | 0.1208 | 3.0 | 0.0 | None | 0.1857 | 0.0 | 0.0 |
| round2 | v1 | 0.0 | 0.6917 | 0.9036 | 0.0 | None | 0.4876 | 0.0 | 0.0 |
| round2 | v2 | 0.0 | 0.6917 | 3.0 | 0.0 | None | 0.4876 | 0.0 | 0.0 |
| round3 | v1 | 0.0 | 0.2333 | 2.9107 | 0.0 | None | 0.6153 | 0.0 | 0.0 |
| round3 | v2 | 0.0 | 0.2333 | 3.0 | 0.0 | None | 0.6153 | 0.0 | 0.0 |
| round4 | v1 | 0.0 | 0.1292 | 0.0 | 0.0 | None | 0.4423 | 0.0 | 0.0 |
| round4 | v2 | 0.0542 | 0.1292 | 3.0 | 0.4516 | 0.6004 | 0.4332 | 0.1532 | 0.0708 |

