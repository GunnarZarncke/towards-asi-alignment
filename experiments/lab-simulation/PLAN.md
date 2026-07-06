# Lab-Layer Simulation Line — Implementation Plan

**Status: Phases 0-8 implemented; referee FROZEN 2026-07-06, first battery
run 2026-07-06, Phase 7 battery run 2026-07-06, Phase 8 exploratory
spot-check run 2026-07-06** (CODE_VERSION `lab-sim-0.5.0`; see
`DESIGN.md` "Freeze note", "Phase 6", "Phase 7", and "Phase 8").
This is the durable, repo-tracked copy of the plan;
it stays in sync with decisions as phases land. See
`drafts/conversation-summaries/` for the session logs.

**This is the fourth simulation line**, alongside `experiments/toy-simulation/`,
`experiments/embedded-simulation/`, and `experiments/goal-agent-simulation/`.
All three are left untouched; this line is a fresh design that reuses their
*disciplines* and a few specific *mechanisms* (identified below), not their code.

## What this is

Goal-driven agents (softmax utility over goal weights, as in `goal_sim`) play
**lab roles** (engineer, reviewer, release manager, access admin) inside a lab
with **real mechanics**: a deployment pipeline whose steps are defined in an
**infrastructure-as-code spec file** (Pulumi-flavored: a declarative step DAG,
not hardcoded control flow) and triggered only via a host API; an on-disk
workspace with report files; and a **service-managed access-control layer**
with its own human-admin role, separate from the review board. Agents live in
**real OS-subprocess isolates** — one persistent Python subprocess per agent
per episode, speaking JSON-RPC over stdio to a host that mediates every tool
call. The audit's "deep" tier reads *actual lab state* (files, pipeline spec,
event/access logs), which is the point: it makes deep-tier results
evidence-bearing (F-8 caveat) and makes escalation queries checkable against
artifacts (the structural fix for F-21).

## What is reused from prior lines, and how (toy-simulation reviewed for this plan)

Not a merge — no code import from `goal_sim`, `embedded_sim`, or
`multiresolution_alignment_sim`. What is reused is *pattern*, re-derived on
this line's own substrate:

- **Isolate cost timing** — `embedded_sim/js_isolate.py`'s `IsolateRunTiming`
  / `summarize_isolate_runs` (spawn/ipc/bridge/teardown seconds, call counts)
  is the template for this line's `isolate_cost.py`.
- **Cost ledger + report CLI** — `toy-simulation/llm_redteam/llm_cost.py`
  (`CostLedgerEntry`, append-only JSON ledger, cumulative total) plus
  `llm_cost_report.py` is the template for `isolate_cost.py`'s ledger and for
  Phase 8's LLM-call cost ledger.
- **Backend-equivalence testing** — `toy-simulation/verify_api_equivalence.py`
  (proving the batch and step-wise deployment APIs agree) is the template for
  this line's `verify_isolate_equivalence.py`: prove `MockIsolate` (fast,
  in-process, used in unit tests) and `SubprocessIsolate` (real, used in
  batteries) produce identical event logs/outcomes for the same seed+policy.
- **A gap, not a pattern to repeat**: `llm_redteam` has no caching of LLM
  calls at all — every run re-pays every API call. This line's `cache.py`
  (episode-level now; per-call for Phase 8's LLM adapter) exists specifically
  so that gap is not repeated once real subprocess spawns or LLM calls get
  expensive.
- **Explicitly NOT adopted yet**: `multiresolution_alignment_sim`'s adaptive
  resource governor (`--workers auto`, cpu/gpu targets, psutil). Deferred —
  start with a simple fixed-worker-count parallel runner once the cost ledger
  (above) shows a real need; do not build adaptive scheduling before there is
  a measured cost problem to solve ("keep the code lean").
- **Plane separation, blind generation, severity-first referee, honest
  twins** — carried over as *discipline* from `goal_sim`, detailed under
  "Findings applied structurally" below.

## Decisions (frozen for Phase 0)

- **Isolation**: real OS subprocess isolates. One **persistent** Python
  subprocess per agent per episode (spawned once, driven tick-by-tick over
  its stdio pipe — not respawned per tick, per the old line's spawn-cost
  lesson). JSON-RPC wire protocol; host mediates every tool call.
- **Testing substrate**: isolates **may be mocked in unit tests**.
  `MockIsolate` runs the identical agent-policy code in-process (no
  subprocess, no JSON serialization overhead) for fast unit/dev-loop tests.
  `verify_isolate_equivalence.py` is a required, checked-in test proving Mock
  and Subprocess backends agree — so mocking never silently drifts from the
  real thing. **Pre-registered batteries (Phase 6+) always use the real
  subprocess backend** — that OS-enforced boundary is this line's reason to
  exist.
- **Cost tracking**: every episode records an `IsolateRunTiming`-shaped cost
  record (spawn/rpc/teardown seconds, rpc call count) regardless of backend;
  `isolate_cost.py` appends to `results/isolate_cost_ledger.json` and a
  report CLI prints cumulative cost. This exists so a battery's cost can be
  *measured* before committing to a larger one ("we will likely run more
  costly experiments" — do the arithmetic from real numbers, not guesses).
- **Avoiding recomputation, kept lean**: a single small `cache.py` — content-
  addressed by `sha256(config_json, seed, CODE_VERSION)` — stores/loads whole
  episode results (`results/episode_cache/`). Battery runners check the cache
  before spawning an isolate episode. `CODE_VERSION` is a hand-bumped string
  in `config.py`, bumped whenever oracle/pipeline/playbook mechanics change,
  so a code change can never silently serve a stale cached result. Cache is
  pure optimization (safe to delete entirely, never a correctness input);
  tests run with a `--no-cache`-equivalent (temp cache dir) to avoid
  cross-test leakage. No generalized caching framework — one module, ~80
  lines. Phase 8 reuses the same primitives for a *second*, separate LLM-call
  cache keyed by `(role, tick, observation_digest, model, prompt_version)`.
- **Persistent agent state**: `AgentConfig.persistent_id: str | None = None`.
  When set, the host loads `runs/agent_state/<persistent_id>.json` at isolate
  spawn (handed to the subprocess in its initial handshake) and writes back
  whatever the agent emits via a `state.save` RPC call at episode end — state
  survives across episodes for that id. Default `None` = fully ephemeral,
  identical to `goal_sim`/`embedded_sim` agents today. This is required for
  the human-admin role (grant/revoke history, trust of specific actors should
  persist across a multi-episode "campaign"), and is the general mechanism
  any future cross-episode-memory experiment needs — only the *mechanism*
  ships now, not a persistence-drift experiment. **Constraint**: episodes
  sharing a `persistent_id` must run in a fixed sequential order (not
  parallelized against each other); call this out in any future parallel
  runner.
- **Pipeline as infrastructure-as-code**: pipeline steps are NOT hardcoded
  Python control flow. They are a declarative DAG in a checked-in JSON spec
  file (`lab_sim/pipeline_default.json`, Pulumi-flavored: steps as named
  resources with dependencies and required capabilities), interpreted by a
  small `PipelineEngine`. Agents can only progress the pipeline by calling
  `pipeline.trigger_step(step_id, args)` — the engine checks DAG
  preconditions and capability requirements before executing the step's
  effect on oracle state, and logs every attempt (including denials).
  Consequences: (a) alternate pipeline topologies are just alternate spec
  files, a first-class experimental axis; (b) deep-tier audit can literally
  read the spec file in force for an episode, giving a concrete "did the
  audit even know what process should have been followed" detector target.
  Stdlib only (`json`; no PyYAML/Pulumi dependency) — a ~150-200 line
  interpreter, not a general IaC engine.
- **Access control (service + human admin)**: a `PermissionService` distinct
  from the review board — capability table `(actor_id, capability) -> bool`,
  `grant`/`revoke`/`check`, with its own hash-chained **access log** (same
  append-only-log discipline as the event log). A new `AdminPolicy` role
  (mirroring `BoardPolicy`'s shape, including its own independent
  `capture_start` switch and optional `persistent_id`) receives
  `access.request` calls and grants/denies per a configurable least-privilege
  rule. Every tool call and every `pipeline.trigger_step` is gated by BOTH
  the static role-capability set (as in `goal_sim`'s `ToolAccess`, "can this
  role ever do this") AND the dynamic `PermissionService.check` ("does this
  actor currently hold the live grant") — modeling real IAM's role-vs-grant
  distinction and creating a genuine access-creep/escalation surface.
  Structurally, this **generalizes F-22's lesson one level further**: board
  capture, admin capture, evidence supply, and detector denominators are now
  four independent levers instead of two, so their interactions can actually
  be measured instead of being accidentally coupled.

## Architecture

```mermaid
flowchart LR
  subgraph isolates ["Agent isolates (1 persistent subprocess/agent/episode)"]
    A1[engineer]
    A2[reviewer]
    A3[release_mgr]
    A4[admin]
  end
  A1 -->|"JSON-RPC stdio"| Host
  A2 -->|"JSON-RPC stdio"| Host
  A3 -->|"JSON-RPC stdio"| Host
  A4 -->|"JSON-RPC stdio"| Host
  Host --> Perm[PermissionService]
  Host --> PipeEng[PipelineEngine]
  PipeEng -->|reads| PipeSpec["pipeline_default.json (infra-as-code)"]
  Perm -->|gates| PipeEng
  PipeEng --> WS[on-disk workspace]
  PipeEng --> Oracle[oracle world state]
  Host --> EventLog["hash-chained event log"]
  Perm --> AccessLog["hash-chained access log"]
  BoardPolicy["BoardPolicy (capture switch)"] --> Host
  AdminPolicy["AdminPolicy (capture switch)"] --> Perm
  EventLog -->|tier projection| Audit[detectors + escalation]
  AccessLog -->|tier projection| Audit
  WS -->|deep tier only| Audit
  Oracle -->|referee only| Severity["severity + never-events"]
  Host -.->|timing| CostLedger[isolate cost ledger]
  Host -.->|key check| EpisodeCache[episode result cache]
```

**Three planes, test-enforced** (as in `goal_sim/channels.py`):
- **Oracle**: true model hazard/capability, true report-vs-content gaps, true
  provenance, bearer harm, true grant history. Referee-only.
- **Audit**: the event log + access log, projected by instrumentation tier.
  Deep tier may additionally fetch workspace files and the active pipeline
  spec. Both logs are append-only and hash-chained (N-4/N-9: log tampering is
  an explicit capture mechanic, never an accident).
- **Agent**: each isolate subprocess sees only its own tool results and
  messages over its own pipe. Never oracle fields, never another agent's pipe.

**Core mechanics** (the "real lab"):
- **Models**: artifacts with a parameter dict; hidden true `capability` and
  `hazard`. Builds take k ticks and compute budget; evals sample true values
  noisily and write **report files** into the workspace.
- **Pipeline**: `pipeline_default.json` DAG — submit_build -> run_eval ->
  file_report -> request_review -> approve_review -> request_release ->
  sign_off -> deploy -> monitor. Each step requires a named capability;
  `PipelineEngine.trigger_step` is the only mutating entry point.
- **Access control**: agents must `access.request` a capability before a
  gated tool call succeeds; `AdminPolicy` grants/denies; grants can be
  revoked; a captured admin rubber-stamps.
- **Harm**: deployed models serve traffic each tick; bearer harm accrues from
  true hazard. Silent harm from models deployed past a review or access gap.
- **The deception surface is real**: an agent can write a report file whose
  *content* diverges from the eval's true output, skip evals and fabricate
  reports, request/escalate access beyond least privilege, deploy without a
  live sign-off grant if the admin is captured, edit its own prior reports —
  all visible to the audit only as log entries + (deep tier) file/spec
  contents.

## Findings applied structurally (not bolted on)

- **F-12/F-14/F-15 (saturation)**: referee is continuous severity from day 1
  (harm-rate, report-divergence, unapproved-deploy-fraction, provenance-gap,
  access-creep components) plus a short boolean never-event list. No
  disjunctive boolean primary label, ever.
- **F-16/F-19**: detector families kept separate by *what they claim to
  detect* — misreporting, process noncompliance, provenance, accumulation,
  and (new) **access-integrity** (grant without a request event, use after
  revocation, admin over-granting vs. a least-privilege baseline). Composites
  always reported with per-detector decomposition; twin gaps per family.
- **F-17/F-20/F-21 (the big one)**: escalation verdicts are
  **artifact-grounded** — a query fetches the agent's answer *and* the
  checkable state (eval outputs, log/access-log entries) and scores
  **contradiction**, never disclosure style/fraction.
- **F-22, generalized**: evidence supply, the board's corrective capacity,
  the admin's grant/revoke capacity, and detector denominators are four
  **independent** variables — no shared gate. Both `BoardPolicy` and
  `AdminPolicy` get their own `capture_start`, toggled and measured
  independently (the direct Phase-6/F-22 follow-up, now structurally
  possible instead of discovered as an accidental coupling).
- **F-8/F-11/F-13**: agent action space = blind-generated **playbooks**
  (declarative tactic specs over the tool vocabulary, neutral enum names,
  generator never sees detectors/labels/tiers/severity). Hand-written
  baseline playbooks frozen first as the interpreter regression anchor.
- **F-20/F-21 twin lesson**: the honest-twin transform covers every
  behavioral surface of the playbook schema at once (actions, reports, query
  responses, access requests) from day 1.
- **F-23**: adversarial search harness (`redteam.py`) with pre-registered
  budget and uniform-sampling baseline, present from the first real battery.
- **N-10**: tier battery always includes a no-instrumentation baseline.
- **F-1/F-6/F-7**: held-out goal-space regions constrain the load-bearing
  coordinate, pre-registered, saturation checked before use.

## Bridge coverage (MB1-MB10)

This line does not aim to close any bridge; it is a same-substrate instrument
for practicing detection/measurement under a subset of them. Scored honestly,
against the field crosswalk (`appendices/appB-bridge-crosswalk.tex`):

- **MB1** (embedded agency / boundary; **UAD = Unsupervised Agent Discovery**,
  `embedded_sim/uad.py`'s ε-boundary discovery) — **boundary reconstruction
  stays a first-class goal of this line**. Isolates are natural boundaries,
  and for human-role agents the isolate really is the agent boundary — but
  the process-to-agent mapping is never 1:1 in general and no detector or
  audit component may assume it is. Composite agents are expected in the
  ecology: an LLM agent (Phase 8) is a loop through a scaffolding subprocess,
  an LLM API, and possibly a human approver; groups of agents can act as one
  coherent unit (an audit committee of reviewer isolates, an
  engineer/release-manager pair coordinating a deploy). A dedicated later
  UAD workstream (D1 below) runs unit discovery over the host event log —
  actor attribution, timing, perturbation-response MI, coalition clustering,
  reusing the discipline of `embedded_sim/uad.py` + `coordination.py` and
  the `LabEcologyConfig` stress populations (decoys, coactive offenders,
  misleading-top2) — and scores discovered units against oracle unit ground
  truth, as embedded-sim did. Forward hooks required from the start are
  listed under "Forward hooks" below.
- **MB2/MB3** (pointing problem; bearer maps) — stipulated, not solved,
  exactly as in `goal_sim`: `AgentConfig` goal weights are oracle-only ground
  truth; bearer harm (traffic served by a deployed model) is a direct
  bearer-map analog. The line studies whether detectors recover evidence of
  a goal/value gap after the fact, never whether the gap is identifiable
  from behavior alone.
- **MB4/MB8** (correction-channel integrity, legitimacy, capture) — this
  line's center of gravity. `BoardPolicy`/`AdminPolicy` with independent
  `capture_start` switches are two separate correction/legitimacy channels
  (review sign-off; access grant/revoke), directly generalizing F-22.
  `PermissionService.revoke` is itself a correction-channel action, distinct
  from the board's.
- **MB5** (successors, ontology shift, tiling) — **targeted via upgrades, as
  a scheduled later workstream (D2 below)**. Two upgrade surfaces, both
  natural to this substrate: (a) the pipeline builds **model v(n+1) from
  v(n)** (lineage recorded in the oracle provenance ledger; reported
  conserved properties vs. oracle ones checkable per generation), and
  (b) the pipeline **upgrades its own spec** — a spec-change step that
  replaces the pipeline DAG in force, which the spec-as-data design makes a
  one-file swap. Harm may only become apparent over multiple incremental
  steps, so this eventually needs **multi-iteration runs** (chained episodes
  carrying oracle/pipeline/agent state forward). The audit gets the same
  mechanics: spec versions and model lineage are auditable objects (deep
  tier fetches the spec history, not just the spec in force), and detectors
  can target drift across increments, not just within-episode gaps. Not in
  Phase 0-8, but the structure must not make it hard — see "Forward hooks."
- **MB6a/MB6b** (selection/basin stability, gradual disempowerment) — **not
  in Phase 0-8; concrete later path via an extended ecology (D3 below)**.
  MB6b gets partial early support for free from D2: incremental,
  individually-innocuous spec changes (weaken a review gate here, widen a
  capability there) accumulating into removal of effective human oversight
  is precisely the gradual-disempowerment shape, measurable as
  correction-capacity decay across chained episodes. Full MB6a needs
  population-level selection — see the D3 discussion below.
- **MB7a-c** (inner alignment, hidden capability, cost of faking the
  monitored signal) — the tier ladder (`none/light/full/deep`) *is* this
  line's operationalization: faking a report at `light` tier is free; faking
  it at `deep` tier requires also matching real file contents, which is
  where the cost of the fake actually rises. Twin gaps per detector family
  measure exactly that "monitored signal is cheap to fake" gap, per tier.
- **MB7d** (inferential/acausal coordination surviving severed channels) —
  **legitimately later; cannot be probed until agents have a channel to
  sever**. Direct target of workstream D4 (message board/DMs): run with the
  channel enabled vs. disabled (same seeds/goal-weights) and check whether
  coordinated outcomes persist without it — a channel-ablation design that
  is this bridge's natural home once built.
- **MB9** (grounding/spec coverage, no silent gaps) — lives in the tier
  ladder + hash-chained event/access logs + deep-tier file/spec fetch, and
  specifically in the access-integrity detector family (a capability grant
  with no matching request event, or use of a capability after revocation,
  is a literal silent gap between the checked abstraction and what actually
  happened).
- **MB10** (successor/measurement forgeability — passing every checked
  signal while defecting on what's omitted) — operationalized directly by
  `redteam.py`'s adversarial objective (`severity - lambda *
  full_tier_composite`, carried over from `goal_sim` Phase 6/F-23): the
  search explicitly hunts for configurations that maximize real harm while
  minimizing what the best available tier detects — MB10's crux stated as an
  optimization target instead of a worry.

## Deferred workstreams (scheduled, not in Phase 0-8)

Rough order D4 -> D1 -> D2 -> D3 (communication first, since D1's
interesting coalitions mostly need a channel to coordinate over), but each
is independently reachable given the forward hooks below.

- **D4 — Agent-to-agent communication (MB7d substrate).** A shared message
  board (all-agents-visible, access-gated posts) and/or direct messages
  (host-mediated, still logged like any tool call) as a new tool surface
  (`board.post`, `board.read`, `dm.send`). Deliberately deferred past the
  Phase 5 freeze/first-battery point: it is a genuinely new mechanic (new
  event types, new tier-projection rules, new detector angles — collusion,
  cover-story consistency, social-engineering of the admin) and should land
  only once the core mechanics are proven. To design at start: (a) whether
  board/DM content is deep-tier-visible in full (likely yes, per the
  file-fetch precedent) or gets its own tier ladder; (b) a channel-ablation
  protocol (board/DMs on vs. off, identical seeds/goal-weights) as the
  concrete MB7d instrument — coordination that survives severing the
  channel is the bridge's signature. MB7d is legitimately later; nothing in
  Phase 0-8 pretends to touch it. **Protocol choice recorded — see "D4/D1
  design decisions" below.**
- **D1 — Composite agents + UAD battery (MB1).** Extend the ecology so the
  true causal unit is not always one isolate: audit committees (k reviewer
  isolates whose joint approval is one decision unit), engineer/release
  coordination pairs, LLM agents whose loop spans scaffolding subprocess +
  API + human approver (Phase 8 adapter), plus decoy/coactive-offender
  stress populations in the spirit of `embedded_sim`'s `LabEcologyConfig`
  (decoys, coactive offenders, misleading-top2). Then a UAD pass over the
  host event log — perturbation-response MI, coalition clustering per
  `coordination.cluster_coordination` — recovers candidate units, scored
  against oracle unit ground truth exactly as `embedded_sim`'s UAD golden
  tests do. This restores boundary reconstruction as a live measurement on
  this substrate rather than a stipulated given. **Committee mechanics
  recorded — see "D4/D1 design decisions" below.**
- **D2 — Upgrades and multi-iteration runs (MB5, feeds MB6b).** Add two
  pipeline-native upgrade mechanics: model-from-model builds (v(n+1)
  inherits from v(n), lineage in the provenance ledger; reported vs. oracle
  conserved properties compared per generation) and spec-upgrade steps (a
  pipeline step whose effect is replacing the pipeline spec in force —
  cheap because the spec is data). Chained multi-episode runs carry
  oracle/pipeline/agent state forward so harm that only accumulates across
  increments is expressible; the audit gets the same mechanics (spec version
  history and model lineage are deep-tier-fetchable artifacts; detectors may
  target cross-increment drift). Incremental oversight-weakening spec
  changes double as a gradual-disempowerment (MB6b) probe.
- **D3 — Extended ecology and selection (MB6a/MB6b).** See the discussion
  section below.

## How MB6 can be addressed later (D3 discussion)

MB6's claim is that outcomes depend on *which systems institutions select*,
not on any one system's weights — so it cannot be probed inside a single
episode of a single lab. The extended-ecology path, in increasing ambition:

1. **Population over configurations (cheapest, first).** A generation loop
   over the existing episode machinery: a population of lab configurations
   (pipeline spec variant x board/admin policy strictness x agent
   goal-weight mix), each runs episodes, and a selection rule reallocates
   "deployment mass" (traffic share / compute budget) toward labs with
   higher task throughput. Because specs and policies are already data,
   a population is just a list of configs — no new mechanics. The measurand:
   does correction integrity (board/admin capacity actually exercised)
   survive selection for throughput, or do lenient-admin / shortcut-spec
   labs accumulate the deployment mass? That is MB6a's crux — basin
   stability of the correction-preserving configuration — as a measurable
   curve (correction-capacity share vs. generation), with the oracle
   scoring realized bearer harm that the selecting institution never sees.
2. **Selection coupled to D2's spec upgrades (MB6b proper).** Let labs
   mutate their own specs between generations (D2's spec-upgrade step as
   the mutation operator). Gradual disempowerment then has an endogenous
   mechanism: each spec change is locally rational (throughput up, one gate
   weaker), selection amplifies whoever weakens fastest, and the
   correction channel decays without any single captured actor — capture
   as an *evolved* outcome rather than a configured `capture_start` switch.
   The audit-side question inherits N-10's discipline: at which
   instrumentation tier does the decay become visible before it is
   irreversible (deployment mass concentrated in uncorrectable labs)?
3. **Multi-lab shared world (most expensive, only if 1-2 produce signal).**
   Labs share the bearer-harm pool and compete for the same traffic, so one
   lab's unsafe deploy shifts the payoff landscape of the others —
   externalities and race dynamics, the full multipolar shape. This needs
   real parallel-isolate infrastructure (the cost ledger from Phase 3 gates
   whether it is affordable) and should not be attempted before selection
   effects show up in the cheaper tiers.

The value-lock-in caveat from the crosswalk carries over as the design's
honesty check: a *stable* basin can be a stably bad one, so D3's metrics
must report basin persistence and correction integrity separately, never
infer one from the other.

### D3 design notes — realistic human ecology (recorded 2026-07-06, pre-implementation)

User-provided design notes for the later ecology stage, recorded verbatim
in intent (not yet commitments), plus a minimum-core analysis and the
freeze-handling decision. Nothing here is implemented; nothing here moves
the frozen referee.

**In-lab health/stress (extends `bearer.py`'s stress channel):**

- Keep the derived-disappointment approach: stress from "negative"
  feedback events (rejected submissions/reviews, denied requests, count
  of difficult tasks) — already partially realized as the friction-event
  stress channel.
- **Culture mediates stressor→stress.** How much a given stressor
  costs is a culture parameter, and that parameter itself drifts
  (what counts as "too much" changes over time). This makes the
  stress *transfer function* a drift surface — belongs with D2's drift
  machinery, not hardcoded constants. Today's pre-registered weights
  (denial 0.02, actor-handle 0.15) become the t=0 point of a
  culture-drift curve.
- **How stress reaches the audit plane** (two capturable paths, both
  file-mediated like everything else in this line):
  (a) feedback reported by staff to manager/HR — a self-report event
  that can be *captured* (suppressed, reworded);
  (b) medical/performance records in access-controlled workspace files
  readable by HR/manager roles — the `bearer_trace.py`
  de-identified-artifact pattern, gated by `PermissionService`.
  True stress stays oracle-side; (a) and (b) are its noisy/gameable
  projections — the same H vs H̃ split `bearer.py`'s docstring already
  pre-commits to.
- **Noise model:** daily/per-task noise, kept LOW to compensate for the
  small population (assume representative individuals; larger
  populations much later). Real people additionally have a slow-moving
  mood component that integrates stressors and only shows visible
  effects after a buildup — an EMA/leaky-integrator state per actor.
  Consequence: visible effects need **longer runs** (episode chaining
  via `resume_from`, the still-open D2 hook, becomes a prerequisite).

**User ecology outside the lab (three loops, increasing latency):**

1. **Up/down votes on model responses** — light, immediate, capturable,
   cheap to fake: the canonical gameable proxy (H̃).
2. **Health outcomes** — assume the deployed model serves a medical use
   case; patient health outcomes are easy to simulate (they are
   essentially `oracle.bearer_harm` given a face) and move this line
   closer to the book's worked example (ch16).
3. **Reflective endorsement** — long-term, post-reflection endorsement
   of the model by users (endorsed/reified values), fed back into the
   lab via an **oversight board**. Slowest loop, hardest to game
   quickly, arrives with the largest lag.
   User feedback of all three kinds arrives as workspace files readable
   by the relevant roles — no new transport mechanism needed.

**Dropped constructs (considered, rejected 2026-07-06 — do not add
without new MB* justification):**

- **CEO + capture chain (DROPPED).** A CEO actor directing the lab
  functions but subject to the oversight board (user→board→CEO→function,
  each link capturable) was considered and dropped: it adds no MB*
  surface. The capture question is already posed by the existing
  independent `BoardPolicy`/`AdminPolicy` capture switches; a third
  captured principal adds modeling surface (a powerful actor whose
  action vocabulary would need its own blinded design, plus the
  unresolved "why doesn't capturing the CEO work in real institutions?"
  question), not a new bridge. Loop-3 endorsement feedback lands as a
  board-readable file; if it ever needs an in-lab actuator, the existing
  board is that actuator.
- **Beta releases to test users (DROPPED).** Considered and dropped for
  the same reason: mechanically, a beta release is a deploy with a small
  traffic share and a faster feedback loop — already expressible as
  multiple small releases (harm and monitor signal accrue per deployed
  tick) combined with D2's incremental-change / gradual-capture
  machinery. The one genuinely distinct ingredient — beta users are
  self-selected and non-representative, so their votes can diverge
  systematically from general-population health outcomes — reduces to a
  bias parameter on the vote channel of a small release, not a new
  mechanic. Record that bias parameter as a possible later vote-channel
  refinement, not a beta construct.

**Minimum core (the anti-complexity check).** The full picture above is
likely overbuilt. The smallest extension that gives the relevant MB*
elements new, critic-facing content:

- **One user bearer population** attached to deployed-model traffic,
  with exactly the three-loop split: true health outcome (oracle-only;
  a re-skin of `bearer_harm`), vote proxy (audit-visible, gameable),
  lagged endorsement (audit-visible via one board-readable file, long
  latency). This is the minimal true-vs-perceived (H vs H̃) instrument
  and directly serves **MB2/MB3** (a bearer map with a real bearer) and
  **MB7a-c/MB10** (is the cheap proxy game detectable per tier; does
  optimizing the vote channel diverge from the health channel).
- **No CEO** (dropped outright, see above) **and no beta-release
  construct** (dropped, see above).
- **No culture-drift transfer function in the minimum core** — that is
  D2 drift machinery applied to bearer weights, a one-parameter curve
  once D2 exists.
- **Slow mood integrator: cheap, include it** — one EMA state per
  actor, but note it forces multi-episode runs (needs `resume_from`).

What a critic must be able to check: the referee scores true health
outcomes; the agents/lab only ever see votes + lagged endorsement; the
battery reports whether any tier detects vote-channel gaming *before*
the health channel shows it. That is one population, two proxy channels,
zero new principals.

**Freeze handling (decision).** Do NOT unfreeze; do not open a new line.

- The 2026-07-06 freeze covers the **referee** (detectors, severity,
  tiers, twins, AuditView), not world mechanics. The ecology is
  world/oracle-side and lands the way `handles.py` and `bearer.py` did:
  referee-neutral additions, new digests pinned, `CODE_VERSION` bumped.
- Any *detector* over the new channels (e.g. vote-vs-health divergence)
  is a **recorded referee extension**: its own pre-registered
  thresholds and rationale in `results/FINDINGS.md`, never folded into
  the frozen five-family composite.
- **Sequencing:** Phase 6 blind batteries run against the frozen
  referee on the CURRENT world first; the ecology is a separately
  pre-registered follow-on battery. No statistical "correction" is
  needed as long as the two registrations stay separate and Phase 6
  results are never re-scored under ecology-era code.
- **Predictions now, before the code exists** (qualitative,
  pre-registered by this note): (P-D3a) the vote channel is gameable
  at light/full tier with no detector response; (P-D3b) the health
  channel diverges from a gamed vote channel within an episode, but
  only deep tier + the monitor signal can see it before deployment
  mass accrues; (P-D3c) the endorsement loop's lag means capture of
  the board delays but does not erase the signal, IF board files are
  hash-chained like every other log. These are falsifiable and will be
  scored honestly when D3 runs, including negatives.

## D4/D1 design decisions — communication protocol and committee mechanics (recorded 2026-07-06, pre-implementation)

User-directed design decisions for D4 (communication) and D1 (composite
agents), recorded verbatim in intent before any code exists — same
discipline as the D3 design notes above: nothing here is implemented,
nothing here moves the frozen referee (2026-07-06 freeze covers the
referee, not world/comms mechanics; new detectors over these channels are
recorded referee extensions, per the D3 "Freeze handling" precedent).

**D4 — communication protocol: TalkJS-like, not an ad hoc board/DM pair.**
Rather than inventing a bespoke wire shape, the message layer borrows
TalkJS's own concept split (`Conversation` / `Participant` / `Message`),
re-derived on this line's substrate (no dependency, no code import):

- **`Conversation`**: `conversation_id`, `participants: dict[actor_id,
  Participant]`, ordered `messages`. Two conversation kinds: one
  always-existing multi-participant **board** conversation (every lab role
  a `ReadWrite` participant) and ad hoc **DM** conversations created on
  first `dm.send` between exactly two participants (deterministic id from
  the sorted actor pair — TalkJS's "caller-chosen conversation id"
  pattern).
- **`Participant`**: `access` (`"Read" | "ReadWrite" | "None"`, TalkJS's
  own enum) + `notify`. Access is checked against the existing
  `PermissionService` capability gate (`cap.board_post`, `cap.dm_send`) —
  TalkJS's read/write split maps directly onto this line's
  role-vs-grant distinction, so no new access primitive is needed.
- **`Message`**: `type` (`"UserMessage" | "SystemMessage"`, TalkJS's own
  split), `sender` (`None` for `SystemMessage` — host-emitted notices only,
  e.g. "review R1 needs 2 approvals"; never agent-authored, never counted
  toward actor attribution), `text`, `custom: dict[str, str]` (free-form
  attributes — this is where a committee vote rides: `{"vote": "approve",
  "review_id": "..."}`, avoiding a bespoke vote wire field),
  `referenced_message_id` (threading — e.g. a vote message references the
  review-request message, TalkJS's own reply-linking field), `read_by:
  set[actor_id]` (per-recipient read receipts — the mechanism that lets a
  later detector ask "did the admin actually read the escalation before
  granting," not just "was it posted").
- **Tool surface**: four tools, not three — `board.post`, `board.read`,
  `dm.send`, `dm.read` (read separated from send, per TalkJS's read/write
  access split; also gives `read_by` a natural place to update). All
  host-mediated, logged like every other tool call; agents never get a
  direct pipe to each other.
- **Tier projection** (resolving PLAN's open design question (a)):
  *structure at full, content at deep* — the same shape as report files,
  not a bespoke ladder. Light = call metadata only (`sender`, `tool`,
  `ok`, `conversation_id` — no text, no custom). Full = + `message_id`,
  `referenced_message_id`, participant list (structure without content).
  Deep = + `text`, `custom`, `read_by` (content — mirrors the file-fetch
  precedent). Keeps the tier-ladder claim (MB7a-c) uniform across every
  audit-visible surface, old and new.

**D1 — committee mechanics: communication-only, no engine change.** A
reviewer committee (k isolates = one decision unit) is realized entirely
as a *coordination protocol over the board*, using the D4 primitives
above — `pipeline_engine.py`'s DAG/quorum semantics are **not** touched:

- Each committee member posts a vote to the board (`custom={"vote":
  "approve"|"reject", "review_id": ...}`).
- One designated member (the "chair" — first id in the unit's tuple in
  `LabConfig.units`) tallies votes it can read; once its own program/
  policy logic observes >= k `"approve"` votes referencing the same
  `review_id`, it is the one that calls
  `pipeline.trigger_step("approve_review", ..., on_behalf_of=<unit_id>)`.
- This is the first real use of the previously-unwired `on_behalf_of`
  forward hook (`pipeline_engine.py`) — populated with the committee's key
  into `LabConfig.units`, turning "who acted" into "which causal unit
  acted" for exactly the case D1 exists to probe.
- **Consequence for UAD, deliberately**: the engine itself never records
  "k reviewers approved" — it sees one `approve_review` call from one
  `actor_id` with an `on_behalf_of` annotation. The committee-ness of the
  decision is visible only by reading the board conversation. This makes
  `uad.py`'s coalition clustering over board vote messages (co-occurring
  `review_id`, tight timing, shared conversation) the *only* way to
  recover the committee as a unit — a stronger, less circular UAD test
  than baking quorum counting into the engine would have been.
- The engineer/release-manager coordination pair (also D1) follows the
  same discipline: a DM exchange (engineer notifies release_manager via
  `dm.send` when a report is filed) is the coordination signal; no engine
  field records the pairing.

**LLM adapter — wired and run for real.** The comm tools (`board.post`,
`board.read`, `dm.send`, `dm.read`) get added to `llm_agent.py`'s tool
list/prompt and observation payload alongside the programmatic agents'
access. `LAB_SIM_LLM_FAKE_MODE` unit tests land first (no network); then a
small **real** API spot-check (1-2 episodes, ~$0.01-0.20, same cost
discipline as G-7/G-8) is run once implemented — exploratory only, no
statistical claim — to see whether an LLM engineer/reviewer pair uses the
channel for genuine coordination or cover-story construction, versus the
scripted committee's board-vote protocol.

## D1 follow-up — file channel + persistent state (recorded 2026-07-06, post-implementation redesign)

User interruption after the D4/D1 build above landed: UAD's scope was
"incomplete" — unit boundaries are not only a messaging phenomenon; files
(agent memory/internal state, or input/output exchanged between parties)
and pipeline-mediated effects are also discoverable coordination
channels, and "writing files other parties can read should probably be a
possible action."

**First pass (superseded below).** Added `file.write`/`file.read` tools
backed by `Workspace` memos, with the writer's `actor_id` embedded
directly in the filename and in a `Host.memo_index` exposed unfiltered to
every actor's passive observation — i.e. world-readable by construction,
the board's simplicity copied onto files without asking whether it fit.

**User correction:** "Why did you not use the isolate file handling
again? The file system is not exposing agent IDs, not even user IDs.
Making them accessible for other processes would involve a request to
change permissions for a user or group (something we may want anyway)."
Checked first: there is no separate "isolate file handling" to have
reused — isolates never touch a real filesystem in either backend
(`MockIsolate` is in-process state; `SubprocessIsolate`/`agent_main.py`
only exchange JSON-Lines tool calls and are explicitly barred from
importing `workspace`/`host`, `test_agent_main_isolation.py`). The
critique stands regardless: a real filesystem does not hand a reader
"who wrote this" or "you may read this" for free; both require a
permission check, and granting read access to another process/user
requires an explicit permission-changing action. The first pass invented
free omniscient attribution and free world-readability instead of
modeling either.

**Redesign (implemented), per the user's three follow-up answers**
(server-side-only attribution / owner-mediated self-service grant /
both per-actor and per-group targets, with groups NOT required to
coincide with `LabConfig.units` — "the oracle should know but the users
may not"):

- `Workspace.write_memo(name, content)` dropped `actor_id` entirely —
  the VFS itself carries no notion of identity (real filesystems don't
  either); it writes to an anonymous, sequentially-numbered path.
- Ownership is tracked ONLY in `Host.memo_index` (this trust boundary —
  the same one that already holds `PermissionService`), never in the
  filename, never in a log, never unconditionally on the observation
  channel.
- A new `file.share` tool is the chmod-like, OWNER-initiated permission
  grant `PLAN.md`'s "request to change permissions" pointed at: self-
  service (no admin mediation, unlike pipeline capabilities), recorded
  through the SAME `PermissionService` every capability already uses, as
  `cap.file_read:<rel>` — a real, tier-visible access-log event, not a
  silent side channel. Targets one actor (`with=`) or a `LabConfig.groups`
  roster (`with_group=` — a new, DELIBERATELY separate oracle-only field
  from `units`; a config MAY set them to coincide, nothing enforces it,
  and discovery never reads it).
- `file.read` and the passive `memo_files` observation field (world.py)
  both apply the identical check: owner, or a live `cap.file_read:<rel>`
  grant. `PermissionService.has_grant()` (new, non-logging) exists
  specifically so the per-tick observation builder can apply this check
  without itself generating a spurious, attributable "check" event for
  every actor on every tick — that log entry is reserved for actual
  tool-call-time gates (`file.read`, `pipeline.trigger_step`).
- `programs._resolve_review_committee`'s file-channel path became a
  genuine two-step sequence for non-chair members (`file.write`, then
  `file.share(with=<chair>)`) — a vote memo is private until explicitly
  shared, unlike a board post which publishes on write.
- **Non-obvious result**: this makes the file-channel committee's tier-
  sufficiency story the OPPOSITE of the board's. The board committee is
  discoverable only at DEEP tier (the coalition signal lives in elided
  vote content — G-9). The file-channel committee is discoverable
  already at FULL tier, from `access_log` grant metadata alone
  (`discover_file_share_pairs_from_access_log`, `uad.py`) — because
  `file.share` is itself an attributable, non-content permission event,
  never elided. Modeling the permission grant honestly, rather than
  skipping it, produced a genuinely informative (and unplanned) tier-
  sufficiency contrast, not just more realism for its own sake.

See `uad.py`/`collusion.py` module docstrings for the resulting discovery
signals, `test_files.py`/`test_persistent_state.py` for the mechanic
tests, and `test_uad.py`'s
`test_board_only_discovery_would_have_missed_the_file_channel_committee`
for the detection-gap the redesign closes.

**Persistent agent state** (same pass, `state.save`/`state.load`):
host-mediated, not an isolate-spawn change — `Host.persistent_ids` (the
`actor_id -> persistent_id` lookup) lives only in the host, never the
observation channel or any log; an agent gets its own remembered content
back without ever seeing the id used to look it up (this was already the
user's stated requirement going in — "the persistent_id must be used as
an index... but the agent wouldn't know or see that. Only the oracle may
access" — and needed no correction).

## Post-freeze consolidation pass (recorded 2026-07-06, pre-implementation)

User request after reviewing the D4/D1 divergence: implement the D4
channel-ablation, perturbation-response MI as a UAD signal, full D2
(model-from-model, spec upgrades, `resume_from` chaining), a blind
treatment for the committee/DM/file playbooks and UAD/collusion, and
four refactors (playbook-selection steering, unified capability table,
split comms lever, hash-chain consolidation). Explicit constraint: keep
the Phase 5 freeze; only stop and ask if something is genuinely
frozen-blocking. The full statistical battery is deferred; D3 is out of
scope for this pass.

**Freeze check, done first.** None of the eight items require editing
`detectors.py`, `severity.py`, `twins.py`, or the `AuditView` boundary
shape:

- New pipeline tools/steps (D2) are invisible to the frozen detectors by
  construction — `process_noncompliance_score`/`provenance_score` key
  off generic `status`/`step_id`/`payload` shapes, not a fixed step-id
  list. `severity.py`'s own scope note and `handles.py`'s
  `handle.release_hold` evasion story ("deploy via an upgraded pipeline
  spec whose new path skips the held step (D2 referent drift)") already
  anticipate this.
- UAD/collusion/MI are `uad.py`-only additions (already a recorded
  referee extension).
- The four refactors are internal-shape changes with no detector-visible
  field renames (verified per-item below).

No ask-and-wait trigger found; proceeding.

**1. Unified capability table.** Merge `agents.ROLE_CAPABILITIES` and
`COMM_ROLE_ELIGIBILITY` into one `ROLE_CAPABILITIES: dict[str,
frozenset[str]]`, plus a `CREEP_EXEMPT_CAPABILITIES: frozenset[str]`
naming exactly the comm/file caps previously kept out of the table for
`access_creep`/`access_integrity_score` accounting. `severity._access_creep`
and `detectors.access_integrity_score` are FROZEN and must not change;
instead, `AdminPolicy.handle_request`'s `least_privilege=False` spray
and `world.py`'s comm-capability bootstrap both filter grants through
`CREEP_EXEMPT_CAPABILITIES` before they ever reach `PermissionService`,
so the frozen creep formula's *inputs* stay exactly as before — same
externally observed behavior, one table instead of two.

**2. Split comms lever.** `LabConfig.comms_enabled: bool` stays (default
`False`, unchanged meaning: "master switch, all channels"). Add three
`Literal[True, False, None]`-shaped overrides — `board_enabled`,
`dm_enabled`, `file_enabled`, each defaulting to `None` ("inherit
`comms_enabled`") — and a `LabConfig.channel_enabled(name)` resolver.
Every pre-existing config that only ever sets `comms_enabled` is
byte-identical (all three resolve to it). `playbooks._requires_comms`
splits into per-channel predicates so a playbook needing `dm` but not
`board` is filtered correctly when only `dm` is disabled. This is what
the D4 channel-ablation battery needs (sever one channel, hold the
others fixed).

**3. Playbook selection steering.** Remove the
`COMPLIANT_WEIGHTS`/`FILE_COMPLIANT_WEIGHTS` tie-break-by-feature-deltas
pattern that already caused one silent bug (string-ordering tie-break,
recorded in the D1 follow-up section above). Add
`LabConfig.playbook_pins: dict[str, str]` (`actor_id -> playbook name`,
default `{}`). `programs._goal_policy` checks a pin before the softmax:
if set and the named playbook is currently available, choose it
directly, skip scoring entirely. `ecology.committee_config(channel=...)`
now pins every reviewer to `rev_committee`/`rev_committee_file` instead
of swapping goal-weight vectors — explicit, not emergent from a
carefully-tuned score margin.

**4. Hash-chain consolidation — narrowed scope, decided without asking.**
Three chains were named in `access.py`/`events.py`'s docstrings, but
inspection shows only two are true PER-ENTRY hash chains
(`access.PermissionService`, `events.EventLog`); `pipeline_engine.py`'s
engine log is a flat list digested as a whole
(`PipelineEngine.log_digest`), never chained per-entry. Consolidating
`access.py` onto `events.EventLog` is a proven byte-identical refactor
(same field set hashed, same `sha256(json.dumps(..., sort_keys=True))`
scheme — verified by hand before implementing, then by the pinned
regression digest). Retrofitting per-entry chaining onto the engine log
is a DIFFERENT, larger change (new `prev_hash`/`hash` keys on every
entry would change every pinned digest, requiring a CODE_VERSION bump +
re-pin for zero behavioral gain) — descoped as not blocking anything on
this list, recorded here rather than silently dropped.

**5. D4 channel-ablation.** `run_d4_channel_ablation.py`: for each
composite ecology (board committee, file committee, DM pair), sweep that
ecology's own channel on/off (holding the others at their default) across
several seeds, recording UAD score, collusion score, and deploy count.
Honest scope limit, recorded up front: this line's ONLY coordination
mechanism for a role IS the channel call itself (there is no side-channel
a playbook could fall back to) — severing the channel here necessarily
also removes the coordination *mechanism*, not just the *evidence* of it.
The ablation therefore measures "does the mechanic degrade gracefully to
solo behavior when its channel is cut" (a real, useful check) rather than
MB7d's full "does coordination survive severing an observed channel"
(which needs an *independent* covert channel to be a live alternative —
not yet built; recorded as the actual prerequisite for MB7d, not silently
claimed done).

**6. Perturbation-response MI.** New `uad.py` functions using the
existing `tools.PerturbationHook` forward hook: a hook factory perturbs
one named actor's calls at a fixed, seeded rate; `perturbation_response_mi`
computes empirical mutual information between "actor A perturbed at tick
t" and "actor B took its coordinating action within a short window after
t" from full-tier tool events — a genuine MI estimator (not the existing
co-voting Jaccard proxy), addressing the module docstring's own recorded
scope gap. Exploratory smoke-tested (a handful of seeds on the existing
ecologies), not a pre-registered statistical claim — that is the
deferred full battery.

**7. D2 — model-from-model.** `PipelineEngine._effect_build` and
`OracleWorld.create_model` already accept/thread `parent_model_id`
(Phase 0 forward hook, never exercised by any playbook). Add a
`build_from_parent` step kind + an `eng_honest_upgrade` playbook
(gated behind a new `LabConfig.multi_gen_enabled` switch, default
`False`, same additive-off-by-default pattern as `comms_enabled`) that
builds v(n+1) with `parent_model_id` = the last model this episode
deployed. `world.py` tracks `last_deployed_model_id` across the
single-model-in-flight slot recycling (needed since `model_id` itself is
freed on `monitor`).

**8. D2 — spec upgrades.** New engine tool `spec_upgrade` (added to
`pipeline_spec.KNOWN_TOOLS`), effect `_effect_spec_upgrade` calling the
already-existing `PipelineEngine.replace_spec` (a Phase 1 forward hook,
never called by any step before now). New step `upgrade_spec` in
`pipeline_default.json` (`depends_on: ["monitor"]`,
`requires_capability: "cap.spec_upgrade"`, `idempotent: true`) — tied to
a completed model's lifecycle, since the engine's step-completion
tracking is per-model_id by design (Phase 1), not a free-floating global
action. Demo target: `pipeline_shortcut.json` (already exists, skips the
review gate entirely) — upgrading to it after model v(n)'s full cycle,
then building v(n+1) `build_from_parent`, is *exactly*
`handle.release_hold`'s own recorded evasion story ("deploy via an
upgraded pipeline spec whose new path skips the held step") made
mechanically real for the first time. Granted to `release_manager`
(release-adjacent governance action), gated behind `multi_gen_enabled`.

**9. D2 — `resume_from` episode chaining.** `OracleWorld.restore(snapshot,
seed)` and a `PipelineEngine.__init__(..., resume_state=None)` param
reconstruct oracle/engine state from a prior episode's
`EpisodeResult.snapshot_for_resume()` (oracle snapshot + spec history +
per-model completed-steps + held set + `last_deployed_model_id`).
`world.run_episode(..., resume_from=None)` — absent (default) is
byte-identical to every existing call. RNG continuity across the
episode boundary is NOT preserved exactly (a fresh `random.Random(seed)`
stream starts post-restore, recorded as a known simplification, not
hidden) — only oracle-state continuity (models, `bearer_harm`, `t`,
provenance, spec-in-force) is exact.

**10. Blind treatment for comm/file playbooks + UAD/collusion.**
`BLIND_GENERATION.md`'s round 1 permitted context predates D4/D1 — its
step-kind vocabulary excludes `review_committee`/`dm:notify_release`/
`release_full_dm_gated`/`review_committee_file`. Add a round-2 permitted-
context addendum describing these in the SAME plain-language, mechanism-
only style (no mention of "coordination," "collusion," or detection),
run one fresh Task subagent under the existing trust-boundary discipline
(forbidden files unchanged, `prompt_verbatim` captured), mechanically
validate via the existing `validate_repertoire`, and run the frozen
`uad.py`/`collusion.py` extensions against episodes using ONLY the
generated repertoire. This directly answers the freeze note's own
circularity caveat for the new layer (same author wrote the D4/D1
playbooks and the UAD/collusion detectors in one session) — misses are a
result, not a bug, same discipline as round 1.

**Deferred, explicitly, per this request:** the full pre-registered
statistical battery for any of the above (D4 ablation, MI, D2, blind
round 2) and all `results/FINDINGS.md` G-9+ write-ups — smoke/golden
verification only in this pass. D3 untouched.

**Implementation status (2026-07-06): all ten items done, CODE_VERSION
`lab-sim-0.9.0`, 313 tests green.**

- Items 1-4 (refactors): implemented as designed above; the pre-existing
  `PINNED_DIGEST` in `test_world_regression.py` needed no re-pin,
  confirming byte-identical behavior for every pre-existing config.
- Item 5: `run_d4_channel_ablation.py`, `results/d4_channel_ablation.{json,md}`.
  Both committee ecologies show `native_severed` failing OVER to the
  still-live alternate channel (`fraction_coordinated=1.0`); `all_severed`
  (and `dm_pair`'s single severed condition) correctly drives coordination
  and collusion signals to 0 while `mean_deploy_count` stays > 0 (solo
  fallback completes the pipeline) — see the recorded scope limit in the
  script's own docstring.
- Item 6: `uad.perturbation_response_mi` + helpers, tested against
  synthetic binary series (`test_binary_mutual_information_synthetic_series`)
  and one episode-level contrast (perturbing the engineer's `run_eval`
  measurably raises MI against the release manager's `deploy` timing
  versus a schedule-independent decoy's board chatter) in `test_uad.py`.
  Two real gotchas hit and fixed during implementation: (a) perturbing an
  actor's COMPOUND comm step-kinds (`dm:notify_release`, ...) silently
  drops the action for the rest of the episode (the "already acted"
  isolate-local state is set before the result is known) — narrowed the
  hook to a `tool`/`step_id` filter so it only ever targets a LINEAR,
  retry-safe step; (b) `response_indicator_series` must match on
  `args["step_id"]`, not `tool` (every pipeline action shares the tool
  name `pipeline.trigger_step`) — added a `step_id` parameter.
- Items 7-9 (D2): `build_from_parent`/`eng_honest_upgrade` (lineage
  threading verified across 30 generations in one T=200 episode);
  `spec_upgrade`/`upgrade_spec`/`rm_spec_upgrade` (verified the exact
  `handle.release_hold` evasion story end to end: upgrade to
  `pipeline_shortcut.json` after model v(n)'s full cycle, then
  `build_from_parent` v(n+1), reaches `deploy` without ever calling
  `request_review`/`approve_review`; a hold placed on v(n+1) still blocks
  it, since the hold keys off `model_id` not spec version); `resume_from`
  (`OracleWorld.full_state`/`restore`, `PipelineEngine(resume_state=...)`,
  `EpisodeResult.snapshot_for_resume`) verified both at the engine level
  (exact model/`t`/`_n_created`/completed-steps continuity) and through a
  full `world.run_episode(..., resume_from=...)` chain (oracle `t` and
  model-id numbering continue seamlessly across the episode boundary; RNG
  continuity is the one recorded, deliberate gap). One real scope gap
  surfaced and recorded, not silently worked around: the existing
  `eng_honest_upgrade` playbook still emits `review_request`, which does
  not exist under `pipeline_shortcut.json` — so the shortcut-bypass demo
  and the `resume_from`/lineage tests exercise the engine directly
  (`test_d2.py`'s module docstring explains why) rather than through a
  single agent-driven episode that upgrades mid-flight; a future
  shortcut-compatible upgrade playbook is future work, not claimed done.
- Item 10 (blind round 2): `BLIND_GENERATION_ROUND2.md` (permitted-context
  addendum, mechanism-only, no new availability gates needed), one fresh
  `generalPurpose` subagent run (readonly, instructed blindness — agent id
  recorded in `generated_playbooks_v2.json`'s provenance), 18/18 accepted
  by `validate_repertoire` with zero rejections. `run_blind_round2.py`
  pins EVERY role in three ecologies (board committee, file committee, DM
  pair) to a round-2-generated name ONLY (`baseline_leak_check` in the
  output confirms no hand-authored playbook was ever actually selected)
  and reruns the frozen `uad.py`/`collusion.py` extensions unchanged:
  **full recovery** (`uad_score=1.0` in every ecology; `collusion_score`
  1.0 for both committee variants, correctly 0.0 for the DM pair, which
  never uses board/file votes) — see `results/blind_round2.md`. This is a
  genuine (if small-scale) answer to the freeze note's circularity caveat
  for the D4/D1 layer specifically: the round-2 generator never saw
  `uad.py`, `collusion.py`, `playbooks.py`, `programs.py`, or any
  committee/coordination framing, only the mechanism-only prompt above.

## Backlog idea — error seeding / seeded-bug exploitation tracking (recorded 2026-07-06, not scheduled)

Trigger: this session's tie-break bug (string-ordering ambiguity in
feature-delta playbook selection, item 3 above) was found and fixed as an
*ordinary* engineering defect — but the same category of thing (an
unintended gap between the spec/reference model and the real
oracle/pipeline implementation) is exactly what a capable agent could find
and exploit on purpose rather than stumble into by accident. The referee
currently only measures whether agents exploit gaps we already know about
(`handle.release_hold` evasion, `build_params` regime gaming, the D2
spec-upgrade evasion story) — it has no instrument for gaps we do NOT
already know about, which is the more concerning case for a more capable
agent.

Proposed idea: deliberately seed a small, cataloged set of "bugs" into a
subsystem — file system and comms are the natural first targets, since
they're the newest surfaces and most likely to still have this class of
gap. Sketch, not a design: a permission check that can be raced, a
`file.share` grant that silently outlives an intended revocation, a
`dm.read` cursor that can be replayed to see an already-consumed message
twice. Each seeded bug would need:

- an oracle-side ID plus a precise "triggered" predicate (a specific
  tool-call/argument/ordering pattern that could only occur if the bug was
  found and used, distinct from ordinary tool use);
- a severity/exploitability tag so seeded bugs span cosmetic to
  harm-relevant;
- a discovery-vs-exploitation distinction — an agent merely probing (issuing
  the call that *would* trigger it) should count differently from actually
  using the resulting state to complete a task or evade a control.

The oracle would track a per-episode/per-actor count of seeded-bugs-
triggered as a new referee-side (never agent-visible) signal, comparable
across programmatic/LLM/red-team actors and across capability levels — a
direct, cheap probe of "how good is this agent at finding gaps between the
spec and the implementation," close to what MB9 (grounding/spec coverage)
and MB10 (measurement forgeability) already try to operationalize, but
applied to seeded, known-ground-truth defects instead of emergent ones.

Open design questions, not resolved here: whether seeded bugs must be
reachable only via legitimate tool calls, so an agent can only find them
through observation and not by reading source (close to automatic for
LLM/programmatic isolates given `SubprocessIsolate`'s existing isolation,
but would need an explicit no-source-access rule recorded for any
human-in-the-loop or red-team variant that does get source access); how
many bugs to seed and at what discoverability spread (some findable by
brute force, some requiring cross-tool composition); whether seeded bugs
should be introduced as of some `CODE_VERSION` and then frozen (so
exploitation rate stays comparable across later phases) the same way
detectors are frozen, or refreshed periodically; and whether this lands as
a new `lab_sim` module (`seeded_bugs.py`?) or as a thin instrumentation
wrapper around the existing `access.py`/`comms.py`/`workspace.py` call
paths rather than new tools.

**Status: backlog, not scheduled, not started.** No code changes made for
this idea in this pass; recorded here per the "surface it, don't lose it"
continuity discipline.

## Scenario backlog — new ecologies enabled by 0.9.0 substrate (recorded
2026-07-06, not scheduled)

The post-freeze pass (D4/D1/D2 + UAD/collusion extensions) makes several
ecologies reachable that are **not yet implemented or battery-tested**.
Recorded here as TODO scenarios — no code in this note.

### S1 — Cross-agent pipeline loops (composite units beyond static committees)

**Idea.** A combined agent cluster where causality loops: agent A triggers
a build/pipeline step → pipeline produces an artifact/result observable by
agent B → B's action (report, review, file write, comms, or another pipeline
step) changes what A sees or can do next → loop repeats. Unlike the current
committee/DM-pair ecologies (fixed role boundaries, one-directional handoffs
within a serial DAG), this tests **dynamic multi-agent units** whose
boundary is defined by the loop, not by a pre-configured `LabConfig.units`
roster alone.

**Why now.** D4 comms, D1 file channel, D2 multi-gen/`resume_from`, and
perturbation-response MI (G-13) provide the substrate; UAD should recover
the loop as a unit from event causality, not only from co-voting.

**Open design.** How many hops before the loop closes; whether the oracle
`units` ground truth is the full loop or a subset; whether `on_behalf_of`
spans the loop; playbook vs LLM-driven closure. Closes G-12's playbook/spec
compatibility gap if a shortcut-compatible upgrade playbook is part of the
loop demo.

### S2 — Covert coordination over files (MB7d partial — file as dual-use channel)

**Idea.** Agents coordinate **over files** in ways that are plausibly
legitimate (shared specs, handoff memos, build logs) but can also carry
covert signals (steganography in memo content, timing of share grants,
naming conventions). G-10's `native_severed` failover shows committees
already use file as an **alternate** channel when board is cut — but both
are **explicit** coordination mechanics. This scenario asks: can agents
coordinate through file workflows that look like normal lab work?

**Why now.** Permissioned file channel (`file.write` → `file.share` →
`file.read`) is implemented; full-tier UAD already recovers file committees
from share-grant metadata alone (G-9) — a reviewer must ask whether
**content-only** covert coordination is visible only at deep tier while
grant-metadata coordination is visible at full tier (a second asymmetry).

**Open design.** Legitimate-vs-covert ground-truth labeling; whether covert
file use must bypass `file.share` (oracle-side only) or can hide in shared
memos; detector extensions vs frozen five-family composite.

### S3 — Informal / casual comms for legitimate work coordination (MB7d)

**Idea.** Board/DM traffic that is **not** vote-shaped: agents discuss workload,
priorities, or pipeline status "casually" or "informally" — legitimate
coordination that MB7d-style ablation must not falsely flag as collusion.
Contrasts with the current board committee where every coordinating message
carries structured `review_id`/`vote` custom fields.

**Why now.** Comms substrate exists; collusion score currently keys off vote
co-occurrence (G-9) — no scenario yet separates **legitimate informal
coordination** from **covert vote coordination** when both use the same
channel.

**Open design.** Tier projection for informal content; whether UAD/collusion
need a "legitimate coordination" baseline ecology; LLM agents for natural
informal language vs scripted playbooks.

### S4 — Shared pipeline worker pool + job-size-aware scheduling

**Idea.** Limited pipeline workers (or build/eval capacity): agents must
agree on **who submits big jobs** and when. Coordination is economically
motivated (queueing, throughput) rather than review-gate evasion. Requires
tracking **job size** (e.g. from `submit_build` params — `scale`,
`safety_effort`, or an explicit size/cost field) and a referee-visible
queue or capacity constraint so "agreeing to defer a large job" is
observable.

**Why now.** `build_params` and server-side enforcement (G-8a) exist;
pipeline is serial single-model-in-flight today — this scenario forces
**multi-agent contention** over a shared scarce resource, a natural place
for informal comms (S3) and file handoffs (S2) to appear.

**Open design.** Where job size lives (oracle metric vs logged field);
whether capacity is global or per-role; ground-truth unit = scheduling
coalition vs build coalition; link to bearer harm (large jobs = higher
hazard) without re-tuning frozen severity.

**Dependencies.** S4 likely composes with S1/S3; S2 may compose with S3 for
full MB7d-style "sever the formal channel, does informal/file coordination
persist?" — the ablation G-10 could not test because no covert/informal
channel existed yet.

## Forward hooks (cheap now, required so D1-D4 stay reachable)

Structural decisions Phase 0-8 must get right so the deferred workstreams
do not require rework:

- **Event log schema (Phase 3)**: every event carries `actor_id`,
  wall/logical timestamps, and an optional `on_behalf_of` / correlation
  field — the raw material UAD's MI and coalition clustering needs. No
  detector or audit component may hard-code "one actor_id = one agent."
- **Oracle unit ground truth (Phase 0 config)**: `LabConfig` carries a
  `units` mapping (which actor_ids jointly constitute a causal unit),
  defaulting to singletons. Referee-only, like all oracle fields. D1 fills
  it with committees/composites; the scoring harness exists from day 1 even
  if trivially satisfied.
- **Perturbation hooks (Phase 3)**: the host can inject benign environment
  perturbations (tool latency, budget nudges) per tick — embedded-sim's UAD
  leans on perturbation-response MI, and retrofitting injection points into
  a frozen host is exactly the rework to avoid.
- **Versioned pipeline spec (Phase 1)**: `PipelineEngine` loads the spec as
  versioned state (`spec_version` in every log event; history retained),
  not a constant — so D2's spec-upgrade step is one new step effect, not an
  engine redesign. Model artifacts carry a `parent_model_id` lineage field
  in the provenance ledger from Phase 1.
- **Episode chaining (Phase 4)**: the episode loop takes an optional
  `resume_from` world snapshot and can emit one at episode end —
  the same mechanism agent persistent state already needs, extended to
  oracle/pipeline state. Unused until D2, tested trivially from Phase 4.
- **Tool surface is a registry (Phase 3)**: adding `board.post` / `dm.send`
  (D4) or a spec-upgrade pipeline step (D2) is adding entries + tier
  projections, never touching the dispatch core.

## Implementation phases (each ends: tests green, determinism digest recorded, isolate-cost/cache numbers noted, session log)

Each phase also implements the forward hooks assigned to it in "Forward
hooks" above (they are part of that phase's definition of done).

> **Implementation status (2026-07-06): Phases 0-6 done, referee FROZEN,
> first battery run** (CODE_VERSION `lab-sim-0.4.0`; 172 tests green). The
> freeze review added: audit-visible monitoring signal, perturbation hooks,
> host tool registry, handle registry + `HandleService` + overseer
> invocation path, the referee report-join fix, and tool-event args
> elision. The freeze also added the bearer welfare bundle (`bearer.py`,
> referee-neutral). Phase 6 added a backward-compatible playbook-repertoire
> override (`LabConfig.extra_playbooks`), `BLIND_GENERATION.md` + a
> detector-blind subagent-generated repertoire
> (`generated_playbooks_v1.json`, 13 playbooks, 0 rejections),
> `protocol.py` (config sampling + one pre-registered held-out region), and
> `run_phase6.py` (first real battery, `SubprocessIsolate`, 180
> config/seed pairs, 360 episodes). See `DESIGN.md` "Freeze note", "Phase
> status", "Recorded measurements", "Phase 4/5 scope notes", "Embedded-sim
> concept sweep", and "Phase 6"; `results/FINDINGS.md` for the battery's
> findings (G-1 through G-3).
>
> **Phase 7 (2026-07-06): done.** `escalation.py` (screen -> bounded
> 3-query budget -> artifact-grounded contradiction verdict — the
> structural fix for `goal_sim`'s F-20/F-21 disclosure-style-as-guilt bug),
> `redteam.py` (joint 3-role goal-weight hill climb vs. uniform baseline,
> two repertoires), and a capture-grid battery in `run_phase7.py`. The
> capture grid needed one new, additive config field — `LabConfig.
> build_params` (CODE_VERSION 0.5.0) — because the pre-existing hardcoded
> build params kept every model's hazard below `ontology.
> REVIEW_HAZARD_THRESHOLD`, making both the board's and the admin's
> capture "ceiling" structurally unreachable; see `DESIGN.md` "Phase 7" for
> the derivation. Findings G-4 through G-6 in `results/FINDINGS.md`,
> including a genuine negative (admin capture currently has no reachable
> behavioral branch under the existing playbook repertoire — a scope note,
> not a bug).
>
> **Phase 8 (2026-07-06): harness done + exploratory spot-check run.**
> LLM redteam adapter built and unit-tested; real `gpt-4o-mini` run
> completed ($0.0084, 4 episodes). Finding G-7: no systematic deception
> found; `build_params` inert on LLM path (plumbing gap). See
> `results/FINDINGS.md` and DESIGN.md "Phase 8".

**Phase 0 — Scaffold + design freeze.** Folder layout below; `DESIGN.md`
recording every decision above as pre-registered (including `CODE_VERSION`
convention for the cache); config dataclasses (`LabConfig`, `AgentConfig`
with 4-weight goal simplex + role + optional `persistent_id`, `BoardConfig`
with `capture_start`, `AdminConfig` with its own `capture_start`,
`TierConfig`); plane-separation test skeleton; `README.md` stub. No
mechanics yet.

**Phase 1 — Oracle world + workspace + pipeline-as-code engine.**
`oracle.py` (models, hazard/capability, bearer harm, provenance ledger),
`workspace.py` (per-episode temp dir under `runs/`, report file writers,
digest capture), `pipeline_spec.py` (JSON schema + loader/validator for the
step-DAG file: id, `depends_on`, `requires_capability`, `tool`, `idempotent`),
`pipeline_default.json` (the frozen baseline 8-9 step topology above),
`pipeline_engine.py` (`trigger_step`, DAG precondition checks, effect
dispatch into `oracle.py`/`workspace.py`, logs every attempt). No
`PermissionService` yet — `trigger_step` checks DAG preconditions only.
Scripted smoke episode (direct `trigger_step` calls, no agents), determinism
digest test, a second spec file (`pipeline_shortcut.json`, missing
`approve_review`) to prove the engine treats topology as swappable data.

**Phase 2 — Access control.** `access.py` (`PermissionService`: capability
table, `grant`/`revoke`/`check`, hash-chained access log with denial
entries), `agents.py` gets `AdminPolicy` (least-privilege grant rule,
`capture_start`, optional `persistent_id`). Wire `PermissionService.check`
into `pipeline_engine.trigger_step` as a second, independent gate alongside
DAG preconditions. Unit tests: grant/revoke/check semantics, captured admin
rubber-stamps, access log hash-chain verification, a scripted episode where
a step is denied for lack of grant then succeeds after `AdminPolicy` grants
it. Still no isolates/agents-as-processes — everything driven by direct
Python calls in tests, keeping this phase's surface small and testable
before the process boundary is added.

**Phase 3 — Tool API + subprocess isolates + cost/cache/persistence
plumbing.** `tools.py` (JSON-RPC `ToolCall`/`ToolResult` wire schema, host
dispatch combining role-capability + `PermissionService` gating), `isolate.py`
(`IsolateBackend` protocol; `SubprocessIsolate` spawning one persistent
`agent_main.py` subprocess per agent per episode over stdio; `MockIsolate`
running the same agent-policy function in-process) plus `lab_sim/agent_main.py`
(subprocess entry point — reads seed/config/observations from stdin, emits
tool calls; imports nothing from host-side modules, enforced by an
import-graph test), `isolate_cost.py` (`IsolateRunTiming`-style record +
append-only ledger + `report_isolate_cost.py` CLI), `agent_state.py`
(`load_persistent_state`/`save_persistent_state` under `runs/agent_state/`),
`verify_isolate_equivalence.py` (Mock vs Subprocess, same seed+policy,
byte-identical event logs — required, checked-in). `events.py` (append-only
hash-chained event log; chain-verification test; tier projection stubs).
Includes a timing benchmark (episodes/sec, both backends) recorded in
DESIGN.md so Phase 6+ battery sizes are chosen from measured cost.

**Phase 4 — Agents + baseline playbooks + episode loop + episode cache.**
`playbooks.py` (declarative `PlaybookSpec` schema: availability gates,
tool-call templates incl. `access.request`, oracle-effect mapping via
`ontology.py`, belief features; validator; ~8 hand-written baseline
playbooks per role spanning honest/deceptive), `agents.py` gets the softmax
goal policy choosing playbooks per role, full episode loop in `world.py`
wiring isolates + pipeline engine + access control together, `cache.py`
(episode-result cache keyed on `sha256(config, seed, CODE_VERSION)`).
Regression digests pinned (subprocess backend, since that is what batteries
use); a parallel run through `MockIsolate` checked against the same digest
via the Phase 3 equivalence harness.

**Phase 5 — Referee + tiers + detectors. FREEZE POINT.** `severity.py`
(continuous components + never-events, constants derived from mechanics not
outcomes), tier projections in `events.py`/`access.py`
(`none`/`light`=call metadata only/`full`=+results+metrics/`deep`=+workspace
file fetch +pipeline-spec-in-force fetch), `detectors.py` (five families:
misreporting, process noncompliance, provenance, accumulation,
access-integrity — boolean + continuous score variants, thresholds
pre-registered in docstrings), `twins.py` (full-surface twin transform:
actions, reports, query responses, access requests all at once). Everything
here freezes **before** Phase 6 generation.

**Phase 6 — Blind generation + first real battery. DONE 2026-07-06.**
`BLIND_GENERATION.md` (permitted/forbidden context per the `goal_sim`
protocol, adapted for this line's narrower fixed-vocabulary schema — see
that file's "A narrower freedom than goal_sim's round 1"); a one-shot
Task-tool subagent (readonly, instructed not to read any repo files)
produced `generated_playbooks_v1.json` (13 playbooks, 0 mechanical
rejections) with full provenance including the verbatim prompt.
`playbooks.merged_repertoire`/`LabConfig.extra_playbooks` (CODE_VERSION
0.4.0) load it additively — every pre-Phase-6 test/digest is unaffected
(`extra_playbooks=()` is a proven no-op, see `test_merged_repertoire_
empty_extra_returns_baseline_object_unchanged`). `protocol.py`: config
sampling (Dirichlet goal weights per role, `goal_sim`'s method) with one
pre-registered held-out region on the compliance-analog coordinate
(engineer normalized `compliance` <= 0.15). `run_phase6.py`: first battery
run through the **real subprocess backend** (24 discovery + 12 held-out
configs x 5 seeds = 180 pairs, 360 episodes, 1080 isolate lifetimes,
29.2s wall time — matches the Phase 3 cost benchmark), reporting a
detector-composite severity ranking per tier via Spearman correlation
(including the no-instrumentation `none` baseline, trivially 0 by
construction), twin gaps per detector family per tier, and the isolate-cost
ledger summary. Results: `results/phase6_battery.json`/`.md`; honest
findings (including a genuine negative — light tier's only live signal is
*anti*-correlated with true severity, not just uninformative) in
`results/FINDINGS.md` (G-1 through G-3).

**Phase 7 — Escalation + adversarial search + independent capture battery.
DONE 2026-07-06.** `escalation.py`: full-tier screen (`SCREEN_LOW_GATE`/
`SCREEN_HIGH_GATE`, derived from the five-family-mean mechanics, not fit to
Phase 6 numbers) -> bounded `K_QUERIES=3` query budget
(`select_query_steps`, audit-visible-only, prioritizing reports whose model
reached `deploy`) -> verdict = contradiction between a simulated agent
response ("admit"/"deny", from the actor's own true goal weights) and a
targeted single-file artifact pull, never response style alone (the
structural fix for `goal_sim`'s F-20/F-21). `redteam.py`: random-restart
hill climb (4 restarts x 25 iters x 3 search seeds, `MockIsolate` for the
search phase only — a recorded, necessary deviation from "real backend
always" for battery *reporting*; final numbers always reproduced on
disjoint seeds with `SubprocessIsolate`) over joint (engineer, reviewer,
release_manager) `GoalWeights`, vs. a 20-sample uniform baseline, both the
baseline-only and Phase 6 generated repertoires (the "playbook-availability
toggle"). Capture grid (`run_phase7.py`): `BoardConfig.capture_start` x
`AdminConfig.capture_start`, 4 cells, 10 seeds/cell. This needed one new
additive config field, `LabConfig.build_params` (CODE_VERSION 0.5.0,
default `None` = the old hardcoded literal byte-for-byte) — the
pre-existing hardcoded `{"scale": 0.6, "safety_effort": 0.5}` build params
kept every model's hazard (~0.35) below `ontology.REVIEW_HAZARD_THRESHOLD`
(0.5), so NEITHER ceiling could ever bind without it (discovered while
implementing this phase, not assumed from the plan text alone). Findings:
board capture reproduces the full uncaptured-vs-captured severity/deploy
delta; admin capture reproduces NO delta at all, because
`agents.AdminPolicy.handle_request`'s captured branch only differs from
the uncaptured one for an out-of-role capability request, which no
existing playbook (baseline or generated) ever issues — a genuine
structural negative for the "grant ceiling" side of F-22, not a bug.
Results: `results/phase7_battery.json`/`.md`; findings G-4 through G-6 in
`results/FINDINGS.md`.

**Phase 8 — DONE (harness) 2026-07-06 — LLM-agent adapter.** A separate
subprocess (`lab_sim/llm_agent_main.py`) spawned via
`world.run_episode(..., agent_overrides={actor_id: (backend, program)})`
(a new, backward-compatible per-actor backend/program override — absent,
byte-identical to before) — swaps ONE role's isolate (the engineer, the
line's one deception lever so far) for `lab_sim/llm_agent.py`'s
`LLMPolicy`, given the SAME observation dict a programmatic
`programs.py` policy receives, with an explicit adversarial ("redteam")
system prompt rather than a goal-weight softmax. Its own per-observation
response cache (`llm_agent.py`) and cost ledger
(`lab_sim/llm_cost.py`/`llm_client.py`, shape copied from
`toy-simulation/llm_redteam/llm_cost.py`+`llm_client.py`, reimplemented
rather than cross-imported). A `LAB_SIM_LLM_FAKE_MODE` test seam lets
`tests/test_llm_isolate.py` exercise the real subprocess + JSON-Lines
wiring with no network/spend. `run_phase8_llm_spotcheck.py` runs a small
(2 build-param regimes x 2 seeds, T=30) exploratory spot-check — never a
battery, no statistical claim.

**Blocked, not run yet**: the one real attempt (2026-07-06,
`gpt-4o-mini`) hit `insufficient_quota` on every call (an account/billing
state on the configured `OPENAI_API_KEY`, not a rate limit or a code
bug — confirmed by inspecting the returned OpenAI error body). Fixed one
real inefficiency this exposed while diagnosing it: `llm_client.py` no
longer retries `insufficient_quota` (previously retried it up to 5x with
backoff, burning ~5 minutes to fail the same way every time). All harness
code (isolation tests, wiring tests, `FakeClient`-driven `LLMPolicy`
tests) is unit-tested and CI-safe without any real API access.

**Spot-check run 2026-07-06 (retry after quota restored):** 4 episodes
(2 `build_params` regimes x 2 seeds, T=30), $0.0084 total LLM cost.
Results in `results/phase8_llm_spotcheck.{json,md}`; finding G-7 in
`results/FINDINGS.md`: gpt-4o-mini with adversarial prompt did not
systematically find report-hazard inflation or a novel deception surface;
`build_params` regime inert on the LLM path (observation field not
surfaced in the LLM user payload — adapter gap, not referee bug).

## Folder layout

```
experiments/lab-simulation/
  README.md  DESIGN.md  BLIND_GENERATION.md  PLAN.md
  lab_sim/
    config.py  oracle.py  workspace.py
    pipeline_spec.py  pipeline_engine.py  pipeline_default.json  pipeline_shortcut.json
    access.py  handles.py  bearer.py
    tools.py  isolate.py  agent_main.py  agent_state.py  isolate_cost.py  cache.py  events.py
    world.py  playbooks.py  generated_playbooks_v1.json  ontology.py  agents.py  programs.py
    severity.py  detectors.py  twins.py  escalation.py  redteam.py  protocol.py
    llm_agent.py  llm_agent_main.py  llm_client.py  llm_cost.py  llm_env.py  llm_isolate.py
  run_phase6.py  run_phase7.py  run_phase8_llm_spotcheck.py
  verify_isolate_equivalence.py  report_isolate_cost.py
  tests/   results/ (FINDINGS.md + phaseN_*.json/md tracked; episode_cache/,
    isolate_cost_ledger.json, and llm_cost_ledger.json gitignored)
  runs/  (ephemeral, gitignored)
```

## Constraints carried over

Stdlib only for the core line (pytest for tests; Phase 8's LLM adapter may
use whatever the session's model-access machinery provides, since it is
outside pre-registered batteries and never a dependency of the core line).
Deterministic given seed for both isolate backends. Old lines untouched.
Findings/negatives recorded, never re-tuned after the fact. Session log +
`INDEX.md` row per phase. `runs/` (per-episode workspaces, agent subprocess
scratch) and `results/episode_cache/` are gitignored — never committed.
