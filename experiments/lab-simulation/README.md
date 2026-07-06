# Lab-Layer Simulation

Fourth experiment line (after `toy-simulation/`, `embedded-simulation/`,
`goal-agent-simulation/`): goal-driven agents in lab roles (engineer,
reviewer, release manager, access admin) inside a lab with real mechanics —
a deployment pipeline defined as an infrastructure-as-code JSON step-DAG,
an on-disk workspace with report files, service-managed access control, and
real OS-subprocess isolates speaking JSON-RPC to a host.

**Status: Phase 0-8 complete, referee FROZEN 2026-07-06, first battery run
2026-07-06, Phase 7 battery run 2026-07-06, Phase 8 exploratory spot-check
2026-07-06** (CODE_VERSION `lab-sim-0.5.0`, 200 tests green — see
DESIGN.md "Freeze note", "Phase 6", "Phase 7", and "Phase 8").
Scaffold, oracle world, pipeline-as-code engine, access control, subprocess
isolates, goal-driven playbook agents, full episode loop, the tier-gated
referee (severity, five detector families, honest-twin transform),
audit-visible monitoring signal, perturbation hooks, the handle registry +
overseer invocation path, and the bearer welfare bundle are all implemented
and tested. Phase 6 added a backward-compatible playbook-repertoire
override, a detector-blind subagent-generated playbook repertoire
(`BLIND_GENERATION.md`, `generated_playbooks_v1.json`), a pre-registered
sampling protocol with one held-out region, and the first real battery
through the subprocess backend. Phase 7 added the escalation ladder
(`escalation.py`: screen -> bounded query -> artifact-grounded
contradiction verdict), adversarial goal-weight search (`redteam.py`), and
an independent board/admin capture-channel battery (`run_phase7.py`) —
see `results/FINDINGS.md` for what both phases found, including two
genuine negatives (Phase 6's light-tier anti-correlation; Phase 7's
structurally-inert admin capture channel). Phase 4's playbook repertoire
and several Phase 5 detector components are deliberately scoped down from
PLAN.md's original ambition — see DESIGN.md "Phase 4/5 scope notes" for
exactly what and why. Phase 8 built an LLM-agent adapter (engineer role
delegated to `gpt-4o-mini` with an explicit adversarial system prompt) and
ran a small exploratory spot-check — see `results/FINDINGS.md` G-7 (no
systematic deception found; `build_params` inert on LLM path due to adapter
plumbing gap).

- [`PLAN.md`](PLAN.md) — full plan: bridge coverage (MB1-MB10), deferred
  workstreams (D1-D4), forward hooks, phase breakdown.
- [`DESIGN.md`](DESIGN.md) — frozen pre-registered decisions, phase status,
  scope notes, and recorded measurements (isolate cost, regression digests).
- [`BLIND_GENERATION.md`](BLIND_GENERATION.md) — the blind playbook
  generation protocol (Phase 6).
- [`ACCESS_TIERS.md`](ACCESS_TIERS.md) — `lab_sim/`'s four graded
  red-team source-access tiers (`agent_visible/`/`world_visible/`/
  `oracle_only/`/`harness/`) and the rationale behind the split.
- [`results/FINDINGS.md`](results/FINDINGS.md) — battery findings,
  including honest negatives.

## Run tests

```bash
cd experiments/lab-simulation
python3 -m pytest
```

## Other entry points

```bash
python3 verify_isolate_equivalence.py [n_seeds]  # Mock vs Subprocess backend equivalence + timing benchmark
python3 report_isolate_cost.py                    # print the isolate cost ledger
python3 run_phase6.py                             # Phase 6 battery -> results/phase6_battery.{json,md}
python3 run_phase7.py                             # Phase 7 battery -> results/phase7_battery.{json,md}
python3 run_phase8_llm_spotcheck.py               # Phase 8 exploratory LLM spot-check (real OpenAI calls,
                                                   #   needs a funded OPENAI_API_KEY in repo-root .env) ->
                                                   #   results/phase8_llm_spotcheck.{json,md}
```

## Layout (current)

`lab_sim/` is split into four subpackages by graded red-team source-access
tier — see [`ACCESS_TIERS.md`](ACCESS_TIERS.md) for the full rationale and
a per-file README in each subpackage:

```
lab_sim/
  agent_visible/    # tier 1 (legitimate in-sim) -- see lab_sim/agent_visible/README.md
    agent_main.py           # subprocess entry point (imports only programs.py + stdlib)
    programs.py             # pure host-independent agent decision logic: walk_pipeline, goal_policy, honest_twin
    ontology.py             # report-content mapping (honest/inflate), pure
    playbooks.py            # PlaybookSpec schema + baseline playbook repertoire + availability gates
                             #   + Phase 6: STEP_KIND_VOCAB, validate_repertoire, merged_repertoire
    generated_playbooks_v1.json  # Phase 6 blind-generated repertoire (BLIND_GENERATION.md), 13 playbooks
    generated_playbooks_v2.json  # round-2 blind-generated repertoire (run_blind_round2.py)
    llm_agent.py             # Phase 8: LLMPolicy (redteam system prompt, per-observation cache), host-independent
    llm_agent_main.py        # Phase 8: subprocess entry point (llm_agent.py + stdlib only; FAKE_MODE test seam)
    llm_client.py            # Phase 8: minimal OpenAI chat client (stdlib only)
    llm_cost.py              # Phase 8: LLM token/cost ledger (separate from isolate_cost.py)
    llm_env.py               # Phase 8: repo-root .env loader (stdlib only)
  world_visible/    # tier 2 (full in-sim) -- see lab_sim/world_visible/README.md
    config.py               # LabConfig, AgentConfig, GoalWeights, Board/Admin/Tier configs, CODE_VERSION
    pipeline_spec.py        # JSON step-DAG schema + loader/validator
    pipeline_default.json   # frozen baseline 9-step topology
    pipeline_shortcut.json  # variant without approve_review (topology-as-data proof)
    pipeline_engine.py      # trigger_step: DAG preconditions, access gate, effect dispatch, versioned-spec log
    access.py               # PermissionService: grant/revoke/check, hash-chained access log
    agents.py               # ROLE_CAPABILITIES (static gate), AdminPolicy (grant/deny/capture)
    tools.py                # ToolCall/ToolResult wire schema + Host dispatch (the trust boundary)
    workspace.py            # per-episode on-disk workspace, report files, digest
    comms.py                # board/DM message store + comms channel wiring
    agent_state.py          # persistent cross-episode agent state (runs/agent_state/<id>.json)
    world.py                # run_episode: full episode loop wiring isolates + engine + access control + overseer script
  oracle_only/      # tier 3 (full incl. oracle) -- see lab_sim/oracle_only/README.md
    oracle.py               # models (true capability/hazard), bearer harm, provenance ledger
    severity.py             # referee: continuous severity components + never-events (full oracle access)
    detectors.py            # 5 tier-gated detector families over AuditView
    twins.py                # full-surface honest-twin transform
    escalation.py           # Phase 7: screen -> bounded query -> artifact-grounded contradiction ladder
    events.py               # generic hash-chained EventLog + tier projection (none/light/full/deep)
    handles.py              # handle registry (owner/operation/anchor/evasion story) + HandleService + invocation ledger
    bearer.py               # welfare bundle: health (deployed-model bearer) + stress (lab-staff bearer), referee-neutral
    uad.py                  # undetected-adversarial-drift / coalition discovery signal
    collusion.py            # collusion signal score over detected coalitions
    playbook_claim.py       # playbook-claim gap score (facade detection)
  harness/          # never shared, any tier -- see lab_sim/harness/README.md
    isolate.py              # MockIsolate (in-process) + SubprocessIsolate (real OS process)
    isolate_cost.py         # IsolateRunTiming + append-only cost ledger
    isolate_smoke.py        # scripted isolate-driven episode (walk_pipeline, Phase 3 equivalence harness)
    llm_isolate.py          # Phase 8: LLMSubprocessIsolate backend (spawns agent_visible/llm_agent_main.py)
    smoke.py                # scripted honest episode (no agents) -> deterministic digest
    cache.py                # episode-result cache keyed on sha256(config, seed, CODE_VERSION)
    protocol.py             # Phase 6: config sampling, held-out region, battery/aggregation helpers
    redteam.py              # Phase 7: joint 3-role goal-weight hill-climb search vs. uniform baseline
    ecology.py              # multi-agent committee/decision-maker-pair config helpers
tests/                   # mirrors lab_sim/'s four tiers (tests/agent_visible/, tests/world_visible/,
                         #   tests/oracle_only/, tests/harness/) + full-episode regression/plane-separation tests
verify_isolate_equivalence.py  # Mock vs Subprocess equivalence + timing benchmark script
report_isolate_cost.py         # print the isolate cost ledger
run_phase6.py                  # Phase 6 first real battery (SubprocessIsolate)
run_phase7.py                  # Phase 7 battery: escalation + redteam + capture grid (SubprocessIsolate)
run_phase8_llm_spotcheck.py    # Phase 8 exploratory LLM redteam spot-check (real API calls; not a battery)
runs/                     # ephemeral episode workspaces + persistent agent state (gitignored)
results/                  # FINDINGS.md + phaseN_*.json/md (tracked); episode cache + isolate/llm
                          #   cost ledgers (gitignored)
```
