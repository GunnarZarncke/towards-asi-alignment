# 2026-06-30 — Unit-scoped CCI + deploy gate

## Trigger
Continue embedded-audit implementation (plan v2).

## Done
- `unit_scope.py`: mask `intervention_active` to UAD unit workflow steps before CCI/detector.
- `referents.py`: audit-visible `/etc/referents/claimed_map.json` for MB5.
- `deploy_gate.py`: certificate → `gate.local` → successor manifest + workflow event (MB5).
- `embedded_audit.py`: scoped CCI, referent map read, deploy gate, `successor_unit` on approval.
- `bridge.py`: gate evaluates pass + unit + `cci_status==passes`; audit caps read `/etc/referents`, `/deploy`.
- Tests: `test_unit_scope`, `test_deploy_gate`; 28 pytest pass.

## Decisions
- Unit scope v2 masks interventional probes only; successor_epoch stays global for MB5 shift detection.
- Gate spawns successor only when cert `pass` + `passes` CCI; baseline MB5 still rejects at gate (reduce).

## Open / next
- MB5 false-pass / successor_shift_witness alignment.
- In-sim referent drift from claimed map vs post-deploy probes.
- MB1 boundary unit; perturbation-response UAD graph.

## Key paths
- `embedded_sim/unit_scope.py`
- `embedded_sim/deploy_gate.py`
- `embedded_sim/referents.py`

## Commits
- (none)
