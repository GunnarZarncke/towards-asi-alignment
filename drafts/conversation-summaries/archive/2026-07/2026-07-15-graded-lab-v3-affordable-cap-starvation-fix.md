# 2026-07-15 — Graded lab v3: affordable-set starvation bug (GL-50)

## Trigger

Follow-up to the slice C (GL-49) session: "Why does the integrated
reference battery fail? Was this expected?" — GL-49 had reported C1-v3 as
`not_exercised` on the integrated fixture and called it a "reportable
finding," implying benign low-variance. The user wanted to know if that was
accurate.

## Done

- Traced the failure precisely: `deploy_rate`/`bearer_harm` were **exactly
  0.0** in every reference-battery episode, not merely low-variance. Root
  cause was two independent bugs (either sufficient alone):
  1. `affordable.py`'s `build_affordable_set()` offers a `read` candidate
     for every workspace artifact path, unbounded; the whole list is
     truncated to `AFFORDABLE_CAP=24` with `read` ranked *ahead of* `call`.
     Any program that repeats a `write`/`communicate` to a uniquely-counted
     artifact path accumulates artifacts without bound, eventually starving
     out `call` actions (pipeline triggers, access requests, votes,
     transfers) entirely. Reproduces in a pure v1 scenario too
     (`watched_flag_config`), not v3-specific.
  2. `programs.py`'s `_try_governed_mechanism()` channel branch was missing
     the one-shot `done` guard the other three branches (artifact/vote/
     transfer) already had, contradicting its own docstring.
- Fixed both (user approved after an `AskQuestion` on how to proceed).
  `_cap()` now reserves all `call` candidates unconditionally (structurally
  bounded), filling remaining budget by the old priority order; channel
  exercise now marks itself done after one send.
- Verified on the integrated fixture (20 seeds): `C4` deploy_rate 0.0→0.7
  with real cross-seed variance; `C1-v3` passes on all 5 conflicts
  (`r ≈ -0.29` to `-0.31`). `C3` still `False` — confirmed pre-existing,
  unrelated to this session (checked against the pre-slice-E/B fixture).
- Ran the full test suite; isolated the blast radius precisely (reverted
  `_cap` alone, re-ran the failing set, to attribute each failure to fix 1
  vs fix 2).
- Fix has a wide blast radius since `affordable.py` is shared by every
  ecology version. Re-pinned two regression digests (mechanical, dated
  comments explaining why). Traced and documented — but per user decision,
  did **not** fix — three UAD ground-truth-recovery test failures and one
  budget-aware-agent comparison test failure, all attributable to the same
  root fix removing a confound the old (buggy) behavior had been providing
  as an accidental detection signal. Full mechanism for each documented in
  FINDINGS GL-50.
- `CODE_VERSION` bumped `0.25.0` → `0.25.1`; also fixed a stale
  `test_config.py::test_code_version` pin unrelated to this session's work
  (leftover from an earlier version bump).
- Updated `FINDINGS.md` (new GL-50 entry + correction to the GL-49
  addendum), `DESIGN.md` (slice C note), and the integrated fixture's
  `v3_fixture_metadata` note to stop claiming `not_exercised`.

## Decisions

- User explicitly chose to fix the starvation bug at the engine level
  (`affordable.py`) rather than only recalibrating the fixture, after being
  shown the trade-off via `AskQuestion`.
- When the engine fix broke 3 UAD tests + 2 pinned digests + 1 comparison
  test, stopped and asked again rather than silently re-pinning/re-tuning.
  User chose: keep the engine fix, re-pin digests now, but **leave the UAD
  methodology question open** (don't change `uad_intervention.py`/
  `uad_passive.py` merge/detection logic this session) — documented as an
  explicit open finding instead.
- Two candidate UAD fix directions were scoped (not implemented): (a)
  accept a strong one-directional `missing_score` in
  `units_from_compensation_matrix` even when the reverse direction is ~0;
  (b) add same-channel co-membership as its own passive edge type
  independent of tick-Jaccard timing overlap.

## Open / next

- **Before citing FINDINGS GL-11/GL-12/GL-16 UAD claims or building slice
  D's growth protocol on ground-truth-recovery assumptions**, resolve the
  three open UAD test failures (see FINDINGS GL-50 for exact diagnosis and
  candidate fixes) and the budget-aware-agent stress-sensitivity comparison
  (GL-16 calibration numbers may need re-measuring now that the starvation
  bug no longer masks `STRONG_AGENT`'s load-sensitivity).
- Slice D (criteria freeze, Part B load-bearing for default/grower paths,
  growth protocol) is next in `PLAN_v3.md`'s build order, but should not
  start until the above UAD question is at least explicitly deferred with
  the user's sign-off (done this session) or resolved.
- C3 (contention liveness) remains `False` on the integrated reference
  fixture — pre-existing, not touched this session, still open.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/world_visible/affordable.py`
  (`_cap`, `AFFORDABLE_CAP`) — the core fix.
- `experiments/graded-lab-simulation/graded_lab/agent_visible/programs.py`
  (`_try_governed_mechanism`) — the one-shot channel fix.
- `experiments/graded-lab-simulation/results/FINDINGS.md` GL-50 — full
  root-cause diagnosis, verification numbers, and the open UAD/budget-aware
  items.
- `experiments/graded-lab-simulation/graded_lab/oracle_only/uad_intervention.py`,
  `.../uad_passive.py` — where the two candidate UAD fixes would land.
- `experiments/graded-lab-simulation/tests/test_uad_blind_scenarios.py`,
  `tests/test_uad_ecology_partition.py`,
  `tests/test_slice_b_completion.py::test_uad_live_coupling_recovers_governed_channel_unit`,
  `tests/test_budget_aware_agent.py::test_budget_aware_agent_more_stress_sensitive_than_frozen_agents`
  — the four tests left failing, all documented, none silently skipped.

## Commits

None — changes are uncommitted in the working tree per the user's standing
"don't commit unless asked" instruction.
