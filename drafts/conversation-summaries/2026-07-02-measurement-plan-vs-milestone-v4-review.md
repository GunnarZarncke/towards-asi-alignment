# 2026-07-02 — Review measurement-protocol plan against Milestone v4

## Trigger

User: "parallel work concluded. Note that there has been work on the
experiment. Review the plan against the changes." Following up on the
Python-first `strengthen_measurement_protocol` plan (queued, not yet
executed) after a parallel session landed embedded-sim Milestone v4.
Same-session follow-up: "additional run results are in. review the plan
again" after a parallel session ran the full-seed frozen validation.

## Done

- Diffed `.cursor/plans/strengthen_measurement_protocol_940d8c38.plan.md`
  against the current `experiments/embedded-simulation/` tree.
- Confirmed Milestone v4 (`0e7d18c`, `eb9fec0`) touched the **main**
  `lab.py` -> `audit_core/simulator.py` pipeline, not the **toy**
  `structural_fixtures.py` -> `trace_ingest.py` path the plan targets;
  they share only `audit_core/info.py`.
- Checked each plan item against the current tree (see plan file's "Review
  update" section for full detail):
  - `probe-scan`/`dense-profiles`/`docs-lean-todo`: unaffected, still valid.
  - `estimator-ci`: partially superseded — generic bootstrap CI helpers now
    exist (`embedded_sim/methodology.py`) but not per-estimate MI/CMI CIs;
    `cci_interventional.py`'s `ivl` CMI is still a bare point estimate.
  - `threshold-calibration`: largely superseded — `frozen_handle_calibration()`
    + a 10-seed holdout already exist, but `results/embedded_frozen_validation.md`
    only exercises 2/10 seeds, one instrumentation level, one blended
    correct-rate, and shows unexplained 0% `capture_mild` recall.
  - `cci-coordinates`: mostly superseded — `cci_audit.py` already computes
    every `CCICertificate` coordinate (latency, manipulation, irreversibility,
    plurality, independence, exit_capacity, ontology_translation) from real
    trace/board signals for the main pipeline; the plan's original premise
    (only `manipulation` measured, rest placeholders) was stale.
  - Verified the N-8 "lag-3" claim is about the *pinned* `408444b` fixture
    (committed separately in `tests/fixtures/trace_biq_calibration_columns.json`),
    unrelated to `structural_fixtures.py`'s live PROBE_LAG 3->0 change, which
    was an earlier, different bugfix (`NEGATIVE_RESULTS.md` #1, interventional
    lag-read mislabeling honest controllers as captured).
- Rewrote the plan file's todos to redirect the superseded items and added
  a "Review update" section documenting the above so the re-scoping is
  traceable without re-deriving it.

## Done (follow-up: full-seed frozen validation landed)

- Noticed (uncommitted, in-flight) working-tree changes: `embedded_sim/progress.py`
  (new progress-logging module) plus a regenerated
  `results/embedded_frozen_validation.{md,json}` from
  `run_suite.py --frozen --full-frozen`: all 10 `FROZEN_VALIDATION_SEEDS`
  (21-30) x all 4 instrumentation levels x all 18 scenarios, T=800,
  2355.87s runtime, 720 raw episodes.
- Confirmed this substantially executes the redirected `threshold-calibration`
  plan item: resolves the earlier 0%-`capture_mild`-recall mystery (now 70%
  at every handle-instrumented level, 0% at `none` -- correct, no
  instrumentation can't detect capture).
- Computed the latent per-scenario x per-level breakdown directly from the
  already-collected `runs` array in `embedded_frozen_validation.json` (ad
  hoc Python, not committed anywhere) since the committed `_md_frozen`
  report only surfaces the blended rate + `capture_mild`. Found two new
  patterns not yet in any report:
  - `light_handles` reads 0% on 5 of 15 held-out scenarios
    (`bearer_mismap`, `bundle_goodhart`, `grounding_silent_gap`,
    `instrument_capture`, `successor_relabel`) that `medium`/`strong_handles`
    catch at 100% -- a cliff, not a gradual curve.
  - `capture_mild` (70%), `legitimacy_theater` (90% at medium/strong), and
    `weak_not_captured` (70%) never reach 100% even at `strong_handles` --
    looks like a real detection ceiling, not an instrumentation-tier gap.
- Updated `.cursor/plans/strengthen_measurement_protocol_940d8c38.plan.md`
  with a "Review update #2" section recording this; did not touch
  `NEGATIVE_RESULTS.md`, `batch.py`, or the committed results files
  themselves since another session has uncommitted edits there.

## Decisions

- Redirect `threshold-calibration` to first strengthen/validate the
  *existing* main-pipeline frozen calibration (full 10-seed holdout,
  per-profile/per-bridge TPR/FPR, explain `capture_mild` 0% recall) rather
  than building a parallel toy-path script from scratch.
- Reduce `cci-coordinates` to an architecture/documentation question (should
  `WorkedInstance.lean` eventually be backed by the richer main-pipeline
  `CCICertificate` instead of the toy fixture?) rather than a new
  `measure_cci_coordinates.py` — nearly everything it would have computed
  already exists.
- Keep `estimator-ci` but reuse `methodology.py`'s bootstrap helpers and
  extend the target to `cci_interventional.py`'s `ivl`, not just the toy path.
- Did not execute any plan item this session — user skipped the follow-up
  "how do you want to proceed" question, so left work paused at the updated
  plan for explicit pickup.

## Open / next

- The full-seed run itself is done (by a parallel session); nothing further
  executed this pass — pure analysis of results already produced.
  Recommended next: (a) add the per-scenario x per-level table to
  `_md_frozen`'s report generator (cheap, data already collected, no
  rerun); (b) investigate the `light_handles` 5-scenario cliff and the
  sub-100%-at-`strong_handles` ceiling on 3 scenarios; (c) record whichever
  of those turns out to be a genuine, confirmed limitation in
  `NEGATIVE_RESULTS.md` — deferred to avoid clobbering that file's other
  in-flight edits.
- `estimator-ci`, `probe-scan`, `dense-profiles` remain queued as originally
  scoped (see plan file).
- `cci-coordinates` needs a human/architecture decision, not just
  implementation, before further work: is porting `WorkedInstance.lean` onto
  the main pipeline's `CCICertificate` in scope, or should the toy path stay
  intentionally simple?

## Key paths

- `.cursor/plans/strengthen_measurement_protocol_940d8c38.plan.md` (updated)
- `experiments/embedded-simulation/embedded_sim/audit_core/cci_audit.py`
- `experiments/embedded-simulation/embedded_sim/audit_core/cci_interventional.py`
- `experiments/embedded-simulation/embedded_sim/audit_core/calibration.py`
- `experiments/embedded-simulation/results/embedded_frozen_validation.md`
- `experiments/embedded-simulation/embedded_sim/methodology.py`

## Commits

- (none this session — plan-file and session-log edits only, outside the
  git-tracked repo tree for the plan file itself)
