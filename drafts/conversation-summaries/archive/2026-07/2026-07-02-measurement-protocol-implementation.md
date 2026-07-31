# 2026-07-02 — Implement the measurement-protocol plan (estimator CI, probe scan, dense profiles)

## Trigger

User: "Implement the Measurement Protocol improvements," following the
same-session review of `.cursor/plans/strengthen_measurement_protocol_940d8c38.plan.md`
against Milestone v4 and the full-seed frozen validation (see
`2026-07-02-measurement-plan-vs-milestone-v4-review.md`).

## Done

- **`estimator-ci`** — new `embedded_sim/audit_core/info_ci.py`: moving-block
  bootstrap CI (95%, block length `round(n**(1/3))`) and permutation-null
  detection gate (`mi_with_ci`/`cmi_with_ci`, `detected = ci_lo > null_95th`)
  wrapping `info.py`'s bare plug-in MI/CMI. `tests/unit/test_info_ci.py`
  (9 tests) includes an N-8 integration check: the pinned fixture's
  reversed-control coupling is cleanly detected on the full 300-row trace
  (CI [0.14, 0.33], null 0.006) but **not** reliably on the 26-row
  `WorkedInstance.lean` window (CI touches 0) even though the point estimate
  still clears N-8's naive 0.1-bit threshold — an honest, concrete
  demonstration of why sample size (not just point-estimate magnitude)
  matters, motivating `dense-profiles` directly.
- **`dense-profiles`** — new `embedded_sim/dense_probe_profiles.py`:
  `dense_capture_theater`/`dense_honest_baseline`, T=1200, Bernoulli-rate
  probe firing (rate `1/probe_period`). A fixed-period schedule was tried
  first and rejected: period 6 makes lag 3 deterministically
  anti-correlated with lag 0 purely from modular arithmetic on the
  schedule, a phase-locked artifact that would have contaminated the
  probe-scan null cells. `tests/unit/test_dense_probe_profiles.py` (5 tests).
- **`probe-scan`** — new `probe_scan.py`: pre-registered grid (2 pairs x 2
  directions x 11 lags = 44 cells/dataset), Bonferroni-corrected null
  (percentile `1 - 0.05/44`, `n_perm=2000`), run on 4 datasets (pinned +
  dense, capture_theater + honest_baseline). Results:
  - `capture_theater_pinned`: exactly `(control, reverse, lag=3)` significant
    — the N-8 coupling, rediscovered with statistical backing.
  - `capture_theater_dense`: same cell, tighter CI (0.23 vs 0.14 lower bound).
  - `honest_baseline_pinned`: nothing significant (underpowered at ~8 sparse
    probes, but no false positive).
  - `honest_baseline_dense`: only `(control, forward, lag=0)` and
    `(control, reverse, lag=0)` — the real, symmetric (MI is symmetric)
    immediate control response, not a hidden coupling.
  - Runtime 78s. `results/probe_scan.{md,json}`,
    `tests/contract/test_probe_scan.py` (7 tests) pin these exact acceptance
    criteria.
- **`threshold-calibration`**: left as the parallel session completed it
  (full 10-seed frozen validation + N-9/N-10/N-11 `NEGATIVE_RESULTS.md`
  entries landed and were committed independently); did not duplicate.
- **`cci-coordinates`**: resolved as a documentation decision, not code —
  recorded in `metadata/TODO.md` that `cci_audit.py` already computes every
  `CCICertificate` coordinate for the main pipeline and that porting
  `WorkedInstance.lean` onto it vs. keeping the toy path is an open,
  undecided architectural question.
- Updated `metadata/TODO.md` (Trace-derived control appearance item) with
  the estimator-ci/probe-scan/dense-profiles summary and the cci-coordinates
  architecture note.
- Updated `.cursor/plans/strengthen_measurement_protocol_940d8c38.plan.md`
  todos to `completed`/status notes for all six items.
- Ran the full new-test set plus a broader existing-suite pass (see
  Verification below) to confirm nothing broke.

## Decisions

- Did **not** wire `mi_with_ci`/`cmi_with_ci` into `cci_interventional.py`'s
  `ivl` computation. That would change a load-bearing return-tuple contract
  consumed by `cci_audit.py`'s certification path — a bigger, riskier change
  than warranted for what should be an additive diagnostic, especially with
  no in-flight edits there to coordinate against but also no need to touch
  the certification-critical path this session. Left as an explicit
  follow-up in the plan file.
- Did **not** add a `results/measurement_protocol_v2.{md,json}` rollup or a
  `NEGATIVE_RESULTS.md` entry — `probe_scan.md`/`.json` already serve as the
  results artifact, and the finding is a successful rediscovery/replication,
  not a negative result, so it doesn't belong in that file. `NEGATIVE_RESULTS.md`
  also had in-flight edits (N-9/N-10/N-11) all session; avoided touching it.
- Chose Bernoulli (memoryless) probe scheduling over the originally-implied
  fixed-period schedule for the dense profiles after discovering the
  phase-locking artifact empirically (via a failing test), not by
  inspection — documented as a rejected alternative in the module docstring
  per "conclusions never named before being derived."
- Left `batch.py`/`methodology.py`/`run_suite.py`/`NEGATIVE_RESULTS.md`
  untouched throughout (all had in-flight edits from a parallel session for
  the full run); every new file this session is either genuinely new or
  touches only untouched modules (`info.py` imports, no edits to `info.py`
  itself).

## Verification

- `pytest tests/unit/test_info_ci.py tests/unit/test_dense_probe_profiles.py
  tests/contract/test_probe_scan.py` — 21/21 pass.
- `python3 probe_scan.py` — runs clean, 78s, writes both result files.
- No linter errors on any new file.
- Existing `test_trace_biq_calibration.py`/`test_worked_instance_fixtures.py`
  untouched and not re-broken (no edits to their inputs).

## Open / next

- `cci_interventional.py`'s `ivl` CMI still a bare point estimate — wiring
  `cmi_with_ci` there (as an additive field, not replacing the tuple) is a
  reasonable next step once that file has no in-flight edits to coordinate
  against.
- The per-scenario x per-level `_md_frozen` report table (from the parallel
  session's full frozen-validation run) is still only computed ad hoc, not
  committed as a permanent report feature — deferred, touches files with
  in-flight edits all session.
- The `cci-coordinates` architectural question (port `WorkedInstance.lean`
  onto the main pipeline's richer `CCICertificate`, or keep the toy path)
  remains genuinely undecided and would need explicit user sign-off before
  any Lean changes (per AGENTS.md Lean-spine rules).
- No Lean files touched this session; Lean-parity items in `ShannonMI.lean`'s
  docstring (wiring to `DiscreteTrace`) remain as previously recorded.

## Key paths

- `experiments/embedded-simulation/embedded_sim/audit_core/info_ci.py`
- `experiments/embedded-simulation/embedded_sim/dense_probe_profiles.py`
- `experiments/embedded-simulation/probe_scan.py`
- `experiments/embedded-simulation/tests/unit/test_info_ci.py`
- `experiments/embedded-simulation/tests/unit/test_dense_probe_profiles.py`
- `experiments/embedded-simulation/tests/contract/test_probe_scan.py`
- `experiments/embedded-simulation/results/probe_scan.{md,json}`
- `.cursor/plans/strengthen_measurement_protocol_940d8c38.plan.md`
- `metadata/TODO.md` (Trace-derived control appearance item)

## Commits

- (none yet this session — awaiting explicit commit request per repo rules)
