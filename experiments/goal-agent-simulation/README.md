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
held-out region = the high-deception corner (`w_task ≥ 0.45`,
`w_compliance ≤ 0.15`, shadow tool available), 8 seeds each, frozen detectors
(`goal_sim/detectors.py`) and a frozen top-k channel-MI selection re-scored on
the held-out region with **no re-fitting** (plan components 3–4).

Results: [`results/phase1_acceptance.md`](results/phase1_acceptance.md) ·
honest caveats and negatives: [`results/FINDINGS.md`](results/FINDINGS.md) —
including one genuine protocol negative (the pre-registered held-out region
saturated at 100% violations, degenerating the MI transfer test).

## Run

```bash
cd experiments/goal-agent-simulation
python3 run_phase1.py            # full acceptance protocol -> results/
python3 -m pytest tests/ -q      # 19 tests
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
