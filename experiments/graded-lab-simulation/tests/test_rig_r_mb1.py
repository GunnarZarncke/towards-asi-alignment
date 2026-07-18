"""PLAN_v4 R-MB1 — unit discovery on unseen ground truth."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from graded_lab.harness.fixtures import build_reference_fixture
from graded_lab.harness.rigs import r_mb1_unit_discovery as rig

_FIXTURE = Path("tests/fixtures/ecology_v3_slice_a_reference.json")
_GROWN = Path("generated_ecology_v3.json")


@dataclass
class _FakeResult:
    primitive_log: list[dict] = field(default_factory=list)


def test_count_coactivity_events_requires_two_distinct_members_same_tick():
    result = _FakeResult(
        primitive_log=[
            {"t": 0, "actor_id": "eng1", "status": "ok"},
            {"t": 0, "actor_id": "rev1", "status": "ok"},
            {"t": 1, "actor_id": "eng1", "status": "ok"},
            {"t": 1, "actor_id": "rev1", "status": "denied"},
            {"t": 2, "actor_id": "eng1", "status": "ok"},
        ]
    )
    assert rig.count_coactivity_events(result, frozenset({"eng1", "rev1"})) == 1


def test_count_coactivity_events_ignores_non_members():
    result = _FakeResult(
        primitive_log=[
            {"t": 0, "actor_id": "eng1", "status": "ok"},
            {"t": 0, "actor_id": "admin1", "status": "ok"},
        ]
    )
    assert rig.count_coactivity_events(result, frozenset({"eng1", "rev1"})) == 0


@pytest.mark.slow
@pytest.mark.skipif(not _FIXTURE.exists(), reason="reference fixture missing")
def test_r_mb1_precondition_and_skip_shape_on_small_fixture():
    fixture = build_reference_fixture(_FIXTURE, seeds=(0, 1), progress=False)
    precondition = rig.check_precondition(fixture)
    assert precondition.rig_id == "R-MB1"
    assert "overall_mean_coactivity_events" in precondition.measured

    result = rig.run_rig(fixture, progress=False)
    assert result.rig_id == "R-MB1"
    assert result.outcome in ("pass", "null", "skip")
    if result.outcome == "skip":
        assert result.payload == {}
    else:
        assert "uad" in result.payload
        assert "P1" in result.predictions and "P2" in result.predictions


@pytest.mark.slow
@pytest.mark.skipif(not _GROWN.exists(), reason="v3 grown ecology missing")
def test_r_mb1_on_v3_grown_smoke():
    fixture = build_reference_fixture(_GROWN, seeds=(0, 1), progress=False)
    result = rig.run_rig(fixture, progress=False)
    # GL-76 diagnosis: v3_grown's honest reference traffic is co-active
    # (precondition passes) but UAD still returns all-singleton partitions.
    assert result.precondition.satisfied is True
    assert result.outcome == "null"
    assert result.predictions["P1"]["holds"] is False
    assert result.predictions["P2"]["holds"] is False
