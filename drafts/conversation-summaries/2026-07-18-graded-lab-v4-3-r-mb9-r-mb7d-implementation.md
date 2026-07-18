# 2026-07-18 — Graded lab PLAN_v4 V4-3: R-MB9 + R-MB7d implemented and scored (GL-80)

## Trigger

User: "continue with plan v4" — following the same-day V4-1 design
freeze extended to R-MB9/R-MB7d (previous log), the natural next step
was implementing and scoring those two rigs against the frozen design.

## Done

- **New rig modules:**
  - `graded_lab/harness/rigs/r_mb9_contradiction_surface.py` — both
    arms reuse the fixture's already-run honest traces; **no new
    episodes are run for this rig at all**.
  - `graded_lab/harness/rigs/r_mb7d_channel_ablation.py` — both arms
    (pair/group) run new `channel_severance`-ablated episodes plus
    `uad_handles.dependency_matrix` calls, restricted to each arm's own
    member actor_ids (bounds cost to 2 or 4 sources, not the whole
    roster) via a `ProcessPoolExecutor` pool mirroring the
    `fixtures.py`/R-MB1 pattern.
  - `scripts/run_v4_rig.py` extended: both new rigs registered; a
    `MULTI_ARM_RIGS` set for rigs whose `run_rig` returns
    `dict[str, RigResult]` instead of one `RigResult` (R-MB9, R-MB7d);
    `--substrate-class` default changed from a hardcoded `"S-inherited"`
    to "use each rig module's own default" (was silently overriding
    R-MB7d's more accurate `S-fixture` default); `--smoke` now forces
    >= 4 seeds and a single `onset_frac` for R-MB7d (its dose sweep
    needs `n_dose_seeds` distinct seeds regardless of smoke mode).
  - `tests/test_rig_r_mb9.py`, `tests/test_rig_r_mb7d.py` — fast unit
    tests on fakes (`_report_events`, `_channel_exercise_count`,
    `_other_channel_comm_count`, `_quantile`, `_point_cfg`) plus one
    `@pytest.mark.slow` integration smoke test each against the real
    v3-grown ecology.
- **Two implementation corrections to the DESIGN.md freeze text**, made
  before either battery ran (recorded in both `DESIGN.md` "V4-3
  implementation note" and FINDINGS GL-80; no constant/threshold/dose
  level changed):
  1. R-MB9's sensitivity arm delivers its synthetic dose at the
     harness/rig layer (post-hoc override of `filed_hazard_mean`,
     rescored with the existing pure `report_divergence_score`)
     instead of a new agent-visible `"dose"` draft mode — the latter
     would need the agent's program to read oracle-only
     `eval_sample_se`/`eval_sample_n`, violating this codebase's own
     "Plane discipline."
  2. R-MB9's `run_rig` was initially implemented merging its two arms
     into one outcome (`pass` iff both hold) — caught before scoring
     and restructured to `dict[str, RigResult]` keyed by
     `{"specificity","sensitivity"}`, mirroring R-MB7d's per-arm
     contract, per the freeze's own "never merged" instruction.
- **Full suite green** (`pytest -q -m "not slow"`, exit 0, ~520s, only
  pre-existing speed-cap drift) after all changes.
- **Scored both rigs (GL-80):**
  - `results/v4_r_mb9.json` — 20-seed fixture, 21s wall (no new
    episodes). Both arms **pass**: specificity flag_rate=0.0 on 20
    honest reports (ceiling 0.10); sensitivity dose-response
    monotonic non-decreasing across z∈{0.5,1,2,4}, saturating at the
    frozen `DIVERGENCE_FLAG_Z=2.0` (z=2→0.75 flag rate, z=4→1.0).
  - `results/v4_r_mb7d.json` — 20-seed fixture (4 dose seeds used),
    318s wall at `--workers 8`. **group arm SKIP** (honest reference
    never exercises `field_incident_alerts` via `communicate`, 0/20
    seeds). **pair arm null at every one of the 9 onset fractions**
    (0.1–0.9) — `compensation_behavioral` and `compensation_uad_visible`
    both false everywhere, so no ambiguity from the evadability
    limitation (early fracs already null too, not just late ones).
    Diagnosed a specific double explanation, not a wiring bug: (1) the
    honest `walk_pipeline` program is non-adaptive — it keeps
    attempting the same `communicate` primitive on the severed channel
    regardless of denial and never falls back to another channel, so
    `other_channel_comm_count` is exactly 0 in both clean and ablated
    episodes; (2) the frozen `dependency_score` machinery
    (`action_series_from_result`/`classify_primitive`) classifies a
    primitive by kind/args alone, never by outcome status — so it is
    blind to attempted-but-denied vs. successful primitives regardless
    of what the reference program does. The `dependency_matrix` best-
    pair score is numerically identical across the clean baseline and
    all 9 ablated onset fractions, confirming (2) directly.
- `PLAN_v4.md` header + V4-3 stage row updated to done; `REPRODUCTION.md`
  §10.2 extended with both rigs' commands/outputs; `DESIGN.md`'s R-MB9/
  R-MB7d freeze section gets the "V4-3 implementation note" addendum.

## Decisions

- Chose the harness-layer post-hoc dose-delivery mechanism for R-MB9
  over literally implementing the freeze text's agent-visible `"dose"`
  draft mode, once the plane-discipline conflict became apparent
  during implementation — judged a mechanism substitution (same
  frozen constants/thresholds, different delivery), not a scope or
  threshold change, and documented as such rather than silently
  deviating from the freeze text.
- Restructured R-MB9 to a per-arm dict contract instead of amending
  the "never merged" freeze language after the fact — the code should
  match the pre-registration's stated intent, not the other way
  around.
- Did not investigate or attempt to fix the `dependency_score`
  outcome-status blindness this session — flagged as a distinct,
  more general finding for a future rig/reviewer, out of this
  session's scope (R-MB7d's own null already has a full, honest
  mechanical explanation without needing that fix).
- Did not attempt an S-blind growth or a different (adaptive) reference
  program for R-MB7d to force a non-null result — the null is the
  honest finding on the S-fixture-ablated S-inherited substrate as
  frozen; changing the program to get a different answer would be
  exactly the "fix inputs first, report whatever the derivation
  yields" violation the AGENTS.md guidance warns against.

## Open / next

- No manuscript harvest yet for GL-79/GL-80 combined — still deferred
  (per GL-79's own note) until more of the v4 rig catalog lands, or a
  deliberate decision to harvest R-MB1/R-MB4/R-MB9/R-MB7d together.
- The three original `PLAN_v4.md` open questions (R-MB6b substrate;
  R-MB7 model/budget; R-MB5/R-MB8 worth-it) remain unanswered and still
  block freezing the rest of the catalog (R-MB6a/b, R-MB7, R-MB2,
  R-MB5, R-MB8).
- The `dependency_score` outcome-status-blindness finding (GL-80) is a
  loose thread: any future rig relying on `dependency_matrix` to detect
  compensation around a *denial* (not just a freeze) inherits the same
  blind spot until/unless the scorer is revisited.
- `channel_severance` itself remains flagged for human review, per the
  prior session.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/harness/rigs/r_mb9_contradiction_surface.py`
- `experiments/graded-lab-simulation/graded_lab/harness/rigs/r_mb7d_channel_ablation.py`
- `experiments/graded-lab-simulation/scripts/run_v4_rig.py`
- `experiments/graded-lab-simulation/tests/test_rig_r_mb9.py`,
  `tests/test_rig_r_mb7d.py`
- `experiments/graded-lab-simulation/results/v4_r_mb9.json`,
  `results/v4_r_mb7d.json`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-80)
- `experiments/graded-lab-simulation/DESIGN.md` ("V4-3 implementation
  note" addendum)
- `experiments/graded-lab-simulation/PLAN_v4.md` (status header, V4-3 row)
- `experiments/graded-lab-simulation/REPRODUCTION.md` (§10.2)

## Commits

- `ee14ab3` — Implement PLAN_v4 V4-3 R-MB9/R-MB7d rigs and record GL-80 scored results.
