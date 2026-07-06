# Lab-Layer Simulation

Fourth experiment line (after `toy-simulation/`, `embedded-simulation/`,
`goal-agent-simulation/`): goal-driven agents in lab roles (engineer,
reviewer, release manager, access admin) inside a lab with real mechanics —
a deployment pipeline defined as an infrastructure-as-code JSON step-DAG,
an on-disk workspace with report files, service-managed access control, and
real OS-subprocess isolates speaking JSON-RPC to a host.

**Status: Phase 0-5 complete, referee FROZEN 2026-07-06** (CODE_VERSION
`lab-sim-0.3.0`, 136 tests green — see DESIGN.md "Freeze note"). Scaffold,
oracle world, pipeline-as-code engine, access control, subprocess isolates,
goal-driven playbook agents, full episode loop, the tier-gated referee
(severity, five detector families, honest-twin transform), audit-visible
monitoring signal, perturbation hooks, and the handle registry + overseer
invocation path are all implemented and tested. Phase 4's playbook
repertoire and several Phase 5 detector components are deliberately scoped
down from PLAN.md's original ambition — see DESIGN.md "Phase 4/5 scope
notes" for exactly what and why. Evaluations have not started: no blind
generation, escalation, or LLM-agent adapter yet (Phases 6-8).

- [`PLAN.md`](PLAN.md) — full plan: bridge coverage (MB1-MB10), deferred
  workstreams (D1-D4), forward hooks, phase breakdown.
- [`DESIGN.md`](DESIGN.md) — frozen pre-registered decisions, phase status,
  scope notes, and recorded measurements (isolate cost, regression digests).

## Run tests

```bash
cd experiments/lab-simulation
python3 -m pytest
```

## Other entry points

```bash
python3 verify_isolate_equivalence.py [n_seeds]  # Mock vs Subprocess backend equivalence + timing benchmark
python3 report_isolate_cost.py                    # print the isolate cost ledger
```

## Layout (current)

```
lab_sim/
  config.py            # LabConfig, AgentConfig, GoalWeights, Board/Admin/Tier configs, CODE_VERSION
  oracle.py             # models (true capability/hazard), bearer harm, provenance ledger
  workspace.py          # per-episode on-disk workspace, report files, digest
  pipeline_spec.py      # JSON step-DAG schema + loader/validator
  pipeline_default.json # frozen baseline 9-step topology
  pipeline_shortcut.json# variant without approve_review (topology-as-data proof)
  pipeline_engine.py    # trigger_step: DAG preconditions, access gate, effect dispatch, versioned-spec log
  smoke.py              # scripted honest episode (no agents) -> deterministic digest
  access.py             # PermissionService: grant/revoke/check, hash-chained access log
  agents.py             # ROLE_CAPABILITIES (static gate), AdminPolicy (grant/deny/capture)
  events.py             # generic hash-chained EventLog + tier projection (none/light/full/deep)
  tools.py              # ToolCall/ToolResult wire schema + Host dispatch (the trust boundary)
  programs.py           # pure host-independent agent decision logic: walk_pipeline, goal_policy, honest_twin
  agent_main.py         # subprocess entry point (imports only programs.py + stdlib)
  isolate.py            # MockIsolate (in-process) + SubprocessIsolate (real OS process)
  isolate_cost.py        # IsolateRunTiming + append-only cost ledger
  isolate_smoke.py       # scripted isolate-driven episode (walk_pipeline, Phase 3 equivalence harness)
  agent_state.py         # persistent cross-episode agent state (runs/agent_state/<id>.json)
  ontology.py            # report-content mapping (honest/inflate), pure
  playbooks.py           # PlaybookSpec schema + baseline playbook repertoire + availability gates
  handles.py             # handle registry (owner/operation/anchor/evasion story) + HandleService + invocation ledger
  bearer.py              # welfare bundle: health (deployed-model bearer) + stress (lab-staff bearer), referee-neutral
  world.py               # run_episode: full episode loop wiring isolates + engine + access control + overseer script
  cache.py               # episode-result cache keyed on sha256(config, seed, CODE_VERSION)
  severity.py            # referee: continuous severity components + never-events (full oracle access)
  detectors.py            # 5 tier-gated detector families over AuditView
  twins.py                # full-surface honest-twin transform
tests/                   # one file per module + full-episode regression/plane-separation tests
verify_isolate_equivalence.py  # Mock vs Subprocess equivalence + timing benchmark script
report_isolate_cost.py         # print the isolate cost ledger
runs/                     # ephemeral episode workspaces + persistent agent state (gitignored)
results/                  # isolate cost ledger, episode cache (gitignored)
```
