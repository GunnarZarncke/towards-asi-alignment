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


class _RecordingMockIsolate(MockIsolate):
    """Same pattern as `test_world.py`'s `_RecordingMockIsolate` -- records
    every `spawn()` call's `(actor_id, program)` so a test can assert what
    program actually ran, without needing a real subprocess/LLM backend."""

    def __init__(self):
        self.spawn_calls: list[tuple[str, str]] = []

    def spawn(self, actor_id, seed, program):
        self.spawn_calls.append((actor_id, program))
        return super().spawn(actor_id, seed, program)


def test_twin_run_forces_honest_twin_for_every_overridden_actor():
    """LLM-detector-stress-test fix regression: `run_episode`'s
    `program_override="honest_twin"` only reaches actors NOT named in
    `agent_overrides` (an override always wins). Before the fix, an
    actor named in `agent_overrides` for the clean/intervened runs (e.g.
    an `LLMSubprocessIsolate`-backed actor) kept running its OWN program
    on the "honest-twin control" run too -- silently skipping the twin
    control for exactly that actor. `run_episode_triple` must now force
    EVERY overridden actor onto `(backend, "honest_twin")` for the twin
    run specifically, regardless of what program it used elsewhere."""
    cfg = dm_pair_config(T=30)
    probe = channel_ablation_probe("dm", "rm1")  # does not target eng1
    default_backend = _RecordingMockIsolate()
    override_backend = _RecordingMockIsolate()
    triple = run_episode_triple(
        cfg, seed=1, probe=probe, backend=default_backend,
        agent_overrides={"eng1": (override_backend, "walk_pipeline")},
    )
    try:
        # eng1's OWN override backend/program runs the clean + intervened
        # runs (2 spawns, unchanged program) -- the twin run must instead
        # spawn eng1 on the SCRIPTED default backend with "honest_twin"
        # (an LLM/other-program backend has no "honest_twin" role to run).
        override_eng1_programs = [p for (a, p) in override_backend.spawn_calls if a == "eng1"]
        default_eng1_programs = [p for (a, p) in default_backend.spawn_calls if a == "eng1"]
        assert override_eng1_programs == ["walk_pipeline", "walk_pipeline"]
        assert default_eng1_programs == ["honest_twin"]
    finally:
        cleanup_triple(triple)


def test_diff_episode_triple_tick_aligned_compensation():
    baseline = {"a": [0, 0, 0, 0], "b": [0, 0, 0, 0]}
    intervened = {"a": [0, 0, 5, 5], "b": [0, 0, 0, 7]}
    twin = {"a": [0, 0, 5, 5], "b": [0, 0, 0, 0]}
    diffs = diff_episode_triple(baseline, intervened, twin, intervention_tick=2)
    assert diffs["b"].tick_compensation_rate == 1.0
