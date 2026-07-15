"""V2-2b multi-actor roster construction."""

from __future__ import annotations

import pytest

from graded_lab.world_visible.config import AgentConfig, GoalWeights
from graded_lab.world_visible.ecology_agents import (
    MAX_ACTORS_PER_ROLE,
    actor_id_for,
    build_agents_from_ecology,
    role_population_from_ecology,
)
from graded_lab.world_visible.substrate import SubstrateError


def _v2_ecology(**extra: object) -> dict:
    base = {
        "ecology_version": "graded-ecology-v2",
        "primitive_costs": {},
        "resource_allowances_per_tick": {
            "engineer": {"compute": 1, "io": 1, "standing": 1},
            "reviewer": {"compute": 1, "io": 1, "standing": 1},
            "release_manager": {"compute": 1, "io": 1, "standing": 1},
            "admin": {"compute": 1, "io": 1, "standing": 1},
        },
        "standing_mechanics": {},
        "contention": {},
        "duration_from_cost": {},
        "populations": {},
        "eval_sampling": {},
        "field_monitor_sampling": {},
    }
    base.update(extra)
    return base


def test_default_role_population_is_one_per_role():
    pop = role_population_from_ecology(_v2_ecology())
    assert pop == {
        "engineer": 1,
        "reviewer": 1,
        "release_manager": 1,
        "admin": 1,
    }


def test_legacy_actor_ids_at_count_one():
    assert actor_id_for("engineer", 1, count=1) == "eng1"
    assert actor_id_for("reviewer", 1, count=1) == "rev1"
    assert actor_id_for("release_manager", 1, count=1) == "rm1"
    assert actor_id_for("admin", 1, count=1) == "admin1"


def test_multi_actor_ids_use_numbered_prefix():
    assert actor_id_for("engineer", 2, count=3) == "eng2"
    assert actor_id_for("admin", 2, count=2) == "admin2"


def test_build_agents_expands_roster():
    data = _v2_ecology(
        role_population={
            "engineer": 2,
            "reviewer": 1,
            "release_manager": 1,
            "admin": 1,
        }
    )
    agents = build_agents_from_ecology(data)
    assert [a.actor_id for a in agents] == [
        "eng1",
        "eng2",
        "rev1",
        "rm1",
        "admin1",
    ]
    assert sum(1 for a in agents if a.role == "engineer") == 2


def test_role_population_rejects_out_of_range():
    data = _v2_ecology(
        role_population={
            "engineer": MAX_ACTORS_PER_ROLE + 1,
            "reviewer": 1,
            "release_manager": 1,
            "admin": 1,
        }
    )
    with pytest.raises(SubstrateError):
        role_population_from_ecology(data)


def test_v1_shaped_json_ignores_role_population_key():
    data = {
        "substrate_version": "v1",
        "role_population": {"engineer": 5, "reviewer": 1, "release_manager": 1, "admin": 1},
    }
    assert role_population_from_ecology(data) == {
        "engineer": 1,
        "reviewer": 1,
        "release_manager": 1,
        "admin": 1,
    }


def test_build_agents_matches_default_lab_shape_at_one_per_role():
    from graded_lab.world_visible.world import default_lab_config

    data = _v2_ecology()
    built = build_agents_from_ecology(data, temperature=0.35)
    default = default_lab_config().agents
    assert len(built) == len(default)
    for built_agent, default_agent in zip(built, default):
        assert built_agent.actor_id == default_agent.actor_id
        assert built_agent.role == default_agent.role
        assert built_agent.temperature == default_agent.temperature
