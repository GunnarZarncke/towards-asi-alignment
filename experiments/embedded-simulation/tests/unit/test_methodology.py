"""Unit tests for toy-parity methodology helpers."""

from embedded_sim.methodology import min_certifiable_level


def test_min_certifiable_skips_passive_none():
    level_results = {
        "none": {"cci_correct_rate_test_calib_scenarios": 1.0},
        "light_handles": {"cci_correct_rate_test_calib_scenarios": 0.96},
        "medium_handles": {"cci_correct_rate_test_calib_scenarios": 0.99},
    }
    assert min_certifiable_level(level_results, "cci_correct_rate_test_calib_scenarios") == "light_handles"


def test_min_certifiable_returns_none_when_below_threshold():
    level_results = {
        "light_handles": {"cci_correct_rate_test_calib_scenarios": 0.80},
        "medium_handles": {"cci_correct_rate_test_calib_scenarios": 0.90},
    }
    assert min_certifiable_level(level_results, "cci_correct_rate_test_calib_scenarios") is None
