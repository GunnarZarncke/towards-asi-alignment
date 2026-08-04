# 2026-07-15 — Graded lab V2-2b external review response (GL-42)

## Trigger
User relayed external-review feedback on the just-landed V2-2b
engineering (GL-40): 4 high-severity + 4 medium-severity findings. User
judged the blinding findings (esp. the C3-oracle pilot) to have merit,
judged the execution-isolation gap real but excessive to fix now (asked
to document it for a larger team instead), and asked for a
`REPRODUCTION.md` of high-effort tasks linked from `COLLABORATION.md`.

## Done
- **Fixed now:**
  - Poisson trigger made actually memoryless (removed fixed-cooldown
    refractory period; gate only on the same event still active) —
    `exogenous_workload.py`.
  - Statefulness: added `EpisodeConfig.ecology_override_path`; checker
    (`ecology_complexity.run_reference_episodes`) and pilot
    (`ecology_pilot.run_pilot_episodes`) both load candidates directly
    instead of staging into the shared canonical
    `generated_ecology_v2.json`. Regression tests added.
  - New end-to-end test (`test_ecology_v2_2b_end_to_end.py`): multi-actor
    + workload ecology clears C3 while staying in C4's interior band,
    through the real checker (not a synthetic stand-in). Passed first
    run; speed baseline refreshed.
  - **C3 blinding claim retracted**, per reviewer's own advice ("no
    leak-free middle position") and user's agreement this was the most
    severe finding: `pilot_generic` documented as reference-roster-
    identical (same programs as `WEAK_AGENT`); pilot output filter no
    longer hides contention/deploy signal (only oracle/referee-plane
    fields); `BLIND_GENERATION.md`'s v2-2b brief now states C3's
    qualitative requirement directly.
- **Documented, not fixed (large tasks for a larger team):**
  - C1/C2/C5 are declarative-only (never wired into runtime
    permissions/budgets/rewards) — caveats added to `DESIGN.md`/`PLAN_v2.md`;
    V2-3's C5-as-UAD-ground-truth plan flagged as only meaningful as a
    UAD-coherence check until this closes.
  - "Exogenous workload" is a cost multiplier, not work injection —
    documented in module docstring + brief.
  - Pilot filter is not an execution-isolation boundary — documented,
    not built (user's explicit call).
  - Multi-actor clones are a load test, not heterogeneous actors —
    already disclosed in brief; noted again.
- **New docs:** `REPRODUCTION.md` (4 large work packages with rationale
  and rough shape), `COLLABORATION.md` (ground rules + how to pick up a
  package); both linked from `README.md`.
- **`FINDINGS.md` GL-42** records the full external-review response.
  Also fixed a duplicate/out-of-order GL-40 entry left by the prior
  session.
- Full related test suite green (47+ tests incl. new end-to-end test).

## Decisions
- Adopted the reviewer's binary framing for C3: since a pilot exists at
  all, C3/C4 cannot be credibly blinded — disclose the qualitative
  requirement, reserve blinding for the oracle/referee-plane machinery
  (EAI/severity/detectors/UAD) that Q1–Q3 should rest on.
- Did not attempt runtime-wiring of institutional structure or real
  work injection this session — too large, listed in `REPRODUCTION.md`
  instead.
- Did not build execution sandboxing — user called this excessive for
  now; documented for future larger-team work.
- `CODE_VERSION` stays at `graded-lab-0.19.0` (this is a within-version
  correctness/honesty pass, no schema change).

## Open / next
- No V2-2b growth round yet — still gated on explicit go-ahead +
  physical isolation, per existing rule.
- Large `REPRODUCTION.md` items are unscoped beyond a rough shape;
  should get their own `PLAN_*.md` before code starts.

## Key paths
- `experiments/graded-lab-simulation/REPRODUCTION.md` (new)
- `experiments/graded-lab-simulation/COLLABORATION.md` (new)
- `experiments/graded-lab-simulation/graded_lab/harness/ecology_pilot.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/exogenous_workload.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/config.py` (`ecology_override_path`)
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-42)

## Commits
None (user did not request commit).
