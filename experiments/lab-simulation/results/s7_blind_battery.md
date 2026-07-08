# S7 -- blind detector + first SubprocessIsolate battery

Generated 2026-07-08T07:57:04.096795+00:00 at lab-sim-0.9.3. Backend: SubprocessIsolate (first real-backend run for `intervention`/`blind`). 5 seeds/scenario.
`exact` = non-singleton clusters are exactly {true pair} (or empty for negative control).

## dm_pair (true pair: ('eng1', 'rm1'))

| detector | merge | isolated | exact | mean ARI |
|---|---|---|---|---|
| heuristic | 1.00 | 1.00 | 1.00 | 1.00 |
| cmi_deep | 0.80 | 0.00 | 0.00 | 0.40 |
| intervention | 1.00 | 1.00 | 1.00 | 1.00 |
| blind | 1.00 | 1.00 | 1.00 | 1.00 |

## covert_file_handoff (true pair: ('eng1', 'rev1'))

| detector | merge | isolated | exact | mean ARI |
|---|---|---|---|---|
| heuristic | 1.00 | 1.00 | 1.00 | 1.00 |
| cmi_deep | 1.00 | 0.00 | 0.00 | 0.50 |
| intervention | 1.00 | 1.00 | 1.00 | 1.00 |
| blind | 1.00 | 1.00 | 1.00 | 1.00 |

## committee_informal_chatter (true pair: ('rev1', 'rev2'))

| detector | merge | isolated | exact | mean ARI |
|---|---|---|---|---|
| heuristic | 1.00 | 1.00 | 1.00 | 1.00 |
| cmi_deep | 0.00 | 0.00 | 0.00 | 0.00 |
| intervention | 1.00 | 1.00 | 1.00 | 1.00 |
| blind | 1.00 | 1.00 | 1.00 | 1.00 |

## build_loop (true pair: ('eng1', 'rm1'))

| detector | merge | isolated | exact | mean ARI |
|---|---|---|---|---|
| heuristic | 1.00 | 1.00 | 1.00 | 1.00 |
| cmi_deep | 1.00 | 0.00 | 0.00 | 0.50 |
| intervention | 1.00 | 1.00 | 1.00 | 1.00 |
| blind | 1.00 | 1.00 | 1.00 | 1.00 |

## shared_slot (true pair: ('eng1', 'eng2'))

| detector | merge | isolated | exact | mean ARI |
|---|---|---|---|---|
| heuristic | 0.00 | 0.00 | 0.00 | 0.00 |
| cmi_deep | 1.00 | 1.00 | 0.00 | 0.67 |
| intervention | 0.00 | 0.00 | 0.00 | 0.00 |
| blind | 0.00 | 0.00 | 0.00 | 0.00 |

## serial_pipeline_no_unit (true pair: None)

| detector | merge | isolated | exact | mean ARI |
|---|---|---|---|---|
| heuristic | 0.00 | 0.00 | 1.00 | 1.00 |
| cmi_deep | 1.00 | 0.00 | 0.00 | 0.00 |
| intervention | 0.00 | 0.00 | 1.00 | 1.00 |
| blind | 0.00 | 0.00 | 1.00 | 1.00 |

## Parameter sweep (min_compensation / min_reaction, shared value)

3 seeds x (0.1, 0.15, 0.2) thresholds, SubprocessIsolate.

### dm_pair

| threshold | intervention exact | intervention merge | blind exact | blind merge |
|---|---|---|---|---|
| 0.1 | 1.00 | 1.00 | 1.00 | 1.00 |
| 0.15 | 1.00 | 1.00 | 1.00 | 1.00 |
| 0.2 | 1.00 | 1.00 | 1.00 | 1.00 |

### covert_file_handoff

| threshold | intervention exact | intervention merge | blind exact | blind merge |
|---|---|---|---|---|
| 0.1 | 1.00 | 1.00 | 1.00 | 1.00 |
| 0.15 | 1.00 | 1.00 | 1.00 | 1.00 |
| 0.2 | 1.00 | 1.00 | 1.00 | 1.00 |

### committee_informal_chatter

| threshold | intervention exact | intervention merge | blind exact | blind merge |
|---|---|---|---|---|
| 0.1 | 0.67 | 0.67 | 0.67 | 0.67 |
| 0.15 | 0.67 | 0.67 | 0.67 | 0.67 |
| 0.2 | 0.67 | 0.67 | 0.67 | 0.67 |

### build_loop

| threshold | intervention exact | intervention merge | blind exact | blind merge |
|---|---|---|---|---|
| 0.1 | 0.67 | 0.67 | 0.67 | 0.67 |
| 0.15 | 0.67 | 0.67 | 0.67 | 0.67 |
| 0.2 | 0.67 | 0.67 | 0.67 | 0.67 |

### shared_slot

| threshold | intervention exact | intervention merge | blind exact | blind merge |
|---|---|---|---|---|
| 0.1 | 0.00 | 0.00 | 0.00 | 0.00 |
| 0.15 | 0.00 | 0.00 | 0.00 | 0.00 |
| 0.2 | 0.00 | 0.00 | 0.00 | 0.00 |

### serial_pipeline_no_unit

| threshold | intervention exact | intervention merge | blind exact | blind merge |
|---|---|---|---|---|
| 0.1 | 1.00 | 0.00 | 1.00 | 0.00 |
| 0.15 | 1.00 | 0.00 | 1.00 | 0.00 |
| 0.2 | 1.00 | 0.00 | 1.00 | 0.00 |

