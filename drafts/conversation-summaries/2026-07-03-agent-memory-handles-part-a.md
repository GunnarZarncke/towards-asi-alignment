# 2026-07-03 — Agent memory (localStorage/VFS), Part D handles, access-tier honest arm

## Trigger
User wanted handle taxonomy aligned with access-uad paper, agent self-memory from isolates, half of new Part D handles, then browser-like memory (localStorage/fs not custom RPCs), test speed fix, and end-of-session commit.

## Done
- **Agent memory:** VFS-backed store at `/home/agent` → `/var/agent-memory/{namespace}/{actor_id}/`; `localStorage` + `fs.appendFileSync('.reasoning/trace.jsonl')` in JS facade; policy via `.memory/policy.json`.
- **Part D handles (5/9):** `memory_read`, `reasoning_trace_read`, `memory_erase`, `memory_capacity_limit`, `compute_budget`; reclassified `memory_freeze` → `operation_resource`, `successor_gate` → `operation_boundary`; documented types + `paper_role` in `handle_registry.py`.
- **Part A:** `run_access_tier_curve` includes `honest` scenario; per-tier `honest_cci_pass_rate` / `violation_cci_pass_rate`; N-11 postscript in `NEGATIVE_RESULTS.md`.
- **Tests:** 185 passed; calibration refit gated behind `--runslow`; fast host-bridge memory tests without Node.
- **Not in commit:** measurement-protocol files (`info_ci.py`, `probe_scan.py`, …) still untracked from prior session; Part B–C (channel-sets, attestation) deferred.

## Decisions
- Memory uses browser-familiar surfaces (localStorage + file paths), not bespoke bridge RPCs — host enforces policy on agent-home writes only.
- Access-tier curve honest arm fixes N-11 design gap; violation-only flat curve kept as historical finding.
- Full `fit_handle_calibration` in CI only with `--runslow`; default test loads frozen artifact.

## Open / next
- Part B: `channel_sets.py`, per-detector `required_channels`, eligibility gating (N-10).
- Part C: attestation anchor on `handle.hardware_tag` (N-9).
- Remaining Part D handles: `output_channel_limit`, `successor_substitution`, `challenge`/`counterfactual`, persistence probe.
- Regenerate `results/embedded_access_tier_curve.{md,json}` before citing new tier numbers.

## Key paths
- `experiments/embedded-simulation/embedded_sim/agent_memory.py`
- `experiments/embedded-simulation/embedded_sim/handle_registry.py`
- `experiments/embedded-simulation/embedded_sim/handle_memory.py`
- `experiments/embedded-simulation/isolate/lib/facade.js`
- `experiments/embedded-simulation/embedded_sim/batch.py`

## Commits
- `51b16b6` — Add VFS-backed agent memory, Part D handles, and access-tier honest arm.
