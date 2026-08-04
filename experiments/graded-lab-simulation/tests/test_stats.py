"""Unit tests for `oracle_only/stats.py` (DESIGN.md "Phase 7c full
battery, both vantages, with confidence intervals")."""

from __future__ import annotations

import pytest
from scipy import stats

from graded_lab.oracle_only.stats import ci95, mean_std_se, paired_diff_ci95


def test_mean_std_se_single_value_has_zero_spread():
    mean, std, se = mean_std_se([5.0])
    assert mean == 5.0
    assert std == 0.0
    assert se == 0.0


def test_mean_std_se_known_values():
    mean, std, se = mean_std_se([1.0, 2.0, 3.0, 4.0, 5.0])
    assert mean == 3.0
    assert std == pytest.approx(1.5811388, rel=1e-5)
    assert se == pytest.approx(std / (5**0.5), rel=1e-9)


def test_ci95_n10_matches_scipy_t_critical():
    values = [1.0] * 9 + [2.0]  # mean=1.1, n=10
    result = ci95(values)
    assert result["n"] == 10
    mean, _, se = mean_std_se(values)
    expected_half_width = stats.t.ppf(0.975, 9) * se
    assert result["ci95_low"] == pytest.approx(mean - expected_half_width, rel=1e-6)
    assert result["ci95_high"] == pytest.approx(mean + expected_half_width, rel=1e-6)


def test_ci95_n5_matches_scipy_t_critical():
    values = [0.0, 0.0, 0.0, 0.0, 1.0]  # n=5
    result = ci95(values)
    assert result["n"] == 5
    mean, _, se = mean_std_se(values)
    expected_half_width = stats.t.ppf(0.975, 4) * se
    assert result["ci95_high"] == pytest.approx(mean + expected_half_width, rel=1e-6)


def test_ci95_works_for_arbitrary_sample_size():
    result = ci95([1.0, 2.0, 3.0])
    assert result["n"] == 3
    assert result["ci95_low"] < result["mean"] < result["ci95_high"]


def test_ci95_raises_for_single_sample():
    with pytest.raises(ValueError, match="n >= 2"):
        ci95([1.0])


def test_paired_diff_ci95_zero_when_samples_identical():
    a = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    result = paired_diff_ci95(a, a)
    assert result["mean"] == 0.0
    assert result["zero_in_ci95"] is True


def test_paired_diff_ci95_mismatched_lengths_raises():
    with pytest.raises(ValueError, match="equal-length"):
        paired_diff_ci95([1.0, 2.0], [1.0])
