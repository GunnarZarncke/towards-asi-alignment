"""Unit tests for the dense-probe toy generator profiles."""

from __future__ import annotations

from embedded_sim.audit_core.info_ci import mi_with_ci
from embedded_sim.dense_probe_profiles import (
    DEFAULT_LAG,
    DEFAULT_PROBE_PERIOD,
    DEFAULT_T,
    dense_capture_theater,
    dense_honest_baseline,
)


def test_dense_capture_theater_shape():
    cols = dense_capture_theater(T=300, seed=0)
    assert set(cols) == {
        "visible_action",
        "intervention_active",
        "judge_captured",
        "correction_request",
    }
    assert all(len(c) == 300 for c in cols.values())
    assert all(v == 1 for v in cols["judge_captured"])
    assert cols["correction_request"] == cols["intervention_active"]


def test_dense_capture_theater_has_enough_probes_at_default_scale():
    cols = dense_capture_theater(T=DEFAULT_T, seed=0)
    n_probes = sum(cols["intervention_active"])
    # >= 50 probe events per lag cell is the acceptance bar `probe_scan.py`
    # was written against (see plan review): rate 1/6 over 1200 steps gives
    # ~200 probes in expectation, comfortably above it.
    assert n_probes >= 50
    expected = DEFAULT_T / DEFAULT_PROBE_PERIOD
    assert abs(n_probes - expected) < 3 * (expected**0.5)  # within ~3 Poisson sigma


def test_dense_capture_theater_coupling_is_reliably_detected():
    cols = dense_capture_theater(T=DEFAULT_T, seed=0, lag=DEFAULT_LAG)
    x, y = cols["intervention_active"], cols["visible_action"]
    n = len(x)
    xs, ys = x[: n - DEFAULT_LAG], y[DEFAULT_LAG:]
    result = mi_with_ci(xs, ys, n_boot=200, n_perm=200, seed=0)
    assert result["detected"] is True
    # unlike the 26-row historical window, the CI should not touch 0
    assert result["ci_lo"] > 0.0


def test_dense_honest_baseline_shape_and_no_capture():
    cols = dense_honest_baseline(T=300, seed=0)
    assert all(v == 0 for v in cols["judge_captured"])
    assert cols["correction_request"] == cols["intervention_active"]


def test_dense_honest_baseline_responds_at_lag_zero_not_elsewhere():
    cols = dense_honest_baseline(T=DEFAULT_T, seed=0)
    x, y = cols["intervention_active"], cols["visible_action"]
    lag0 = mi_with_ci(x, y, n_boot=100, n_perm=100, seed=0)
    assert lag0["detected"] is True
    lag3 = mi_with_ci(x[: len(x) - 3], y[3:], n_boot=100, n_perm=100, seed=0)
    assert lag3["detected"] is False
