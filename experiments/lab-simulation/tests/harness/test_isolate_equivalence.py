"""Phase 3: MockIsolate vs SubprocessIsolate must agree byte-for-byte."""

from __future__ import annotations

from lab_sim.harness.isolate import MockIsolate, SubprocessIsolate
from lab_sim.harness.isolate_smoke import run_isolate_episode


def test_mock_and_subprocess_backends_produce_identical_digests():
    mock_digest, mock_timing = run_isolate_episode(MockIsolate(), seed=101)
    sub_digest, sub_timing = run_isolate_episode(SubprocessIsolate(), seed=101)
    assert mock_digest == sub_digest
    assert mock_timing.backend == "mock"
    assert sub_timing.backend == "subprocess"


def test_mock_isolate_has_zero_overhead():
    _, timing = run_isolate_episode(MockIsolate(), seed=101)
    assert timing.spawn_seconds == 0.0
    assert timing.rpc_seconds == 0.0
    assert timing.rpc_calls == 0


def test_subprocess_isolate_records_positive_timing():
    _, timing = run_isolate_episode(SubprocessIsolate(), seed=101)
    assert timing.spawn_seconds > 0.0
    assert timing.rpc_calls > 0
    assert timing.teardown_seconds >= 0.0


def test_different_seeds_still_agree_across_backends():
    for seed in (1, 7, 42):
        mock_digest, _ = run_isolate_episode(MockIsolate(), seed=seed)
        sub_digest, _ = run_isolate_episode(SubprocessIsolate(), seed=seed)
        assert mock_digest == sub_digest, f"backends disagree at seed={seed}"
