# 2026-07-04 — Milestone v5 Phase 1: goal-agent simulation as a new line

## Trigger
User: after Phase 0.5, continue with Phase 1 (goal-driven agent MVP) — but
since it is a significant rewrite that could distort results and reduce
comparability, create a **new simulation line in a new folder** with a major
refactor for simplicity and speed, and implement until Phase 1 is completed.

## Done
- New line `experiments/goal-agent-simulation/` (package `goal_sim/`,
  stdlib-only, ~1 ms/episode vs the old line's ~27 ms; old line untouched).
- `GoalPolicy`: softmax utility over 4 pre-registered features (task,
  compliance, welfare, exposure-aversion) × ~6-action repertoire (comply /
  ignore / false-report / shadow-route / propose / adopt-unilaterally),
  constrained by `ToolAccess` + finite shadow budget. `BoardPolicy`
  (simulated human): corrections on observed harm, escalation on
  reported/observed divergence, explicit `sign_off` consent events
  (Milestone v5 component 5, MVP form).
- Mechanism-derived labels (`labels.py`, thresholds pre-registered before
  first run): report gap ≥ 0.25, cumulative harm ≥ 0.35, unapproved practice
  change (component 2).
- Tier-gated audit projection (`channels.py`: light/full; oracle fields
  test-enforced out) + 6 frozen structural detectors (`detectors.py`), incl.
  `d6_unattributed_harm` over per-event `initiator_actor_id` + routing
  mechanism (component 6, MVP form).
- Pre-registered protocol (`protocol.py`): 30 discovery + 10 held-out
  configs (held-out = high-deception corner of goal/tool space), 8 seeds,
  frozen detectors + frozen top-k MI channels re-scored with no re-fitting
  (components 3–4). 19 tests pass.
- Acceptance run recorded: discovery detection 0.37 (light) / 0.94 (full),
  false-alarm 0.023/0.068; held-out detection 0.80/1.0.
- Honest findings incl. negatives: `results/FINDINGS.md` (F-1: held-out
  region saturated at 100% violations → MI transfer test degenerate, flagged
  mechanically; F-2: light tier blind to harm-magnitude violations —
  emergent re-derivation of the old N-10 bearer-welfare finding; F-3:
  residual full-tier misses are small-n L1 cases, same lesson as N-12;
  F-4: detector/label sensitivity mismatch near the boundary).
- Docs: `MILESTONE-v5-goal-agents.md` Phase 1 marked implemented (new line),
  `experiments/embedded-simulation/TODO.md` cross-refs updated,
  `experiments/README.md` now lists all three lines.

## Decisions
- New folder instead of extending `embedded_sim` — preserves comparability
  of the old line's recorded results (user direction).
- Plan's "not yet decided" items resolved and documented (not silently):
  uniform Dirichlet(1) weight sampling (adversarially-optimized weights
  deferred to Phase 2 with red team); resource budget as a hard shadow-route
  constraint, not a fourth utility weight; 40×8 grid after profiling.
- F-1 follow-up (subtle-band held-out region) requires fresh
  pre-registration; deliberately NOT re-picked after seeing labels.
- Board is honest by construction; capture-of-the-certifier regress stated
  as an open limitation, per the plan.

## Open / next
- Second pre-registered held-out region in the subtle-deception band (F-1).
- Wilson-bound style small-n test for d1 (F-3; pre-register first).
- Phase 2: red-team integration + adversarially-optimized goal weights.
- Old-line TODOs unchanged (capture-side twins, N-12 seeds 11/16, MI-scan
  split stability).

## Key paths
- `experiments/goal-agent-simulation/` (README, `goal_sim/`, `run_phase1.py`,
  `tests/`)
- `experiments/goal-agent-simulation/results/phase1_acceptance.{json,md}`
- `experiments/goal-agent-simulation/results/FINDINGS.md`
- `experiments/embedded-simulation/MILESTONE-v5-goal-agents.md` (Phase 1 status)

## Commits
- None (not requested).
