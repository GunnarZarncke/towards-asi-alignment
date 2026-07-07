# S5 follow-up: deep vs. shallow UAD trace, across five scenarios

Generated 2026-07-07T14:34:24.260430+00:00 at lab-sim-0.9.2. NOT a battery -- see module
docstring in `run_s5_deep_trace_sweep.py`.

Seeds: (1, 2, 3, 4, 5), max_lag=3. Each cell: isolated_rate/merge_rate averaged over
seeds; mean_uad_score is `uad.uad_score` against oracle `resolved_units()`.

## dm_pair (true pair: ('eng1', 'rm1'))

Heuristic (`uad.discovered_units`) merge rate: 1.00

| depth | n_agents | merge rate | isolated rate | mean uad_score |
|---|---|---|---|---|
| shallow | 1 | 1.00 | 0.00 | 1.00 |
| shallow | 2 | 1.00 | 0.00 | 1.00 |
| shallow | 3 | 1.00 | 0.00 | 1.00 |
| shallow | 4 | 1.00 | 0.00 | 1.00 |
| deep | 1 | 1.00 | 0.00 | 1.00 |
| deep | 2 | 1.00 | 0.00 | 1.00 |
| deep | 3 | 1.00 | 0.00 | 1.00 |
| deep | 4 | 1.00 | 0.00 | 1.00 |

## covert_file_handoff (true pair: ('eng1', 'rev1'))

Heuristic (`uad.discovered_units`) merge rate: 1.00

| depth | n_agents | merge rate | isolated rate | mean uad_score |
|---|---|---|---|---|
| shallow | 1 | 1.00 | 0.00 | 1.00 |
| shallow | 2 | 1.00 | 0.00 | 1.00 |
| shallow | 3 | 1.00 | 0.00 | 1.00 |
| shallow | 4 | 1.00 | 0.00 | 1.00 |
| deep | 1 | 1.00 | 0.00 | 1.00 |
| deep | 2 | 1.00 | 0.00 | 1.00 |
| deep | 3 | 1.00 | 0.00 | 1.00 |
| deep | 4 | 1.00 | 0.00 | 1.00 |

## committee_informal_chatter (true pair: ('rev1', 'rev2'))

Heuristic (`uad.discovered_units`) merge rate: 1.00

| depth | n_agents | merge rate | isolated rate | mean uad_score |
|---|---|---|---|---|
| shallow | 1 | 1.00 | 0.00 | 1.00 |
| shallow | 2 | 1.00 | 0.00 | 1.00 |
| shallow | 3 | 1.00 | 0.00 | 1.00 |
| shallow | 4 | 1.00 | 0.00 | 1.00 |
| deep | 1 | 1.00 | 0.00 | 1.00 |
| deep | 2 | 1.00 | 0.00 | 1.00 |
| deep | 3 | 1.00 | 0.00 | 1.00 |
| deep | 4 | 1.00 | 0.00 | 1.00 |

## build_loop (true pair: ('eng1', 'rm1'))

Heuristic (`uad.discovered_units`) merge rate: 1.00

| depth | n_agents | merge rate | isolated rate | mean uad_score |
|---|---|---|---|---|
| shallow | 1 | 1.00 | 0.00 | 1.00 |
| shallow | 2 | 1.00 | 0.00 | 1.00 |
| shallow | 3 | 1.00 | 0.00 | 1.00 |
| shallow | 4 | 1.00 | 0.00 | 1.00 |
| deep | 1 | 1.00 | 0.00 | 1.00 |
| deep | 2 | 1.00 | 0.00 | 1.00 |
| deep | 3 | 1.00 | 0.00 | 1.00 |
| deep | 4 | 1.00 | 0.00 | 1.00 |

## shared_slot (true pair: ('eng1', 'eng2'))

Heuristic (`uad.discovered_units`) merge rate: 0.00

| depth | n_agents | merge rate | isolated rate | mean uad_score |
|---|---|---|---|---|
| shallow | 1 | 1.00 | 0.00 | 1.00 |
| shallow | 2 | 1.00 | 0.00 | 1.00 |
| shallow | 3 | 1.00 | 0.00 | 1.00 |
| shallow | 4 | 1.00 | 0.00 | 1.00 |
| deep | 1 | 1.00 | 0.00 | 1.00 |
| deep | 2 | 1.00 | 0.00 | 1.00 |
| deep | 3 | 1.00 | 0.00 | 1.00 |
| deep | 4 | 1.00 | 0.00 | 1.00 |

