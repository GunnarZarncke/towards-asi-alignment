# Embedded simulation report

Episodes: 13

| Bridge | Substrate | Scenario | Red-team | In-sim | Outer certifies | False pass |
| --- | --- | --- | --- | --- | --- | --- |
| none | js | honest | none | pass/passes | True | False |
| MB1 | js | boundary_alias | none | pass/passes | False | True |
| MB2 | js | bundle_goodhart | none | reduce/belowThreshold | True | False |
| MB3 | js | bearer_mismap | none | reduce/belowThreshold | True | False |
| MB4 | js | capture_theater | none | invalid_certificate/capturedInvalid | True | False |
| MB5 | js | successor_relabel | none | reduce/belowThreshold | True | False |
| MB6 | js | selection_basin | none | pass/passes | False | True |
| MB6b | js | basin_lock_in | none | pass/passes | False | True |
| MB7 | js | hidden_capability | none | pass/passes | False | True |
| MB7d | js | hidden_capability | none | pass/passes | False | True |
| MB8 | js | legitimacy_theater | none | pass/passes | False | True |
| MB9 | js | grounding_silent_gap | none | reduce/belowThreshold | True | False |
| instrument_capture | js | grounding_silent_gap | none | reduce/belowThreshold | True | False |

## Isolate timing

Runs: 26
Total: 3.942s
Spawn: 0.859s
IPC (Node wait): 2.024s
Bridge (host): 0.002s
Teardown: 0.144s
Bridge calls: 78

Batch wall: 2.308s
Workers: 4

False passes: 6
Outer certifies: 7
In-sim CCI correct: 7
