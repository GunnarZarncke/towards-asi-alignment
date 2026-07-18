# 2026-07-18 — Graded lab PLAN_v4: V4-0/V4-1/V4-2 implemented for R-MB1 + R-MB4 (GL-79)

## Trigger

User: "read the v4 plan and implement up to v4-2 unless you are blocked
or have to ask. Stop if questions timeout." (`experiments/graded-lab-simulation/PLAN_v4.md`.)

## Done

- **V4-0 (fixture layer + rig contract):**
  - New `graded_lab/harness/fixtures.py` — `ReferenceFixture` +
    `build_reference_fixture()` (serial and `ProcessPoolExecutor`-parallel);
    promotes the GL-75c parallel-runner pattern.
  - New `graded_lab/harness/rigs/` package: `base.py` (`PreconditionReport`,
    `RigResult` with `outcome ∈ {pass, null, skip}`,
    `substrate_class ∈ {S-blind, S-fixture, S-inherited}`),
    `r_mb1_unit_discovery.py`, `r_mb4_detector_transfer.py`.
  - `machinery_transfer.py` left **unmodified** (not decomposed) — the new
    rigs import its public/private functions instead of duplicating logic,
    so GL-76/GL-77 stay the frozen coupled-battery record and trivially
    reproduce bit-for-bit (nothing changed).
  - New CLI `scripts/run_v4_rig.py --rig {r-mb1,r-mb4} [--workers N] [--smoke]`.
  - `CODE_VERSION` bumped to `graded-lab-0.40.0`; pin updated in
    `tests/test_config.py`.
- **V4-1 (pre-registration freeze), scoped to R-MB1 + R-MB4 only:**
  - `DESIGN.md` "PLAN_v4 pre-registration (V4-1, frozen 2026-07-18, R-MB1 +
    R-MB4 scope)" — preconditions, constants, predictions, and pass/null/SKIP
    harvest sentences, written **before** either battery ran.
  - R-MB1 precondition: mean same-tick co-activity events per multi-member
    C5 mechanism (computed from `primitive_log` only, never UAD output),
    threshold `K_MIN_MEAN_COACTIVITY = 1.0`.
  - R-MB4 precondition: ≥ 3 of {ACL-membership denials, `vote.cast` calls,
    pressure-injected tasks} exercised across seeds (mechanical count),
    `MIN_PHENOMENA_KINDS_EXERCISED = 3`.
  - The other eight rigs (`R-MB9`, `R-MB7d`, `R-MB6a/b`, `R-MB7`, `R-MB2`,
    `R-MB5`, `R-MB8`) are explicitly **not** frozen — `PLAN_v4.md`'s open
    questions (R-MB6b substrate; R-MB7 budget; R-MB5/R-MB8 worth-it) were
    not needed for this scope and were not asked (no blocker for V4-2).
- **V4-2 (scored batteries on S-inherited `generated_ecology_v3.json`, 20 seeds):**
  - `results/v4_r_mb1.json`: precondition **satisfied** (mean 36.77
    co-activity events/mechanism); P1/P2 **false**; outcome **null**.
    Interesting result: co-activity is *not* the reason UAD fails on
    v3_grown (GL-76's original diagnosis is falsified as a full
    explanation), narrowing rather than closing the open question.
  - `results/v4_r_mb4.json`: precondition **not satisfied** (0 ACL
    denials across all 20 honest reference seeds; votes=103,
    pressure_injected=179; only 2/3 kinds); outcome **SKIP**.
  - `results/FINDINGS.md` GL-79 records both with full tables and the
    honest interpretation (does not conflate with GL-74's
    `machinery_transfer_verified=true`, which is about hand-built
    slice-D probes, not the honest reference fixture).
- Tests: `tests/test_fixtures.py`, `tests/test_rigs_base.py`,
  `tests/test_rig_r_mb1.py`, `tests/test_rig_r_mb4.py` (fast unit tests +
  `@pytest.mark.slow` integration tests against the real fixtures/ecology).
  Full `pytest -q -m "not slow"` suite green (exit 0) after the change.
- `REPRODUCTION.md` §10.2 added (rig CLI usage, smoke commands).
- `PLAN_v4.md` header + stage table updated to mark V4-0/1/2 done for
  R-MB1/R-MB4 and to flag every other rig as still unfrozen.

## Decisions

- Did not literally "decompose `machinery_transfer.py`" as PLAN_v4's
  architecture section suggested — reusing its functions from the new
  rigs (including two underscore-prefixed helpers) satisfies the reuse
  intent with materially less regression risk to the frozen GL-76/77
  numbers, and the plan's own gate ("GL-76 reproduces bit-for-bit through
  the new plumbing") is met trivially by not touching it.
- R-MB1's `run_rig` reuses the fixture's already-run passive episode
  directly rather than calling `score_uad_on_reference_episodes` (which
  would have re-simulated every reference episode a second time) —
  caught and fixed mid-session; only the intervention arm pays for its
  own additional counterfactual episodes, per PLAN_v4 architecture item 2.
- Chose not to block on PLAN_v4's three open questions (R-MB6b substrate,
  R-MB7 budget/model, R-MB5/R-MB8 worth-it) since none of them gate
  R-MB1/R-MB4/V4-2; documented them as still-open in both `PLAN_v4.md` and
  `DESIGN.md` rather than guessing answers.
- Deferred the manuscript harvest for GL-79 until more rigs land, so
  ch07/ch33/ch41/ch42 get one coherent v4 update instead of a partial one.

## Open / next

- Answer PLAN_v4's three open questions to unblock V4-1 freeze for the
  remaining rig catalog.
- V4-3 next per the plan: R-MB9 (contradiction surface) ∥ R-MB7d (channel
  ablation), both "small build" rigs on S-inherited/S-fixture.
- R-MB1's null (co-activity present, UAD still fails) is a loose thread
  worth a small follow-up: is the bottleneck action-series granularity,
  CMI window/lag, or per-tick signal sparsity? Not investigated here.
- No manuscript harvest yet for GL-79 — flagged for a later session once
  more v4 rigs land.

## Key paths

- `experiments/graded-lab-simulation/PLAN_v4.md`
- `experiments/graded-lab-simulation/DESIGN.md` ("PLAN_v4 pre-registration" section)
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-79)
- `experiments/graded-lab-simulation/graded_lab/harness/fixtures.py`
- `experiments/graded-lab-simulation/graded_lab/harness/rigs/`
- `experiments/graded-lab-simulation/scripts/run_v4_rig.py`
- `experiments/graded-lab-simulation/results/v4_r_mb1.json`,
  `results/v4_r_mb4.json`

## Commits

- `e85e5e3` — "Implement PLAN_v4 fixture layer + R-MB1/R-MB4 rigs
  (GL-79), freeze V4-1 design for R-MB9/R-MB7d, and add
  channel_severance primitive." (combined with the V4-1 R-MB9/R-MB7d
  freeze session below — committed together, end of session).
