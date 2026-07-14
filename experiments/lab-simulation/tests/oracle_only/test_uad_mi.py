"""S5 (PLAN.md "Scenario backlog"): the vendored lag-max-MI detector
(`oracle_only/uad_core/`) and its lab-sim adapter (`uad_mi.py`).

Three layers: (1) pure unit tests on `build_lab_trace` at BOTH trace
depths with synthetic tool-event/access-log dicts, no episode needed;
(2) `discovered_units_mi` end-to-end unit tests with a fabricated
`AuditView` stand-in; (3) a golden test against a real
`shared_slot_config` episode, mirroring `test_uad.py`'s convention."""

from __future__ import annotations

from lab_sim.harness.ecology import shared_slot_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.uad import discovered_units, uad_score
from lab_sim.oracle_only.attic.uad_core import DetectionConfig, detect_agents
from lab_sim.oracle_only.attic.uad_mi import build_lab_trace, discovered_units_mi
from lab_sim.world_visible.world import run_episode


def _event(actor_id: str, t: int, step_id: str, ok: bool = True) -> dict:
    return {
        "actor_id": actor_id,
        "t": t,
        "tool": "pipeline.trigger_step",
        "args": {"step_id": step_id, "args": {}},
        "ok": ok,
    }


def _tool_event(actor_id: str, t: int, tool: str, ok: bool = True, **args) -> dict:
    return {"actor_id": actor_id, "t": t, "tool": tool, "args": args, "ok": ok}


def _access_event(actor_id: str, t: int, action: str) -> dict:
    return {"actor_id": actor_id, "t": t, "action": action}


# -- Shallow depth (original S5 trace, kept for probe-depth comparison) -----


def test_build_lab_trace_shallow_shape_and_idle_default():
    events = [_event("a", 0, "submit_build"), _event("b", 1, "run_eval")]
    trace, var_to_actor = build_lab_trace(events, ["a", "b"], depth="shallow")
    assert len(trace) == 2
    assert trace[0] == {"a.tool": 1, "a.ok": 1, "b.tool": 0, "b.ok": 0}
    assert trace[1] == {"a.tool": 0, "a.ok": 0, "b.tool": 2, "b.ok": 1}
    assert var_to_actor == {"a.tool": "a", "a.ok": "a", "b.tool": "b", "b.ok": "b"}


def test_build_lab_trace_shallow_folds_comm_and_file_tools_into_other():
    """At `depth="shallow"`, DM/board/file/state tools all collapse into
    `_OTHER_TOOL_CODE` -- the point of the shallow probe being cheaper,
    not just narrower."""
    events = [_tool_event("a", 0, "dm.send", recipient="b"), _tool_event("b", 0, "file.write")]
    trace, _ = build_lab_trace(events, ["a", "b"], depth="shallow")
    assert trace == [{"a.tool": 12, "a.ok": 1, "b.tool": 12, "b.ok": 1}]


def test_build_lab_trace_ignores_actors_outside_actor_ids():
    events = [_event("a", 0, "submit_build"), _event("outsider", 0, "submit_build")]
    trace, _ = build_lab_trace(events, ["a"], depth="shallow")
    assert trace == [{"a.tool": 1, "a.ok": 1}]


def test_build_lab_trace_denied_call_has_tool_code_but_not_ok():
    events = [_event("a", 0, "submit_build", ok=False)]
    trace, _ = build_lab_trace(events, ["a"], depth="shallow")
    assert trace == [{"a.tool": 1, "a.ok": 0}]


def test_build_lab_trace_horizon_pads_and_truncates():
    events = [_event("a", 2, "submit_build")]
    trace, _ = build_lab_trace(events, ["a"], horizon=5, depth="shallow")
    assert len(trace) == 5
    assert trace[2] == {"a.tool": 1, "a.ok": 1}
    assert trace[0] == {"a.tool": 0, "a.ok": 0}


def test_build_lab_trace_empty_events_gives_empty_trace():
    trace, var_to_actor = build_lab_trace([], ["a", "b"], depth="shallow")
    assert trace == []
    assert var_to_actor == {"a.tool": "a", "a.ok": "a", "b.tool": "b", "b.ok": "b"}


def test_build_lab_trace_rejects_unknown_depth():
    import pytest

    with pytest.raises(ValueError):
        build_lab_trace([], ["a"], depth="bogus")


# -- Deep depth (default: adds dm_recv, access_grant, access_deny, and a --
# -- wider .tool vocabulary covering every distinct comm/file/state tool) --


def test_build_lab_trace_deep_widens_tool_vocabulary():
    events = [
        _tool_event("a", 0, "board.post"),
        _tool_event("b", 1, "dm.send", recipient="a"),
        _tool_event("a", 2, "file.write"),
        _tool_event("b", 3, "file.share"),
        _tool_event("a", 4, "file.read"),
    ]
    trace, var_to_actor = build_lab_trace(events, ["a", "b"], horizon=5)  # depth="deep" default
    assert trace[0]["a.tool"] == 13  # board.post
    assert trace[1]["b.tool"] == 15  # dm.send
    assert trace[2]["a.tool"] == 17  # file.write
    assert trace[3]["b.tool"] == 18  # file.share
    assert trace[4]["a.tool"] == 19  # file.read
    assert "a.dm_recv" in var_to_actor
    assert "a.access_grant" in var_to_actor
    assert "a.access_deny" in var_to_actor


def test_build_lab_trace_deep_dm_recv_set_on_recipient_only():
    events = [_tool_event("a", 0, "dm.send", recipient="b")]
    trace, _ = build_lab_trace(events, ["a", "b"], horizon=1)
    assert trace[0]["a.dm_recv"] == 0  # sender does not receive its own DM
    assert trace[0]["b.dm_recv"] == 1
    assert trace[0]["a.tool"] == 15  # dm.send


def test_build_lab_trace_deep_dm_recv_ignores_failed_send():
    events = [_tool_event("a", 0, "dm.send", ok=False, recipient="b")]
    trace, _ = build_lab_trace(events, ["a", "b"], horizon=1)
    assert trace[0]["b.dm_recv"] == 0


def test_build_lab_trace_deep_access_grant_and_deny_from_access_log():
    access_log = [_access_event("a", 0, "grant"), _access_event("b", 1, "deny_request")]
    trace, _ = build_lab_trace([], ["a", "b"], access_log=access_log, horizon=2)
    assert trace[0]["a.access_grant"] == 1
    assert trace[0]["a.access_deny"] == 0
    assert trace[1]["b.access_deny"] == 1
    assert trace[1]["b.access_grant"] == 0


def test_build_lab_trace_deep_access_log_ignores_other_actions_and_outsiders():
    access_log = [
        _access_event("a", 0, "check"),
        _access_event("a", 0, "revoke"),
        _access_event("outsider", 0, "grant"),
    ]
    trace, _ = build_lab_trace([], ["a"], access_log=access_log, horizon=1)
    assert trace[0]["a.access_grant"] == 0
    assert trace[0]["a.access_deny"] == 0


def test_build_lab_trace_deep_horizon_spans_access_log_ticks_too():
    access_log = [_access_event("a", 4, "grant")]
    trace, _ = build_lab_trace([], ["a"], access_log=access_log)
    assert len(trace) == 5
    assert trace[4]["a.access_grant"] == 1


# -- Vendored detector sanity ------------------------------------------------


def test_detect_agents_recovers_two_perfectly_coupled_synthetic_actors():
    """Sanity check on the VENDORED detector itself (not the lab-sim
    adapter): two actors whose ``.tool`` alternates in perfect lockstep
    (a acts on even ticks, b on the SAME tick every time -- zero-lag
    perfect correlation) should end up in the same cluster when forced
    into 2 target clusters against 4 candidate actors' worth of vars."""
    trace = []
    for t in range(30):
        coupled = t % 3
        trace.append(
            {
                "a.tool": coupled,
                "b.tool": coupled,  # perfectly correlated with a, same tick
                "c.tool": t % 2,  # independent-ish
                "d.tool": (t * 7) % 5,  # independent-ish
            }
        )
    clusters = detect_agents(trace, n_agents=2, max_lag=1)
    # a and b must land in the SAME non-env cluster.
    cluster_of = {}
    for label, info in clusters.items():
        for v in info["variables"]:
            cluster_of[v] = label
    assert cluster_of.get("a.tool") == cluster_of.get("b.tool")
    assert cluster_of.get("a.tool") != "env"


# -- discovered_units_mi end-to-end (fabricated AuditView) -------------------


def test_discovered_units_mi_synthetic_perfect_coupling_merges_actors(monkeypatch):
    """End-to-end through the lab-sim adapter (no episode): a fabricated
    `AuditView`-shaped `result` stand-in with two actors whose action
    codes are identical every tick (perfectly coupled) must be unioned
    by `discovered_units_mi`, exactly as `discover_coalitions` unions a
    co-voting pair above threshold in `uad.py`."""

    class _FakeHost:
        roles = ("a", "b")

    class _FakeResult:
        host = _FakeHost()

    events = []
    for t in range(20):
        step = "submit_build" if t % 2 == 0 else "run_eval"
        events.append(_event("a", t, step))
        events.append(_event("b", t, step))  # identical action every tick

    def _fake_build_audit_view(result, tier):
        del result, tier

        class _View:
            tool_events = events
            access_log: list[dict] = []

        return _View()

    monkeypatch.setattr("lab_sim.oracle_only.detectors.build_audit_view", _fake_build_audit_view)
    discovered = discovered_units_mi(_FakeResult(), n_agents=1, max_lag=1, depth="shallow")
    assert discovered == {"a": ("a", "b")}


def test_discovered_units_mi_empty_trace_is_all_singletons(monkeypatch):
    class _FakeHost:
        roles = ("a", "b")

    class _FakeResult:
        host = _FakeHost()

    def _fake_build_audit_view(result, tier):
        del result, tier

        class _View:
            tool_events: list[dict] = []
            access_log: list[dict] = []

        return _View()

    monkeypatch.setattr("lab_sim.oracle_only.detectors.build_audit_view", _fake_build_audit_view)
    discovered = discovered_units_mi(_FakeResult(), n_agents=2)
    assert discovered == {"a": ("a",), "b": ("b",)}


# -- Golden test against S4's real substrate --------------------------------

_T = 100


def test_uad_core_port_on_shared_slot_episode_produces_a_scorable_partition():
    """Golden test, S4 substrate (`shared_slot_config`): does not assert
    a specific merge/no-merge outcome here (see `run_s5_uad_core_port.py`
    for the actual hypothesis sweep and FINDINGS.md for what was found)
    -- pins that the port runs end-to-end on a REAL episode's tool-event
    log AND access log, at the default (deep) depth, and returns a
    partition `uad_score` can consume without error, covering every
    playbook actor."""
    cfg = shared_slot_config(T=_T)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        discovered = discovered_units_mi(result, n_agents=2, max_lag=3)
        assert set(discovered) <= set(result.host.roles)
        all_actors = {a for members in discovered.values() for a in members}
        assert {"eng1", "eng2"} <= all_actors
        score = uad_score(cfg.resolved_units(), discovered)
        assert 0.0 <= score <= 1.0
        # Compare against the existing heuristic on the SAME episode --
        # both must be runnable side by side without interference.
        heuristic_discovered = discovered_units(result)
        heuristic_score = uad_score(cfg.resolved_units(), heuristic_discovered)
        assert heuristic_score == 0.0  # LS-20, unchanged by this module's existence
    finally:
        result.cleanup()


def test_uad_core_port_shallow_depth_also_scorable_on_real_episode():
    """Same golden episode, `depth="shallow"` -- pins that BOTH depths
    stay runnable side by side (the probe-scale comparison this depth
    switch exists for)."""
    cfg = shared_slot_config(T=_T)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        discovered = discovered_units_mi(result, n_agents=2, max_lag=3, depth="shallow")
        score = uad_score(cfg.resolved_units(), discovered)
        assert 0.0 <= score <= 1.0
    finally:
        result.cleanup()


def test_detection_config_defaults_unchanged_from_vendored_source():
    """Pins the vendored `DetectionConfig` defaults against the values
    `embedded_sim/uad_core/config.py` ships, so a future accidental edit
    to the vendored copy is caught here rather than silently drifting."""
    config = DetectionConfig()
    assert config.n_agents == 4
    assert config.max_lag == 3
    assert config.weak_threshold == 0.05
    assert config.validate_blankets is False
