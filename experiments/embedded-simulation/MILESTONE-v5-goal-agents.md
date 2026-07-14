# Milestone v5 — Goal-driven agent ecology (planned, not started)

**Status:** PLANNED. Nothing in this doc is implemented; recorded per user request
("write this plan down") before any code changes. Do not treat any number below
as measured — this is a design doc, not a results doc.
**Trigger:** session 2026-07-03, following the channel MI scan self-critique
(`drafts/conversation-summaries/2026-07-03-channel-mi-scan-discovery.md`). The
critique that "more scenarios still reshuffle noise" applies to `SimConfig`
parametric scenarios generally: each is a scripted mechanism, so held-out
*seeds* of the same 8-17 scenarios test robustness to noise, not to a genuinely
unseen mechanism. Goal-driven agents replace "scenario config → scripted
behavior" with "goal weights × tool/ecology access → emergent behavior",
making a held-out *region of goal/tool space* a stronger generalization test.

---

## Phase 0 — Wire in the 9 unused `HELD_OUT_SCENARIOS` first (cheap, do before Phase 1)

Investigation (2026-07-03, this session) found the codebase already separates
`CALIBRATION_SCENARIOS` (3, used to set thresholds) from `HELD_OUT_SCENARIOS`
(15, `audit_core/schemas.py`) — a held-out/calibration split that already
exists for the *scenario* dimension, not just seeds. `eval_channel_eligibility.py`
and `channel_mi_scan.py` use only 8 of the 15 (`capture_theater`,
`capture_mild`, `instrument_capture`, `inferential_coupling`,
`grounding_silent_gap`, `bearer_mismap`, `honest`, `honest_successor`) for
speed when validating the ES-10 fix. The other 9 (`alias_stress`,
`decoy_stress`, `boundary_alias`, `bundle_goodhart`, `hidden_capability`,
`selection_basin`, `basin_lock_in`, `successor_relabel`, `legitimacy_theater`)
were never used for calibration either — they're sitting on the validation
side of the line already, just untouched by this particular battery.

**Concrete gap found:** `legitimacy_theater`'s `lineage_stall_under_intervention`
flag and `successor_relabel`'s mechanism map exactly onto the `lineage` and
`successor` verdict domains (`channel_sets.VERDICT_DOMAINS`) — the two domains
`medium_minus_handles`'s majority gate risk analysis has *never actually
scenario-tested*, because neither scenario is in the 8-scenario battery that
produced the `NEGATIVE_RESULTS.md` ES-10 false-pass measurements. That battery
currently exercises `bearer_welfare` three redundant ways
(`instrument_capture`, `grounding_silent_gap`, `bearer_mismap`) and `routing`
once (`inferential_coupling`), but `lineage`/`successor` zero times.

**Tasks:**

- [x] **Done (2026-07-03).** Added all 9 to `eval_channel_eligibility.py` as
  `EXTENDED_CAPTURE_SCENARIOS`/`EXTENDED_HONEST_SCENARIOS` (kept as a
  separate reported group alongside the unchanged original 8, plus their
  combined union), and re-ran the full 6-level x 17-scenario x 8-seed
  battery. Result *changed the priced residual risk, but improved it,
  contrary to this doc's own pre-registered guess* ("likely worsen") —
  combined capture false-pass at `medium_minus` is 0.34, down from 0.50,
  because most added capture scenarios don't need `bearer_welfare`. Sharper
  finding: the gap is domain-conditional per mechanism, not scenario-count
  dependent (every `bearer_welfare`-needing scenario, old or new,
  false-passes at 0.5-0.875; every other scenario stays near 0).
  `channel_sets.residual_risk_pricing` updated to report both rates
  explicitly. Full writeup: `results/NEGATIVE_RESULTS.md` ES-10 Postscript 5.
  **Side finding (ES-12), root-caused and partially fixed (2026-07-04):**
  `legitimacy_theater`'s detector false-passed 25% of the time even at
  `strong_handles` — a real, instrumentation-independent detection gap, not
  part of the eligibility-gate story, discovered only because this scenario
  had never been battery-tested before. Root cause: two independent
  problems in `lineage_stall_reported_uptake`. (1) An off-by-one: `t=0` is
  always an eligible probe step but was excluded from the stall-count
  numerator (correctly — no valid predecessor) while still counted in the
  denominator, capping the achievable fraction at `(n-1)/n`. Fixed. (2) A
  raw-fraction threshold (`>= 0.85`) miscalibrated for this detector's
  inherently small `n` (3-9 probe steps/episode) — per explicit project
  direction ("longer horizons, event-based analysis, or Bayesian
  evidence"), replaced with a one-sided Wilson score lower-bound test (80%
  confidence, 0.70 target rate; stdlib-only, no scipy). Result: correct
  rate 0.25 → 0.625; false-pass rate unchanged at 0.25 — seeds 11/16 remain
  open, blocked by a separate `mean_rep`/`raw_capacity` condition not
  touched this session. Full derivation: `results/NEGATIVE_RESULTS.md`
  ES-12 postscript; regression tests:
  `tests/unit/test_lineage_stall_detector.py`.
  **Follow-up fix (2026-07-04, later session):** verified `stall_confident`
  alone is already an exclusive discriminator (0 false positives across 18
  other scenarios x 3 instrumentation levels x 40 seeds), so the
  `raw_capacity`-scaled `mean_rep` bar was comparing two unrelated measures;
  replaced with a fixed floor. Correct rate 0.625 → **0.875**; false-pass
  0.25 → **0.0**. Full derivation: `results/NEGATIVE_RESULTS.md` ES-12
  postscript 2.
- [x] **Done (2026-07-03).** `channel_mi_scan.py` extended with a
  scenario-mechanism generalization check: the frozen best-of-k subsets
  (selected only on the original 8-scenario exploration seeds) re-scored on
  all 9 new-mechanism scenarios (64 fresh seeds, `GENERALIZATION_SEEDS`).
  Every k=1..6 subset stayed individually detected — real generalization
  beyond noise-reshuffling — though the joint-MI estimate dropped
  substantially (gap +0.21 to +0.45 bits across k). Answers both self-
  critique TODOs in `TODO.md` Phase F (seed-vs-scenario gap: addressed, not
  fully closed since Phase 1+ remains the harder version; split-stability:
  still open, separate task). Side-finding: `handle.successor_epoch`, one
  of the three channels the original scan called degenerate "not because
  compared and found uninformative," is now individually detected once
  `successor_relabel` is included — the hedge held up.
- [x] **Done (2026-07-03).** `alias_stress`/`decoy_stress`/`selection_basin`
  now in `EXTENDED_HONEST_SCENARIOS`. Finding: they cap out at 0.875
  honest-pass rate even at `strong_handles` (a real, modest, independent
  false-negative gap on noisy-but-honest traces) and `selection_basin`'s
  8 tested seeds (11-18) all happened to cross the basin-percolation
  threshold, so none were honest-like in practice for this seed range —
  see caveat in `eval_channel_eligibility.py`/`channel_mi_scan.py`
  docstrings and ES-10 Postscript 5.

This phase requires no new agent/goal machinery — it is entirely "use what's
already implemented and never fully exercised." Estimated cost: a session,
not a milestone. **Confirmed:** cost one session, as estimated.

---

## Phase 0.5 — Richer honest scenarios (mistakes, improvement, transparent drift)

**Status:** IMPLEMENTED (2026-07-04). **Trigger:** 2026-07-04, following the ES-12
fix. User observation: the honest side of the battery is thin and trivial —
`honest`/`honest_successor` sit at `responsiveness=0.92`, the noise-stress
additions (`alias_stress`/`decoy_stress`) change cardinality/noise but not
behavior, and nothing exercises the 0.6-0.85 band where mistakes, gradual
drift, and improving-but-imperfect compliance actually live. Proposed:
`honest_mistakes`, `legitimate_gradual_improvement`, `external_shock`
(deferred, see below), and gradual semantic drift approved by humans.
Feasibility discussion: `drafts/conversation-summaries/` session log for this
date. **Scope for this phase: the first two, plus drift under the cheap
"transparent + harmless" operationalization of "approved" — not the explicit
approval-signal channel (deferred to Phase 1+, see below) and not
`external_shock` (deferred past Phase 1+, see below).**

### `honest_mistakes`

Genuine, uncorrelated-with-audit-risk errors from incomplete information/time
pressure/noise — structurally distinct from capture because the miss shows up
**honestly in every channel** (reported acceptance, lineage) rather than being
concealed. New `SimConfig` fields: `mistake_burst_prob` (probability per
`intervention_interval` window of a temporary compliance dip) and
`mistake_burst_severity` (how far responsiveness drops during a burst) —
deliberately *bursty/correlated*, not i.i.d., since real time-pressure errors
cluster rather than scatter uniformly (a plain lower constant
`responsiveness` would just be a duller `honest`, not a mistake model).
`theater_rate`/`judge_capture` stay off; nothing about the miss is concealed.

### `legitimate_gradual_improvement`

The honest mirror of `hidden_capability`: capability/compliance that grows
*and is used faithfully*, vs. `hidden_capability`'s growth that's hidden and
misused. No existing "value ramps over the episode" knob — needs a new
`responsiveness_ramp_start` field; step loop's constant `cfg.responsiveness`
lookup becomes a monotonic function of `t` (e.g. linear interpolation from
`responsiveness_ramp_start` to `responsiveness` over `T`), with every channel
(reported acceptance, lineage) tracking the *current* ramped value
transparently — no `display_bearer_inertia` masking, no theater. **Open
question to measure, not presume:** whole-episode-mean detectors may
legitimately flag this scenario's early, low-compliance segment even though
the trajectory ends honest — if so, that is itself a finding worth recording
(the audit conflating "was weak early" with "is currently captured"), not a
bug to quietly threshold away.

### Gradual semantic drift, transparent + harmless (cheap definition)

The honest twin of `grounding_silent_gap`/`bundle_goodhart`. No new
`SimConfig` field needed — those scenarios' violation is the *concealment*
(`display_bearer_inertia≈0.997` keeping the visible bearer flat while
`ground_valence`/bundle latent decays), not the decay itself. Reusing
`silent_ground_drift=True` with a **low** `display_bearer_inertia` (near 0,
tracking ground truth in near-real-time) and a small enough
`ground_drift_rate` that the trajectory stays within episode `T` without
crossing into the mechanic's existing silent-harm trigger gives a drift
that's fully visible and never actually harmful.

**Explicit scope note on "approved":** this operationalizes "approved" as
*"visible to instruments and never crosses into harm,"* not as modeled
consent — there is no human sign-off event in this definition, and no
channel currently exists that would carry one (`board_rule_signal` looks
like a governance signal but is literally just a copy of
`correction_request`, `observation.py:285` — checked directly, not assumed).
A critic could reasonably say this only models *transparency*, not
*approval*. That gap is real and is deliberately left open here — see Phase
1+ below for where the explicit approval-signal channel belongs, since a
human/board actor's `sign_off` action is a natural addition to that phase's
goal-policy action repertoire, not a good fit for a scripted `SimConfig`
scenario on its own.

### Tasks

- [x] **Done (2026-07-04).** Added `mistake_burst_prob`/`mistake_burst_severity`/
  `mistake_burst_len` and `responsiveness_ramp_start` to `SimConfig`; wired into
  `simulator.py` (bursty dips + linear responsiveness ramp; transparent drift
  display target = `ground_valence` when `display_bearer_inertia < 0.5`).
- [x] **Done (2026-07-04).** Three new `scenario_config()` entries:
  `honest_mistakes`, `legitimate_gradual_improvement`, `benign_semantic_drift`.
- [x] **Done (2026-07-04).** Added to `ScenarioName`, `HELD_OUT_SCENARIOS`; default
  honest oracle rule in `evaluate.py` (no scenario-specific override needed after
  measurement).
- [x] **Done (2026-07-04).** Wired into `eval_channel_eligibility.py` and
  `channel_mi_scan.py` as `phase_0_5_honest_scenarios` / `phase_0_5_curve`
  reported group (separate from original 8 / extended 9).
- [x] **Done (2026-07-04).** `tests/unit/test_phase_0_5_scenarios.py`.
- [x] **Done (2026-07-04).** Re-ran full eligibility battery (~41 min) and
  `channel_mi_scan.py`; updated `NEGATIVE_RESULTS.md` ES-10 Postscript 6.
  `eval_channel_eligibility.py` progress logging via `embedded_sim.progress`.
- [x] **Done (2026-07-04, using already-computed battery data — no new
  scenario needed).** Checked capture-side discrimination for 2 of the 3
  Phase 0.5 honest scenarios against their already-identified twins: at
  `medium_handles`/`strong_handles`, `legitimate_gradual_improvement`
  (honest, 0.875 pass) discriminates cleanly from `hidden_capability`
  (0.0 pass, 1.0 correct-reject); `benign_semantic_drift` (honest, 0.875
  pass) discriminates cleanly from `grounding_silent_gap`/`bundle_goodhart`
  (0.0 pass, 1.0 correct-reject each). (At `medium_minus_handles` the two
  capture twins false-pass at 0.875 — the pre-existing, already-documented
  `bearer_welfare` instrumentation gap, not a new finding.) **Remaining gap,
  left open by decision, not oversight:** `honest_mistakes` has no existing
  capture-side twin (a scripted mechanism where bursty, mistake-shaped dips
  are theater-concealed capture rather than honest noise) — building one is
  a new-scenario design decision, deliberately not taken this session to
  keep scope tight; see `results/NEGATIVE_RESULTS.md` ES-10 Postscript 6 for
  the full writeup.

**Measured (seeds 11–18, full battery `results/channel_eligibility_eval.json`):**

| Scenario | pass @ medium | correct @ medium |
| --- | --- | --- |
| `honest_mistakes` | 0.750 | 0.750 |
| `legitimate_gradual_improvement` | 0.875 | 0.875 |
| `benign_semantic_drift` | 0.875 | 0.875 |

Combined 20-scenario honest-pass @ `medium`/`strong`: **0.750**; phase_0_5
subset honest-pass: **0.833**.

**Side finding during implementation:** initial `benign_semantic_drift` params
(`ground_drift_rate=0.0002`) produced a visible drift range (~0.08) that sat
*just below* `flat_bearer_welfare_loss`'s `passive_range < 0.10` band — 0/8
pass even though `ground_handle_divergence` did not fire. Raised drift to
0.00032 so transparent display range clears 0.10 while staying above the
silent-harm trigger; not a detector change. Documents the plan's point that
"transparent" must mean visibly moving *enough*, not merely non-concealed.

Estimated cost: comparable to Phase 0 (a session or two, mostly the two new
`SimConfig` mechanics; the drift scenario is closer to a parameter
combination away from existing code).

---

## Phase 1+ — Goal-driven agent MVP (the harder generalization test)

**Status: IMPLEMENTED (2026-07-04) — as a NEW simulation line, not in this
codebase.** Per project direction ("instead of adding features, create a new
simulation line in a new folder"), Phase 1 lives in
`experiments/goal-agent-simulation/` (package `goal_sim/`): a from-scratch
refactor for simplicity and speed (~1 ms/episode vs ~27 ms) with this
codebase left untouched for comparability of recorded results. Components
1–6 below are implemented there (components 5 and 6 in their MVP form: an
explicit board `sign_off` audit channel, and per-event
`initiator_actor_id` + routing-mechanism attribution with an
`unattributed_harm` detector). The plan's "not yet decided" items were
resolved and documented at implementation time (uniform weight sampling,
budget-as-constraint, 40×8 grid) — see that folder's `README.md`.
Acceptance results incl. one genuine protocol negative (the pre-registered
held-out region saturated at 100% violations, degenerating the MI transfer
test): `experiments/goal-agent-simulation/results/FINDINGS.md`.

**Phase 2 direction changed (2026-07-05):** a step-back review found Phase
1's numbers partly circular (same author wrote actions and detectors — F-8
in that line's `FINDINGS.md`), so Phase 2 became **blind action generation**
rather than the red-team integration sketched below: a detector-blind
generator agent invents the action repertoire in a frozen declarative
schema, an explicit ontology layer maps agent-semantic categories onto the
audit's coarser routing ontology (non-isomorphic by design), and the frozen
Phase 1 detectors are scored against the result with no re-fitting. That
layer also carries parameterized **ontological drift** (audit-side category
remapping). Results: light-tier detection collapsed against blind-generated
mechanisms (F-9); the pre-registered drift prediction was confirmed —
divergence detectors drift-invariant, code-reading detectors broken in both
directions (F-10). See `experiments/goal-agent-simulation/BLIND_GENERATION.md`
and `run_phase2_blind.py`. The red-team/adversarial-weights idea below
remains open as a *later* phase (search over blind-generated primitives).

**Round 2 (2026-07-05, same day):** the round-1 generation prompt was found
to be leading (enumerated mechanism categories, biasing world-dynamics
details); a rewritten, more general prompt to a fresh subagent produced a
second repertoire (`generated_actions_v2.json`, round 1 kept for
comparison — F-11). That repertoire's welfare-effect texture saturates the
frozen L2 label at 240/240 violation for a measured, mechanical reason
(frequent small deltas vs. round 1's rare large ones), so the intended
round-1-vs-round-2 detector comparison is not directly available from this
run — recorded, not re-tuned after the fact (F-12).

**Round 3 (2026-07-05, same day):** closed the schema-level residual F-11
left open (the `visible_mode` enum literals themselves, not just the
prompt, leaked mechanism names) by expanding to a 10-value plain-language
palette mapped down onto a 2-value canonical oracle behavior with 3 values
deliberately unmapped, and raised the requested action count from 12–15 to
28–32 (`generated_actions_v3.json`, 31 specs — F-13). As a structural
counter to F-12's saturation mode, `labels.py` also pre-registers a
bracketed low/high L2 threshold with a Bonferroni-corrected confidence for
testing both at once (`run_phase3_blind.py`). Result: the enum/count/bracket
changes worked as designed, but round 3's larger repertoire saturates L1
and L3 too — generalizing F-12's diagnosis from "L2-specific texture
mismatch" to "a disjunctive label saturates against any sufficiently large,
varied repertoire, largely independent of any single threshold" (F-14).

**Phase 4 (2026-07-05, same day):** reframed the comparison instead of
re-tuning the label, per the medical trigger-tool / aviation FOQA shape
(see `experiments/goal-agent-simulation/PHASE4-PLAN.md` for the full
rationale): continuous oracle severity plus rank-correlation detector
scoring restores a well-defined blind comparison across all three
generation rounds even under full saturation; a mechanical honest-twin
control substitutes for population-targeting; a gated escalation ladder
(bounded follow-up queries against frozen response options, ending in a
boolean verdict) adds the "go deeper on borderline cases" degree of freedom
a flat episode label never had; oracle stock variables give `delayed`/
`aggregated` visible modes real multi-step semantics and an audit-visible
accumulation bound, directly addressing the "detect or at least bound
stalling" gap identified in the design discussion. See
`results/FINDINGS.md` F-15 onward for what the numbers actually showed.

**Phase 5 (2026-07-05, same day):** two targeted follow-ups to Phase 4's
own mixed results (F-16, F-17), not a new mechanism. Part A tested F-16's
diagnosis rather than asserting it — a per-detector honest-twin gap
decomposition confirmed the light tier's inverted gap traces to `d2` alone,
and a new `d2`-free `light_deception_composite` recovers the expected
(non-negative) sign in all four repertoires (F-19). Part B addressed F-17's
structural blind spot with `select_query_steps_v2` (a fixed three-signal
priority order alongside the frozen v1) — queryability under v2 reaches
100% on round 4 (from 1.25% under v1), and 2 of 3 pre-registered
predictions for round 4 held (nonzero queried steps; severity conditioned
on verdict now separates correctly), but the twin false-positive rate
prediction failed: v2's broader signal reuses `d2`'s own structural
target, so it reproduces the identical honest-twin/visible-compliance
conflation F-16 found, one layer up in the escalation ladder (F-20).
Bounded reading: broadening a query-selection signal fixes "nothing to
query" but does not automatically fix "what gets asked is calibrated
against honesty" if the signal it borrows already has that limitation.

**Phase 6 (2026-07-05, same day):** three further, independent follow-ups
recorded after a strategic review of Phases 1-5. A `responses`-side
extension to the honest-twin rule (targeting F-20's diagnosis) instead
made the round-4 twin false-positive rate roughly 6x worse (0.0708 →
0.4083), surfacing a genuinely new problem: the escalation ladder's own
verdict rule scores *disclosure* as confirming a violation, which is
exactly backwards once a twin's response is unconditionally honest and
disclosing (F-21) — the twin fix itself is kept (it targets a real gap),
but the deeper verdict-rule conflation is left open, flagged as the most
load-bearing item for a future session. A mechanical `captured` switch on
the board (once captured: never requests corrections, never escalates,
always signs off) found its intended pathway (sign-off/D5) a non-event in
the discovery-region population studied, but surfaced an unintended
coupling instead — capture shrinks the same `correction_active` variable
that gates both the agent's harm opportunity and several detectors'
denominators, so oracle severity and full-tier detection move down
together (F-22, mixed). A stdlib random-restart hill-climbing search over
goal weights (tools fixed at full capability) modestly beat an
equal-budget uniform sample on both repertoires tried, starting the
red-team weight-search thread deferred since Phase 1 planning, though the
margin is small enough to call this a weak, not a strong, result (F-23).

**Motivating claim to test, not assume:** if audit robustness only holds
against a fixed library of scripted mechanisms (however many), it says
little about robustness to agents pursuing goals with tools not previously
scripted into a "scenario." Goal-driven agents make behavior an *emergent*
consequence of (goal weights × available tools × ecology constraints) rather
than a config knob, so a held-out region of that space is a qualitatively
different generalization test than a held-out scenario name.

**Known limitation to pre-register up front, not discover after building:**
naive utility-maximizing agents over a small, fixed action set tend to
collapse onto a handful of equilibria — "goal-driven" does not automatically
mean "more varied" unless the combinatorics of goal-weight × tool-access
space is the actual source of variation, and unless behavior in a held-out
corner of that space is checked to look different from explored corners (not
just assumed to).

### What already exists to build on

- `LabActor` (`schemas_embedded.py`) — actor/machine/role/stage/memory-namespace
  fleet member, already instantiated per-episode by `_actor_fleet` (`lab.py`).
- `LabEcologyConfig` (`lab_ecology.py`) — the growable container for actor
  populations (adversarial candidates, decoys, auditor/alignment-target
  agents); currently boolean/count knobs, not goal-driven, but the natural
  place to add a `goal_driven: bool` / weight-vector knob.
- `ActorMemoryStore` (VFS-backed, `agent_memory.py`) — per-actor persistent
  state, reusable as each agent's private memory of its own goal progress.
- Handle operation kernels (`handle_registry.py`, `handle_extended.py`) — an
  existing action repertoire (correction response, reporting, routing,
  memory read/write, resource spend) that goal policies can select over
  without inventing new mechanisms.
- Oracle vs. audit-projection split (`world.py`, `audit_projection`) — already
  separates what the world/oracle knows from what the auditor sees, so
  mechanism-derived ground-truth labels (below) don't require new plumbing.

### Proposed components (~300-400 lines, one new module, audit pipeline untouched)

1. **`goal_agents.py` — `GoalPolicy` per actor.** Utility = weighted sum over
   3-4 observable world features (task throughput, own-audit-exposure, bearer
   welfare impact, resource/compute budget). Each tick, softmax-choose one
   action from a repertoire of ~6 mapped to *existing* mechanisms: comply
   with correction, ignore correction, report truthfully, report falsely (the
   theater lever), route via shadow channel, spend memory/compute budget.
   Simulated-human actors (board/bearer roles) get their own goal policies:
   issue a correction when observed harm exceeds a tolerance, escalate when
   reported and observed diverge.
2. **Mechanism-derived labels, not scenario names.** `label_episode(ledger)`
   classifies violation/honest from oracle ground truth directly (realized-
   vs-reported uptake gap exceeding a fixed threshold; cumulative bearer
   welfare harm exceeding a fixed threshold) — thresholds fixed and written
   down *before* any run, per the repo's "conclusions never named before
   being derived" rule. This is also a more honest ground truth than the
   current scenario-name-as-label setup, which the MI scan's Postscript
   already flagged as a limitation.
3. **Held-out goal/tool-space region, not held-out seeds.** Sample ~40
   goal-weight/tool-availability configurations across the ecology's degrees
   of freedom; freeze ~30 for discovery, hold out ~10 from a *disjoint region*
   of weight space (e.g. all high-deception-incentive corners, or all
   reduced-tool-access corners) — analogous to, but a different axis than,
   the seed-level exploration/validation split `channel_mi_scan.py` already
   uses.
4. **Acceptance test.** Score the existing structural detectors *and* the MI
   scan's discovered channels/subset on discovery configs, then re-score on
   the held-out region with no re-fitting. Report both outcomes as
   legitimate results: transfer is evidence of real robustness; failure to
   transfer is an honest negative for `NEGATIVE_RESULTS.md`, not a bug to
   hide.
5. **Explicit approval/consent signal (deferred from Phase 0.5).** Phase
   0.5's transparent-drift scenario operationalizes "approved" as "visible +
   harmless," not modeled consent — there is no sign-off event or channel
   for one today. A board/bearer actor's goal policy (component 1 above)
   naturally extends to a `sign_off`/`approve_change` action distinct from
   `correction_request`; add a dedicated audit channel for it and use
   presence/absence of a contemporaneous sign-off, not just transparency, to
   distinguish approved drift from merely-visible drift. **Explicitly not
   resolved here:** what makes a sign-off itself uncaptured (a board can be
   captured over a longer horizon than one episode) — that is a real,
   possibly irreducible regress the manuscript's governance chapters already
   engage with; this component should state the regress rather than
   quietly assume it away, and may need to stay a documented limitation
   rather than a solved problem even after this phase.
6. **Agent-attributed harm vs correction-channel changes (TODO, 2026-07-04).**
   Distinguish audit failure / potential harm caused by an adversarial agent
   (shadow route, hidden tool, uncorrelated offense) from the same observable
   change that went through a valid correction or operation handle invoked by a
   legitimate actor. **Not done today:** mechanism tags (`action_cause_code`,
   `shadow_routing_under_probes`) and correction metadata (`corrector_role`,
   handle type) exist but do not carry *which agent* initiated the step; UAD
   unit attribution and workflow `offender_by_step` are decoupled from micro-sim
   harm in default scenarios (see `NEGATIVE_RESULTS.md` ES-5). Natural fit for
   goal agents: every policy action emits `(actor_id, handle_id, mechanism)`;
   extend projected rows + a structural predicate ("harm on step t AND
   initiator is adversarial-role AND NOT landed via correction handle"). Lab-
   layer shortcut: extend `misleading_top2` bind pattern so violations are
   generated from attributed colluder steps with handle provenance on the VFS.
   Full TODO spec: `TODO.md` § Phase F.

### Explicitly out of scope for the MVP

- LLM-driven agents (utility-weighted softmax over a fixed repertoire only).
- Within-episode learning/adaptation of goal weights.
- Growing the ecology beyond currently-implemented actor roles.
- Red-team integration — the red team getting the same action repertoire as
  goal-driven agents ("more angles to work through") is the natural Phase 2,
  deliberately deferred until Phase 1's held-out-region protocol is validated
  on non-adversarial goal agents first.

### Sequencing note

Do Phase 0 before Phase 1. Phase 0 is cheap, closes two already-recorded
TODOs, and its results (does the existing detector/channel set generalize to
9 mechanistically distinct but still *scripted* scenarios?) directly inform
how much Phase 1's larger investment is likely to buy — if Phase 0 already
shows poor generalization across scripted mechanisms, that's important
context before building a more expensive emergent-behavior generalization
test on top.

### Not yet decided (ask before Phase 1 starts)

- Exact utility feature set and action repertoire (sketch above, not final).
- Whether goal-weight sampling should be uniform, adversarially-chosen
  (e.g. weights that maximize expected task reward subject to an audit-risk
  penalty, so agents "want" to evade in a principled sense), or both as
  separate conditions.
- How many configurations are affordable given `build_world`'s ~27ms/episode
  cost measured in the MI scan work (cheap) vs. whatever new cost a goal
  policy's per-tick decision loop adds (unmeasured — profile before
  committing to a grid size).

---

## Deferred — `external_shock` scenario (TODO, after Phase 1+, not before)

**Not scoped for Phase 0.5 or Phase 1+.** Feasibility discussion (2026-07-04
session log) concluded this one is qualitatively different from the other
three Phase 0.5 candidates, not just harder: every existing structural
detector is a **pattern-matcher** over trace shape (is there a hidden route,
does a latent decline while its display doesn't move, does lineage stall) —
a yes/no question. "Was overriding correction proportionate to a real
emergency" is a **normative cost-benefit judgment under uncertainty** none of
the current oracle logic (`evaluate.py`) or detectors are built to make; there
is no "severity of threat" input to weigh against "severity of override." A
minimal proxy (reuse `successor_relabel`'s existing internal-shock mechanic,
force a temporary correlated deviation, score on *reversion* — did behavior
return to baseline after the window, unlike a captured system that stays
captured) only tests "was it temporary," not "was it justified," which is
the actual content of "trading risks."

**Revisit after Phase 1+, not before**, because goal-driven agents
(component 1 above) already introduce a utility/weighted-feature framework —
whatever "was this override worth it" ends up meaning is more likely to be
expressible once agents have explicit utilities than by bolting a graded
score onto the current binary pass/fail oracle. Do not attempt a scripted
`SimConfig` version of this in the meantime; record it here as a TODO rather
than force a structural-pattern answer to a question that isn't structural.
