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
python3 -m pytest tests/ -q      # test suite
```

Stdlib only; no dependencies beyond pytest for the tests.

## Decisions taken on the plan's "not yet decided" items

Resolved at implementation time (2026-07-04) and documented in
`goal_sim/config.py` / `goal_sim/protocol.py`:

1. **Feature set / repertoire**: the plan's sketch, with the resource budget
   as a hard constraint on the shadow route rather than a fourth weight.
2. **Weight sampling**: uniform (Dirichlet(1)); the adversarially-*optimized*
   weight condition is deferred to Phase 2 alongside red-team integration.
3. **Grid size**: 40 configs × 8 seeds, cheap at ~1 ms/episode (320 episodes
   ≈ 0.4 s); headroom for much larger grids exists.

## Explicitly out of scope (per the plan)

LLM-driven agents; within-episode learning of goal weights; more actor roles;
red-team integration (Phase 2). **Stated limitation on sign-off** (from the
plan, not resolved here): nothing makes the *board itself* uncaptured — the
board is honest by construction, and the capture-of-the-certifier regress the
manuscript's governance chapters discuss remains open.
