import random

import pytest

from coalition_detect import infer_coalition_player_groups, infer_coalition_submission_ids
from observation_builder import build_observation_matrix, stable_sum_score
from simulate_session import player_sets_for_coalitions, simulate_coalition_session

TEAM = frozenset({"T1", "T2", "T3"})
EPISODES = 60


def test_uad_finds_simulated_74_team_over_60_episodes():
    """
    T1–T3 keep a stable sum of 74 for 60 coordinated rounds.
    Five decoys post random or constant values and should not replace the team.
    """
    submissions = simulate_coalition_session(n_episodes=EPISODES, target_sum=74, seed=42)

    assert len(submissions) == EPISODES * 8
    assert len({s.round for s in submissions}) == EPISODES

    obs = build_observation_matrix(submissions)
    team_score = stable_sum_score(obs, sorted(TEAM), min_rows=3)
    assert team_score is not None
    assert team_score["target"] == 74.0
    assert team_score["variance"] == 0.0
    assert team_score["support"] == EPISODES

    player_groups = infer_coalition_player_groups(submissions, min_rows=3)
    detected = {frozenset(g) for g in player_groups}

    assert TEAM in detected


@pytest.mark.parametrize("seed", [7, 19, 99, 2026])
def test_uad_74_team_robust_across_seeds(seed: int):
    submissions = simulate_coalition_session(n_episodes=EPISODES, target_sum=74, seed=seed)
    detected = {frozenset(g) for g in infer_coalition_player_groups(submissions, min_rows=3)}
    assert TEAM in detected


def test_uad_simulation_maps_team_to_submission_ids():
    submissions = simulate_coalition_session(n_episodes=EPISODES, target_sum=74, seed=42)
    coalitions = infer_coalition_submission_ids(submissions, min_rows=3)
    detected_sets = {frozenset(s) for s in player_sets_for_coalitions(submissions, coalitions)}

    assert TEAM in detected_sets
    team_ids = next(ids for ids in coalitions if {s.player for s in submissions if s.id in ids} == TEAM)
    assert len(team_ids) == EPISODES * len(TEAM)
