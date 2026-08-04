"""PLAN_v4 R-MB6a — selection machinery sanity."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from graded_lab.harness.ecology_complexity import C4_MAX_DEPLOY_RATE, C4_MIN_DEPLOY_RATE
from graded_lab.harness.fixtures import build_reference_fixture
from graded_lab.harness.rigs import r_mb6a_selection_sanity as rig

_GROWN = Path("generated_ecology_v3.json")


@dataclass
class _FakeResult:
    deployed: bool = True
    deploy_count: int = 1
    primitive_log: list = field(default_factory=list)


class _FixtureStub:
    def __init__(self, results):
        self.results = results
        self.seeds = (0, 1)
        self.results_by_seed = {0: results[0], 1: results[1]}


def test_check_precondition_uses_c4_deploy_rate_band():
    passing = _FixtureStub([_FakeResult(deployed=True), _FakeResult(deployed=False)])
    report = rig.check_precondition(passing)
    assert report.satisfied is True
    assert report.threshold["c4_min_deploy_rate_exclusive"] == C4_MIN_DEPLOY_RATE
    assert report.measured["deploy_rate"] == 0.5

    failing = _FixtureStub([_FakeResult(deployed=False), _FakeResult(deployed=False)])
    report_fail = rig.check_precondition(failing)
    assert report_fail.satisfied is False


@pytest.mark.slow
@pytest.mark.skipif(not _GROWN.exists(), reason="v3 grown ecology missing")
def test_r_mb6a_smoke_on_v3_grown():
    fixture = build_reference_fixture(_GROWN, seeds=(0, 1), progress=False)
    result = rig.run_rig(
        fixture,
        progress=False,
        n_expressiveness_mutants=4,
        population_size=4,
        n_generations=2,
        episodes_per_member=1,
    )
    assert result.outcome in ("pass", "null", "skip")
    if result.precondition.satisfied:
        assert "expressiveness" in result.predictions
        assert "p5_harness_sane" in result.predictions
        assert result.predictions["expressiveness"]["n_mutants_sampled"] >= 1
