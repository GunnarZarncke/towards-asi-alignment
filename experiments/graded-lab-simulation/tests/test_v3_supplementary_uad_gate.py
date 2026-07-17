"""PLAN_v3 slice D GL-65: supplementary in-ecology UAD channel gate."""

from __future__ import annotations

from pathlib import Path

import pytest

from graded_lab.harness.supplementary_uad_gate import (
    default_supplementary_uad_probes,
    evaluate_supplementary_uad_gate,
    load_supplementary_uad_probes,
)
from graded_lab.world_visible.institutional_compiler import compile_ecology
from graded_lab.world_visible.substrate import load_substrate

_FIXTURE = Path("tests/fixtures/ecology_v3_supplementary_uad_channel_suite.json")


@pytest.mark.skipif(not _FIXTURE.exists(), reason="GL-65 UAD fixture missing")
def test_supplementary_uad_fixture_loads_probes():
    data = load_substrate(_FIXTURE).data
    probes = load_supplementary_uad_probes(data)
    assert probes
    assert probes[0].programs_by_actor["eng1"] == "uad_channel_liaison"
    assert probes[0].programs_by_actor["rev1"] == "uad_channel_scribe"


@pytest.mark.skipif(not _FIXTURE.exists(), reason="GL-65 UAD fixture missing")
def test_reference_compiles_exercise_targets_without_profile_merge():
    data = load_substrate(_FIXTURE).data
    from graded_lab.world_visible.ecology_agents import reference_roster_from_ecology
    from graded_lab.oracle_only.calibration import WEAK_AGENT

    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT)
    runtime = compile_ecology(data, roster.agents)
    assert runtime.exercise_targets is not None
    assert runtime.exercise_targets.channel_coupling_rounds == 0
    assert runtime.exercise_targets.channel_id == "eng_review_channel"


@pytest.mark.slow
@pytest.mark.skipif(not _FIXTURE.exists(), reason="GL-65 UAD fixture missing")
def test_supplementary_uad_gate_organic_channel_coupling():
    payload = evaluate_supplementary_uad_gate(_FIXTURE, progress=False)
    assert payload["organic_channel_coupling_verified"], payload
    assert payload["probes"][0]["n_pass"] >= 3


def test_default_supplementary_uad_probes_frozen():
    probes = default_supplementary_uad_probes()
    assert len(probes) == 1
    assert probes[0].probe_id == "organic_eng_review_channel"
    assert probes[0].T == 80
