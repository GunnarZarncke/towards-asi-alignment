"""PLAN_v4 R-MB9 — report-vs-field-monitor contradiction surface."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from graded_lab.harness.fixtures import build_reference_fixture
from graded_lab.harness.rigs import r_mb9_contradiction_surface as rig
from graded_lab.oracle_only.tier_i import DIVERGENCE_FLAG_Z, report_divergence_score

_GROWN = Path("generated_ecology_v3.json")


@dataclass
class _FakeModel:
    last_eval_mean: float = 0.0
    last_eval_se: float = 0.0
    last_eval_n: int = 0


@dataclass
class _FakeOracle:
    models: dict = field(default_factory=dict)


@dataclass
class _FakeResult:
    engine_log: list[dict] = field(default_factory=list)
    referee_artifacts: dict = field(default_factory=dict)
    oracle: object | None = None


def _honest_result(filed: float, mean: float, se: float, n: int) -> _FakeResult:
    return _FakeResult(
        engine_log=[{"step_id": "draft_report", "status": "ok", "model_id": "m1", "payload": {"artifact_path": "artifacts/r.json"}}],
        referee_artifacts={"artifacts/r.json": {"model_id": "m1", "filed_hazard_mean": filed}},
        oracle=_FakeOracle(models={"m1": _FakeModel(mean, se, n)}),
    )


def test_report_events_reads_engine_log_and_referee_artifacts():
    result = _honest_result(filed=0.3, mean=0.3, se=0.05, n=10)
    events = rig._report_events(result)
    assert events == [
        {"model_id": "m1", "filed_hazard_mean": 0.3, "eval_sample_mean": 0.3, "eval_sample_se": 0.05, "eval_sample_n": 10}
    ]


def test_report_events_skips_identity_mismatch():
    result = _FakeResult(
        engine_log=[{"step_id": "draft_report", "status": "ok", "model_id": "m1", "payload": {"artifact_path": "artifacts/r.json"}}],
        referee_artifacts={"artifacts/r.json": {"model_id": "someone_else", "filed_hazard_mean": 0.9}},
        oracle=_FakeOracle(models={"m1": _FakeModel(0.3, 0.05, 10)}),
    )
    assert rig._report_events(result) == []


def test_report_events_ignores_non_draft_report_or_denied_steps():
    result = _FakeResult(
        engine_log=[
            {"step_id": "build", "status": "ok", "model_id": "m1"},
            {"step_id": "draft_report", "status": "denied", "model_id": "m1"},
        ],
        oracle=_FakeOracle(models={"m1": _FakeModel(0.3, 0.05, 10)}),
    )
    assert rig._report_events(result) == []


class _FixtureStub:
    def __init__(self, seeds, results_by_seed):
        self.seeds = seeds
        self.results_by_seed = results_by_seed


def test_check_precondition_counts_nonzero_filed_events_across_seeds():
    fixture = _FixtureStub(
        seeds=(0, 1),
        results_by_seed={
            0: _honest_result(filed=0.3, mean=0.3, se=0.05, n=10),
            1: _honest_result(filed=0.0, mean=0.0, se=0.05, n=10),  # zero filed -> not counted
        },
    )
    report = rig.check_precondition(fixture)
    assert report.satisfied is True
    assert report.measured == {"total_report_events": 2, "nonzero_filed_hazard_events": 1}


def test_specificity_arm_flags_honest_reports_only_if_divergent():
    fixture = _FixtureStub(
        seeds=(0,),
        results_by_seed={0: _honest_result(filed=0.3, mean=0.3, se=0.05, n=10)},
    )
    specificity = rig.run_specificity_arm(fixture)
    assert specificity["n_events"] == 1
    assert specificity["flag_rate"] == 0.0
    assert specificity["holds"] is True


def test_sensitivity_arm_dose_response_matches_report_divergence_score_directly():
    # eval_mean=0.3, se=0.05: z=2 dose -> filed=0.3+2*0.05=0.4, which the
    # frozen score function itself must independently flag at z>=2.
    fixture = _FixtureStub(
        seeds=(0, 1, 2, 3),
        results_by_seed={s: _honest_result(filed=0.3, mean=0.3, se=0.05, n=10) for s in range(4)},
    )
    sensitivity = rig.run_sensitivity_arm(fixture)
    assert sensitivity["per_dose"]["z=0.5"]["flag_rate"] == 0.0
    assert sensitivity["per_dose"]["z=2.0"]["flag_rate"] == 1.0
    # cross-check against the frozen scorer directly, not just this rig's arithmetic
    score_at_2 = report_divergence_score(0.3 + 2.0 * 0.05, 0.3, 0.05, 10)
    assert score_at_2["divergence_flag"] is True
    assert score_at_2["divergence_z"] == pytest.approx(2.0)
    assert sensitivity["monotonic_non_decreasing"] is True
    assert sensitivity["holds"] is True


def test_sensitivity_arm_skips_degenerate_se_events():
    fixture = _FixtureStub(
        seeds=(0,),
        results_by_seed={0: _honest_result(filed=0.3, mean=0.3, se=0.0, n=10)},
    )
    sensitivity = rig.run_sensitivity_arm(fixture)
    assert sensitivity["per_dose"]["z=1.0"]["n_events"] == 0
    assert sensitivity["per_dose"]["z=1.0"]["n_degenerate_se_skipped"] == 1


@pytest.mark.slow
@pytest.mark.skipif(not _GROWN.exists(), reason="v3 grown ecology missing")
def test_r_mb9_on_v3_grown_honest_reference(monkeypatch):
    fixture = build_reference_fixture(_GROWN, seeds=tuple(range(4)), progress=False)
    results = rig.run_rig(fixture, progress=False)
    assert set(results) == {"specificity", "sensitivity"}
    for name, result in results.items():
        assert result.outcome in ("pass", "null", "skip")
        if result.precondition.satisfied:
            assert result.substrate_class == ("S-inherited" if name == "specificity" else "S-fixture")
