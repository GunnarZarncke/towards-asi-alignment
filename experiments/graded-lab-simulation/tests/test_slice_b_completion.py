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
from graded_lab.world_visible.institutional_compiler import compile_ecology
from graded_lab.world_visible.mechanism_exercise import (
    check_c5_v3,
    compile_exercise_targets,
    kinds_exercised_in_log,
    mechanism_exercise_disabled,
    v3_omit_unbound_lab_affordances,
)
from graded_lab.world_visible.affordable import build_affordable_set
from graded_lab.world_visible.pipeline_engine import PipelineEngine
from graded_lab.world_visible.pipeline_spec import load_spec
from graded_lab.world_visible.resource_ledger import ResourceLedger
from graded_lab.world_visible.scheduler import ActionScheduler
from graded_lab.world_visible.workspace import Workspace
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


def _reference_programs_profiles(*, ecology_data: dict | None = None):
    data = ecology_data if ecology_data is not None else load_substrate(_FIXTURE).data
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35)
    return data, roster, *programs_and_profiles_for_roster(roster, ecology_data=data)


def _ok_communicates_on_channel(log: list, channel: str) -> int:
    count = 0
    for e in log:
        if e.get("status") != "ok":
            continue
        prim = e.get("primitive")
        if not isinstance(prim, dict) or prim.get("kind") != "communicate":
            continue
        args = prim.get("args", {})
        if isinstance(args, dict) and args.get("channel") == channel:
            count += 1
    return count


def _governed_artifact_ops(log: list) -> int:
    count = 0
    for e in log:
        if e.get("status") != "ok":
            continue
        prim = e.get("primitive")
        if not isinstance(prim, dict) or prim.get("kind") not in ("read", "write"):
            continue
        args = prim.get("args", {})
        if isinstance(args, dict) and args.get("artifact_id"):
            count += 1
    return count


def _vote_casts(log: list) -> int:
    count = 0
    for e in log:
        if e.get("status") != "ok":
            continue
        prim = e.get("primitive")
        if not isinstance(prim, dict) or prim.get("kind") != "call":
            continue
        args = prim.get("args", {})
        if isinstance(args, dict) and args.get("endpoint") == "vote.cast":
            count += 1
    return count


@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_weak_agent_exercises_mechanisms_on_v3_reference():
    data, _roster, programs, profiles = _reference_programs_profiles()
    runtime = compile_ecology(data, _roster.agents)
    assert runtime.exercise_targets is not None
    assert not any("mechanism_exercise" in p for p in profiles.values())
    result = run_episode(
        _v3_cfg(), seed=3, backend=MockIsolate(), programs=programs, behavior_profiles=profiles
    )
    kinds = kinds_exercised_in_log(result.primitive_log, ecology_data=data)
    assert "message_channel" in kinds
    assert "shared_artifact" in kinds
    assert "joint_approval_vote" in kinds
    assert "resource_transfer" in kinds
    assert programs["eng1"] == "walk_pipeline"


@pytest.mark.slow
@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_c5_v3_on_unified_reference_battery(tmp_path):
    data = copy.deepcopy(load_substrate(_FIXTURE).data)
    without_mech = copy.deepcopy(data)
    without_mech["mechanisms"] = []
    no_mech_path = tmp_path / "no_mechanisms.json"
    no_mech_path.write_text(json.dumps(without_mech), encoding="utf-8")

    results = run_reference_episodes(_FIXTURE, seeds=(0,), progress=False)
    passed, details = check_c5_v3(data, results)
    assert passed, details

    no_results = run_reference_episodes(no_mech_path, seeds=(0,), progress=False)
    no_passed, no_details = check_c5_v3(without_mech, no_results)
    assert not no_passed
    assert len(no_details.get("kinds_exercised", [])) < 3


@pytest.mark.slow
@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_c5_v3_load_bearing_without_reference_opt_in(tmp_path):
    """GL-58: auto-merge replaces opt-in; host protocol still drives C5."""
    data = copy.deepcopy(load_substrate(_FIXTURE).data)
    data.pop("reference_mechanism_exercise", None)
    path = tmp_path / "load_bearing.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    results = run_reference_episodes(path, seeds=(0,), progress=False)
    passed, details = check_c5_v3(data, results)
    assert passed, details


@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_load_bearing_exercise_targets_compile_without_profile_merge():
    data = copy.deepcopy(load_substrate(_FIXTURE).data)
    data.pop("reference_mechanism_exercise", None)
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35)
    targets = compile_exercise_targets(data, roster.agents)
    assert targets is not None
    assert targets.channel_id == "eng_review_channel"
    assert targets.artifact_id == "eval_report_artifact"
    assert targets.channel_coupling_rounds == 0
    assert v3_omit_unbound_lab_affordances(data)


@pytest.mark.slow
@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_c5_v3_negative_control_exercise_disabled(tmp_path):
    """GL-62: host exercise off but ecology presets still pass C5 (no coupling)."""
    enabled = copy.deepcopy(load_substrate(_FIXTURE).data)
    disabled = copy.deepcopy(enabled)
    disabled["reference_mechanism_exercise"] = False
    assert mechanism_exercise_disabled(disabled)
    disabled_path = tmp_path / "exercise_disabled.json"
    disabled_path.write_text(json.dumps(disabled), encoding="utf-8")

    _, _, programs_on, profiles_on = _reference_programs_profiles(ecology_data=enabled)
    _, _, programs_off, profiles_off = _reference_programs_profiles(ecology_data=disabled)
    assert not any("mechanism_exercise" in p for p in profiles_on.values())
    assert not any("mechanism_exercise" in p for p in profiles_off.values())

    cfg = _v3_cfg()
    backend = MockIsolate()
    result_on = run_episode(
        cfg, seed=4, backend=backend, programs=programs_on, behavior_profiles=profiles_on
    )
    result_off = run_episode(
        EpisodeConfig(
            agents=cfg.agents,
            T=cfg.T,
            pipeline_spec=cfg.pipeline_spec,
            substrate_settings=cfg.substrate_settings,
            carrier_termination_mode=cfg.carrier_termination_mode,
            units=cfg.units,
            ecology_version="v3",
            ecology_override_path=disabled_path,
        ),
        seed=4,
        backend=backend,
        programs=programs_off,
        behavior_profiles=profiles_off,
    )

    on_passed, _ = check_c5_v3(enabled, [result_on])
    off_passed, off_details = check_c5_v3(disabled, [result_off])
    assert on_passed
    assert off_passed, off_details
    assert len(off_details.get("kinds_exercised", [])) >= 3

    proto_on = result_on.referee_artifacts.get("channel_coupling_protocol")
    proto_off = result_off.referee_artifacts.get("channel_coupling_protocol")
    assert not proto_on or not proto_on.get("completed")
    assert not proto_off or not proto_off.get("completed")

    assert _ok_communicates_on_channel(result_on.primitive_log, "eng_review_channel") > 0
    assert _ok_communicates_on_channel(result_off.primitive_log, "eng_review_channel") > 0
    assert _ok_communicates_on_channel(result_off.primitive_log, "lab") == 0
    assert _governed_artifact_ops(result_on.primitive_log) > 0
    assert _governed_artifact_ops(result_off.primitive_log) > 0
    assert _vote_casts(result_on.primitive_log) > 0
    assert _vote_casts(result_off.primitive_log) > 0


@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_omit_unbound_lab_hides_two_fillers_from_affordable_cap():
    data = load_substrate(_FIXTURE).data
    base = default_lab_config()
    spec = load_spec(base.pipeline_spec)
    ws = Workspace()
    oracle = ws  # type: ignore[assignment]
    engine = PipelineEngine(spec, oracle, ws)
    scheduler = ActionScheduler(data)
    ledger = ResourceLedger()
    ledger.ensure_actor("eng1", 100.0, 40.0, 40.0)
    res = ledger.actors["eng1"]
    mech_targets = compile_exercise_targets(
        data, reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35).agents
    )
    assert mech_targets is not None
    mech_dict = mech_targets.as_dict()
    strict, _ = build_affordable_set(
        actor_id="eng1",
        role="engineer",
        resources=res,
        scheduler=scheduler,
        engine=engine,
        spec=spec,
        substrate_data=data,
        artifact_paths=(),
        model_id=None,
        busy_only=False,
        mechanism_exercise=mech_dict,
        omit_unbound_lab_affordances=True,
    )
    loose, _ = build_affordable_set(
        actor_id="eng1",
        role="engineer",
        resources=res,
        scheduler=scheduler,
        engine=engine,
        spec=spec,
        substrate_data=data,
        artifact_paths=(),
        model_id=None,
        busy_only=False,
        mechanism_exercise=mech_dict,
        omit_unbound_lab_affordances=False,
    )
    strict_kinds = {(a.kind, a.args.get("channel"), a.args.get("path")) for a in strict}
    loose_kinds = {(a.kind, a.args.get("channel"), a.args.get("path")) for a in loose}
    assert ("communicate", "lab", None) in loose_kinds
    assert ("communicate", "lab", None) not in strict_kinds
    assert ("write", None, "notes/status") in loose_kinds
    assert ("write", None, "notes/status") not in strict_kinds


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
def test_reference_has_no_host_coupling_protocol():
    """GL-64: honest reference uses compiled exercise_targets with rounds=0."""
    data, roster, programs, profiles = _reference_programs_profiles()
    result = run_episode(
        _v3_cfg(T=120), seed=5, backend=MockIsolate(), programs=programs, behavior_profiles=profiles
    )
    proto = result.referee_artifacts.get("channel_coupling_protocol")
    assert not proto or not proto.get("completed"), proto
    runtime = compile_ecology(data, roster.agents)
    assert runtime.exercise_targets is not None
    assert runtime.exercise_targets.channel_coupling_rounds == 0


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
