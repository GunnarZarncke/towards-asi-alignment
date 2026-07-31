# 2026-07-05 — Phase 6: responses-side twin, certifier capture, adversarial search

## Trigger

User asked to implement the three Phase 6 candidates recorded at the end of
the prior session (`2026-07-05-goal-agent-line-next-steps-recorded.md`):
responses-side honest twin, capture-of-the-certifier, adversarial
optimization. A mode-switch to Plan was proposed (three substantial new
mechanisms, real design decisions) and declined by the user; proceeded in
Agent mode, designing and documenting each mechanism's pre-registration in
code/docstrings before running anything, consistent with the repo's
existing discipline.

## Done

- **Part A (responses-side twin)**: `goal_sim/twins.py`'s `make_twin`
  extended to replace a twinned spec's `responses` with a single
  full-disclosure `HONEST_TWIN_RESPONSE` whenever the source spec carries
  any responses (targeting F-20's diagnosis). Specs with no responses
  (rounds 1-3) unaffected.
- **Part B (certifier capture)**: `config.BoardConfig.capture_start`
  (new, default `None` = fully backward compatible); `agents.BoardPolicy`
  gets a `tick()`/`captured` mechanism — once captured, `wants_correction()`
  always False, `observe_probe()` no longer escalates, `review_proposal()`
  always approves. `world.py` calls `board.tick()` once per step and
  records a new oracle-only field `board_captured` on every row
  (`channels.ORACLE_ONLY_FIELDS`), never audit-visible by construction.
- **Part C (adversarial search)**: new `goal_sim/redteam.py` — stdlib
  random-restart Gaussian-perturbation hill climbing over `GoalWeights`
  (`ADVERSARY_TOOLS` fixed at full capability), objective = mean severity
  minus full-tier composite (lambda=1.0), plus a uniform-sampling baseline
  at the same evaluation budget for comparison.
- `run_phase6.py`: pre-registered docstring (all three parts), runs all
  three batteries, writes `results/phase6.{json,md}`.
- `tests/test_phase6.py`: 16 new tests (responses-twin transform,
  capture mechanics incl. default-unaffected regression, oracle-only
  field never projected, adversarial objective/search determinism and
  structure).
- `tests/test_actions_and_ontology.py`: extended the Phase-4d field-drop
  helper to also drop the new `board_captured` field so
  `REGRESSION_DIGESTS` (Phase 1) and `PHASE4D_FULL_ROW_DIGESTS` stay
  byte-identical to their originally recorded values; added a fresh
  `PHASE6_FULL_ROW_DIGESTS` baseline over the now fully-grown row schema.
- `results/FINDINGS.md`: F-21 (negative, prediction falsified), F-22
  (mixed), F-23 (positive, weak).
- `README.md`: new "Phase 6" section; "Decisions taken" item 2 and
  "Explicitly out of scope" updated to reflect the now-started
  adversarial-search thread and the now-measured (not resolved) capture
  limitation; "Next steps" rewritten around F-21's escalation-verdict-rule
  finding as the most load-bearing follow-up.
- `MILESTONE-v5-goal-agents.md`: Phase 6 paragraph added.
- Test suite: 87 → 104 tests, all green.

## Decisions

- **Certifier capture is a single binary switch, not probabilistic or
  reversible** (`capture_start` step index) — the simplest mechanism that
  isolates "what happens to every existing signal once the overseer's
  willingness to act goes dark", without adding an unregistered degree of
  freedom.
- **The fixed probe schedule is unaffected by capture** — models routine
  audits continuing on schedule even though the overseer evaluating them
  has stopped acting, the sharper and more realistic failure mode.
- **Adversarial search objective uses the FULL tier composite as the
  penalty term**, not light — models the adversary assuming worst-case
  audit exposure, the strongest test of whether severity/detection can be
  separated.
- **`board_captured` is oracle-only by construction** (never in
  `LIGHT_FIELDS`/`FULL_EXTRA_FIELDS`) — an audit that could see capture
  directly would beg the question the mechanism exists to explore.
- **Kept the Part A twin fix despite the negative result** — it is still
  the correct transform for what it claims (an honest twin's response
  menu should not be the deceptive spec's unmodified menu); the negative
  result is about a separate, pre-existing flaw in the escalation
  ladder's verdict rule that the fix exposed rather than caused.
- **Did not attempt to fix the escalation verdict-rule conflation (F-21)
  in this session** — redesigning `DISCLOSE_FRACTION_GATE` semantics is a
  new mechanism requiring its own pre-registration, out of scope for
  "implement the three next steps"; recorded as the top follow-up instead.
- **Did not re-run Part B under a region where the sign-off ceiling binds**
  (e.g. the held-out high-deception corner) after seeing the discovery-
  region null result — would be exactly the post-hoc region-shopping
  AGENTS.md forbids; recorded as an open follow-up instead.

## Open / next

The most load-bearing open item is new, not one of the original three:
**F-21's escalation verdict-rule conflation** (disclosure-as-style vs.
disclosure-as-admission) needs its own design pass before anything else in
`escalation.py` is trusted for a genuinely honest actor. Also open,
lower-priority: re-testing certifier capture where the sign-off ceiling
actually binds; a larger/different adversarial search. The "later" lab-layer
simulation direction is unchanged (still not started, still gated on these).

## Key paths

- `experiments/goal-agent-simulation/goal_sim/{twins,agents,config,world,
  channels,redteam}.py`
- `experiments/goal-agent-simulation/run_phase6.py`
- `experiments/goal-agent-simulation/tests/test_phase6.py`
- `experiments/goal-agent-simulation/results/FINDINGS.md` (F-21/F-22/F-23)
- `experiments/goal-agent-simulation/README.md` ("Phase 6", "Next steps")

## Commits

None yet — not committed this session (pending explicit user instruction).
