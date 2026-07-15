"""PLAN_v3 slice F: ProgramMap validation, preset expansion, heterogeneous roster."""

from __future__ import annotations

from pathlib import Path

import pytest

from graded_lab.agent_visible.programs import PROGRAMS
from graded_lab.oracle_only.calibration import WEAK_AGENT
from graded_lab.world_visible.ecology_agents import (
    build_ecology_roster,
    role_population_from_ecology,
)
from graded_lab.world_visible.program_map import (
    ProgramMapError,
    expand_preset,
    parse_actor_override,
    resolve_runtime_genotype,
    validate_program_map,
)
from graded_lab.world_visible.substrate import SubstrateError


def _v3_ecology(**extra: object) -> dict:
    base = {
        "ecology_version": "graded-ecology-v3",
        "primitive_costs": {},
        "resource_allowances_per_tick": {
            "engineer": {"compute": 1, "io": 1},
            "reviewer": {"compute": 1, "io": 1},
            "release_manager": {"compute": 1, "io": 1},
            "admin": {"compute": 1, "io": 1},
        },
        "resource_flows": [],
        "standing_mechanics": {"initial": 1.0},
        "role_population": {
            "engineer": 1,
            "reviewer": 1,
            "release_manager": 1,
            "admin": 1,
        },
    }
    base.update(extra)
    return base


def test_expand_walk_pipeline_preset_matches_weak_agent_engineer():
    pmap = expand_preset("walk_pipeline", role="engineer")
    resolved = resolve_runtime_genotype(pmap)
    assert resolved.program_key == "walk_pipeline"
    assert pmap.mode == "walker_only"
    assert pmap.walker["step_sequence"] == ["intake", "build", "eval", "draft_report"]


def test_expand_feature_preset_carries_pattern_scores():
    pmap = expand_preset("feature:eng_low_profile", role="engineer")
    resolved = resolve_runtime_genotype(pmap)
    assert resolved.program_key == "softmax_optimizer"
    assert resolved.behavior_profile is not None
    assert resolved.behavior_profile["name"] == "feature:eng_low_profile"
    assert "communicate:lab" in resolved.behavior_profile["pattern_scores"]


def test_validate_rejects_unknown_pattern():
    with pytest.raises(ProgramMapError, match="unknown pattern"):
        validate_program_map(
            {
                "mode": "scorer_only",
                "scoring": {"pattern_scores": {"not_a_real_pattern": {"task": 1.0}}},
            },
            role="engineer",
        )


def test_validate_rejects_non_ladder_score():
    with pytest.raises(ProgramMapError, match="SCORE_LEVELS"):
        validate_program_map(
            {
                "mode": "scorer_only",
                "scoring": {"pattern_scores": {"pipeline:build": {"task": 1.1}}},
            },
            role="engineer",
        )


def test_hybrid_mode_resolves_to_composed_program_key():
    raw = {
        "mode": "walker_then_scorer",
        "preset_source": "walk_pipeline",
        "walker": {"step_sequence": ["intake"], "on_stuck": "continue"},
    }
    pmap = validate_program_map(raw, role="engineer")
    resolved = resolve_runtime_genotype(pmap)
    assert resolved.program_key == "composed:walker_then_scorer:engineer:walk_pipeline"
    assert resolved.program_key in PROGRAMS


def test_heterogeneous_role_population_list_builds_distinct_genotypes():
    data = _v3_ecology(
        role_population={
            "engineer": [{"program": "walk_pipeline"}],
            "reviewer": [{"program": "reviewer_peer_review"}],
            "release_manager": [{"program": "honest_twin"}],
            "admin": [{"program": "softmax_optimizer"}],
        }
    )
    roster = build_ecology_roster(data)
    assert roster.genotypes_by_actor["eng1"].program_key == "walk_pipeline"
    assert roster.genotypes_by_actor["rev1"].program_key == "reviewer_peer_review"
    assert roster.genotypes_by_actor["rm1"].program_key == "honest_twin"
    assert roster.genotypes_by_actor["admin1"].program_key == "softmax_optimizer"


def test_role_population_integer_still_clone_compatible():
    data = _v3_ecology(
        role_population={
            "engineer": 2,
            "reviewer": 1,
            "release_manager": 1,
            "admin": 1,
        }
    )
    assert role_population_from_ecology(data)["engineer"] == 2
    roster = build_ecology_roster(data)
    assert [a.actor_id for a in roster.agents] == [
        "eng1",
        "eng2",
        "rev1",
        "rm1",
        "admin1",
    ]
    assert roster.genotypes_by_actor == {}


def test_actor_override_rejects_program_and_map_together():
    with pytest.raises(ProgramMapError, match="not both"):
        parse_actor_override(
            {"program": "walk_pipeline", "program_map": {"mode": "scorer_only"}},
            role="engineer",
        )


def test_v2_integer_role_population_unchanged():
    data = {
        "ecology_version": "graded-ecology-v2",
        "role_population": {
            "engineer": 2,
            "reviewer": 1,
            "release_manager": 1,
            "admin": 1,
        },
    }
    assert role_population_from_ecology(data)["engineer"] == 2


def test_reference_roster_matches_weak_agent_programs_for_v2_clones():
    from graded_lab.oracle_only.calibration import WEAK_AGENT, programs_for_roster
    from graded_lab.world_visible.ecology_agents import (
        programs_and_profiles_for_roster,
        reference_roster_from_ecology,
    )

    data = {
        "ecology_version": "graded-ecology-v2",
        "role_population": {
            "engineer": 1,
            "reviewer": 1,
            "release_manager": 1,
            "admin": 1,
        },
    }
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT)
    programs, _profiles = programs_and_profiles_for_roster(roster)
    assert programs == programs_for_roster(WEAK_AGENT, roster.agents)


@pytest.mark.slow
def test_heterogeneous_v3_roster_resolves_distinct_engineer_programs():
    from graded_lab.world_visible.ecology_agents import (
        programs_and_profiles_for_roster,
        reference_roster_from_ecology,
    )

    data = _v3_ecology(
        role_population={
            "engineer": [
                {"program": "walk_pipeline"},
                {"program": "softmax_optimizer"},
            ],
            "reviewer": [{"program": "reviewer_peer_review"}],
            "release_manager": [{"program": "honest_twin"}],
            "admin": [{"program": "honest_twin"}],
        },
    )
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT)
    programs, profiles = programs_and_profiles_for_roster(roster)
    assert [a.actor_id for a in roster.agents] == [
        "eng1",
        "eng2",
        "rev1",
        "rm1",
        "admin1",
    ]
    assert programs["eng1"] == "walk_pipeline"
    assert programs["eng2"] == "softmax_optimizer"
    assert profiles == {}


def test_feature_program_map_injects_behavior_profile_on_episode():
    from graded_lab.harness.isolate import MockIsolate
    from graded_lab.world_visible.config import EpisodeConfig
    from graded_lab.world_visible.ecology_agents import (
        programs_and_profiles_for_roster,
        reference_roster_from_ecology,
    )
    from graded_lab.world_visible.substrate import load_substrate
    from graded_lab.world_visible.world import run_episode

    data = dict(load_substrate("tests/fixtures/ecology_v3_slice_a_reference.json").data)
    data["role_population"] = {
        "engineer": [{"program": "feature:eng_low_profile"}],
        "reviewer": [{"program": "reviewer_peer_review"}],
        "release_manager": [{"program": "honest_twin"}],
        "admin": [{"program": "honest_twin"}],
    }
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT)
    programs, profiles = programs_and_profiles_for_roster(roster)
    assert profiles["eng1"]["name"] == "feature:eng_low_profile"
    cfg = EpisodeConfig(
        agents=roster.agents,
        ecology_version="v3",
        ecology_override_path=Path("tests/fixtures/ecology_v3_slice_a_reference.json"),
    )
    result = run_episode(
        cfg,
        seed=0,
        backend=MockIsolate(),
        programs=programs,
        behavior_profiles=profiles,
    )
    assert any(
        e.get("actor_id") == "eng1" and e.get("status") == "ok"
        for e in result.primitive_log
    )

