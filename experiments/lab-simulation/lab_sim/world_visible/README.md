# `lab_sim/world_visible/` — tier 2 (full in-sim)

A grantee at this grade gets tier 1 (`agent_visible/`) plus everything
here: the lab's mechanics/infrastructure, with no referee/ground-truth
internals. See [`../../ACCESS_TIERS.md`](../../ACCESS_TIERS.md) for the
full four-tier scheme and rationale.

| File | What it is |
| --- | --- |
| `config.py` | `LabConfig`, `AgentConfig`, `GoalWeights`, Board/Admin/Tier configs, `CODE_VERSION` |
| `pipeline_spec.py` | JSON step-DAG schema + loader/validator |
| `pipeline_default.json` | Frozen baseline 9-step topology |
| `pipeline_shortcut.json` | Variant without `approve_review` (topology-as-data proof) |
| `pipeline_engine.py` | `trigger_step`: DAG preconditions, access gate, effect dispatch, versioned-spec log |
| `access.py` | `PermissionService`: grant/revoke/check, hash-chained access log |
| `agents.py` | `ROLE_CAPABILITIES` (static gate), `AdminPolicy` (grant/deny/capture) |
| `tools.py` | `ToolCall`/`ToolResult` wire schema + `Host` dispatch (the trust boundary) |
| `workspace.py` | Per-episode on-disk workspace, report files, digest |
| `comms.py` | Board/DM message store + comms channel wiring |
| `agent_state.py` | Persistent cross-episode agent state (`runs/agent_state/<id>.json`) |
| `world.py` | `run_episode`: full episode loop wiring isolates + engine + access control + overseer script |

`world.py` imports from `oracle_only/` (real oracle state) and from
`harness/` (the default `MockIsolate` backend) — this is the expected,
correct runtime coupling described in `ACCESS_TIERS.md`: the grading here
is about *whose eyes get to read which files*, not a runtime import
sandbox (only `agent_visible/` is mechanically import-isolated).
