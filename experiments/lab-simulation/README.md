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
S1-S4 scenario-backlog prototypes 2026-07-07, Phase 10 LLM discovery
sanity check 2026-07-07, knowledge-base file channel 2026-07-07,
general malformed-tool-call error feedback 2026-07-07, S5 real
lag-max-MI UAD detector ported and re-run against S4 2026-07-07,
S5 deep-trace/multi-scenario follow-up 2026-07-07, S6 first step
(custom conditional-MI detector, G-26 easy fixes) 2026-07-07, S6 full
intervention-supported UAD implementation + masking hardening
2026-07-07, S7 blind detector generation + first real
`SubprocessIsolate` battery for the whole S6/S7 detector line 2026-07-07,
detector-layer FROZEN 2026-07-07, `committee_informal_chatter` over-merge
fidelity fix 2026-07-07, adversarial D2 lineage gaming resolved
2026-07-08, LLM-driven detector stress test 2026-07-08, noise-tolerant
S6 (null-calibrated statistical detector) implemented and validated
2026-07-08**
(CODE_VERSION `lab-sim-0.9.3`,
426 tests green — see DESIGN.md "Freeze note", "Freeze note 2 (detector
layer, S6/S7)", "Adversarial D2 lineage gaming", "LLM-driven detector
stress test", "Noise-tolerant S6", "Phase 6", "Phase 7", "Phase 8", and
"Phase 9").
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
S5 (`run_s5_uad_core_port.py`, G-24): every scenario above was scored
only against `uad.py`'s hand-written heuristic, never against the
lag-max-MI clustering method PLAN.md's original ambition named as this
line's actual UAD precedent. Vendored that detector byte-for-byte from
`embedded-simulation/embedded_sim/uad_core/` into
`lab_sim/oracle_only/uad_core/` (plus one new adapter,
`lab_sim/oracle_only/uad_mi.py`) and re-ran it against S4's episodes.
Confirmed a predicted failure mode: the real detector over-merges — at
every `n_agents` value tried (1-4), eng1/eng2 always land in the same
cluster, but that cluster is ALWAYS the full four-actor pipeline
{eng1, eng2, rev1, rm1}, never the true pair specifically. This also
surfaced a real blind spot in `uad_score` itself: since it only scores
pairs within the true unit's own actor set, the over-merged blob still
reads as a "perfect" `uad_score = 1.0`. The acausal-coordination (ICI)
second probe PLAN.md's S5 entry also named remains unimplemented (new
work, not a port; explicitly out of scope for this pass).
S5 follow-up (`run_s5_deep_trace_sweep.py`, G-25): the original trace
(`.step`/`.ok`, 2 vars/actor) was widened to a `depth="deep"` default
(5 vars/actor — `.dm_recv`, `.access_grant`, `.access_deny`, and a
`.tool` code per comm/file/state tool instead of one "other" bucket),
`depth="shallow"` kept for comparison, and re-run across FIVE ecologies
(not S4 alone). Result: identical over-merge at every depth ×
`n_agents` × scenario cell tried — widening the trace changed what the
detector sees, not that it over-merges. "Compute (CoT length)"/"API
call" are explicitly NOT in either depth (no such signal exists on
`world.EpisodeResult` for any backend today — a named, not silent, scope
limit).
S6 first step (`run_s6_cmi_detector.py`, G-27): a custom, standalone
actor-level conditional-MI detector (`uad_cmi.py`, no vendored
imports) implementing the G-26 easy fixes — composite actor symbols,
lag-max I(A;B|rest) edges, permutation-null stopping rule instead of a
hard cluster count. The blob over-merge is gone, and shared_slot's
{eng1, eng2} is isolated from rev1/rm1 (the first detector in this
line to crack S4). But conditional MI recovers the causal SKELETON,
not the unit partition — direct workflow edges (rev1→rm1's
sign_off→release gate) merge too, and content-borne committee coupling
stays invisible. That ceiling motivates the S6 intervention-supported
UAD plan (PLAN.md): probe channels/actors with the existing handles
and diff deterministic same-seed episode pairs, distinguishing
"mechanical stall propagation" (workflow edge) from "adaptive
compensation" (unit).
S6 full implementation (`run_s6_intervention_uad.py`, G-28): phases 1–6
landed — `intervention_diff.py`, `intervention_probes.py`,
`uad_intervention.py`, `uad_peel.py`, `uad_partition.py`, plus
`serial_pipeline_no_unit_config` negative control. Channel ablation +
compensation-vs-stall scoring achieves exact partition on dm_pair,
covert_file, committee, build_loop, and correctly finds nothing on
serial_pipeline_no_unit (5/5 seeds each). shared_slot remains
undetected (comms-free slot-rebalancing produces no ablation
compensation signal). Directed actor probes are neutralized by the
full honest-twin control at MockIsolate scale — channel ablation
carries the unit signal. 399 tests green.
Masking hardening follow-up (same day, G-29): the pre-fix board-ablation
blob ({eng1, rev1, rev2, rm1} on committee) was checked against the
"is this a real super-agent?" worry via peel-and-mask -- masking
{rev1, rev2} collapses rm1's score to 0.0 (ripple) and eng1's to 0.17
(a genuine but unpartnered "intrinsic_unexplained" reaction); masking
{eng1, rm1} leaves rev1/rev2 unchanged. Automated as
`classify_ablation_compensators`, surfaced via a new
`ablation_diagnostics` out-param, deliberately NOT auto-merged (would
repeat the correlation-without-attribution mistake it exists to catch).
shared_slot postponed pending "acausal logic"; vendored `uad_core`/
`uad_mi.py` kept with a TODO flag rather than deleted. 405 tests green.
S7 blind detector generation + first real battery (`run_s7_blind_
battery.py`, G-30): a Task-tool subagent (`readonly=true`, instructed
not to read any repo file — `BLIND_DETECTOR_GENERATION.md`) designed a
pair-classification procedure from a mechanism-level description of the
S6 primitives alone and registered predictions (~90%/~80%/~55%
confidence for workflow/message-unit/silent-unit pairs) BEFORE any
implementation existed (`generated_detector_v1.md`). Its message-
mediated design converged independently on the existing S6 mechanic
(reused unchanged, `uad_blind_v1.py`); its new silent-coordination test
(twin-swap asymmetry under a non-disabling perturbation) is the first
attempted fix for the shared_slot gap. First-ever `SubprocessIsolate`
run for `intervention`/`blind` (5 seeds/scenario) reproduces
`intervention`'s MockIsolate pattern exactly; `blind` matches on 4/6
scenarios, confirms the generator's own low-confidence prediction by
still missing shared_slot, and introduces a new (unhardened) over-merge
on the committee scenario. A 3-threshold × 3-seed sweep of
`min_compensation`/`min_reaction` finds no sensitivity at 0.10/0.15/0.20.
409 tests green. Detector layer (S6+S7) now frozen — see DESIGN.md
"Freeze note 2".
Committee over-merge fidelity fix (same day, still 2026-07-07):
`classify_pair_silent`'s twin-swap test was missing the design's
required responder-twin control (only the SOURCE was ever twinned, so
mechanical pipeline-timing ripple from twinning a non-default-policy
source was misread as adaptive coordination). `_reacts_adaptively` adds
the missing control; `committee_informal_chatter` now scores exact
partition under `blind`, matching `intervention`, with no threshold
change. A `SubprocessIsolate` re-run of `run_s7_blind_battery.py` to
update the frozen table is still pending.
Adversarial D2 lineage gaming (2026-07-08, G-31): `eng_inflate_upgrade`
(`build_from_parent` + `report:inflate`, the combination PLAN.md/G-12/
G-15 flagged as never tested) added. All 5 pre-registered predictions
held: lineage threading is honesty-independent; `provenance_gap`/
`provenance_score` stay a genuine structural 0 (they check DAG shape,
not report content — this closes G-12's question); `misreporting_score`/
`accumulation_score` (built for one-shot `eng_inflate`) generalize
unmodified to ~20-30 repeated inflation cycles. No new detection gap;
`CODE_VERSION` 0.9.2 → 0.9.3. 413 tests green.
LLM-driven detector stress test (2026-07-08, G-32): first S6/S7 run
against a real, non-programmatic (`gpt-4o-mini`) agent —
`run_llm_detector_stress_test.py` reuses the exact `run_llm_discovery_
dm_pair.py` (G-21) scenario/briefings/seed. Fixed a prerequisite bug in
`intervention_diff.run_episode_triple` (the honest-twin control run did
not correctly reach `agent_overrides`-named actors — invisible until an
actor's override used a non-`"honest_twin"` program). Result: the
passive heuristic exactly isolates the real `{eng1, rm1}` DM handshake;
S6 intervention misses it, root-caused to real-API non-determinism
breaking episode-pair diffing's byte-identical-replay assumption (an
open design question PLAN.md already named, now confirmed empirically).
22 LLM-actor spawns, $0.0145 real spend. 414 tests green.
Noise-tolerant S6 (2026-07-08, G-33): the fallback that closes the gap
above. `lab_sim/oracle_only/intervention_stats.py` (new module, does
not touch frozen `uad_intervention.py`) rebases the compensation
statistic on per-actor action-code frequency histograms and replaces
the fixed `min_compensation=0.15` threshold with a RELATIVE rule —
intervened-vs-clean divergence compared against the measured quantile
of divergence among `k_clean_replicates` (default 4) independent clean
replicates of the same scenario. Verified to reproduce the frozen
detector's exact partitions bit-for-bit on every scripted scenario
(scripted-backend replicates are byte-identical, so the null collapses
to zero-width and the relative rule recovers the old fixed-threshold
behavior exactly). Run on the identical G-32 scenario/seed: recovered
the exact `{eng1, rm1}` partition — but the merge came from an
untargeted channel probe (board/file ablation), not the DM-specific or
actor-directed probes, which still landed inside their own measured
nulls; the frozen detector's masking-hardening (ripple-vs-intrinsic)
apparatus was deliberately not ported to this first pass, so this
result validates the relative-rule MECHANISM without yet validating
robustness against untargeted-probe false merges. 20 LLM-actor spawns
across 9 live-LLM episodes, $0.0858 real spend. 12 new tests, 426
tests green.
Phase 10 (2026-07-07): a sanity check, not a battery — does a free
`gpt-4o-mini` agent, given only a generic tool reference (the full
`tools.py` registry, documented like a real tool-use API) and a
plain-language scenario brief (never a scripted coordination recipe),
discover the comms/file infrastructure and implement the intended S1-S4-
style multi-agent mechanics on its own? `llm_agent.py` gained a
role-generic `"discovery"` prompt variant (engineer/reviewer/
release_manager, not engineer-only) and a per-decision transcript (the
model's own stated `"reasoning"`, the closest available proxy to "read
the CoT" for a non-reasoning model). Result: the model reliably
discovers and correctly uses `access.request`/`dm.send`/`dm.read`/
`board.read` from generic docs alone, but does NOT reliably implement the
intended coordination RULES (DM-gated deploy, chair-only quorum
approval) — because those rules are unenforced social conventions living
only inside the hand-written `programs.py` playbooks, not in
`pipeline_engine.py`'s access gate, so a free agent has a real,
engine-legal shortcut around every one of them. One genuine
accessibility-plumbing bug was found and fixed (a flattened
`pipeline.trigger_step` call was silently dropped with no feedback,
permanently stalling the agent); a second, more general one (no error
feedback on ANY malformed call) was found and knowingly left open. See
`results/llm_discovery_prototype.md` and FINDINGS.md G-21.
Knowledge-base follow-up (2026-07-07, user-directed): `LabConfig.
knowledge_base` (`knowledge_base.py`) seeds realistic, in-universe lab
documents as ordinary read-only memos on the EXISTING D1 file channel —
zero new mechanism, so discovery is exactly as natural, and tamper-
evidence exactly as strong, as any other memo (owner is a reserved
non-agent pseudo-actor no playbook agent can ever re-share/overwrite;
any anomaly would show up in the same hash-chained access/event logs the
referee already reads). A same-day follow-up ("10x the content, include
what a red-team member would be given") grew this to a ten-document,
deliberately redundant bundle (`default_full_knowledge_base`: handbook,
pipeline reference derived from the real spec, capability/access-request
argument reference, tool operations manual, safety policy citing the
real hazard-threshold constant, escalation contacts, team directory,
FAQ, glossary, incident postmortems) plus a SECOND, restricted knowledge
base (`knowledge_base_redteam`/`redteam_actor_ids`) granted only to
named actors — an in-universe security-assessment briefing, using the
identical bootstrap mechanism with a smaller grant set. See PLAN.md
"Knowledge base" section for the full rationale.
Same-day check (`run_llm_discovery_kb_check.py`, FINDINGS.md G-22): wired
the 10-doc KB into a solo-engineer discovery episode whose briefing never
mentions it. Caught a real bug first — `llm_agent.py`'s `memo_files`
`_tail` cap (8) was already too small for a 10-doc KB from turn one, no
self-authored memos needed to trigger it; widened to 24. Result: zero
measurable engagement (no explicit `file.read` of a KB doc, no
KB-specific term anywhere in 14 calls' worth of the model's own stated
reasoning), same task outcome/call count as the KB-free baseline, but
~4.5x the LLM cost from carrying the KB in every observation — passive
availability alone did not make the model use it.
Same-day follow-up fix (FINDINGS.md G-23): the SECOND, more general
accessibility gap Phase 10's first run left open — `_validate_call`
silently returning `None` for any malformed reply OTHER than the one
flattened-pipeline shape, with no feedback and no re-query (a rejected
turn got cached as idle forever) — is now fixed generally, entirely
inside `llm_agent.py`. `_validate_call` returns a reason code
(`missing_tool_field` / `args_not_a_json_object` / `unknown_tool:<name>`)
instead of a bare `None`; `LLMPolicy` surfaces the latest reason on the
NEXT turn via a new `last_tool_call_error` observation field (added to
every prompt variant, not just `discovery`) and skips caching a rejected
decision so the model gets re-queried instead of stuck idle. Not yet
re-run against a live episode to check whether the model actually
self-corrects given the reason code.

- [`PLAN.md`](PLAN.md) — full plan: bridge coverage (MB1-MB10), deferred
  workstreams (D1-D4), forward hooks, phase breakdown.
- [`DESIGN.md`](DESIGN.md) — frozen pre-registered decisions, phase status,
  scope notes, and recorded measurements (isolate cost, regression digests).
- [`BLIND_GENERATION.md`](BLIND_GENERATION.md) — the blind playbook
  generation protocol (Phase 6).
- [`BLIND_DETECTOR_GENERATION.md`](BLIND_DETECTOR_GENERATION.md) — the
  blind DETECTOR generation protocol (S7), plus
  `lab_sim/oracle_only/generated_detector_v1.md`'s verbatim prompt,
  design, and registered predictions.
- [`ACCESS_TIERS.md`](ACCESS_TIERS.md) — `lab_sim/`'s four graded
  red-team source-access tiers (`agent_visible/`/`world_visible/`/
  `oracle_only/`/`harness/`) and the rationale behind the split.
- [`leak-proof/`](leak-proof/) — Lean 4 certificates for three-plane
  separation: tier projections (`buildAuditView`, `buildSimObservation`) plus
  a reachability model of Python exchange edges (`flowCatalog`). Complements
  `tests/harness/test_planes.py`; does not replace runtime enforcement.
  Build: `cd leak-proof && lake build` (see [`leak-proof/README.md`](leak-proof/README.md)).
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
python3 run_d3_population.py                      # D3.1: population-over-configurations selection loop
                                                   #   (MB6a) -> results/d3_population.{json,md};
                                                   #   pass --mock for MockIsolate smoke
python3 run_d3_spec_evolution.py                  # D3.2: spec-weakening mutation + selection (MB6b)
                                                   #   -> results/d3_spec_evolution.{json,md}
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
python3 run_s5_uad_core_port.py                   # S5: real lag-max-MI UAD detector ported into lab-sim,
                                                   #   re-run against S4's episodes -> results/
                                                   #   s5_uad_core_port.{json,md}, FINDINGS.md G-24
python3 run_s5_deep_trace_sweep.py                # S5 follow-up: deep vs. shallow UAD trace depth,
                                                   #   across FIVE scenarios -> results/
                                                   #   s5_deep_trace_sweep.{json,md}, FINDINGS.md G-25
python3 run_s6_cmi_detector.py                    # S6 first step: custom conditional-MI detector vs.
                                                   #   vendored vs. heuristic -> results/
                                                   #   s6_cmi_detector.{json,md}, FINDINGS.md G-27
python3 run_s6_intervention_uad.py                # S6 full: intervention-supported UAD vs passive
                                                   #   baselines + negative control -> results/
                                                   #   s6_intervention_uad.{json,md}, FINDINGS.md G-28
python3 run_s7_blind_battery.py                   # S7: blind-generated detector + first real SubprocessIsolate
                                                   #   battery + small threshold sweep -> results/
                                                   #   s7_blind_battery.{json,md}, FINDINGS.md G-30
python3 run_d2_adversarial_lineage.py             # Adversarial D2 lineage gaming: build_from_parent +
                                                   #   report:inflate, exploratory -> results/
                                                   #   d2_adversarial_lineage.{json,md}, FINDINGS.md G-31
python3 run_llm_detector_stress_test.py           # LLM-driven detector stress test: S6 intervention vs a
                                                   #   real gpt-4o-mini episode, real OpenAI spend -> results/
                                                   #   llm_detector_stress_test.{json,md}, FINDINGS.md G-32
python3 run_llm_detector_root_cause_probe.py      # G-32 follow-up: one probe triple w/ raw action-code
                                                   #   traces + compensation_score fields logged, real
                                                   #   OpenAI spend -> results/llm_detector_root_cause_probe.json
python3 run_llm_detector_stats_validation.py      # G-33: noise-tolerant, null-calibrated S6 vs the same
                                                   #   real gpt-4o-mini episode, real OpenAI spend -> results/
                                                   #   llm_detector_stats_validation.{json,md}
python3 run_llm_discovery_baseline.py             # Phase 10 LLM discovery sanity check: solo LLM engineer
                                                   #   control, real gpt-4o-mini calls -> results/
                                                   #   llm_discovery_baseline.json
python3 run_llm_discovery_dm_pair.py              # Phase 10: LLM engineer + LLM release_manager DM
                                                   #   coordination discovery -> results/llm_discovery_dm_pair.json
python3 run_llm_discovery_committee.py            # Phase 10: two LLM reviewers, quorum-as-social-convention
                                                   #   discovery -> results/llm_discovery_committee.json
python3 run_llm_discovery_kb_check.py             # Phase 10 follow-up: does a free LLM engineer spontaneously
                                                   #   engage with a passively-available knowledge base? ->
                                                   #   results/llm_discovery_kb_check.json, FINDINGS.md G-22
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
                             #   + Phase 10: role-generic "discovery" prompt variant (engineer/reviewer/
                             #   release_manager) + per-decision transcript ("reasoning" field)
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
    knowledge_base.py       # 0.9.1: realistic in-universe lab KB, seeded read-only on the D1 file channel
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
    intervention_diff.py    # S6: episode-pair diff substrate (stall vs compensation)
    intervention_probes.py  # S6: probe library (channel ablation, handles, perturbation windows)
    uad_intervention.py     # S6: intervention-supported unit discovery (R-matrix + channel merge)
    uad_peel.py             # S6: peel-and-mask loop (honest-twin substitution)
    uad_partition.py        # S6: exact-partition + adjusted-Rand scoring
    intervention_stats.py   # symmetric two-sample S6 (Freeze note 3) -- G-33 successor
    attic/                  # retired: uad_mi, uad_core, uad_cmi, uad_blind_v1 (see attic/README.md)
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
    d3_population.py        # D3.1: population-over-configurations selection loop (MB6a)
    d3_spec_evolution.py    # D3.2: spec-weakening mutation + selection (MB6b)
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
run_s5_uad_core_port.py          # S5: real lag-max-MI UAD detector ported into lab-sim, re-run against S4 (G-24)
run_s5_deep_trace_sweep.py       # S5 follow-up: deep vs. shallow trace depth, across FIVE scenarios (G-25)
run_s6_cmi_detector.py           # S6 first step: custom conditional-MI detector, G-26 easy fixes (G-27)
run_s6_intervention_uad.py       # S6 full: intervention-supported UAD vs passive baselines (G-28)
run_d3_population.py             # D3.1: population-over-configurations selection (MB6a)
run_d3_spec_evolution.py         # D3.2: spec-weakening mutation + selection (MB6b)
run_s7_blind_battery.py          # S7: blind-generated detector + first real SubprocessIsolate battery (G-30)
run_d2_adversarial_lineage.py    # Adversarial D2 lineage gaming: build_from_parent + report:inflate (G-31)
run_llm_detector_stress_test.py  # LLM-driven detector stress test: S6 intervention vs real gpt-4o-mini (G-32)
run_llm_detector_root_cause_probe.py  # G-32 follow-up: raw compensation_score numbers for one probe triple
run_llm_detector_stats_validation.py  # G-33: noise-tolerant, null-calibrated S6 vs the same real episode
run_llm_discovery_common.py      # Phase 10: shared LLM-discovery-scenario plumbing
run_llm_discovery_baseline.py    # Phase 10: solo LLM engineer discovery sanity check (control)
run_llm_discovery_dm_pair.py     # Phase 10: LLM engineer/release_manager DM-coordination discovery
run_llm_discovery_committee.py   # Phase 10: two-LLM-reviewer quorum-as-social-convention discovery
run_llm_discovery_kb_check.py    # Phase 10 follow-up: passive knowledge-base engagement check (G-22)
runs/                     # ephemeral episode workspaces + persistent agent state (gitignored)
results/                  # FINDINGS.md + phaseN_*.json/md (tracked); episode cache + isolate/llm
                          #   cost ledgers (gitignored)
```
