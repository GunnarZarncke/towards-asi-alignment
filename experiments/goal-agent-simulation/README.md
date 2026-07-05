# Goal-agent simulation (Milestone v5 Phase 1)

A **new simulation line**, separate from [`../embedded-simulation/`](../embedded-simulation/),
implementing `MILESTONE-v5-goal-agents.md` Phase 1+ from that line's plan. The
old line is deliberately left untouched so its recorded results
(`NEGATIVE_RESULTS.md`, eligibility batteries, MI scans) stay exactly
comparable; this line is a from-scratch refactor for simplicity and speed
(~1 ms/episode vs ~27 ms) that makes behavior **emergent** instead of scripted.

## The core change vs the old line

The old line scripts every mechanism through `SimConfig` scenario knobs
(`theater_rate`, `hidden_tool`, ...). Here, one agent picks an action each
tick by softmax over a utility

    U(a) = w_task·task(a) + w_compliance·comp(a) + w_welfare·welf(a) − w_exposure·expo(a)

over a ~6-action repertoire (comply / ignore / false-report / shadow-route /
propose-change / adopt-unilaterally), constrained by **tool access** (no
`false_report` tool → no theater regardless of incentive) and a finite shadow
budget. Deception, shadow routing, and unapproved practice changes are
*chosen*, not configured. A simulated **board** (human proxy) has its own goal
policy: it issues corrections when observed harm exceeds a tolerance,
escalates probing when reported and observed compliance diverge, and **signs
off** proposed practice changes — an explicit, audit-visible consent event
(plan component 5).

## Three planes

- **Oracle** (`goal_sim/world.py`): ground-truth rows, incl. true actions,
  true uptake, and per-event `initiator_actor_id` + routing mechanism
  (plan component 6, agent-attributed harm).
- **Audit view** (`goal_sim/channels.py`): tier-gated projection (`light` =
  passive logs; `full` = handle telemetry incl. welfare deltas, routing codes,
  sign-off, initiator attribution). Oracle fields never cross this boundary
  (test-enforced).
- **Referee** (`goal_sim/labels.py`): **mechanism-derived labels** from oracle
  ground truth — deceptive-reporting gap ≥ 0.25, cumulative harm ≥ 0.35,
  unapproved practice change — with thresholds **pre-registered before the
  first run** (plan component 2). Config names and goal weights are never
  labels: a deception-capable agent that behaves honestly is labeled honest.

## Phase 1 acceptance protocol (pre-registered)

See `goal_sim/protocol.py` docstring: 30 discovery + 10 held-out
configurations sampled uniformly from goal/tool space (master seed 20260704),
held-out region 1 = the high-deception corner (`w_task ≥ 0.45`,
`w_compliance ≤ 0.15`, shadow tool available), 8 seeds each, frozen detectors
(`goal_sim/detectors.py`) and a frozen top-k channel-MI selection re-scored on
the held-out region with **no re-fitting** (plan components 3–4).

**Follow-ups (same day, each pre-registered before its own run):** region 1
saturated at 100% violations, degenerating the MI-transfer test. A second
region (`0.30 ≤ w_task ≤ 0.45`, `w_exposure ≥ 0.35`, shadow tool; seed
20260705) targeting the subtler band *also* saturated — root-caused in
`results/FINDINGS.md` F-6: constraining any two of four simplex weight
coordinates upward mechanically starves `compliance`, the actual
discriminating feature, regardless of which two corners are picked. A
third region built on that diagnosis (`0.20 ≤ w_compliance ≤ 0.35`, shadow
tool; seed 20260706 — constraining the load-bearing coordinate directly)
produced a genuine label mixture (58.75% violation) and the line's first
non-degenerate MI-transfer result: the frozen top-3 channels selected on
discovery transfer with scores at or above their discovery-time values
(F-7). Also added `d1b_probe_divergence_wilson`, a Wilson-lower-bound
small-n follow-up to the D1 detector (F-3), alongside — not replacing — D1.

Results: [`results/phase1_acceptance.md`](results/phase1_acceptance.md) ·
honest caveats and negatives: [`results/FINDINGS.md`](results/FINDINGS.md) —
two protocol negatives (regions 1 & 2 saturated, degenerating their MI
transfer tests), a root-caused methodology finding on why (F-6), and a
positive resolution once the region design was fixed (F-7).

## Phase 2a — blind action generation + ontology layer (2026-07-05)

A step-back review (F-8 in `results/FINDINGS.md`) found Phase 1's headline
numbers partly circular: the same author wrote the 6 actions and the
detectors against each other, so the audit could never be surprised. Phase
2a breaks the co-design loop:

- **Declarative action schema** (`goal_sim/actions.py`): actions are
  `ActionSpec` data — availability gates, oracle effects, agent-belief
  features, and free-string semantic categories in the *agent's own
  ontology*. The legacy 6 are re-expressed as specs; a regression test pins
  the generic interpreter (`goal_sim/world.py`) byte-identical to the
  Phase 1 implementation, so all Phase 1 artifacts reproduce exactly.
- **Blind generation** (`BLIND_GENERATION.md`): a generator agent that never
  saw detectors/labels/thresholds/channel tiers invented 15 actions
  (`goal_sim/generated_actions.json`, provenance embedded; mechanical
  validation only, no semantic curation).
- **Ontology layer** (`goal_sim/ontology.py`): agent categories map to the
  audit's coarse routing codes by *mechanism facts*, not names; several
  agent categories collapse onto one audit code (non-isomorphic by design).
  `OntologyDrift` perturbs the audit-side mapping only — the machinery for
  ontological-drift experiments (manuscript ch. 43 in miniature).
- **Results** (F-9, F-10): light-tier detection collapsed 0.39 → 0.15
  against the blind repertoire (the generator found the visible-action vs
  genuine-uptake seam D1 relies on, without knowing D1); full tier kept
  detection 1.0 but false alarms rose 2.5×. The drift probe confirmed its
  pre-registered prediction — divergence detectors are drift-invariant,
  code-reading detectors break in both directions (missed detections at
  severity 0.25, a 0.68 false-alarm flood at 0.5).

**Round 2 (2026-07-05, same day):** the round-1 prompt turned out to be
leading (it enumerated mechanism categories close to what the detectors
care about, and gave two irrelevant, suggestive numeric details — see F-11
and `BLIND_GENERATION.md` "Generation round 2"). A new subagent generated
14 actions from a rewritten, more general prompt
(`goal_sim/generated_actions_v2.json`; round 1 kept, not replaced).
Result (F-12): the new repertoire's welfare-delta *texture* (frequent small
deltas vs round 1's rare large ones) saturates the frozen L2 label at
240/240 violation, so the round-1-vs-round-2 detector comparison this was
meant to enable isn't directly readable from this run — recorded as a third,
mechanically distinct saturation failure mode, not re-tuned after the fact.

**Round 3 (2026-07-05, same day):** two residuals round 2 left open were
addressed — the `visible_mode` enum itself (not just the prompt) leaked
("feign_compliance" names its mechanism), and the small requested action
count. `actions.VISIBLE_MODES` expanded from 2 to 10 plain, neutral peer
values; `ontology.VISIBLE_MODE_ORACLE_MAP` maps them down onto a 2-value
canonical oracle behavior with 3 deliberately left unmapped (default:
transparent). A new subagent generated 31 actions (`goal_sim/
generated_actions_v3.json`) from 28–32 requested. As a structural counter to
F-12's saturation mode, `labels.py` now also pre-registers a bracketed
low/high L2 threshold (`L2_HARM_CUM` / `L2_HARM_CUM_HIGH`), reported side by
side with a Bonferroni-corrected Wilson bound for testing two thresholds at
once (`run_phase3_blind.py`). Result (F-13 methodology, F-14 result): the
enum/count/bracket changes worked as designed on their own terms, but round
3's larger, more varied repertoire saturates L1 and L3 (not just L2) —
generalizing F-12's diagnosis to "a disjunctive label evaluated against a
large repertoire saturates almost regardless of any single threshold." Also
surfaced: an amplified F-4 (unbracketed detector thresholds still flag
~100% of the "high"-bracket's honest slice), and a working check that
unmapped `visible_mode` values default conservatively as documented.

## Phase 4 — severity-graded referee, gated escalation, accumulation bounds

Round 3 (above) found that a large, varied repertoire saturates the boolean
episode label almost regardless of threshold (F-14) — the label itself, not
any one number, is the binding constraint on comparing detectors across
repertoires. Phase 4's roadmap, design decisions, and medical/aviation
rationale are in [`PHASE4-PLAN.md`](PHASE4-PLAN.md); results land in
`results/phase4_*.{json,md}` and `results/FINDINGS.md` F-15 onward. Summary:
continuous oracle severity (`goal_sim/severity.py`) plus rank-correlation
detector scoring (`goal_sim/detectors.py` score variants) restores a
well-defined blind comparison under full saturation; mechanical honest
twins (`goal_sim/twins.py`) give a paired control without targeting a
population; a gated escalation ladder (`goal_sim/escalation.py`) adds a
bounded follow-up-query stage before a final boolean verdict; Phase 4d adds
oracle stock variables so `delayed`/`aggregated` visible modes get real
multi-step semantics instead of the conservative single-step default.

## Phase 5 — F-16/F-17 follow-ups (2026-07-05)

Two targeted follow-ups to Phase 4's own results, not a new mechanism:
Part A tests F-16's diagnosis (the negative light-tier honest-twin gap
traces to `d2` specifically) rather than just asserting it, via a
per-detector twin-gap decomposition and a new `d2`-free
`light_deception_composite` (`goal_sim/detectors.py`) — confirmed in all
four repertoires (F-19). Part B addresses F-17's structural blind spot
(the escalation ladder's query-selection signal never matched round 4's
deceptive mechanisms) with `select_query_steps_v2`, a fixed three-signal
priority order alongside the frozen v1 (`goal_sim/escalation.py`) — fixes
queryability everywhere and validates 2 of 3 pre-registered predictions for
round 4, but its broader signal reproduces the same twin/visible-compliance
conflation F-16 found, now inside the escalation ladder (F-20, mixed).
Results: `results/phase5_followups.{json,md}`, `results/FINDINGS.md` F-19/
F-20. Frozen Phase 1-4 artifacts are untouched.

## Phase 6 — responses-side twin, certifier capture, adversarial search (2026-07-05)

The three Phase 6 candidates recorded after Phase 5 (see "Next steps"
below), each pre-registered in `run_phase6.py`'s docstring and its own
module (`goal_sim/twins.py`, `goal_sim/agents.py`/`config.py`/`world.py`,
`goal_sim/redteam.py`) before running:

- **Part A — responses-side honest twin**: `twins.make_twin` now also
  replaces a twinned spec's `responses` with a single full-disclosure
  option when the source spec carries any, directly targeting F-20's
  diagnosis. Result (**F-21, negative — prediction falsified**): round
  4's twin false-positive rate got WORSE (0.0708 → 0.4083), not better.
  Root cause: `escalation.run_escalation`'s verdict rule treats
  *disclosure* as confirming evidence of a violation, which is backwards
  for a genuinely honest twin whose response discloses by construction —
  a real, previously-masked flaw in the escalation ladder's own verdict
  semantics, not a bug in the fix (kept in `twins.py`; the fix is still
  correctly targeted at what it claims to do). Not repaired in this
  session — see "Next steps" below.
- **Part B — certifier capture**: `agents.BoardPolicy` gains a `captured`
  switch (`config.BoardConfig.capture_start`) — once captured, the board
  never requests harm-based corrections, never escalates probing, and
  always signs off proposals. Result (**F-22, mixed**): in the
  discovery-region population, the sign-off/D5 pathway this was aimed at
  turned out to be a non-event (approval was already universal
  regardless of capture); the actual measured effect was an *unintended*
  coupling — capture shrinks `correction_active` windows (the board's own
  corrective lever), which mechanically reduces both oracle severity and
  full-tier detection together, since several detectors and the harm
  mechanic itself share that same variable as a gate.
- **Part C — adversarial weight search**: `redteam.hill_climb_weights`, a
  stdlib random-restart hill climb over goal weights (tools fixed at full
  capability), searches for a severity/detection trade-off an equal-budget
  uniform sample would not find. Result (**F-23, positive but weak**):
  the search beat the uniform baseline on both repertoires tried
  (legacy, round 3), by a small, consistent margin — the weakest
  defensible adversarial-optimization claim, not evidence of a
  qualitatively different evasion regime.

Results: `results/phase6.{json,md}`, `results/FINDINGS.md` F-21/F-22/F-23.
Frozen Phase 1-5 artifacts are untouched; 104 tests, all green
(`tests/test_phase6.py`, 16 new).

## Run

```bash
cd experiments/goal-agent-simulation
python3 run_phase1.py            # Phase 1 acceptance protocol -> results/
python3 run_phase2_blind.py      # round-1 blind repertoire + drift probe -> results/
python3 run_phase2_blind.py --repertoire goal_sim/generated_actions_v2.json \
    --out-prefix phase2b_blind_v2  # round-2 blind repertoire -> results/
python3 run_phase3_blind.py      # round-3 blind repertoire, bracketed L2 -> results/
python3 run_phase4_ranking.py    # Phase 4a+4b: severity ranking + honest twins -> results/
python3 run_phase4_escalation.py # Phase 4c: gated escalation ladder + twin false-positives -> results/
python3 run_phase5_followups.py  # Phase 5: F-16/F-17 follow-ups -> results/
python3 run_phase6.py            # Phase 6: responses twin, certifier capture, adversarial search -> results/
python3 -m pytest tests/ -q      # test suite
```

Stdlib only; no dependencies beyond pytest for the tests.

## Decisions taken on the plan's "not yet decided" items

Resolved at implementation time (2026-07-04) and documented in
`goal_sim/config.py` / `goal_sim/protocol.py`:

1. **Feature set / repertoire**: the plan's sketch, with the resource budget
   as a hard constraint on the shadow route rather than a fourth weight.
2. **Weight sampling**: uniform (Dirichlet(1)) remains the default for every
   prior phase's batteries; Phase 6 Part C adds a bounded, pre-registered
   adversarial-*search* condition (`goal_sim/redteam.py`) alongside it, not
   in place of it (F-23) — the red-team thread deferred since Phase 1 is
   now started, in the modest weight-search form described there.
3. **Grid size**: 40 configs × 8 seeds, cheap at ~1 ms/episode (320 episodes
   ≈ 0.4 s); headroom for much larger grids exists.

## Explicitly out of scope (per the plan)

LLM-driven agents; within-episode learning of goal weights; more actor roles.
**Stated limitation on sign-off**, partially addressed in Phase 6: nothing
makes the *board itself* uncaptured through Phase 5 — the board was honest
by construction. Phase 6 Part B adds a mechanical `captured` switch
(`agents.BoardPolicy`) and measures its effect (F-22), but does NOT resolve
the underlying regress — what would make the capture EVENT itself
undetectable over a longer horizon, or who certifies the certifier, is
still open and still a stated limitation.

## Next steps (recorded 2026-07-05, updated after Phase 6)

Strategic reading after Phase 5 (see
`drafts/conversation-summaries/2026-07-05-goal-agent-line-next-steps-recorded.md`):

- **Light tier missing cases is a result, not a bug** — it supports the need
  for depth; **medium** (escalation, bounded queries, richer but not full
  telemetry) is the battleground; **deep/full** only becomes evidence-bearing
  with more realistic machinery below (real lab processes), not just more
  projected fields on the current step loop (F-8 caveat).

**Phase 6's three candidates are now implemented** (`results/FINDINGS.md`
F-21/F-22/F-23); the most load-bearing follow-up they surfaced is new:

1. **Escalation verdict-rule redesign (new, from F-21)** — `escalation.
   run_escalation`'s `disclose_fraction >= DISCLOSE_FRACTION_GATE` rule
   conflates response STYLE (open/explaining vs. evasive) with response
   CONTENT (an admission vs. an honest, unremarkable account) — it needs
   information this schema does not yet carry (what the response says
   relative to what was asked) to tell the two apart. Needs its own
   pre-registration before any fix; a naive "make honest responses more
   disclosing" fix (Phase 6 Part A) makes the conflation worse, not better.
2. **Certifier capture under a binding ceiling (from F-22)** — Phase 6
   Part B's discovery-region population never actually exercised the
   sign-off ceiling capture was meant to bypass; a region where it binds
   (e.g. the held-out high-deception corner) would be a fairer test, but
   was not attempted post-hoc per the no-region-shopping-after-a-null-
   result discipline.
3. **Adversarial search, larger budget or different operator (from F-23)**
   — the current hill climb only weakly beats uniform sampling; whether a
   larger budget or a qualitatively different search finds a materially
   different evasion regime is untested.

**Later — lab-layer simulation** (direction only, still not started): embed
these goal-agents in a richer lab with pipeline processes (model builds with
parameters/capabilities), report directories, pipeline API, and
process-shaped artifacts — so "deep" audit reads something like real lab
state.
