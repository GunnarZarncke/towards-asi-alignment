# 2026-06-30 — MB5/MB6b bridge scenarios

## Trigger
User asked to implement MB5 and MB6 (MB6b basin lock-in); skip MB7b and compositions.

## Done
- **MB6b `basin_lock_in`:** fast peer saturation, crushed responsiveness post-percolation, local reported theater; audit `basin_lock_in_detected` (stable high basin pressure + raw_capacity < 0.20). Distinct from MB6a rising-pressure signal.
- **MB5 `successor_relabel`:** T/2 ID permute + discontinuity spike; medium+ `handle.successor_epoch`; audit epoch-splits interventional CCI (`successor_shift_witnessed`).
- `mb5_mb6_diagnostic.py` → `experiments/toy-simulation/results/mb5_mb6_diagnostic.json` (includes `selection_basin` control).

## Diagnostic (seeds 11–20, T=1000)
| Scenario | none | light | medium | strong |
|----------|------|-------|--------|--------|
| successor_relabel | 100% | 0% (false-pass demo) | 100% | 100% |
| basin_lock_in | 100% | 100% | 100% | 100% |
| selection_basin (MB6a) | 100% | 100% | 100% | 100% |

## Caveat / interpretation
- User noted that direct handle attacks are trivial in this toy because handle names and mutable fields are exposed; in a real environment the adversary must know or discover audited handles, gain write access, and avoid inconsistency with redundant/passive traces.
- Treat current MB5/MB6b results as bridge-witness tests under honest/protected handles, not as validation against instrument capture or adaptive handle discovery.
- Regenerated `experiments/toy-simulation/results/mb5_mb6_diagnostic.json` after an earlier short smoke run had overwritten it; current artifact is the full seeds 11–20 diagnostic.

## Key paths
- `experiments/toy-simulation/multiresolution_alignment_sim/simulator.py`
- `experiments/toy-simulation/multiresolution_alignment_sim/cci_audit.py`
- `experiments/toy-simulation/mb5_mb6_diagnostic.py`

## Open
- `instrument_capture` (handle protection)
- Re-run full curve + frozen validation with new held-out scenarios
