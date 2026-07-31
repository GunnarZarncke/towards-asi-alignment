# 2026-07-06 — Lab-layer sim Phase 7: escalation ladder, red-team search, capture grid

## Trigger

User agreed to delay analysis of Phase 6's light-tier anti-correlation
finding and asked to continue with Phases 7 and 8 "until you run into
questions, then stop (even if question times out)."

## Done

- **`lab_sim/escalation.py`** (new file): full-tier screen
  (`SCREEN_LOW_GATE=0.02`/`SCREEN_HIGH_GATE=0.08`, derived from the
  five-family-mean mechanics, not fit to any battery's numbers) -> bounded
  `K_QUERIES=3` query budget (`select_query_steps`, audit-visible-only,
  prioritizing filed reports whose model reached `deploy`) -> verdict =
  contradiction between a simulated "admit"/"deny" response (drawn from
  the actor's own true `GoalWeights` — the same weights already driving
  playbook choice, since `world.py` never records which playbook an agent
  ran) and a targeted single-file artifact pull, never response style
  alone. This is a deliberate structural fix for `goal-agent-simulation`'s
  own F-20/F-21 finding (disclosure-style scoring inverted guilt). 9 unit
  tests (`tests/test_escalation.py`), including an explicit regression
  guard against the F-21 shape
  (`test_honest_episode_has_zero_divergence_and_never_contradicts_even_
  if_denying`).
- **`lab_sim/redteam.py`** (new file): random-restart coordinate-
  perturbation hill climb (mirrors `goal_sim.redteam` exactly: same
  objective `severity - LAMBDA * full_tier_composite`, same algorithm, same
  "no re-fitting" discipline) over joint (engineer, reviewer,
  release_manager) `GoalWeights`, vs. a uniform-sampling baseline, once per
  repertoire (baseline-only / Phase 6 generated). Uses `MockIsolate` for
  the search phase (hundreds of evaluations) — a recorded, necessary
  deviation from "real backend always," documented in the module
  docstring — and always reproduces the final reported numbers on a
  disjoint seed set with `SubprocessIsolate`. 7 unit tests
  (`tests/test_redteam.py`).
- **`LabConfig.build_params`** (new additive field, CODE_VERSION 0.4.0 →
  0.5.0): discovered mid-phase, not planned — tracing PLAN.md's "regime
  chosen so the sign-off/grant ceiling actually binds" instruction back
  through the mechanics showed the pre-existing hardcoded build params
  (`{"scale": 0.6, "safety_effort": 0.5}`) give an expected hazard (~0.35)
  that never crosses `ontology.REVIEW_HAZARD_THRESHOLD` (0.5), so neither
  capture ceiling had EVER been reachable in any prior battery, including
  Phase 6's. Added one new `LabConfig` field, plumbed through the
  observation channel exactly like `extra_playbooks`, default `None`
  reproducing the old literal byte-for-byte (`programs.py`'s "build" case
  is the only call site touched). Judged in-scope to implement directly
  (additive, one call site, fully backward-compatible, same pattern as
  prior additive fields) rather than stopping to ask. 4 new tests in
  `tests/test_world.py`.
- **`run_phase7.py`** (new file): three batteries run and reported
  together — escalation (27 fresh configs x 5 seeds = 135 episodes,
  `SubprocessIsolate`), red-team (both repertoires, `MockIsolate` search +
  `SubprocessIsolate` report reproduction), capture grid (`BoardConfig.
  capture_start` x `AdminConfig.capture_start`, 4 cells, 10 seeds/cell,
  `SubprocessIsolate`, the new high-hazard `build_params` regime). Wall
  time ~39s total (13.0s of real `SubprocessIsolate` time over 525 isolate
  lifetimes). Output: `results/phase7_battery.json`/`.md`.
- **`results/FINDINGS.md`**: G-4 (escalation ladder: precision 0.97,
  recall 0.87 against oracle-side `report_divergence` ground truth — most
  of the discriminative power comes from the bounded query step, not the
  cheap screen), G-5 (red-team search saturates on the engineer's
  inflate-vs-honest choice; reviewer/release_manager weights are
  behaviorally inert without `build_params`, the same structural gap G-6
  needed to fix for the capture grid — traced, not a search bug), G-6
  (capture grid: board capture alone reproduces the FULL captured-vs-not
  delta; admin capture alone reproduces NONE of it — traced to
  `agents.AdminPolicy.handle_request`'s captured branch only differing
  from the uncaptured one for an out-of-role capability request, which no
  existing playbook, baseline or generated, ever issues — a genuine
  structural negative for that half of F-22's generalization, not a
  contradiction of it).
- Updated `PLAN.md` (status banner, implementation-status note, Phase 7
  block, folder layout), `DESIGN.md` (phase status table, recorded
  measurements, new "Phase 7" section, corrected three forward-hooks notes
  that had prematurely implied Phase 7 covered handle calibration/
  persistence-probe/writer-compromise — it does not), `README.md` (status,
  layout, run instructions), and the top-level `docs/EXPERIMENTS.md` (was
  stale at "Phases 0-5... evaluations have not started," now reflects
  Phase 6 AND Phase 7).
- Test suite: 184 → 200 tests green.

## Decisions

- **`build_params` addition treated as in-scope, not a stop-and-ask
  question.** It is additive, touches exactly one call site in
  `programs.py`, defaults to reproducing prior behavior byte-for-byte, and
  follows the identical pattern already used twice (`extra_playbooks`,
  `persistent_id`). The alternative (reporting "neither ceiling can bind"
  as a pure negative and running the grid anyway) was rejected because it
  would have made the WHOLE capture grid a null result by construction,
  not because the ceilings are actually independent-but-currently-inert —
  a distinction worth surfacing empirically rather than asserting from
  code reading alone.
- **Response propensity in `escalation.py` is keyed off the actor's true
  `GoalWeights`, not off which playbook it ran.** `world.py` deliberately
  never logs playbook identity (see Phase 4 decisions), so there is no
  other host-visible channel to key a response mechanism off of without
  adding one; reusing the same weights that already drive playbook choice
  keeps this "joining the same playbook-driven surface" (DESIGN.md's
  Phase-5-era forward-looking note) rather than inventing a second,
  independent response-choice mechanism `goal_sim.escalation` has
  (`ResponseOption` objects with their own cost/exposure terms) — a
  smaller, recorded scope reduction. One consequence, recorded in
  `escalation.py`'s `RECORDED_COUPLING_NOTE`: at temperature 0,
  "inflate-then-admit" is algebraically unreachable, since action and
  response are pulled in opposite directions on the same two features.
- **`redteam.py` does NOT set `build_params`.** Deliberately kept aligned
  with `goal_sim.redteam`'s "no new tools/mechanisms" scope statement —
  the search is a pure goal-weight search over the EXISTING mechanics, so
  it inherits whichever levers are live under the default config. That
  this made reviewer/release_manager weights provably inert was an
  unplanned discovery (G-5), reported rather than silently patched by
  adding `build_params` to the search too (which would have been a second,
  larger scope decision — left open).
- **Verdict rule uses "at least one contradiction," not a disclose-
  fraction gate.** A single proven contradiction against a pulled artifact
  is already a binary fact; grading it on a continuum would reintroduce
  exactly the "style, not substance" shape `goal_sim`'s F-21 flagged.

## Open / next

- Phase 8 (LLM-agent adapter) remains pending — optional/exploratory per
  PLAN.md, not started this session (see PLAN.md's Phase 8 description for
  scope).
- A red-team variant that ALSO sets a high-hazard `build_params` (giving
  the reviewer axis a genuinely live second lever) is a natural G-5
  follow-up, not attempted.
- An admin-ceiling-binding playbook/probe (a deliberate out-of-role
  capability request) is a natural G-6 follow-up; would need a new
  `step_kind`, so likely belongs with a future BLIND_GENERATION round
  rather than a hand-authored addition.
- Escalation's 10 false negatives (recall 0.87) were not investigated
  further — a query-budget-vs-recall sweep (`K_QUERIES` != 3) is a natural,
  left-open follow-up (G-4).
- The three corrected DESIGN.md forward-hooks notes (handle calibration,
  persistence probe, writer compromise) are genuinely still open, not
  covered by Phase 7 despite PLAN.md's original phrasing suggesting
  otherwise.
- `resume_from` episode chaining (D2) remains the one still-open Phase
  0-5-era forward hook.
- Phase 6's light-tier anti-correlation (G-1) is still explicitly deferred
  per the user's instruction at the start of this session.

## Key paths

- `experiments/lab-simulation/lab_sim/escalation.py`
- `experiments/lab-simulation/lab_sim/redteam.py`
- `experiments/lab-simulation/run_phase7.py`
- `experiments/lab-simulation/results/FINDINGS.md` (G-4 through G-6)
- `experiments/lab-simulation/results/phase7_battery.md`
- `experiments/lab-simulation/DESIGN.md` ("Phase 7" section)
- `experiments/lab-simulation/lab_sim/config.py` (CODE_VERSION 0.5.0 note)

## Commits

(none yet this session — pending user request to commit)
