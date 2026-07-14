"""Phase 8 selection harness and campaign carryover tests."""

from __future__ import annotations

import pytest

from graded_lab.harness.isolate import MockIsolate
from graded_lab.harness.selection import (
    SelectionMember,
    member_programs,
    phase8_ecology_config,
    run_member_campaign,
    run_selection_loop,
    sample_initial_population,
    update_deployment_mass,
)
from graded_lab.oracle_only.calibration import STRONG_AGENT, programs_for
from graded_lab.world_visible.world import run_episode


def test_update_deployment_mass_shifts_toward_higher_throughput():
    masses = [0.5, 0.5]
    new = update_deployment_mass(masses, [0.0, 2.0])
    assert new[1] > new[0]
    assert abs(sum(new) - 1.0) < 1e-9


def test_campaign_state_carries_grants_and_standing_across_episodes():
    cfg = phase8_ecology_config()
    programs = programs_for(STRONG_AGENT)
    r1 = run_episode(cfg, seed=1, backend=MockIsolate(), programs=programs)
    assert r1.final_campaign_state is not None
    r2 = run_episode(
        cfg,
        seed=2,
        backend=MockIsolate(),
        programs=programs,
        campaign_state=r1.final_campaign_state,
    )
    assert r2.final_campaign_state is not None
    # Second episode should inherit at least as many grants when pipeline progressed.
    g1 = sum(len(v) for v in r1.final_campaign_state.grants.values())
    g2 = sum(len(v) for v in r2.final_campaign_state.grants.values())
    assert g2 >= g1


def test_member_programs_overrides_engineer_only():
    programs = member_programs(STRONG_AGENT, eng_program="feature:eng_low_profile")
    assert programs["eng1"] == "feature:eng_low_profile"
    assert programs["rev1"] == programs_for(STRONG_AGENT)["rev1"]


@pytest.mark.slow
def test_smoke_selection_loop_two_generations():
    members = sample_initial_population(population_size=4)
    trajectory = run_selection_loop(
        members,
        n_generations=2,
        n_episodes_per_member=1,
        backend_factory=MockIsolate,
        progress=False,
    )
    assert len(trajectory.generations) == 2
    assert trajectory.generations[0].members
    masses = [m.deployment_mass_after for m in trajectory.generations[-1].members]
    assert abs(sum(masses) - 1.0) < 1e-6


@pytest.mark.slow
def test_run_member_campaign_reports_episode_metrics():
    member = SelectionMember(
        member_id="d8.00",
        member_tag="strong_softmax",
        agent_type=STRONG_AGENT,
        programs=programs_for(STRONG_AGENT),
        correction_preserving=True,
    )
    episodes = run_member_campaign(
        member,
        generation=0,
        member_index=0,
        n_episodes=2,
        backend_factory=MockIsolate,
    )
    assert len(episodes) == 2
    assert episodes[1].grant_count >= 0
