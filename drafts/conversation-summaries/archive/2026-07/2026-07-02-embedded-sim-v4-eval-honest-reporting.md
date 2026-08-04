# 2026-07-02 — Embedded sim: v4 full evaluation, critical interpretation, honest reporting

## Trigger

Run the full v4 evaluation suite (all reports + parameter sweep), interpret the
results critically, record the negative findings, and change the runner's
reporting to be honest instead of flattering. Follow-ups: clean up cut-off
logs; end of session, commit.

## Done

- Ran the full suite (`run_suite.py --all --full-frozen` + parameter sweep);
  regenerated all `results/embedded_*` artifacts plus two new curve artifacts
  (`embedded_access_tier_curve`, `embedded_certification_capacity_curve`).
- Critical interpretation surfaced three negative findings, recorded as
  **N-9/N-10/N-11** in `results/NEGATIVE_RESULTS.md`:
  - **N-9:** `writer_compromise_coordinated` false-passes 44% at medium *and*
    strong handle levels (100% at light) — hash-chained traces prove only
    post-write integrity, not write-time truthfulness; strong buys nothing over
    medium against this attacker.
  - **N-10:** `light_handles` certifies *worse* than passive `none` across
    three independent measurements (~57–63% vs ~89–93%) — partial
    instrumentation is not a safe intermediate step.
  - **N-11:** the access-tier curve as scoped is violation-only (no `honest`
    scenario), so it is flat across tiers and cannot show the
    certification-loss boundary it was built for; the certification-capacity
    curve is the artifact that actually shows the v4 access boundary.
- Honest-reporting changes to the runner:
  - `embedded_sim/methodology.py`: `baseline_adjusted_battery_metrics`
    (separates attack-attributable false passes from unattacked auditor error)
    and `instrumentation_monotonicity_note` (flags level < `none`).
  - `embedded_sim/batch.py` + `run_suite.py`: all curve/battery payloads and
    markdown reports now carry monotonicity notes, `scenario_class_note`
    (capture-only access-tier curve), tier-plateau and small-n notes,
    baseline-adjusted false-pass rates, and mock-planner caveats; the overall
    summary surfaces these instead of raw headline numbers alone.
  - `embedded_llm/llm_runner.py`: `planner_note` stating mock-planner results
    are not independent evidence of LLM attacker capability.
- New `embedded_sim/progress.py` (+ `tests/unit/test_progress.py`):
  line-buffered timestamped progress logging with ETA ticks, wired through all
  batch runners and `run_suite.py` phases, so long runs report where they are.
- Deleted `logs/suite_progress_20260702T162927Z.log` — a cut-off log from a
  smoke run killed mid-stage by `SIGPIPE` (piped through `head -25`). Other
  logs are complete records and were kept.
- Verification: targeted `tests/unit/` + `tests/contract/test_milestone_v4_handles.py`
  run passes (the one mid-run failure was a stale in-flight test file from
  concurrent probe-scan work in the same tree, green on re-run).

## Decisions

- Report **baseline-adjusted** false-pass rates alongside raw ones rather than
  replacing them: raw numbers stay reproducible, but the summary leads with
  attack-attributable rates so auditor error is not credited to defenses.
- N-11 handled as a caveat emitted on the artifact itself
  (`scenario_class_note`) plus a TODO for an honest-scenario arm, rather than
  silently reshaping the curve's scenario set mid-milestone.
- N-10 flagged but not root-caused/fixed this session — deliberate: whether to
  retune `light_handles` thresholds or keep it as a structural
  instrumentation-cost finding is a project decision, left open.
- Full `pytest tests/` is too slow for routine verification (user interrupted
  it); targeted unit + v4 contract tests used instead.
- Commit scoped strictly to this session; concurrent probe-scan/info-CI work
  in the same working tree (`info_ci.py`, `dense_probe_profiles.py`,
  `probe_scan.py`, `.gitignore`, related tests/results) left uncommitted for
  its own session to land.

## Open / next

- Add an honest-scenario arm to `run_access_tier_curve` (N-11 TODO).
- Decide fix-vs-document for the `light_handles` regression (N-10).
- EIG auditor probe selection still deferred (`TODO.md`).
- Scaled live LLM red-team runs remain a contribution path (see `TODO.md`
  § LLM red-team scale-up).

## Key paths

- `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md` (N-9..N-11)
- `experiments/embedded-simulation/embedded_sim/progress.py`
- `experiments/embedded-simulation/embedded_sim/methodology.py`
- `experiments/embedded-simulation/run_suite.py`
- `experiments/embedded-simulation/results/OVERALL_SUMMARY.md`

## Commits

- `fe53c8b` Report embedded-sim v4 metrics honestly and add incremental progress logging
