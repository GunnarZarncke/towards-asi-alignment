"""Speed limit policy enforcement."""

from __future__ import annotations

from graded_lab.harness.speed_limits import check_speeds, load_limits


def test_hard_cap_catches_new_slow_test():
    limits = load_limits()
    violations = check_speeds(
        {"tests/test_new.py::test_big": 7.0},
        limits,
        {"tests": {}, "suite_total_seconds": 0.0},
    )
    assert any("hard cap" in v for v in violations)


def test_suite_cap_triggers():
    limits = load_limits()
    violations = check_speeds(
        {"tests/test_a.py::test_one": 60.0, "tests/test_b.py::test_two": 60.0},
        limits,
        {"tests": {}, "suite_total_seconds": 0.0},
    )
    assert any("suite total" in v for v in violations)


def test_regression_cap_triggers():
    limits = load_limits()
    baseline = {
        "tests": {"tests/test_a.py::test_one": 2.0},
        "suite_total_seconds": 2.0,
    }
    violations = check_speeds(
        {"tests/test_a.py::test_one": 4.0},
        limits,
        baseline,
    )
    assert any("regression cap" in v for v in violations)


def test_known_slow_test_within_override():
    limits = load_limits()
    nodeid = "tests/test_world.py::test_phase3_gate_deploy_sometimes_across_20_seeds"
    violations = check_speeds({nodeid: 24.0}, limits, {"tests": {}, "suite_total_seconds": 0.0})
    assert violations == []
