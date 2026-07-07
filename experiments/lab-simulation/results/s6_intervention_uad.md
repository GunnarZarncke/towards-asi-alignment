# S6 intervention-supported UAD vs passive baselines

Generated 2026-07-07T16:26:10.762121+00:00 at lab-sim-0.9.2. NOT a battery.
`exact` = non-singleton clusters are exactly {true pair} (or empty for negative control).

## dm_pair (true pair: ('eng1', 'rm1'))

| detector | merge | isolated | exact | mean ARI |
|---|---|---|---|---|
| heuristic | 1.00 | 1.00 | 1.00 | 1.00 |
| intervention | 1.00 | 1.00 | 1.00 | 1.00 |
| vendored_mi_shallow | 1.00 | 0.00 | 0.00 | 0.50 |
| vendored_mi_deep | 1.00 | 0.00 | 0.00 | 0.50 |
| cmi_shallow | 1.00 | 0.00 | 0.00 | 0.50 |
| cmi_deep | 1.00 | 0.00 | 0.00 | 0.50 |

## covert_file_handoff (true pair: ('eng1', 'rev1'))

| detector | merge | isolated | exact | mean ARI |
|---|---|---|---|---|
| heuristic | 1.00 | 1.00 | 1.00 | 1.00 |
| intervention | 1.00 | 1.00 | 1.00 | 1.00 |
| vendored_mi_shallow | 1.00 | 0.00 | 0.00 | 0.50 |
| vendored_mi_deep | 1.00 | 0.00 | 0.00 | 0.50 |
| cmi_shallow | 1.00 | 0.00 | 0.00 | 0.50 |
| cmi_deep | 1.00 | 0.00 | 0.00 | 0.50 |

## committee_informal_chatter (true pair: ('rev1', 'rev2'))

| detector | merge | isolated | exact | mean ARI |
|---|---|---|---|---|
| heuristic | 1.00 | 1.00 | 1.00 | 1.00 |
| intervention | 1.00 | 1.00 | 1.00 | 1.00 |
| vendored_mi_shallow | 1.00 | 0.00 | 0.00 | 0.29 |
| vendored_mi_deep | 1.00 | 0.00 | 0.00 | 0.29 |
| cmi_shallow | 0.00 | 0.00 | 0.00 | 0.00 |
| cmi_deep | 0.00 | 0.00 | 0.00 | 0.00 |

## build_loop (true pair: ('eng1', 'rm1'))

| detector | merge | isolated | exact | mean ARI |
|---|---|---|---|---|
| heuristic | 1.00 | 1.00 | 1.00 | 1.00 |
| intervention | 1.00 | 1.00 | 1.00 | 1.00 |
| vendored_mi_shallow | 1.00 | 0.00 | 0.00 | 0.50 |
| vendored_mi_deep | 1.00 | 0.00 | 0.00 | 0.50 |
| cmi_shallow | 1.00 | 0.00 | 0.00 | 0.50 |
| cmi_deep | 1.00 | 0.00 | 0.00 | 0.50 |

## shared_slot (true pair: ('eng1', 'eng2'))

| detector | merge | isolated | exact | mean ARI |
|---|---|---|---|---|
| heuristic | 0.00 | 0.00 | 0.00 | 0.00 |
| intervention | 0.00 | 0.00 | 0.00 | 0.00 |
| vendored_mi_shallow | 1.00 | 0.00 | 0.00 | 0.29 |
| vendored_mi_deep | 1.00 | 0.00 | 0.00 | 0.29 |
| cmi_shallow | 1.00 | 1.00 | 0.00 | 0.67 |
| cmi_deep | 1.00 | 1.00 | 0.00 | 0.67 |

## serial_pipeline_no_unit (true pair: None)

| detector | merge | isolated | exact | mean ARI |
|---|---|---|---|---|
| heuristic | 0.00 | 0.00 | 1.00 | 1.00 |
| intervention | 0.00 | 0.00 | 1.00 | 1.00 |
| vendored_mi_shallow | 1.00 | 0.00 | 0.00 | 0.00 |
| vendored_mi_deep | 1.00 | 0.00 | 0.00 | 0.00 |
| cmi_shallow | 1.00 | 0.00 | 0.00 | 0.00 |
| cmi_deep | 1.00 | 0.00 | 0.00 | 0.00 |

