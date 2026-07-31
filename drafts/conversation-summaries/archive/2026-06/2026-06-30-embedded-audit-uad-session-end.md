# 2026-06-30 — Embedded audit session (UAD v1/v2)

## Trigger
Continue embedded-audit experiment plan: oracle separation, proper UAD, unit grounding clarity, unit-scoped CCI, successor deploy gate. Session ended on user request.

## Done
- **Oracle separation** — split inference vs bridge checks in `oracle_guard.py`; smoke + contract tests.
- **UAD v1** — VFS workflow parsing; heterogeneous units (actor, machine, source_lineage, memory_namespace, coalition); `handles.py`; UAD-before-CCI pipeline; pass requires grounded unit.
- **Docs** — `PLAN.md` (UAD spec + MB* grounding table), `TODO.md`, README updates.
- **UAD v2** — `unit_scope.py` (mask interventional probes to unit workflow steps); `referents.py` (claimed map on VFS for MB5); `deploy_gate.py` (cert → gate.local → successor artifacts).
- **Tests** — 28 pytest pass (`tests/unit`, `contract`, `golden`); smokes: `smoke_oracle_separation.py`.

## Decisions
- Lab UAD is bridge-agnostic workflow heuristics; MB-specific failure modes still primarily in micro CCI/detector until unit-scoped detector work lands.
- Unit scope v2 masks `intervention_active` only; `successor_epoch_series` stays global for MB5.
- Deploy gate approves only on `pass` + `cci_status==passes` + unit; baseline MB5 still rejects at gate (reduce/belowThreshold) — known false-pass gap remains in micro CCI witness, not gate.
- Oracle fields never on audit path; claimed referent map is audit-visible, true referents stay in `OuterTruthLedger`.

## Open / next (recommended resume order)
1. **MB5 false-pass** — align `successor_shift_witnessed` with toy held-out behavior under embedded audit.
2. **In-sim referent drift** — score claimed map vs post-deploy probes (not oracle-only).
3. **MB1 boundary unit** — source/machine lineage correlates in workflow UAD.
4. **Perturbation-response UAD graph** — replace heuristic ranks.
5. Golden UAD precision/recall per bridge; artifact-only CCI rebuild (`world.micro` removal).

## Key paths
- `experiments/embedded-simulation/PLAN.md`
- `experiments/embedded-simulation/TODO.md`
- `experiments/embedded-simulation/embedded_sim/embedded_audit.py`
- `experiments/embedded-simulation/embedded_sim/uad.py` · `handles.py` · `unit_scope.py` · `deploy_gate.py` · `referents.py`
- `experiments/embedded-simulation/run.py`

## Verify
```bash
cd experiments/embedded-simulation
../../.venv/bin/python -m pytest tests/ -q
python3 smoke_oracle_separation.py
python3 run.py --substrate js --workers 4
```

## Commits
- (none — user did not request commit)

## Untracked
All of `experiments/embedded-simulation/` remains largely untracked/new in git; do not commit unless asked.
