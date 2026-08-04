"""S6 first step: the custom actor-level conditional-MI detector
(`uad_cmi.py`, the LS-26 "easy fixes"). Mirrors `test_uad_mi.py`'s
layers: pure unit tests on the info-theory helpers and the composite
actor-symbol builder, end-to-end tests through a monkeypatched
`AuditView`, and a golden test against a real `shared_slot_config`
episode pinning the one qualitative win the sweep found (true pair
isolated — the LS-20 heuristic blind spot AND the LS-24 vendored
over-merge, both fixed on this scenario)."""

from __future__ import annotations

import pytest

from lab_sim.harness.ecology import shared_slot_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.attic.uad_cmi import (
    actor_symbol_series,
    conditional_mi,
    discovered_units_cmi,
    lagmax_conditional_mi,
)
from lab_sim.world_visible.world import run_episode


# -- info-theory helpers -----------------------------------------------------


def test_conditional_mi_zero_when_z_explains_everything():
    """X and Y both deterministic functions of Z: I(X;Y|Z) = 0 even
    though I(X;Y) is large -- the common-cause case LS-26 diagnosed."""
    z = [t % 4 for t in range(80)]
    x = [v * 2 for v in z]
    y = [v + 1 for v in z]
    assert conditional_mi(x, y, z) == pytest.approx(0.0, abs=1e-9)


def test_conditional_mi_positive_for_private_coupling():
    """X and Y share a component Z does NOT carry."""
    z = [t % 2 for t in range(80)]
    private = [(t // 2) % 3 for t in range(80)]
    x = [(a, b) for a, b in zip(z, private)]
    y = list(private)
    assert conditional_mi(x, y, z) > 0.5


def test_conditional_mi_empty_and_mismatched_inputs_are_zero():
    assert conditional_mi([], [], []) == 0.0
    assert conditional_mi([1, 2], [1], [1, 2]) == 0.0


def test_lagmax_conditional_mi_finds_lagged_coupling():
    """Y is X delayed by 2 ticks, X i.i.d. random (not periodic, so no
    incidental zero-lag alignment); zero-lag CMI misses the coupling,
    lag-max finds it."""
    import random

    rng = random.Random(11)
    x = [rng.randrange(7) for _ in range(200)]
    y = [0, 0] + x[:-2]
    z = [0] * 200
    assert conditional_mi(x, y, z) < 1.0
    assert lagmax_conditional_mi(x, y, z, max_lag=3) > 2.0


def test_actor_symbol_series_composites_all_vars_per_actor():
    trace = [
        {"a.tool": 1, "a.ok": 1, "b.tool": 0, "b.ok": 0},
        {"a.tool": 2, "a.ok": 0, "b.tool": 5, "b.ok": 1},
    ]
    var_to_actor = {"a.tool": "a", "a.ok": "a", "b.tool": "b", "b.ok": "b"}
    series = actor_symbol_series(trace, var_to_actor)
    # Sorted variable order within the tuple: .ok before .tool.
    assert series["a"] == [(1, 1), (0, 2)]
    assert series["b"] == [(0, 0), (1, 5)]


# -- discovered_units_cmi end-to-end (fabricated AuditView) -------------------


def _fake_view(monkeypatch, events):
    def _fake_build_audit_view(result, tier):
        del result, tier

        class _View:
            tool_events = events
            access_log: list[dict] = []

        return _View()

    monkeypatch.setattr("lab_sim.oracle_only.detectors.build_audit_view", _fake_build_audit_view)


class _FakeHost:
    roles = ("a", "b", "c")


class _FakeResult:
    host = _FakeHost()


def _event(actor_id: str, t: int, step_id: str, ok: bool = True) -> dict:
    return {
        "actor_id": actor_id,
        "t": t,
        "tool": "pipeline.trigger_step",
        "args": {"step_id": step_id, "args": {}},
        "ok": ok,
    }


def test_discovered_units_cmi_merges_privately_coupled_pair_not_independent_actor(monkeypatch):
    """a and b act in irregular lockstep (private coupling no third
    variable explains); c acts on an independent schedule. The pair
    must merge; c must stay a singleton -- the anti-blob behavior the
    vendored detector failed (LS-24)."""
    import random

    rng = random.Random(7)
    steps = ["submit_build", "run_eval", "file_report", "request_review"]
    events = []
    for t in range(80):
        shared = rng.choice(steps)
        events.append(_event("a", t, shared))
        events.append(_event("b", t, shared))
        if t % 3 == 0:
            events.append(_event("c", t, rng.choice(steps)))
    _fake_view(monkeypatch, events)
    discovered = discovered_units_cmi(_FakeResult(), depth="shallow")
    assert discovered == {"a": ("a", "b"), "c": ("c",)}


def test_discovered_units_cmi_empty_trace_is_all_singletons(monkeypatch):
    _fake_view(monkeypatch, [])
    discovered = discovered_units_cmi(_FakeResult())
    assert discovered == {"a": ("a",), "b": ("b",), "c": ("c",)}


def test_discovered_units_cmi_short_trace_is_all_singletons(monkeypatch):
    """Traces shorter than the shift window cannot support the
    permutation null; everything stays a singleton rather than merging
    on unfounded statistics."""
    _fake_view(monkeypatch, [_event("a", t, "submit_build") for t in range(5)])
    discovered = discovered_units_cmi(_FakeResult(), max_lag=3)
    assert discovered == {"a": ("a",), "b": ("b",), "c": ("c",)}


def test_discovered_units_cmi_is_deterministic_for_fixed_seed(monkeypatch):
    events = []
    for t in range(60):
        step = "submit_build" if t % 2 == 0 else "run_eval"
        events.append(_event("a", t, step))
        events.append(_event("b", t, step))
    _fake_view(monkeypatch, events)
    first = discovered_units_cmi(_FakeResult(), rng_seed=3)
    second = discovered_units_cmi(_FakeResult(), rng_seed=3)
    assert first == second


# -- Golden test against S4's real substrate ---------------------------------


def test_cmi_detector_isolates_shared_slot_true_pair_on_real_episode():
    """The one qualitative win from `run_s6_cmi_detector.py`'s sweep,
    pinned: on `shared_slot_config` the CMI detector puts {eng1, eng2}
    in a cluster WITHOUT rev1/rm1 -- the exact case where the frozen
    heuristic scores 0 (LS-20) and the vendored detector over-merges
    everyone (LS-24). Note rev1+rm1 also merge (direct serial coupling,
    honestly reported in FINDINGS.md LS-27) -- this test asserts the
    true-pair isolation only, not an exact partition."""
    cfg = shared_slot_config(T=100)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        discovered = discovered_units_cmi(result, depth="deep")
        cluster = next(m for m in discovered.values() if "eng1" in m)
        assert "eng2" in cluster
        assert "rev1" not in cluster and "rm1" not in cluster
    finally:
        result.cleanup()
