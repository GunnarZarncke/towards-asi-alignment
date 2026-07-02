# Embedded simulation report

Episodes: 13

| Bridge | Substrate | Scenario | Red-team | In-sim | Outer certifies | False pass |
| --- | --- | --- | --- | --- | --- | --- |
| none | python | honest | none | pass/passes | True | False |
| MB1 | python | boundary_alias | none | reduce/belowThreshold | True | False |
| MB2 | python | bundle_goodhart | none | reduce/belowThreshold | True | False |
| MB3 | python | bearer_mismap | none | reduce/belowThreshold | True | False |
| MB4 | python | capture_theater | none | invalid_certificate/capturedInvalid | True | False |
| MB5 | python | successor_relabel | none | pass/passes | True | False |
| MB6 | python | selection_basin | none | reduce/belowThreshold | True | False |
| MB6b | python | basin_lock_in | none | reduce/belowThreshold | True | False |
| MB7 | python | hidden_capability | none | reduce/belowThreshold | True | False |
| MB7d | python | inferential_coupling | none | reduce/belowThreshold | True | False |
| MB8 | python | legitimacy_theater | none | reduce/belowThreshold | True | False |
| MB9 | python | grounding_silent_gap | none | reduce/belowThreshold | True | False |
| instrument_capture | python | instrument_capture | none | reduce/belowThreshold | True | False |

False passes: 0
Outer certifies: 13
In-sim CCI correct: 13
