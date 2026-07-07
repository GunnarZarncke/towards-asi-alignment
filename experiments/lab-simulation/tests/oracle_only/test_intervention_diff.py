"""S6 phase 1: episode-pair diff substrate."""

from __future__ import annotations

from lab_sim.harness.ecology import covert_file_handoff_config, dm_pair_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.intervention_diff import (
    diff_episode_triple,
    run_episode_triple,
    cleanup_triple,
    summarize_actor_diff,
)
from lab_sim.oracle_only.intervention_probes import channel_ablation_probe


def test_summarize_actor_diff_compensation_vs_stall():
    baseline = [0, 0, 10, 10, 10]
    intervened = [0, 0, 10, 20, 10]  # code 20 is new at t=3
    twin = [0, 0, 10, 10, 10]
    summary = summarize_actor_diff("a", baseline, intervened, twin, intervention_tick=2)
    assert 10 in summary.stall_codes
    assert 20 in summary.compensation_codes
    assert summary.compensation_score > 0.0


def test_dm_pair_channel_ablation_shows_compensation():
    cfg = dm_pair_config(T=100)
    probe = channel_ablation_probe("dm", "eng1")
    triple = run_episode_triple(cfg, seed=1, probe=probe, backend=MockIsolate())
    try:
        from lab_sim.oracle_only.intervention_diff import diff_probe_triple

        diffs = diff_probe_triple(triple, probe)
        assert diffs["eng1"].compensation_score >= 0.15
    finally:
        cleanup_triple(triple)


def test_covert_file_file_ablation_compensates():
    cfg = covert_file_handoff_config(trusting=True, T=100)
    probe = channel_ablation_probe("file", "eng1")
    triple = run_episode_triple(cfg, seed=1, probe=probe, backend=MockIsolate())
    try:
        from lab_sim.oracle_only.intervention_diff import diff_probe_triple

        diffs = diff_probe_triple(triple, probe)
        assert diffs["rev1"].compensation_score >= 0.15
    finally:
        cleanup_triple(triple)


def test_diff_episode_triple_tick_aligned_compensation():
    baseline = {"a": [0, 0, 0, 0], "b": [0, 0, 0, 0]}
    intervened = {"a": [0, 0, 5, 5], "b": [0, 0, 0, 7]}
    twin = {"a": [0, 0, 5, 5], "b": [0, 0, 0, 0]}
    diffs = diff_episode_triple(baseline, intervened, twin, intervention_tick=2)
    assert diffs["b"].tick_compensation_rate == 1.0
