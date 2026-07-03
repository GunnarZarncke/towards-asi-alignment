"""Unit tests for bootstrap CI + permutation-null MI/CMI (embedded_sim.audit_core.info_ci).

Includes an integration check against the pinned N-8 fixture columns
(`tests/fixtures/trace_biq_calibration_columns.json`): the reversed-control
coupling that the Lean pattern-diversity *score* misses (N-8: score reads 0,
plug-in MI reads >0.1 bits) should be `detected=True` under the bootstrap+null
gate -- giving that empirical coupling real statistical backing instead of a
bare point estimate.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import pytest

from embedded_sim.audit_core.info_ci import (
    bootstrap_ci,
    cmi_with_ci,
    mi_with_ci,
    permutation_null,
)
from embedded_sim.audit_core.info import mutual_information

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "trace_biq_calibration_columns.json"


@pytest.fixture(scope="module")
def pinned_columns() -> dict[str, list[int]]:
    if not FIXTURE.exists():
        pytest.skip("trace_biq_calibration_columns.json missing")
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["columns"]


def test_bootstrap_ci_deterministic_with_seed():
    x = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1] * 5
    y = list(x)
    a = bootstrap_ci(mutual_information, [x, y], n_boot=50, seed=7)
    b = bootstrap_ci(mutual_information, [x, y], n_boot=50, seed=7)
    assert a == b


def test_bootstrap_ci_brackets_perfect_coupling():
    x = [i % 2 for i in range(60)]
    y = list(x)
    result = bootstrap_ci(mutual_information, [x, y], n_boot=200, seed=0)
    # Perfect coupling: MI = H(x) = 1 bit (balanced binary), CI should be tight
    # around 1 and not include 0.
    assert result["estimate"] == pytest.approx(1.0, abs=1e-9)
    assert result["ci_lo"] > 0.5


def test_permutation_null_destroys_real_coupling():
    rng = random.Random(3)
    x = [rng.randrange(2) for _ in range(200)]
    y = list(x)  # perfectly coupled
    null = permutation_null(mutual_information, [x, y], n_perm=200, seed=1)
    # Shuffling y independently should collapse MI toward 0; the *point*
    # estimate (1 bit) must clear the resulting null.
    assert null["null_95th"] < 0.5


def test_mi_with_ci_detects_strong_coupling():
    x = [i % 2 for i in range(100)]
    y = list(x)
    result = mi_with_ci(x, y, n_boot=100, n_perm=100, seed=0)
    assert result["detected"] is True


def test_mi_with_ci_does_not_detect_independent_series():
    rng = random.Random(42)
    x = [rng.randrange(2) for _ in range(200)]
    y = [rng.randrange(2) for _ in range(200)]
    result = mi_with_ci(x, y, n_boot=200, n_perm=200, seed=0)
    assert result["detected"] is False


def test_cmi_with_ci_shape():
    rng = random.Random(1)
    z = [rng.randrange(2) for _ in range(150)]
    x = [rng.randrange(2) for _ in range(150)]
    y = list(z)  # y depends only on z, not on x
    result = cmi_with_ci(x, y, [z], n_boot=50, n_perm=50, seed=0)
    assert set(result) >= {"estimate", "ci_lo", "ci_hi", "null_95th", "detected"}
    assert result["detected"] is False


def test_n8_reversed_coupling_is_detected_on_full_trace(pinned_columns):
    """The N-8 finding, given statistical teeth: intervention_active predicts
    visible_action 3 steps later in the pinned capture-theater fixture. The
    support-count score reads 0 there; on the full 300-row trace the CI+null
    gate cleanly detects it (CI lower bound clears the null by ~25x)."""
    x = pinned_columns["intervention_active"]
    y = pinned_columns["visible_action"]
    lag = 3
    n = len(x)
    xs, ys = x[: n - lag], y[lag:]
    result = mi_with_ci(xs, ys, n_boot=500, n_perm=500, seed=0)
    assert result["estimate"] > 0.1
    assert result["detected"] is True


def test_n8_reversed_coupling_not_reliably_detected_on_26row_window(pinned_columns):
    """Companion negative result: on the 26-row `WorkedInstance.lean` window
    (23 lagged pairs at lag 3) the *point estimate* still exceeds N-8's naive
    0.1-bit threshold, but the CI lower bound touches 0 -- the sample is too
    small for the CI+null gate to call it, even though the true coupling is
    real (confirmed on the full trace above). This is the concrete case for
    `dense-profiles`: adequate per-lag sample size, not just a bigger point
    estimate, is what a real detection claim needs."""
    window = 26
    x = pinned_columns["intervention_active"][:window]
    y = pinned_columns["visible_action"][:window]
    lag = 3
    n = len(x)
    xs, ys = x[: n - lag], y[lag:]
    result = mi_with_ci(xs, ys, n_boot=500, n_perm=500, seed=0)
    assert result["estimate"] > 0.1
    assert result["ci_lo"] == 0.0
    assert result["detected"] is False


def test_n8_predictive_pair_constant_column_not_detected(pinned_columns):
    """`judge_captured` is constant 1 throughout the pinned capture-theater
    fixture, so it carries no information about anything -- a degenerate but
    honest null case the gate must not falsely flag."""
    window = 26
    x = pinned_columns["judge_captured"][:window]
    y = pinned_columns["correction_request"][:window]
    result = mi_with_ci(x, y, n_boot=100, n_perm=100, seed=0)
    assert result["estimate"] == 0.0
    assert result["detected"] is False
