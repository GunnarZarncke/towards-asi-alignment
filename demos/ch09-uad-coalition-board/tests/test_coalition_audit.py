import logging

import pytest

from coalition_audit import audit_coalition, check_plausibility, log_coalition_audits
from coalition_detect import run_coalition_detection
from observation_builder import build_observation_matrix
from simulate_session import simulate_coalition_session

TEAM = ("T1", "T2", "T3")


def test_audit_74_team_roles_and_blanket():
    submissions = simulate_coalition_session(n_episodes=60, seed=42)
    obs = build_observation_matrix(submissions)
    audit = audit_coalition(TEAM, obs)

    assert set(audit.players) == set(TEAM)
    assert set(audit.sensors) | set(audit.actions) | set(audit.internal) == set(TEAM)
    assert len(audit.internal) >= 1
    assert len(audit.environment) == 5
    assert audit.blanket_valid is True
    assert audit.stable_sum_target == 74.0
    assert audit.stable_sum_variance == 0.0
    assert not any(issue.level == "error" for issue in audit.issues)


def test_audit_warns_on_symmetric_channel():
    submissions = simulate_coalition_session(n_episodes=60, seed=42)
    obs = build_observation_matrix(submissions)
    audit = audit_coalition(TEAM, obs)

    codes = {issue.code for issue in audit.issues}
    assert "symmetric_channel" in codes


def test_run_coalition_detection_emits_audit_logs(caplog: pytest.LogCaptureFixture):
    submissions = simulate_coalition_session(n_episodes=60, seed=42)

    with caplog.at_level(logging.INFO, logger="uad.coalition"):
        result = run_coalition_detection(submissions, log_audit=True)

    assert frozenset(TEAM) in {frozenset(g) for g in result.player_groups}
    assert len(result.audits) >= 1
    assert "UAD coalition T1, T2, T3" in caplog.text
    assert "roles  S=" in caplog.text
    assert "blanket valid=" in caplog.text


def test_plausibility_errors_on_empty_internal():
    issues = check_plausibility(
        ["A", "B"],
        {"S": ["A", "B"], "A": [], "I": []},
        environment=["C"],
        blanket={"valid": False, "details": "no internal"},
    )
    assert any(issue.code == "no_internal" for issue in issues)
