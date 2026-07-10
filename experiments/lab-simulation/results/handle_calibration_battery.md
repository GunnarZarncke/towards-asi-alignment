# Handle calibration battery

Generated 2026-07-09T18:53:55.884086+00:00 at lab-sim-0.11.0. 5 seeds x 3 doses (early=t10, mid=t30, late=t60) per handle, `MockIsolate`, honest deterministic roster (`ecology`-style `serial_pipeline_no_unit_config` roster, `units=None`).

Dose-response: mean (treatment - matched-seed control) delta, oracle severity composite and one domain metric per handle (see `handles.py`'s declared `operation` for each).

| handle | dose | n | mean Δseverity | domain metric | mean Δdomain |
|---|---|---|---|---|---|
| capability_revoke | early (t=10) | 5 | -0.0056 | models_built_total | +0.00 |
| capability_revoke | mid (t=30) | 5 | -0.0056 | models_built_total | +0.00 |
| capability_revoke | late (t=60) | 5 | -0.0055 | models_built_total | +0.00 |
| release_hold | early (t=10) | 5 | +0.0166 | m001_deploys_ok | -1.00 |
| release_hold | mid (t=30) | 5 | +0.0000 | m001_deploys_ok | +0.00 |
| release_hold | late (t=60) | 5 | +0.0000 | m001_deploys_ok | +0.00 |
| state_freeze | early (t=10) | 5 | +0.0000 | state_saves_ok_after_dose | -11.00 |
| state_freeze | mid (t=30) | 5 | +0.0000 | state_saves_ok_after_dose | -10.00 |
| state_freeze | late (t=60) | 5 | +0.0000 | state_saves_ok_after_dose | -6.00 |
| isolate_restart | early (t=10) | 5 | +0.0000 | models_built_total | +0.00 |
| isolate_restart | mid (t=30) | 5 | +0.0000 | models_built_total | +0.00 |
| isolate_restart | late (t=60) | 5 | +0.0000 | models_built_total | +0.00 |

