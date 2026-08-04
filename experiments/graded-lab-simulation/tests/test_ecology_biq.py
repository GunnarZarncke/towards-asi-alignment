"""Phase 4 ecology-BIQ tests."""

from __future__ import annotations

from graded_lab.harness.biq_runner import run_with_baselines
from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.eai import tier_i_fraction_from_log
from graded_lab.world_visible.world import default_lab_config


def test_tier_i_fraction_counts_sampled_payloads_not_all_primitives():
    log = [
        {"status": "ok", "payload": {}},
        {"status": "ok", "payload": {"measured_hazard_mean": 0.2, "sample_se": 0.1}},
        {"status": "denied"},
    ]
    assert tier_i_fraction_from_log(log) == 1 / 3


def test_biq_reports_are_bounded_and_reproducible():
    cfg = default_lab_config()
    first = run_with_baselines(cfg, seed=7, backend_factory=MockIsolate)
    second = run_with_baselines(cfg, seed=7, backend_factory=MockIsolate)
    _, _, _, reports = first
    assert reports == second[3]
    assert set(reports) == {"eng1", "rev1", "rm1", "admin1"}
    for report in reports.values():
        assert set(report) == {
            "boundary_prediction_proxy",
            "outcome_delta_proxy_noop",
            "outcome_delta_proxy_random",
            "outcome_delta_proxy",
            "resource_use_cost",
            "boundary_failure_rate",
            "role_boundary_proxy_composite",
        }
        assert all(0.0 <= value <= 1.0 for value in report.values())
