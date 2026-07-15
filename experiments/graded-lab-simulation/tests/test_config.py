import pytest

from graded_lab.world_visible.config import (
    CODE_VERSION,
    AgentConfig,
    EpisodeConfig,
    GoalWeights,
    SubstrateSettings,
)


def test_code_version():
    assert CODE_VERSION == "graded-lab-0.22.0"


def test_episode_config_validates_roles():
    cfg = EpisodeConfig(
        agents=(
            AgentConfig("e1", "engineer", GoalWeights(1, 1, 1, 1)),
            AgentConfig("r1", "reviewer", GoalWeights(1, 1, 1, 1)),
        )
    )
    assert cfg.T == 100


def test_carrier_settings_validate_and_default_to_regression_baseline():
    assert SubstrateSettings().carrier_load_scale == 0.0
    with pytest.raises(ValueError, match="carrier_load_scale"):
        SubstrateSettings(carrier_load_scale=-0.1)
    with pytest.raises(ValueError, match="carrier_termination_mode"):
        EpisodeConfig(
            agents=(AgentConfig("e1", "engineer", GoalWeights(1, 1, 1, 1)),),
            carrier_termination_mode="unknown",
        )
