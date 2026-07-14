# S5: real lag-max-MI UAD detector ported into lab-sim, re-run against S4

Generated 2026-07-07T13:09:46.769848+00:00 at lab-sim-0.9.2. NOT a battery -- see module
docstring in `run_s5_uad_core_port.py` for the hypothesis, scope note, and FINDINGS.md.

Seeds: (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), T=100, max_lag=3. Existing heuristic (`uad.discovered_units`)
never merges {eng1, eng2} in any seed: True (LS-20, re-confirmed here).

| n_agents | eng1/eng2 merge rate | isolated from rev1/rm1 rate | deterministic across seeds |
|---|---|---|---|
| 1 | 1.0 | 0.0 | True |
| 2 | 1.0 | 0.0 | True |
| 3 | 1.0 | 0.0 | True |
| 4 | 1.0 | 0.0 | True |

Seed 1 detail, per `n_agents`:

| n_agents | discovered partition | eng1/eng2 merged | uad_score |
|---|---|---|---|
| 1 | admin1=['admin1']; eng1=['eng1', 'eng2', 'rev1', 'rm1']; overseer1=['overseer1'] | True | 1.0 |
| 2 | admin1=['admin1']; eng1=['eng1', 'eng2', 'rev1', 'rm1']; overseer1=['overseer1'] | True | 1.0 |
| 3 | admin1=['admin1']; eng1=['eng1', 'eng2', 'rev1', 'rm1']; overseer1=['overseer1'] | True | 1.0 |
| 4 | admin1=['admin1']; eng1=['eng1', 'eng2', 'rev1', 'rm1']; overseer1=['overseer1'] | True | 1.0 |
