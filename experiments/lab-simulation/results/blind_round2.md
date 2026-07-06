# Blind treatment round 2: committee/DM/file playbooks (smoke scale)

CODE_VERSION `lab-sim-0.8.0`. 5 seeds per ecology, MockIsolate, `generated_playbooks_v2.json` (18 accepted / 0 rejected by `playbooks.validate_repertoire`).

Every actor in every ecology below is pinned (`LabConfig.playbook_pins`) to a NAMED round-2 generated playbook only -- `baseline_leak_check` in the JSON confirms no hand-authored baseline playbook was ever actually selected.

| ecology | mean deploys | frac. coordinated | mean UAD score | mean collusion score |
|---|---|---|---|---|
| committee_board | 26.2 | 1.0 | 1.0 | 1.0 |
| committee_file | 23.8 | 1.0 | 1.0 | 1.0 |
| dm_pair | 26.2 | 1.0 | 1.0 | 0.0 |

Comparison point: `results/d4_channel_ablation.json`'s baseline (unsevered) rows for the SAME three ecologies, built from hand-authored playbooks. Recovery here at a comparable score is the headline result (frozen detectors generalize past the playbooks their own author wrote); any gap is a real, recordable miss, not hidden.