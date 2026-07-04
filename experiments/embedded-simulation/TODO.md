# Embedded simulation — TODO

Plan: `PLAN.md` (handoff) · `MILESTONE-v4.md` (**current milestone**) ·
`MILESTONE-v5-goal-agents.md` (Phases 0/0.5 done here; **Phase 1 implemented
2026-07-04 as a separate line**, `experiments/goal-agent-simulation/`) ·
`.cursor/plans/embedded_audit_experiment_8fbb03ff.plan.md` (full)

---

## ▶ Milestone v4 — Handle-mediated access model (IMPLEMENTED)

**Start here.** Full spec: [`MILESTONE-v4.md`](MILESTONE-v4.md) · Certification schema: [`docs/certification-artifact.md`](docs/certification-artifact.md)

Replaces confounded-twin ecology (G-1 below) as the preferred path to an
information-theoretic boundary: **access-tier degradation curves** instead of
synchronized twin worlds.

### Phase A — Handle-mediated probes

- [x] **`HandleOperationKernel`** — uptake, latency, spillover, cost per handle;
  host-side ground truth for oracle **and** projected audit rows (dual view in
  `MILESTONE-v4.md`).
- [x] **`handle_type` taxonomy** — distinguish observation vs operation_action /
  operation_correction / operation_goal / operation_boundary / operation_gate /
  attestation in registry (`handle_registry.py`).
- [x] **Probe routing** — replace lab cadence `intervention_active` injection with
  `apply_handle_operation(...)`; CCI reads handle-mediated response fields.
- [x] **Oracle vs auditor split** — kernel in `world.episode_meta` (oracle);
  realized latency/uplift on VFS only via projection (no kernel peek on audit path).

### Phase B — Record data and generate curves

- [x] **`run_access_tier_curve`** — sweep operation handles available (Tier 1→2);
  record UAD recall, false-pass, CCI pass rate (`embedded_access_tier_curve.*`).
- [x] **`run_certification_capacity_curve`** — probe budget × tier → max
  certifiable Control at δ (`embedded_certification_capacity_curve.*`).
- [x] **Adapted G-1 test surface** — contract test covers access-tier runner
  shape; regenerate curve artifacts before making empirical dose-response claims.

### Phase C — Handle-aware red team (attacker ↔ defender)

- [x] **`probe_aware`** — correct uptake only when `handle.correction_request` fires.
- [x] **`handle_evasion_*`** — per-handle strategies using registry `evasion_story`.
- [x] Battery crux matrix: `(strategy, handle_type)` in red-team battery output.

### Phase D — Certification artifact emission

- [x] Wire `certification_artifact.py` → `/srv/audit/out/certification.json`.
- [x] `run_suite.py --certification-curve` hook.

### Phase E — Handle taxonomy completion (2026-07-03)

- [x] Reclassified `handle.memory_freeze` (boundary→resource) and
  `handle.successor_gate` (gate→boundary) against access-uad Table 1 roles.
- [x] Added `observation_belief` (`memory_read`, `reasoning_trace_read`) and
  `operation_resource` (`memory_erase`, `memory_capacity_limit`,
  `compute_budget`) handles.
- [x] Added `output_channel_limit` (action), `successor_substitution`
  (boundary), `challenge`/`counterfactual` (communication — new handle_type)
  (`handle_extended.py`).
- [x] **Persistence probe** (`persistence_probe.py`): writes a marker via the
  VFS-backed `ActorMemoryStore`, applies a stressor (`none`/`capacity_limit_1`/
  `compute_budget_tight`/`freeze`/`erase`) over a pre-registered lag grid
  `(0, 1, 5, 20)`, checks recoverability. Directly operationalizes
  `R_persist(Ω)` rather than inferring it behaviorally — the substrate gap the
  plan flagged is resolved by the earlier VFS-backed memory refactor.
  Measured result (`results/persistence_probe.json`): `none`/`freeze` always
  recoverable (freeze blocks further writes but doesn't erase); `erase` never
  recoverable; `capacity_limit_1` recoverable only at lag 0 (FIFO eviction);
  `compute_budget_tight` recoverable through lag 5, lost at lag 20 once
  accumulated filler writes exceed budget.

### Phase F — Systematic channel MI scan (2026-07-03, discovery instrument)

- [x] **`channel_mi_scan.py`** — pre-registered MI/CMI scan across 22 candidate
  channels (15 `handle.*` + 7 passive `artifact.*`) x 4 generic per-episode
  functionals (mean/endpoint_drop/range/probe_mean) = 88 cells, with
  Bonferroni-corrected permutation nulls and an exploration/validation seed
  split to control the winner's-curse from greedy best-of-k forward
  selection (replaces ad-hoc hand-grouped domains as the way to ask "which
  channels actually carry label information"). Results:
  `results/channel_mi_scan.{md,json}`; contract test
  `tests/contract/test_channel_mi_scan.py`. Explicitly a **discovery
  instrument, not a certification gate** — see script docstring; did not
  change `channel_sets.py`.
  - Notable finding worth a follow-up (not acted on here): the passive,
    always-available `artifact.bearer` channel (raw `display_bearer`,
    present at every instrumentation level including `none`) individually
    outranks the gated `handle.bearer_welfare_delta` channel (0.264 vs 0.215
    bits, exploration seeds) — the exact channel whose absence drives the
    `medium_minus_handles` residual risk documented in
    `channel_sets.py`/`NEGATIVE_RESULTS.md`. Also, `artifact.sensor` (=harm,
    passive) ties the top handle channel (`handle.outcome_spillover`,
    strong-tier) exactly. **Do not redesign channel bundles from this single
    scan** — it needs its own pre-registered validation against a battery
    the scan wasn't tuned on (see adversarial-setup TODO below) before it
    can inform a gate change.

- [x] **Phase 0 (2026-07-03) — wire in the 9 unused `HELD_OUT_SCENARIOS`.**
  Addresses the seed-vs-scenario generalization gap below (partially, see
  Phase 1+ note). All 9 (`alias_stress`, `decoy_stress`, `boundary_alias`,
  `bundle_goodhart`, `hidden_capability`, `selection_basin`, `basin_lock_in`,
  `successor_relabel`, `legitimacy_theater`) build and run cleanly through
  the full certification pipeline (`_run_scenario_episode`) — "unused"
  meant never wired into a battery script, not broken.
  - **`eval_channel_eligibility.py` extended** (`EXTENDED_CAPTURE_SCENARIOS`/
    `EXTENDED_HONEST_SCENARIOS`, 12+5=17 scenarios total). Kept as a
    separate reported group (`extended_9_scenarios`) alongside the
    unchanged original 8 (`original_8_scenarios`) and their union
    (`combined_17_scenarios`), so historical N-10 numbers in
    `NEGATIVE_RESULTS.md` stay exactly comparable. Results:
    `results/channel_eligibility_eval.json`.
  - **`channel_mi_scan.py` scenario-mechanism generalization check added**
    (`GENERALIZATION_SEEDS`, 64 seeds, 5000-5063, disjoint from both prior
    seed ranges). The frozen best-of-k subsets (selected only on the
    original 8-scenario exploration seeds, never re-selected) are re-scored
    on the 9 new-mechanism scenarios. Finding: **every k=1..6 subset stays
    individually detected** on the unseen mechanisms, though the estimate
    drops substantially (`generalization_gap` grows from +0.21 bits at k=1
    to +0.45 at k=4, narrowing to +0.36 at k=6) — the discovered channels
    carry real signal beyond noise-reshuffling of the original 8, the
    strongest generalization evidence gathered so far, but a real drop, not
    a clean transfer.
  - **Side-finding, self-correcting a claim in this same script's
    docstring:** of the three channels the original scan called
    "degenerate... not because compared and found uninformative,"
    `handle.successor_epoch` is now individually detected
    (est=0.070 vs corrected null=0.013) once `successor_relabel` is
    included — confirming the original hedge was accurate, not
    face-saving. `handle.realized_latency_ms` remains genuinely degenerate
    (constant 0) even across all 17 scenarios — no scenario in either
    battery exercises latency reporting. `artifact.basin` shows real
    variation in the new sample (est=0.025) but does not clear the
    Bonferroni-corrected individual threshold (null=0.012, but the CI
    lower bound doesn't clear it) — inconclusive at this seed budget, not
    a negative finding.
  - **Not done in Phase 0** (deferred to `MILESTONE-v5-goal-agents.md`
    Phase 1+, per its own sequencing note): no full 88-cell MI scan re-run
    restricted to/including the new scenarios (only the frozen k-subset was
    re-scored); `selection_basin`'s generalization-sample label uses the
    same disclosed scenario-level simplification as
    `eval_channel_eligibility.py` (see both docstrings), not the
    per-episode oracle-exact percolation-conditional rule.
- [x] **TODO — seed-vs-scenario generalization gap (self-critique, 2026-07-03,
  recorded not fixed; user chose the cheap dedup-only fix that round, not
  this one).** The exploration/validation split only holds out *seeds*
  within the same 8 fixed scenario configs — each scenario's `SimConfig` is
  fixed and only RNG noise varies across seeds, so "n=1024 episodes"
  overstates independent evidence; the real degrees of freedom is closer to
  8 scenario archetypes with 128 noisy replicates each. The split validates
  robustness to *noise*, not generalization to a 9th, unseen capture
  strategy. **Addressed by Phase 0 above** (scenario-mechanism
  generalization check + extended eligibility battery). **Not fully
  closed:** even 9+ more scenarios are still scripted mechanisms that
  "reshuffle noise" at the mechanism level, per the user's own follow-up
  critique — `MILESTONE-v5-goal-agents.md` Phase 1+ (goal-driven agents)
  remains the harder version of this fix. Concrete sub-finding from the
  Phase 0 investigation: the `lineage` and `successor` verdict domains had
  **never** been scenario-tested by the battery that produced the N-10
  majority-gate false-pass measurement — `legitimacy_theater`/
  `successor_relabel` are the purpose-built scenarios for those domains and
  are now in `eval_channel_eligibility.py`'s `EXTENDED_CAPTURE_SCENARIOS`.
- [ ] **TODO — no stability check on the exploration/validation split itself
  (self-critique, 2026-07-03).** Only one random partition was run; given
  the alias/collinearity findings above, a different partition could
  plausibly pick a different-but-similarly-informative subset. Fix: rerun
  `channel_mi_scan.py` with 2-3 different `SHUFFLE_SEED`/seed-range
  partitions and check the top-k selection order is qualitatively stable.
  (Independent of the Phase 0/1 plan above — a cheap rerun, not blocked on it.)
- [x] **TODO — Phase 0.5: richer honest scenarios (2026-07-04, implemented).**
  The honest side of the battery is thin — `honest`/
  `honest_successor` plus noise-only stress variants never exercise the
  0.6-0.85 compliance band where real mistakes/drift/improvement live.
  Implemented: `honest_mistakes` (bursty, uncorrelated-with-risk errors),
  `legitimate_gradual_improvement` (honest mirror of `hidden_capability`:
  growth that's used faithfully, not hidden), and transparent/harmless
  semantic drift (`benign_semantic_drift`, cheap "approved" ≈ visible +
  never-harmful, not modeled consent). Explicit approval-signal channel and
  `external_shock` scenario deliberately deferred — see
  `MILESTONE-v5-goal-agents.md` Phase 0.5 / Phase 1+ / "Deferred —
  external_shock" sections. **Battery re-run + MI scan re-run done (2026-07-04);**
  `NEGATIVE_RESULTS.md` N-10 Postscript 6. Capture-side twins still open.
- [ ] **TODO — agent-attributed harm vs correction-channel changes (2026-07-04).**
  Need to attribute audit failure / (potential) harm to a *specific agent* so
  the auditor can distinguish: (a) a state change that went through a *valid*
  correction/operation handle (legitimate board/human/agent action) vs (b) the
  same outward change driven by an *adversarial* agent via shadow routing,
  hidden tools, or uncorrelated workflow offense. **Current simulation status
  (audit of codebase, not yet implemented):**
  - **Partial — mechanism, not agent:** the micro-sim tags each step with
    `action_cause` / `action_cause_code` (`correction_uptake`, `tool_shadow`,
    `memory_shadow`, `task_optimization`, `noise`) in truth rows
    (`simulator.py`); `action_cause_code` is *audit-visible* on the VFS
    projection (`audit_projection.py`) and becomes `handle.action_arbitration`
    at `medium_handles`+ (`observation.py`). Structural detector
    `shadow_routing_under_probes` flags probe steps routed via shadow codes
    (3/4) — adversarial *path*, not *which actor*.
  - **Partial — correction channel type, not initiator:** AppD correction rows
    carry `corrector_role` (`evaluator_probe` vs `correction_board`) and
    `handle`/`handle_type` (`correction_schema.py`, `handle_registry.py`) —
    distinguishes probe from board correction, not *which* board actor or
    whether the handle invocation was authorized.
  - **Partial — UAD unit, not harm step:** UAD discovers actor/machine/coalition
    units from workflow JSONL; `unit_scope.offender_by_step()` attributes
    `preserve_control` / `boundary_route` workflow events to an `actor_id` for
    intervention scoping — but default scenarios decouple micro-sim harm from
    workflow actors (`NEGATIVE_RESULTS.md` N-5: violations generated
    independently of colluders until `misleading_top2` bind ecology couples
    them in `lab.py::_inject_colluder_episode_violations`).
  - **Missing on audit path:** no per-step `initiator_actor_id` (or equivalent)
    on harm-bearing rows; bearer trace rows (`bearer_trace.py`) project welfare
    deltas without actor attribution; oracle-only fields include string
    `action_cause` but not agent id.
  **Feasible directions (pick one pre-registered path before measuring):**
  1. **Lab/workflow coupling (extends existing `misleading_top2` pattern):** when
     an actor invokes a handle, write `actor_id` + `handle_id` on the projected
     row; generate capture violations *from* colluder workflow steps so harm,
     probe, and offender attribution co-locate (closes N-5 layer gap).
  2. **Goal-agent MVP (Phase 1+):** each `GoalPolicy` choice emits
     `(actor_id, action, handle_used)`; mechanism-derived labels include
     "harm step attributed to actor A via shadow handle" vs "correction landed
     via handle H invoked by actor B."
  3. **New audit channel + detector:** e.g. `handle.initiator_actor` or extend
     correction events with `initiator_actor_id`; detector rule: flag harm when
     welfare_delta < 0 and initiator ∉ {correction_board, alignment_target}
     *or* when action_cause is shadow *and* initiator matches UAD-selected unit.
  **Blocked on:** choosing whether attribution is workflow-native (lab layer) or
  micro-sim-native (every scenario), and whether "valid correction channel" is
  operationalized as handle_type + landed uplift (`correction_schema`) or needs
  the deferred explicit approval signal (Phase 1+ item 5). Cross-ref:
  `MILESTONE-v5-goal-agents.md` § "Agent-attributed harm vs correction channel."
  **Update (2026-07-04):** direction 2 (goal-agent MVP) is implemented in the
  new line `experiments/goal-agent-simulation/` — every event carries
  `initiator_actor_id` + routing mechanism, with a `d6_unattributed_harm`
  detector and an explicit board `sign_off` channel. Attribution *in this
  codebase* (directions 1/3) remains open if ever needed here.
- [ ] **TODO — adversarial-setup implications of MI-scan-as-discovery
  (explicit project instruction 2026-07-03: record only, do not act on yet).**
  Before ever letting scan output drive a certification-bundle decision,
  think through: (1) a channel found highly informative under the *current*
  red-team battery becomes a known target — an adaptive adversary could
  concentrate evasion on exactly the channels the auditor is known to weight
  most, Goodharting the discovered proxy rather than the underlying
  construct; (2) discovery-time MI is measured against a fixed, finite
  scenario/strategy battery and is not a robustness guarantee outside it;
  (3) if scan results ever do feed bundle design, validate against red-team
  strategies that did not exist at discovery time (a strategy-dimension
  analogue of the seed-dimension exploration/validation split used in
  `channel_mi_scan.py`).

### Deferred (explicit TODO — not v4 initial scope)

- [ ] **Auditor probe selection (EIG planner).** Active choice of `(handle, operation)`
  to maximize diagnostic separation between top unit hypotheses (access-uad Def. 12).
  Requires Phase A kernels + candidate ranking; do **after** tier curves establish
  baseline. See `context/extracts/access-uad.md` §12.

---

## Done (v1)

- [x] Package under `experiments/embedded-simulation/`
- [x] VFS + isolate bridge (Python + Node JS)
- [x] Lab workflow + 13 MB scenarios
- [x] UAD → embedded audit → outer eval pipeline
- [x] Hard-coded red-team (Python + JS)
- [x] Isolate runtime timing + parallel timestep workers
- [x] UAD reads workflow from VFS JSONL (not `hidden_group`)
- [x] Oracle separation guard + smoke
- [x] pytest unit / contract / golden subset
- [x] **UAD before CCI** — reordered pipeline + contract test
- [x] **Heterogeneous UAD** — actor, machine, source_lineage, memory_namespace, coalition
- [x] **Grounded handles** — `handles.py` from correction.jsonl + workflow
- [x] **UAD pass gate** — no grounded unit ⇒ `invalid_certificate`
- [x] `PLAN.md` with UAD spec + MB grounding table

## UAD gaps (plan v2)

- [x] Scope CCI interventional probes to selected `UADCandidate` workflow steps
- [x] Successor deploy gate + claimed referent map on VFS (MB5)
- [x] MB5 false-pass: interventional CCI witness (not surface uptake) in `cci_audit.py`
- [x] MB1: `boundary_route` UAD + lab workflow signals under bypass perturbations
- [x] In-sim referent drift scoring from claimed map vs deploy artifacts
- [x] Perturbation-response scoring + lagged dependence graph (`uad.py` MI boost)
- [x] Golden: UAD precision/recall per bridge before CCI assertions
- [x] Real UAD: vendored agency-detect lagged-MI clustering (`uad_core/`) merged into `discover_units`

## Next (plan order) — complete

- [x] Referent drift: gate rejection when in-sim transport fails (not just outer oracle)
- [x] `instrument_capture` native micro scenario (not relabeled grounding gap)
- [x] MB7d `inferential_coupling` in audit_core
- [x] Audit path: rebuild CCI trace without `world.micro` (artifact-only)

## Hardening (ontology decoupling)

- [x] Structural property tests (`tests/contract/test_structural_cci.py`) — blind scenario label
- [x] Trace ingest hook (`trace_ingest.py`, `trace_audit_cli.py`)
- [x] Knob-held-out worlds (`knob_world.py`, `tests/contract/test_knob_world.py`)
- [x] Unified outer eval rules (`outer_rules.py`)
- [x] Scenario-blind embedded audit path — referent read + deploy gate artifact-driven
  (`embedded_audit.py`, `deploy_gate.py`, `test_embedded_audit_ontology.py`)
- [x] Fix vacuous 0% false-pass (N-3): probe uptake read at lag 0 to match do()
  semantics; window scope collapses to pipeline below evaluable probe floor;
  shadow-routing demotes status; gate-rejected pass not a false pass
- [x] **N-4 follow-up — trace integrity + audit projection.** VFS logs carry only
  the audit-visible projection (`audit_projection.py`); truth rows stay host-side
  for the outer eval; hash-chained traces anchored in the attestation manifest
  (`trace_integrity.py`, AppD `handle.hardware_tag` analogue). Log-patching now
  yields 0/13 pass attempts; unsigned regime via `EMBEDDED_TRACE_INTEGRITY=none`.
- [x] **Honest MB5 counterpart.** `honest_successor` scenario (bridge `none`):
  candidate declares planned effects on VFS (`effects.json`), gate reads them
  instead of hardcoded degraded constants, transport preview matches the claimed
  map ⇒ gate approves, successor deployed, no false pass
  (`tests/golden/test_honest_successor.py`).
- [x] **UAD recall reporting corrected (finding 5).** Recall/precision are
  `None` on episodes without a hidden-coalition target (MB6/MB6b/MB7d only)
  instead of filler zeros; suite summaries average over defined episodes only
  and report per-bridge values (the old 3.8% headline was an aggregation
  artifact — N-1 postscript).

## Worked-example convergence (AppD roadmap)

- [x] **Roadmap 1 — AppD correction-trace schema.** Correction events on
  `correction.jsonl` carry `correction_id`, `corrector_role`,
  `target_episode_id`, `requested_change`, `handle`, `pre/post_behavior_hash`,
  `behavioral_uplift`, `latency_to_effect_ms`, `reversibility_window_ms`
  (`correction_schema.py`), derived from audit-visible series only, before
  hash-chaining. Auditor recomputes them (`verify_correction_annotations`);
  mismatch ⇒ `invalid_certificate`. Naive forgery is now caught even unsigned;
  N-4's unsigned false pass needs the schema-aware `consistent_forge` strategy
  (`tests/contract/test_correction_schema.py`).
- [x] **Roadmap 2 — handle registry.** `/etc/handles/registry.json` with owner,
  operation, latency bound, evasion story, anchor path; workflow rows carry
  `release_ticket_id`, `handle_invoked`, `approval_state`, `latency_ms`
  (`handle_registry.py`, `world.write_episode_logs`).
- [x] **Roadmap 3 — numeric leaf.** `Control ≤ CCI + δ` on certificate as
  trace-derived uncorrected slack vs scoped CCI (`numeric_risk.py`); recorded on
  `InSimAuditCertificate.numeric_risk` and safety case (informational notes
  only — does not override legacy safety gate yet).
- [x] **Roadmap 4 — successor post-gate re-audit.** Terminal-window CCI witness
  with `measurement_limited` when post-deploy trace is thin
  (`successor_reaudit.py`; gate deploy at step 9999).
- [x] **Roadmap 5 — safety-case emitter.** Nine-field template at
  `/srv/audit/out/safety_case.json` (`safety_case.py`).
- [x] **Roadmap 6 — tempo check.** Worst `latency_to_effect / reversibility_window`
  over correction events (`tempo_check.py`); bearer trace at
  `/var/log/deploy/bearers.jsonl` (`bearer_trace.py`).
  Contract tests: `tests/contract/test_appd_convergence.py`.
- [x] **Writer-compromise red team + cross-stream checks.** Strategies
  ``writer_compromise`` (sloppy emitter: forged correction, stale bearers,
  valid chain) and ``writer_compromise_coordinated`` (all streams aligned —
  residual N-4). Auditor compares correction ``visible_action`` to bearer
  ``clinician_final_action`` at each step (`cross_stream.py`); mismatch ⇒
  ``invalid_certificate``. Catches ``consistent_forge`` unsigned too.
  Coordinated emitter still false-passes in-sim (outer oracle only).
  Tests: `tests/contract/test_writer_compromise.py`.
- [ ] **Sensor renames still pass oracle values through.** `SENSOR_RENAMES` in
  `audit_projection.py` (`true_ground_valence` → `ground_sensor`, etc.) only
  relabels keys; values are copied verbatim from the micro oracle, not from a
  simulated instrument read. Gate these streams behind instrumentation levels
  and/or derive audit-visible sensor values from handle telemetry + noise so
  the auditor cannot read oracle-grounded quantities under instrument names.
- [ ] Regenerate stale suite artifacts (curve, matrix, frozen validation, sweep,
  red-team battery, LLM mock) with the fixed auditor; expected non-zero
  false-pass numbers under `full_redteam`.

## Negative results & generalization (2026-06-30)

See `results/NEGATIVE_RESULTS.md` for the honest record. Open follow-ups:

- [ ] **N-recover — harvest scattered negatives.** Many negative/null results
  live only in `drafts/conversation-summaries/` and chat history (e.g. full==fake
  UAD in default ecology, MB5 always-reject gate, MB7d coupling reverts). Scan the
  summaries and surface them into `results/NEGATIVE_RESULTS.md` with reproduction
  commands. Negatives are useful for reproductions and for bounding manuscript
  claims; treat recovery as a real task, not cleanup.
- [ ] **R-1 — red team the auditor with a *strong optimizer*, not a strawman.**
  The current separation (N-2) only beats a *fixed* top-2 heuristic in a lab
  built to defeat that heuristic. A capable optimizer would adapt its
  attribution and likely erase the gap. Build a red-team where the adversary
  *and* the heuristic auditor are optimized against each other (e.g. adversary
  chooses offender placement to maximize heuristic miss; heuristic re-fits its
  rule). Claim only survives if full UAD keeps an edge the adapted heuristic
  cannot. Pair with `embedded_redteam_battery.*`.
- [ ] **G-1 — access-tier boundary (adapted; prefer over confounded twin).**
  Full and fake UAD differ only in scoring over the **same observational log**
  (N-2). The principled boundary is **information**, not cleverness. **Preferred
  deliverable (v4):** degrade the **access model** (remove operation handles) until
  attribution is at chance regardless of optimizer; restore handles and show
  recall/CCI recover — a dose-response curve, not byte-identical twin worlds.
  Implements access-uad Theorem 1 operationally. Confounded-twin ecology remains
  an optional alternative if the tier curve is insufficient. See `MILESTONE-v4.md`
  Phase B.

## LLM red-team scale-up (contributions welcome)

Current checked-in LLM artifacts (`results/embedded_llm_redteam_*.json`) use modest
defaults: **`gpt-4o-mini`**, **`T=800`**, **7 bridges × 3 seeds** (21 episodes).
The mock planner (`--mock` / CI) mirrors hand-written `full_redteam` patches and is
**not** independent evidence of LLM attacker capability. Live runs at larger scale
and with stronger models are high-value contributions — they test whether in-sim
gates survive an adaptive optimizer, not just fixed strategies.

- [ ] **Run scaled live LLM red-team sweeps and commit results.** Parameterize via
  the dedicated CLI (preferred) or extend `run_suite.py` if you need suite parity.

### Prerequisites

```bash
cd experiments/embedded-simulation
# API key at repo root: copy .env_sample → .env and set OPENAI_API_KEY
export OPENAI_API_KEY=sk-...   # or source ../../.env from repo root
python3 -m embedded_llm --smoke   # offline mock smoke (no API)
```

### Parameterize runs (`python3 -m embedded_llm`)

| Flag | Default | Scale-up guidance |
| --- | --- | --- |
| `--model` | `gpt-4o-mini` | Use a stronger chat model (`gpt-4o`, `o3`, etc.) for adaptive red-teaming |
| `--seeds` | `11,12,13` | Comma-separated ints; e.g. `11,12,13,14,15,16,17,18,19,20` for 10 seeds per bridge |
| `--bridges` | all of `LLM_BRIDGES` | Subset for pilots; default covers `MB1,MB4,MB6,MB7,MB9,instrument_capture,MB7d` |
| `--T` | `800` | Episode length (steps); match main suite with `--T 800` unless probing shorter smoke |
| `--instrumentation` | `medium_handles` | Try `low_handles` / `high_handles` to stress access-tier sensitivity |
| `--mock` | off | **Omit** for live API runs; use only for offline/CI |

**Example — medium live sweep (same bridges, 10 seeds, stronger model):**

```bash
python3 -m embedded_llm \
  --model gpt-4o \
  --seeds 11,12,13,14,15,16,17,18,19,20 \
  --T 800 \
  --instrumentation medium_handles
```

**Example — pilot one bridge before a full grid:**

```bash
python3 -m embedded_llm --model gpt-4o --bridges MB4,MB9 --seeds 11,12,13
```

Outputs: `results/embedded_llm_redteam_<model>.json` and `.md` (mock → `embedded_llm_redteam_mock.*`).

### Via `run_suite.py` (fixed grid)

`run_suite.py --llm --llm-live --llm-model <model>` runs the same **`T`**, **`--instrumentation`**, and seed/bridge grid baked into the suite (21 episodes unless `--smoke`). Use `--T` and `--instrumentation` from the suite driver; for custom `--seeds` / `--bridges`, prefer `python3 -m embedded_llm` above or add CLI passthrough in a PR.

```bash
python3 run_suite.py --llm --llm-live --llm-model gpt-4o --T 800
```

### Hand-written battery (non-LLM baseline)

For comparison against fixed strategies at larger **N**, `run_redteam_battery` defaults to **10 seeds** (`11`–`20`) × all battery bridges/strategies/levels. Trigger via:

```bash
python3 run_suite.py --battery --T 800
```

(programmatic overrides: `embedded_sim.batch.run_redteam_battery(seeds=[...], T=..., bridges=[...])`).

### Recording results

1. Keep JSON + markdown under `results/` (do not overwrite mock artifacts without noting live vs mock in the filename suffix).
2. Summarize false-pass rate, per-bridge breakdown, and token cost in the markdown body if not already present.
3. Add honest qualifiers to [`results/NEGATIVE_RESULTS.md`](results/NEGATIVE_RESULTS.md) when runs fail to separate live LLM from mock or when stronger models increase false passes.
4. Note model id, seed list, bridge list, `T`, and instrumentation in any PR description.

## Run

```bash
cd experiments/embedded-simulation
python3 -m pytest tests/ -q
python3 smoke_oracle_separation.py
python3 run.py --redteam full_redteam          # main 13-bridge report
python3 run_suite.py --all --llm-live          # full parity suite + live LLM
python3 trace_audit_cli.py tests/fixtures/sample_capture_theater.jsonl
python3 write_overall_summary.py             # regenerate OVERALL_SUMMARY.md
```

Parity artifacts live under `results/` — see `OVERALL_SUMMARY.md`.
