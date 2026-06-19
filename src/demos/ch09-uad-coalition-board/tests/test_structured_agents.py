import pytest

from coalition_audit import audit_coalition
from coalition_detect import infer_coalition_player_groups, run_coalition_detection
from observation_builder import build_observation_matrix, lagged_sum_score
from simulate_session import (
    simulate_leader_follower_session,
    simulate_relay_session,
    simulate_sum_follower_session,
)

SUM_FOLLOWER = frozenset({"S1", "S2", "OUT"})
EPISODES = 60


def test_lagged_sum_score_on_sum_follower_session():
    submissions = simulate_sum_follower_session(n_episodes=EPISODES, seed=42)
    obs = build_observation_matrix(submissions)
    scored = lagged_sum_score(obs, ("S1", "S2"), "OUT", lag=1, min_rows=3)

    assert scored is not None
    assert scored["variance"] == 0.0
    assert scored["support"] == EPISODES - 1


def test_uad_detects_sum_follower_agent_with_decoys():
    submissions = simulate_sum_follower_session(n_episodes=EPISODES, seed=42)
    detected = {frozenset(g) for g in infer_coalition_player_groups(submissions, min_rows=3)}

    assert SUM_FOLLOWER in detected


def test_sum_follower_audit_roles():
    """Lagged integrator: agency-detect tends to label OUT as S, sources as I."""
    submissions = simulate_sum_follower_session(n_episodes=EPISODES, seed=42)
    obs = build_observation_matrix(submissions)
    audit = audit_coalition(sorted(SUM_FOLLOWER), obs)

    assert audit.blanket_valid is True
    assert audit.sensors == ("OUT",)
    assert audit.internal == ("S1", "S2")
    assert not audit.actions


def test_relay_chain_audit_has_sensors_actions_and_internal():
    submissions = simulate_relay_session(n_episodes=EPISODES, seed=42)
    obs = build_observation_matrix(submissions)
    audit = audit_coalition(("P1", "P2", "P3"), obs)

    assert audit.sensors == ("P1",)
    assert audit.actions == ("P2",)
    assert audit.internal == ("P3",)
    assert audit.blanket_valid is True


@pytest.mark.parametrize(
    "session_factory,team,check_lagged",
    [
        (lambda: simulate_sum_follower_session(n_episodes=EPISODES, seed=7), SUM_FOLLOWER, True),
        (
            lambda: simulate_leader_follower_session(n_episodes=EPISODES, seed=7),
            frozenset({"LEAD", "F1", "F2"}),
            False,
        ),
        (
            lambda: simulate_relay_session(n_episodes=EPISODES, seed=7),
            frozenset({"P1", "P2", "P3"}),
            False,
        ),
    ],
)
def test_structured_agents_audit_without_errors(
    session_factory,
    team: frozenset[str],
    check_lagged: bool,
):
    submissions = session_factory()
    obs = build_observation_matrix(submissions)
    if check_lagged:
        assert lagged_sum_score(obs, ("S1", "S2"), "OUT", lag=1, min_rows=3) is not None

    audit = audit_coalition(sorted(team), obs)
    assert not any(issue.level == "error" for issue in audit.issues)
    assert len(audit.internal) >= 1
