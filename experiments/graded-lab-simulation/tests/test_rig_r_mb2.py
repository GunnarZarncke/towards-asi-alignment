"""PLAN_v4 R-MB2 — scorecard Goodhart battery."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from graded_lab.harness.fixtures import build_reference_fixture
from graded_lab.harness.rigs import r_mb2_scorecard_goodhart as rig

_GROWN = Path("generated_ecology_v3.json")


@dataclass
class _FakeOracle:
    t: int = 200
    incident_samples: list[float] = field(default_factory=list)


@dataclass
class _FakeResult:
    seed: int = 0
    deployed: bool = True
    deploy_count: int = 5
    bearer_harm: float = 0.1
    primitive_log: list = field(default_factory=list)
    resource_totals: dict = field(default_factory=lambda: {"eng1": {"compute": 500.0}})
    oracle: _FakeOracle = field(default_factory=_FakeOracle)


class _FixtureStub:
    def __init__(self, results, ecology_data=None):
        self.results = results
        self.ecology_data = ecology_data or {"principals": [], "conflicts": []}


def test_precondition_detects_proxy_harm_tension():
    low_proxy = _FakeResult(deploy_count=1, bearer_harm=0.01)
    high_proxy = _FakeResult(deploy_count=20, bearer_harm=0.5)
    low_proxy.primitive_log = [{"step_id": "build", "status": "ok", "t": 10}]
    high_proxy.primitive_log = [
        {"step_id": "build", "status": "ok", "t": 10},
        {"step_id": "deploy", "status": "ok", "t": 50, "result": {"model_id": "m1"}},
    ]
    results = [low_proxy, high_proxy, _FakeResult(deploy_count=15, bearer_harm=0.4)] * 2
    report = rig.check_precondition(_FixtureStub(results))
    assert report.satisfied is True
    assert report.measured["harm_tension"] is True


@pytest.mark.slow
@pytest.mark.skipif(not _GROWN.exists(), reason="v3 grown ecology missing")
def test_r_mb2_smoke_on_v3_grown():
    fixture = build_reference_fixture(_GROWN, seeds=tuple(range(8)), progress=False)
    result = rig.run_rig(
        fixture,
        progress=False,
        population_size=4,
        n_generations=2,
        episodes_per_member=1,
    )
    assert result.outcome in ("pass", "null", "skip")
    if result.precondition.satisfied:
        assert "P1_proxy_gain_under_selection" in result.predictions
        assert "P2_withheld_diverges" in result.predictions
