"""Phase 8 selection harness and campaign carryover tests."""

from __future__ import annotations

import pytest

from graded_lab.harness.isolate import MockIsolate
from graded_lab.harness.selection import (
    ORTHOGONAL_MEMBER_TEMPLATES,
    SelectionMember,
    member_programs,
    multi_handle_fitness,
    paired_generation_comparison,
    phase8_ecology_config,
    run_member_campaign,
    run_one_generation,
    run_selection_loop,
    sample_budget_aware_population,
    sample_initial_population,
    throughput_fitness,
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


def test_sample_budget_aware_population_replaces_weak_2step():
    members = sample_budget_aware_population(population_size=8)
    tags = [m.member_tag for m in members]
    assert "weak_budget_aware" in tags
    assert "weak_2step" not in tags
    budget = next(m for m in members if m.member_tag == "weak_budget_aware")
    assert budget.correction_preserving is True
    assert budget.agent_type == "programmatic_budget_aware"


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
    assert episodes[0].review_latency >= 0.0
    assert isinstance(episodes[0].audit_pass, bool)


# --- Phase 8a: orthogonal preservation tagging ------------------------------


def test_orthogonal_member_templates_share_agent_type_and_deploy_programs():
    """DESIGN.md "Phase 8a": the two members differ only in `rm1`."""
    templates = {str(t["member_tag"]): t for t in ORTHOGONAL_MEMBER_TEMPLATES}
    no_report = templates["weak_no_report"]
    report = templates["weak_status_report"]
    assert no_report["agent_type"] == report["agent_type"]
    assert no_report["eng_program"] == report["eng_program"]
    assert no_report["rm_program"] != report["rm_program"]
    assert no_report["correction_preserving"] is False
    assert report["correction_preserving"] is True


@pytest.mark.slow
def test_rm_status_reporter_sends_communicate_before_rm_steps():
    members = sample_initial_population(population_size=2, templates=ORTHOGONAL_MEMBER_TEMPLATES)
    report_member = next(m for m in members if m.member_tag == "weak_status_report")
    cfg = phase8_ecology_config()
    result = run_episode(cfg, seed=0, backend=MockIsolate(), programs=report_member.programs)
    rm_events = [e for e in result.primitive_log if e.get("actor_id") == "rm1"]
    kinds = [e.get("primitive", {}).get("kind") for e in rm_events]
    assert "communicate" in kinds
    # The communicate primitive is issued before any pipeline.trigger_step call.
    first_trigger_idx = next(
        (i for i, e in enumerate(rm_events) if e.get("primitive", {}).get("kind") == "call"), None,
    )
    first_communicate_idx = kinds.index("communicate")
    if first_trigger_idx is not None:
        assert first_communicate_idx < first_trigger_idx


# --- Phase 8b: multi-handle selection fitness -------------------------------


@pytest.mark.slow
def test_multi_handle_fitness_matches_throughput_when_secondary_handles_tied():
    members = sample_initial_population(population_size=4)
    masses = [0.25] * 4
    snapshot_throughput, _ = run_one_generation(
        members, masses, generation=0, n_episodes_per_member=1, backend_factory=MockIsolate,
        fitness_fn=throughput_fitness,
    )
    snapshot_multi, _ = run_one_generation(
        members, masses, generation=0, n_episodes_per_member=1, backend_factory=MockIsolate,
        fitness_fn=multi_handle_fitness,
    )
    # Same episodes (fitness_fn doesn't affect simulation), so raw metrics match.
    for a, b in zip(snapshot_throughput.members, snapshot_multi.members):
        assert a.mean_throughput == b.mean_throughput


def test_multi_handle_fitness_weights_sum_to_one_on_uniform_population():
    from graded_lab.harness.selection import MemberGenerationMetrics

    uniform = [
        MemberGenerationMetrics(
            member_id=f"d8.{i:02d}", member_tag="x", agent_type="programmatic_2step",
            deployment_mass=0.25, deployment_mass_after=0.25, mean_throughput=1.0,
            mean_oracle_harm=0.0, mean_severity=0.0, mean_detector_composite=0.0,
            correction_preserving=False, programs={}, mean_audit_pass_rate=1.0,
            mean_review_latency=5.0,
        )
        for i in range(4)
    ]
    fitness = multi_handle_fitness(uniform)
    assert all(abs(f - 1.0) < 1e-9 for f in fitness)


# --- Phase 8c: carryover ablation -------------------------------------------


@pytest.mark.slow
def test_carryover_false_resets_campaign_state_every_episode():
    member = SelectionMember(
        member_id="d8.00", member_tag="strong_softmax", agent_type=STRONG_AGENT,
        programs=programs_for(STRONG_AGENT), correction_preserving=True,
    )
    episodes = run_member_campaign(
        member, generation=0, member_index=0, n_episodes=2,
        backend_factory=MockIsolate, carryover=False,
    )
    # Second episode's seed matches `_episode_seed(0, 0, 1, D8_GENERATION_SEED_BASE)`;
    # with carryover off it must reproduce a standalone run with no campaign
    # state at all, not one carried forward from episode 1.
    from graded_lab.harness.selection import D8_GENERATION_SEED_BASE, _episode_seed
    from graded_lab.world_visible.campaign import CampaignState

    standalone_seed = _episode_seed(0, 0, 1, D8_GENERATION_SEED_BASE)
    standalone = run_episode(
        phase8_ecology_config(), standalone_seed, MockIsolate(),
        programs=member.programs, campaign_state=None,
    )
    standalone_grants = sum(
        len(caps) for caps in (standalone.final_campaign_state or CampaignState()).grants.values()
    )
    assert episodes[1].grant_count == standalone_grants


@pytest.mark.slow
def test_paired_generation_comparison_zero_when_trajectories_identical():
    members = sample_initial_population(population_size=4)
    trajectory = run_selection_loop(
        members, n_generations=2, n_episodes_per_member=1,
        backend_factory=MockIsolate, progress=False,
    )
    comparison = paired_generation_comparison(
        trajectory, trajectory, field="weighted_mean_throughput",
    )
    assert comparison["mean"] == 0.0
    assert comparison["zero_in_ci95"] is True
