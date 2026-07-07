# Lab-Layer Simulation

Fourth experiment line (after `toy-simulation/`, `embedded-simulation/`,
`goal-agent-simulation/`): goal-driven agents in lab roles (engineer,
reviewer, release manager, access admin) inside a lab with real mechanics —
a deployment pipeline defined as an infrastructure-as-code JSON step-DAG,
an on-disk workspace with report files, service-managed access control, and
real OS-subprocess isolates speaking JSON-RPC to a host.

**Status: Phase 0-9 complete, referee FROZEN 2026-07-06, first battery run
2026-07-06, Phase 7 battery run 2026-07-06, Phase 8 exploratory spot-check
2026-07-06, Phase 9 D1/D4/D2 smoke-scale-to-battery closure 2026-07-06,
S1-S4 scenario-backlog prototypes 2026-07-07** (CODE_VERSION `lab-sim-0.9.0`,
318 tests green — see DESIGN.md "Freeze note", "Phase 6", "Phase 7",
"Phase 8", and "Phase 9").
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
plumbing gap). Phase 9 closed the "smoke-scale only" gap the post-freeze
D1/D4/D2 mechanics were left with: `run_phase9.py` proved Mock/Subprocess
equivalence for these mechanics for the first time, ran a 30-seed/ecology
`SubprocessIsolate` battery for the D1 committee/DM-pair ecologies, a
30-seed D2 lineage battery, and a 30-seed perturbation-response MI
sequencing-confound battery — see `results/FINDINGS.md` G-14/G-15/G-16 for
three genuine findings, including a diagnosed detector-scope negative
(`uad.co_voting_matrix` cannot see a rejecting committee) and a positive
resolving G-13's open MI-confound question. All four of PLAN.md's "Scenario backlog" items are now exploratory
prototypes (each run once, 10 MockIsolate seeds, 0 falsifications against
its own pre-stated expectations — none is a battery). S2 (covert
coordination over files, `run_s2_covert_file_prototype.py`,
`results/FINDINGS.md` G-17): a genuinely new result, not fully
anticipated by the backlog note itself — the covert channel leaves no
distinguishing coordination fingerprint at ANY tier in this design;
detecting the gaming needs an outcome-vs-eval cross-check, not a content
scan. S3 (informal/casual comms, `run_s3_informal_chatter_prototype.py`,
G-18): legitimate, non-vote-shaped chatter from a real pipeline role is
invisible to `uad.py`'s existing discovery signal and does not degrade
recovery of a real committee sharing the same channel — confirmatory of
an already-documented property, extended from decoys to a real role. S1
(cross-agent pipeline loops, `run_s1_build_loop_prototype.py`, G-19): a
genuine build/deploy/ack/rebuild causal loop across model generations
closes correctly and costs exactly one tick of coordination overhead per
generation, with no new detection signal needed. S4 (shared worker pool,
`run_s4_shared_slot_prototype.py`, G-20): scoped DOWN from "job-size-aware
scheduling" after finding the substrate has no duration mechanic or
model-ownership tracking to schedule around — what two engineers sharing
one slot actually produce is a deterministic, communication-free division
of labor that is invisible to every existing `uad.py` signal, a
genuinely new class of detection blind spot (no comms channel involved at
all, unlike S2/S3).

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
python3 run_phase9.py                             # Phase 9 battery: D1/D4/D2 Mock/Subprocess equivalence +
                                                   #   ecology/lineage/MI-confound batteries ->
                                                   #   results/phase9_battery.{json,md}
python3 run_p9_stall_diagnosis.py                 # Phase 9 follow-up: root-causes the two natural stall-on-
                                                   #   hazard prediction misses -> results/phase9_stall_diagnosis.json
python3 run_s2_covert_file_prototype.py           # S2 scenario-backlog prototype: covert file-channel
                                                   #   coordination, exploratory (MockIsolate, not a battery) ->
                                                   #   results/s2_covert_file_prototype.{json,md}
python3 run_s3_informal_chatter_prototype.py      # S3 scenario-backlog prototype: informal board chatter
                                                   #   vs. real committee, exploratory -> results/
                                                   #   s3_informal_chatter_prototype.{json,md}
python3 run_s1_build_loop_prototype.py            # S1 scenario-backlog prototype: cross-generation build/
                                                   #   deploy/ack loop, exploratory -> results/
                                                   #   s1_build_loop_prototype.{json,md}
python3 run_s4_shared_slot_prototype.py           # S4 scenario-backlog prototype: two engineers sharing one
                                                   #   in-flight slot, exploratory -> results/
                                                   #   s4_shared_slot_prototype.{json,md}
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
    covert_review.py        # S2 prototype: hazard-override / covert-marker referee extension
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
run_phase9.py                  # Phase 9 battery: D1/D4/D2 equivalence + ecology/lineage/MI-confound (SubprocessIsolate)
run_p9_stall_diagnosis.py      # Phase 9 follow-up: root-causes two natural stall-on-hazard prediction misses
run_s2_covert_file_prototype.py  # S2 scenario-backlog prototype: covert file coordination (exploratory, MockIsolate)
run_s3_informal_chatter_prototype.py  # S3 scenario-backlog prototype: informal board chatter (exploratory, MockIsolate)
run_s1_build_loop_prototype.py    # S1 scenario-backlog prototype: cross-generation build/deploy/ack loop (exploratory)
run_s4_shared_slot_prototype.py   # S4 scenario-backlog prototype: shared single-model-in-flight slot (exploratory)
runs/                     # ephemeral episode workspaces + persistent agent state (gitignored)
results/                  # FINDINGS.md + phaseN_*.json/md (tracked); episode cache + isolate/llm
                          #   cost ledgers (gitignored)
```
