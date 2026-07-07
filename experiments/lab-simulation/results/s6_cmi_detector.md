# S6 first step: custom actor-level conditional-MI detector vs. vendored vs. heuristic

Generated 2026-07-07T16:07:29.584266+00:00 at lab-sim-0.9.2. NOT a battery -- see module
docstring in `run_s6_cmi_detector.py`. `exact` = non-singleton clusters are exactly
{true pair} (found, isolated, nothing else spuriously merged).

## dm_pair (true pair: ('eng1', 'rm1'))

| detector | merge rate | isolated rate | exact rate |
|---|---|---|---|
| heuristic | 1.00 | 1.00 | 1.00 |
| vendored_mi_shallow | 1.00 | 0.00 | 0.00 |
| vendored_mi_deep | 1.00 | 0.00 | 0.00 |
| cmi_shallow | 1.00 | 0.00 | 0.00 |
| cmi_deep | 1.00 | 0.00 | 0.00 |

## covert_file_handoff (true pair: ('eng1', 'rev1'))

| detector | merge rate | isolated rate | exact rate |
|---|---|---|---|
| heuristic | 1.00 | 1.00 | 1.00 |
| vendored_mi_shallow | 1.00 | 0.00 | 0.00 |
| vendored_mi_deep | 1.00 | 0.00 | 0.00 |
| cmi_shallow | 1.00 | 0.00 | 0.00 |
| cmi_deep | 1.00 | 0.00 | 0.00 |

## committee_informal_chatter (true pair: ('rev1', 'rev2'))

| detector | merge rate | isolated rate | exact rate |
|---|---|---|---|
| heuristic | 1.00 | 1.00 | 1.00 |
| vendored_mi_shallow | 1.00 | 0.00 | 0.00 |
| vendored_mi_deep | 1.00 | 0.00 | 0.00 |
| cmi_shallow | 0.00 | 0.00 | 0.00 |
| cmi_deep | 0.00 | 0.00 | 0.00 |

## build_loop (true pair: ('eng1', 'rm1'))

| detector | merge rate | isolated rate | exact rate |
|---|---|---|---|
| heuristic | 1.00 | 1.00 | 1.00 |
| vendored_mi_shallow | 1.00 | 0.00 | 0.00 |
| vendored_mi_deep | 1.00 | 0.00 | 0.00 |
| cmi_shallow | 1.00 | 0.00 | 0.00 |
| cmi_deep | 1.00 | 0.00 | 0.00 |

## shared_slot (true pair: ('eng1', 'eng2'))

| detector | merge rate | isolated rate | exact rate |
|---|---|---|---|
| heuristic | 0.00 | 0.00 | 0.00 |
| vendored_mi_shallow | 1.00 | 0.00 | 0.00 |
| vendored_mi_deep | 1.00 | 0.00 | 0.00 |
| cmi_shallow | 1.00 | 1.00 | 0.00 |
| cmi_deep | 1.00 | 1.00 | 0.00 |

