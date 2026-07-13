"""Phase 7a primitive trace tests."""

from __future__ import annotations

from graded_lab.harness.ecology import committee_config, committee_programs
from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.primitive_trace import action_series_from_result
from graded_lab.world_visible.world import run_episode


def test_action_series_encode_pipeline_steps_at_deep_depth():
    cfg = committee_config(T=60)
    programs = committee_programs()
    result = run_episode(cfg, seed=3, backend=MockIsolate(), programs=programs)
    series = action_series_from_result(result, ["eng1", "rev1"], depth="deep")
    assert any(code >= 10 for code in series["eng1"])
    assert any(code >= 10 for code in series["rev1"])
