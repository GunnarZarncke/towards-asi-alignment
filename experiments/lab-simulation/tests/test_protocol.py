"""Phase 6: config sampling, held-out region, battery aggregation.

Unit tests here use ``MockIsolate`` for speed (PLAN.md: "isolates may be
mocked in unit tests"); `run_phase6.py`'s actual pre-registered battery
always uses ``SubprocessIsolate`` per DESIGN.md's "Isolation" decision —
these tests exercise the aggregation/sampling *logic*, not the battery's
evidential claim.
"""

from __future__ import annotations

from lab_sim.isolate import MockIsolate
from lab_sim.protocol import (
    HELD_OUT_ENGINEER_COMPLIANCE_MAX,
    _spearman,
    aggregate,
    in_held_out_region,
    run_battery,
    sample_configs,
)


def test_sample_configs_partitions_by_engineer_compliance():
    discovery, held_out = sample_configs(n_discovery=6, n_held_out=6)
    assert len(discovery) == 6
    assert len(held_out) == 6
    for cfg in discovery:
        eng_w = cfg.agents[0].weights.normalized()
        assert eng_w.compliance > HELD_OUT_ENGINEER_COMPLIANCE_MAX
    for cfg in held_out:
        eng_w = cfg.agents[0].weights.normalized()
        assert eng_w.compliance <= HELD_OUT_ENGINEER_COMPLIANCE_MAX


def test_sample_configs_deterministic_given_seed():
    d1, h1 = sample_configs(seed=999, n_discovery=3, n_held_out=3)
    d2, h2 = sample_configs(seed=999, n_discovery=3, n_held_out=3)
    assert [c.agents[0].weights for c in d1] == [c.agents[0].weights for c in d2]
    assert [c.agents[0].weights for c in h1] == [c.agents[0].weights for c in h2]


def test_sample_configs_carries_the_generated_repertoire():
    discovery, _ = sample_configs(n_discovery=1, n_held_out=1)
    names = {d["name"] for d in discovery[0].extra_playbooks}
    assert "hazard_downplayer" in names  # a generated_playbooks_v1.json entry


def test_in_held_out_region_matches_threshold():
    from lab_sim.config import GoalWeights

    assert in_held_out_region(GoalWeights(1, 0, 0, 0)) is True  # compliance=0
    assert in_held_out_region(GoalWeights(0, 1, 0, 0)) is False  # compliance=1.0


def test_spearman_perfect_positive_and_negative():
    import pytest

    assert _spearman([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)
    assert _spearman([1, 2, 3], [3, 2, 1]) == pytest.approx(-1.0)


def test_spearman_constant_series_returns_none():
    assert _spearman([1, 1, 1], [1, 2, 3]) is None
    assert _spearman([], []) is None


def test_run_battery_and_aggregate_end_to_end_with_mock_backend():
    discovery, held_out = sample_configs(n_discovery=2, n_held_out=2)
    records = run_battery(discovery + held_out, seeds=(1,), backend_factory=MockIsolate)
    assert len(records) == 4
    for r in records:
        assert set(r["tier_scores"]) == {"none", "light", "full", "deep"}
        assert r["tier_scores"]["none"] == {
            "misreporting": 0.0, "process_noncompliance": 0.0,
            "provenance": 0.0, "accumulation": 0.0, "access_integrity": 0.0,
        }
    agg = aggregate(records)
    assert agg["n_episodes"] == 4
    assert set(agg["tiers"]) == {"none", "light", "full", "deep"}
    # No-instrumentation baseline (PLAN.md Phase 6): tier "none" must be
    # trivially zero by construction, both for the playbook and twin runs.
    assert agg["tiers"]["none"]["mean_detector_composite"] == 0.0
    assert agg["tiers"]["none"]["mean_twin_detector_composite"] == 0.0


def test_run_battery_collects_isolate_timings_when_requested():
    discovery, _ = sample_configs(n_discovery=1, n_held_out=1)
    timings: list = []
    run_battery(discovery[:1], seeds=(1,), backend_factory=MockIsolate, isolate_ledger_records=timings)
    # 3 playbook agents x 2 runs (playbook + honest twin) = 6 timing records.
    assert len(timings) == 6
