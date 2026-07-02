# 2026-07-02 — Embedded sim: Milestone v4 (handle-mediated access)

## Trigger
User: new milestone after AppD + writer-compromise commit; adapt access-uad plan,
then "Implement." Scope: handle-mediated probes, curves, certification artifact,
handle-aware red team; defer EIG probe selection.

## Done
- **`MILESTONE-v4.md`** — canonical v4 spec: kernel dual-view (oracle + auditor),
  handle types, attacker/defender red team, phases A–D, claim strength.
- **`docs/certification-artifact.md`** — `certification.json` schema, curve artifact formats.
- **`embedded_sim/certification_artifact.py`** — schema dataclasses + write stub (no audit wiring).
- **`TODO.md`** — v4 section at top (IMPLEMENTED); G-1 adapted to access-tier curve vs twin ecology.
- **`PLAN.md`** — v4 milestone pointer.
- **`handle_kernel.py`** — `HandleOperationKernel` + realization/projection helpers.
- **`handle_registry.py`** — `handle_type`, access tier, kernel parameters.
- **Probe path** — episode rows routed through handle realizations; host truth keeps
  `_handle_kernel_truth`; VFS projection carries only handle id/type/latency/landed/uplift.
- **CCI** — `cci_interventional.py` uses handle landing/latency when present.
- **Certification artifact** — `/srv/audit/out/certification.json` emitted alongside
  safety case; `InSimAuditCertificate` records path and exercised handle types.
- **Curves** — `run_access_tier_curve`, `run_certification_capacity_curve`; CLI flags
  `--access-tier-curve`, `--certification-curve`.
- **Red team** — `probe_aware`, `handle_evasion_tool_scope`, and
  `summary_by_strategy_handle` battery matrix.
- **Tests** — `tests/contract/test_milestone_v4_handles.py`; full embedded test suite
  passes (150 passed).

## Decisions
- **G-1 preferred path:** access-tier degradation curve (Theorem 1 operationalized)
  over confounded-twin ecology — fewer gears, same information boundary.
- **EIG probe selection:** explicit deferred TODO, not v4 initial scope.
- **Kernel contract:** one `HandleOperationKernel` on host truth; audit sees projection only.

## Open / next
- Regenerate large batch artifacts if fresh `embedded_access_tier_curve.*` and
  `embedded_certification_capacity_curve.*` should be checked in.
- EIG auditor probe selection remains deferred.

## Key paths
- `experiments/embedded-simulation/MILESTONE-v4.md`
- `experiments/embedded-simulation/docs/certification-artifact.md`
- `experiments/embedded-simulation/embedded_sim/certification_artifact.py`
- `experiments/embedded-simulation/embedded_sim/handle_kernel.py`
- `experiments/embedded-simulation/tests/contract/test_milestone_v4_handles.py`
- `context/extracts/access-uad.md`

## Commits
- `0e7d18c` — Implement embedded-sim Milestone v4: handle-mediated probes and certification.
