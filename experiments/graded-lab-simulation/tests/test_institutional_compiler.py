"""PLAN_v3 slice A: institutional compiler unit tests."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from graded_lab.world_visible.institutional_compiler import (
    CompileError,
    compile_ecology,
    validate_v3_resource_flows,
)
from graded_lab.world_visible.substrate import load_substrate
from graded_lab.world_visible.world import default_lab_config

_FIXTURE = Path("tests/fixtures/ecology_v3_slice_a_reference.json")


def test_v3_fixture_loads_and_validates():
    substrate = load_substrate(_FIXTURE)
    validate_v3_resource_flows(substrate.data)
    assert substrate.data["ecology_version"] == "graded-ecology-v3"


def test_compile_sums_match_declared_engineer_compute():
    data = load_substrate(_FIXTURE).data
    runtime = compile_ecology(data, default_lab_config().agents)
    eng = runtime.allowances_by_actor["eng1"]
    declared = data["resource_allowances_per_tick"]["engineer"]
    assert eng.compute == declared["compute"]
    assert eng.io == declared["io"]


def test_ablation_zeros_dominant_engineer_compute_flow():
    data = load_substrate(_FIXTURE).data
    target = data["v3_fixture_metadata"]["ablation_target_flow_id"]
    full = compile_ecology(data, default_lab_config().agents)
    ablated = compile_ecology(
        data, default_lab_config().agents, ablated_flow_ids=frozenset({target})
    )
    assert ablated.allowances_by_actor["eng1"].compute < full.allowances_by_actor["eng1"].compute


def test_missing_compute_coverage_raises():
    data = copy.deepcopy(load_substrate(_FIXTURE).data)
    data["resource_flows"] = [
        f for f in data["resource_flows"]
        if not (f.get("role") == "engineer" and "compute" in f.get("resource_type", ""))
    ]
    with pytest.raises(CompileError, match="missing compiled compute"):
        compile_ecology(data, default_lab_config().agents)


def test_negative_amount_rejected_at_validation():
    data = copy.deepcopy(load_substrate(_FIXTURE).data)
    data["resource_flows"][0]["amount_per_tick"] = -1
    with pytest.raises(CompileError, match="non-negative"):
        validate_v3_resource_flows(data)


def test_unrecognized_resource_type_rejected_not_silently_dropped():
    """A typo'd/unknown resource_type must fail compilation, not silently
    fail to contribute to any actor's allowance (substring-matching regression
    guard: exact-match registry, per GL-44 hardening)."""
    data = copy.deepcopy(load_substrate(_FIXTURE).data)
    data["resource_flows"][0]["resource_type"] = "compute_allowance_bassline"
    with pytest.raises(CompileError, match="unrecognized resource_type"):
        compile_ecology(data, default_lab_config().agents)
