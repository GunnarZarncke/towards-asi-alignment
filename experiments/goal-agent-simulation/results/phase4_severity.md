# Phase 4a+4b — continuous severity ranking and honest-twin gaps

Protocol pre-registered in `run_phase4_ranking.py` docstring. 30 configs x 8 seeds per repertoire.

## Phase 4a — Spearman(oracle severity, detector composite score), per repertoire

| repertoire | n | mean severity | n never-event | light | full |
| --- | --- | --- | --- | --- | --- |
| legacy | 240 | 0.2079 | 36 | 0.8206 | 0.9747 |
| round1 | 240 | 0.1857 | 43 | 0.6318 | 0.979 |
| round2 | 240 | 0.4876 | 120 | 0.4596 | 0.9129 |
| round3 | 240 | 0.6152 | 154 | 0.0732 | 0.7287 |

## Phase 4b — honest-twin gaps (agent minus twin; positive = twin scores lower)

| repertoire | severity gap (frac>0) | light gap (frac>0) | full gap (frac>0) |
| --- | --- | --- | --- |
| legacy | 0.0963 (0.5) | 0.0164 (0.2083) | 0.0289 (0.2792) |
| round1 | 0.0911 (0.35) | -0.0074 (0.1208) | 0.0296 (0.2292) |
| round2 | 0.1884 (0.7792) | -0.0493 (0.0875) | 0.0554 (0.525) |
| round3 | 0.3006 (0.9667) | -0.1219 (0.1083) | 0.0418 (0.6833) |

