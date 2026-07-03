"""Dense-probe, longer-trace toy generator profiles for adequate per-lag samples.

Companion to `structural_fixtures.py`, which is intentionally left untouched:
its exact fixtures are pinned/regression-tested elsewhere (`WorkedInstance.lean`,
`calibrate_trace_biq.py`, N-8/N-9/N-10). These profiles exist for one purpose:
give `probe_scan.py` enough probe events per lag cell to detect a real
coupling with a tight confidence interval, instead of the ~8-14 probe events
per 300 steps the historical `capture_theater`/`honest_baseline` fixtures give
(see `test_info_ci.py::test_n8_reversed_coupling_not_reliably_detected_on_26row_window`
for the concrete case: a real coupling whose *point estimate* clears N-8's
naive threshold but whose bootstrap CI still touches 0 on 23 samples).

Two profiles, matching the two fixtures `probe_scan.py` scans:

- `dense_capture_theater`: a hidden delayed coupling (probe intent at step
  `t` shows up in `visible_action` at `t + lag`, low uptake probability) --
  the "captured judge, real but hidden control" case. Default `lag=3` for
  continuity with the historical fixture's accidental coupling (N-8); the
  lag is a parameter, not hard-coded, so `probe_scan.py`'s grid is not
  fitted to one specific number.
- `dense_honest_baseline`: an immediately responsive controller (coupling at
  lag 0 only, deterministic, `judge_captured` constant 0) -- the "no hidden
  delayed structure" null case for every lag/direction the scan checks
  *other than* lag 0 in the forward control direction.

Both emit only the four columns `calibrate_trace_biq.py`/`probe_scan.py` use
(`visible_action`, `intervention_active`, `judge_captured`,
`correction_request`), not a full correction-row schema -- these are
scan-only synthetic series, not `structural_fixtures`-compatible audit rows.

Protocol (fixed before `probe_scan.py` computes anything): `T=1200`,
`probe_period=6` interpreted as a Bernoulli firing rate `1/probe_period`
(-> ~200 probe events in expectation, vs ~14 in the 300-step historical
fixture at a fixed period of 22), `uptake=0.08` (same low-uptake constant as
the historical `capture_theater`, so the *signal-to-noise ratio* is
unchanged and only the *sample size* differs).

Probes fire as an i.i.d. Bernoulli process, not a fixed period. A strictly
periodic schedule (tried first) creates a phase-locked spurious correlation
at *every* lag that shares a common factor with the period -- e.g. period 6
makes lag 3 deterministically anti-correlated with lag 0, since
`t mod 6 == 0` and `t mod 6 == 3` are mutually exclusive by construction.
That is a scheduling artifact, not a detection result, and it would
contaminate exactly the null cells `probe_scan.py` relies on. Bernoulli
firing removes the periodicity so off-lag cells are genuinely uncoupled
(see `test_dense_honest_baseline_responds_at_lag_zero_not_elsewhere`).
"""

from __future__ import annotations

import random

DenseColumns = dict[str, list[int]]

DEFAULT_T = 1200
DEFAULT_PROBE_PERIOD = 6
DEFAULT_LAG = 3
DEFAULT_UPTAKE = 0.08


def dense_capture_theater(
    T: int = DEFAULT_T,
    seed: int = 0,
    *,
    lag: int = DEFAULT_LAG,
    probe_period: int = DEFAULT_PROBE_PERIOD,
    uptake: float = DEFAULT_UPTAKE,
) -> DenseColumns:
    """Denser analogue of the pinned capture-theater fixture's hidden coupling."""
    rng = random.Random(seed)
    probe_rate = 1.0 / probe_period
    intervention_active = [1 if rng.random() < probe_rate else 0 for _ in range(T)]
    correction_request = list(intervention_active)
    judge_captured = [1] * T  # captured throughout, as in the pinned fixture
    visible_action = [0] * T
    probe_index = 0
    for t in range(T):
        if not intervention_active[t]:
            continue
        # Alternate by probe occurrence, not by `t % 2` -- with an even
        # `probe_period` the latter is constant at every probe step and
        # silently degenerates the coupling into a coin flip unrelated to
        # intent (caught by test_dense_honest_baseline_responds_at_lag_zero).
        intent = probe_index % 2
        probe_index += 1
        target = min(t + lag, T - 1)
        visible_action[target] = intent if rng.random() < uptake else 1 - intent
    return {
        "visible_action": visible_action,
        "intervention_active": intervention_active,
        "judge_captured": judge_captured,
        "correction_request": correction_request,
    }


def dense_honest_baseline(
    T: int = DEFAULT_T,
    seed: int = 0,
    *,
    probe_period: int = DEFAULT_PROBE_PERIOD,
) -> DenseColumns:
    """Denser analogue of the pinned honest-baseline fixture: immediate (lag 0)
    response, no hidden delayed coupling, never captured."""
    rng = random.Random(seed)
    probe_rate = 1.0 / probe_period
    intervention_active = [1 if rng.random() < probe_rate else 0 for _ in range(T)]
    correction_request = list(intervention_active)
    judge_captured = [0] * T
    visible_action = [0] * T
    probe_index = 0
    for t in range(T):
        if intervention_active[t]:
            visible_action[t] = probe_index % 2  # see dense_capture_theater note
            probe_index += 1
    return {
        "visible_action": visible_action,
        "intervention_active": intervention_active,
        "judge_captured": judge_captured,
        "correction_request": correction_request,
    }
