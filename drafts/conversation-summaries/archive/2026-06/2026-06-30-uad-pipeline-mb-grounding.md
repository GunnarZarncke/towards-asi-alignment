# 2026-06-30 — UAD pipeline + MB grounding doc

## Trigger
Ensure proper UAD is in the plan; continue implementation; clarify current MB* unit grounding.

## Done
- Reordered `embedded_audit.py`: UAD + handles **before** CCI; pass gate requires grounded unit anchors.
- Enhanced `uad.py`: actor, machine, source_lineage, memory_namespace, coalition candidates with workflow anchors.
- Added `handles.py`: grounded handles from correction.jsonl probes/uptake/bearer/lineage + workflow control_boundary.
- Contract tests: `test_uad_before_cci.py`; unit tests for handles and source_lineage.
- `PLAN.md` with UAD-before-CCI spec and MB* grounding table; `TODO.md` UAD v2 gaps.
- 22 pytest tests pass.

## Decisions
- v1 keeps CCI global on full micro trace; UAD unit is attached to certificate but does not yet filter CCI (documented gap).
- Lab UAD is bridge-agnostic workflow heuristics; MB-specific failures still live mainly in micro CCI/detector.

## Open / next
- Scope CCI to selected unit; MB1 boundary unit; MB5 successor deploy gate + referent maps.
- UAD golden precision/recall per bridge.

## Key paths
- `experiments/embedded-simulation/PLAN.md`
- `experiments/embedded-simulation/embedded_sim/uad.py`
- `experiments/embedded-simulation/embedded_sim/handles.py`
- `experiments/embedded-simulation/embedded_sim/embedded_audit.py`

## Commits
- (none)
