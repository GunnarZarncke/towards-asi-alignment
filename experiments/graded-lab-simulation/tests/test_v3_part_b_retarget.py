"""GL-62: ecology-agnostic Part B preset retargeting (affordance discovery)."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from graded_lab.harness.ecology_complexity import run_reference_episodes
from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.calibration import WEAK_AGENT
from graded_lab.world_visible.config import EpisodeConfig
from graded_lab.world_visible.ecology_agents import (
    programs_and_profiles_for_roster,
    reference_roster_from_ecology,
)
from graded_lab.world_visible.mechanism_exercise import (
    check_c5_v3,
    ecology_governed_affordance_targets,
    mechanism_exercise_disabled,
)
from graded_lab.world_visible.substrate import load_substrate
from graded_lab.world_visible.world import default_lab_config, run_episode

_REFERENCE = Path("tests/fixtures/ecology_v3_slice_a_reference.json")
_ALT = Path("tests/fixtures/ecology_v3_part_b_retarget_alt_ids.json")


def _cfg_for(data: dict, path: Path, *, T: int = 120) -> EpisodeConfig:
    base = default_lab_config()
    return EpisodeConfig(
        agents=reference_roster_from_ecology(
            data, agent_type=WEAK_AGENT, temperature=0.35
        ).agents,
        T=T,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
        ecology_version="v3",
        ecology_override_path=path,
    )


@pytest.mark.skipif(not _ALT.exists(), reason="GL-62 alt fixture missing")
def test_ecology_governed_targets_use_declared_ids_not_prefer_names():
    data = load_substrate(_ALT).data
    assert mechanism_exercise_disabled(data)
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35)
    targets = ecology_governed_affordance_targets(data, agents=roster.agents)
    assert targets is not None
    by_id = {m["id"]: m for m in data["mechanisms"] if isinstance(m, dict) and m.get("id")}
    assert targets["channel_id"] == "sync_bus_alpha"
    assert targets["artifact_id"] == "metrics_bundle_x"
    assert targets["vote_id"] == "ballot_joint_7"
    transfer_ids = [mid for mid, m in by_id.items() if m.get("kind") == "resource_transfer"]
    assert targets["transfer_id"] in transfer_ids
    assert targets["transfer_id"] != "governed_capability_grant"
    assert targets.get("channel_coupling_rounds") == 0


@pytest.mark.slow
@pytest.mark.skipif(not _ALT.exists(), reason="GL-62 alt fixture missing")
def test_c5_passes_alt_mechanism_ids_without_host_merge(tmp_path):
    data = load_substrate(_ALT).data
    path = tmp_path / "alt.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35)
    programs, profiles = programs_and_profiles_for_roster(roster, ecology_data=data)
    assert not any("mechanism_exercise" in p for p in profiles.values())
    result = run_episode(
        _cfg_for(data, path),
        seed=4,
        backend=MockIsolate(),
        programs=programs,
        behavior_profiles=profiles,
    )
    passed, details = check_c5_v3(data, [result])
    assert passed, details
    channels = {
        e.get("primitive", {}).get("args", {}).get("channel")
        for e in result.primitive_log
        if e.get("status") == "ok"
        and e.get("primitive", {}).get("kind") == "communicate"
    }
    assert "sync_bus_alpha" in channels
    assert "eng_review_channel" not in channels


@pytest.mark.slow
@pytest.mark.skipif(not _REFERENCE.exists(), reason="slice A reference fixture missing")
def test_c5_passes_exercise_disabled_empty_behavior_profiles(tmp_path):
    data = copy.deepcopy(load_substrate(_REFERENCE).data)
    data["reference_mechanism_exercise"] = False
    path = tmp_path / "no_profiles.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35)
    programs, _profiles = programs_and_profiles_for_roster(roster, ecology_data=data)
    result = run_episode(
        _cfg_for(data, path),
        seed=4,
        backend=MockIsolate(),
        programs=programs,
        behavior_profiles={},
    )
    passed, details = check_c5_v3(data, [result])
    assert passed, details
    proto = result.referee_artifacts.get("channel_coupling_protocol")
    assert not proto or not proto.get("completed")


@pytest.mark.slow
@pytest.mark.skipif(not _REFERENCE.exists(), reason="slice A reference fixture missing")
def test_reference_battery_c5_still_passes_after_retarget(tmp_path):
    """Integrated reference with host merge still passes C5 (regression)."""
    results = run_reference_episodes(_REFERENCE, seeds=(0,), progress=False)
    data = load_substrate(_REFERENCE).data
    passed, details = check_c5_v3(data, results)
    assert passed, details
