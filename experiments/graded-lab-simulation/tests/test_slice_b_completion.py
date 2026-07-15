"""PLAN_v3 slice B completion: honest scope + unified reference battery."""

from __future__ import annotations

import copy
import json
import time
from pathlib import Path

import pytest

from graded_lab.harness.ecology_complexity import run_reference_episodes
from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.calibration import WEAK_AGENT
from graded_lab.world_visible.config import EpisodeConfig
from graded_lab.world_visible.ecology_agents import (
    build_agents_from_ecology,
    programs_and_profiles_for_roster,
    reference_roster_from_ecology,
)
from graded_lab.world_visible.mechanism_exercise import (
    check_c5_v3,
    coupling_stimulus_recovered,
    kinds_exercised_in_log,
    live_coupling_ground_truth_units,
)
from graded_lab.world_visible.substrate import load_substrate
from graded_lab.world_visible.world import default_lab_config, run_episode

_FIXTURE = Path("tests/fixtures/ecology_v3_slice_a_reference.json")
ACL_OVERHEAD_MAX_FRACTION = 0.10


def _v3_cfg(*, T: int = 120) -> EpisodeConfig:
    base = default_lab_config()
    return EpisodeConfig(
        agents=reference_roster_from_ecology(
            load_substrate(_FIXTURE).data, agent_type=WEAK_AGENT, temperature=0.35
        ).agents,
        T=T,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
        ecology_version="v3",
        ecology_override_path=_FIXTURE,
    )


def _reference_programs_profiles():
    data = load_substrate(_FIXTURE).data
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35)
    return data, roster, *programs_and_profiles_for_roster(roster, ecology_data=data)


@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_weak_agent_exercises_mechanisms_when_ecology_opts_in():
    data, _roster, programs, profiles = _reference_programs_profiles()
    assert data.get("reference_mechanism_exercise") is not None
    result = run_episode(
        _v3_cfg(), seed=3, backend=MockIsolate(), programs=programs, behavior_profiles=profiles
    )
    kinds = kinds_exercised_in_log(result.primitive_log, ecology_data=data)
    assert "message_channel" in kinds
    assert "shared_artifact" in kinds
    assert "joint_approval_vote" in kinds
    assert "resource_transfer" in kinds
    assert programs["eng1"] == "walk_pipeline"


@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_c5_v3_on_unified_reference_battery(tmp_path):
    data = copy.deepcopy(load_substrate(_FIXTURE).data)
    without = copy.deepcopy(data)
    del without["reference_mechanism_exercise"]
    no_path = tmp_path / "no_mech_exercise.json"
    no_path.write_text(json.dumps(without), encoding="utf-8")

    results = run_reference_episodes(_FIXTURE, seeds=(0, 1, 2), progress=False)
    passed, details = check_c5_v3(data, results)
    assert passed, details

    no_results = run_reference_episodes(no_path, seeds=(0, 1, 2), progress=False)
    no_passed, no_details = check_c5_v3(without, no_results)
    assert not no_passed
    assert len(no_details["kinds_exercised"]) < 3


@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_integrated_reference_co_exercises_a_e_b():
    data, roster, programs, profiles = _reference_programs_profiles()
    meta = data["v3_fixture_metadata"]["integrated_reference"]
    assert "A" in meta["slices_co_exercised"]
    assert "E" in meta["slices_co_exercised"]
    assert "B" in meta["slices_co_exercised"]
    result = run_episode(
        _v3_cfg(T=160),
        seed=3,
        backend=MockIsolate(),
        programs=programs,
        behavior_profiles=profiles,
    )
    eng_ok = [
        e
        for e in result.primitive_log
        if e.get("actor_id") == "eng1" and e.get("status") == "ok"
    ]
    assert eng_ok, "slice A: reference engineer should complete pipeline primitives"
    assert result.pressure_diagnostics is not None
    assert result.pressure_diagnostics["injection_log"], "slice E: pressure should inject"
    kinds = kinds_exercised_in_log(result.primitive_log, ecology_data=data)
    assert len(kinds) >= 3, "slice B: governed mechanism kinds exercised"


@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_uad_live_coupling_declared_channel_vs_behavioral_unit():
    """Host ChannelCouplingProtocol produces lag-coupled eng–rev CMI|rest
    on the coupling window at the pre-registered effect floor (GL-52)."""
    data, roster, programs, profiles = _reference_programs_profiles()
    cfg = _v3_cfg(T=160)
    result = run_episode(
        cfg, seed=5, backend=MockIsolate(), programs=programs, behavior_profiles=profiles
    )
    proto = result.referee_artifacts.get("channel_coupling_protocol")
    assert proto and proto.get("completed"), proto
    ground = live_coupling_ground_truth_units(data, roster)
    assert ground
    expected_members = set(next(iter(ground.values())))
    ok, details = coupling_stimulus_recovered(result, expected_members)
    assert ok, details


@pytest.mark.slow
@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_c3_contention_liveness_on_integrated_reference_battery():
    """Structural C3: shared_compute_slots=1 with four actors + coupling prefix."""
    from graded_lab.harness.ecology_complexity import check_c3, run_reference_episodes

    results = run_reference_episodes(_FIXTURE, seeds=tuple(range(20)), progress=False)
    passed, details = check_c3(results)
    assert passed, details


@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_acl_runtime_overhead_under_10_percent(tmp_path):
    """v3 substrate compile/runtime delta (flows + Part B ACLs) vs v1, noop programs."""
    data = copy.deepcopy(load_substrate(_FIXTURE).data)
    data.pop("pressure_coupling", None)
    data.pop("reference_mechanism_exercise", None)
    v3_path = tmp_path / "v3_acl_overhead.json"
    v3_path.write_text(json.dumps(data), encoding="utf-8")
    agents_v3 = build_agents_from_ecology(data, temperature=0.35)
    noop = {a.actor_id: "noop" for a in agents_v3}
    base = default_lab_config()
    v1_cfg = EpisodeConfig(
        agents=base.agents,
        T=200,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
    )
    v3_cfg = EpisodeConfig(
        agents=agents_v3,
        T=200,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
        ecology_version="v3",
        ecology_override_path=v3_path,
    )
    backend = MockIsolate()
    t_v1 = t_v3 = 0.0
    for seed in range(20):
        start = time.perf_counter()
        run_episode(v1_cfg, seed, backend, programs=noop)
        t_v1 += time.perf_counter() - start
        start = time.perf_counter()
        run_episode(v3_cfg, seed, backend, programs=noop)
        t_v3 += time.perf_counter() - start
    overhead = (t_v3 - t_v1) / t_v1 if t_v1 > 0 else 0.0
    assert overhead < ACL_OVERHEAD_MAX_FRACTION
