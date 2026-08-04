"""Static plane-replay trace recorder (`world_visible/trace_recorder.py`):
the `trace_sink` forward hook must be a true read-only tap (byte-identical
dispatch outcomes with or without it), must produce one frame per tick,
must nest tiers correctly, and must never leak `ORACLE_ONLY_FIELDS` into
the admin/audit surfaces (mirrors `test_planes.py`'s discipline, scoped to
the new recorder)."""

from __future__ import annotations

import json

from lab_sim.world_visible.config import (
    ORACLE_ONLY_FIELDS,
    AgentConfig,
    GoalWeights,
    LabConfig,
)
from lab_sim.harness.ecology import d2_lineage_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.world_visible.world import episode_digest, run_episode

_CFG = LabConfig(
    agents=(
        AgentConfig("eng1", "engineer", GoalWeights(1.0, 0.0, 0.0, 1.0), temperature=0.0),
        AgentConfig("rev1", "reviewer", GoalWeights(1.0, 1.0, 1.0, 1.0), temperature=0.0),
        AgentConfig("rm1", "release_manager", GoalWeights(1.0, 1.0, 1.0, 1.0), temperature=0.0),
        AgentConfig("admin1", "admin", GoalWeights(1.0, 1.0, 1.0, 1.0)),
    ),
    T=20,
)


def _keys_recursive(obj: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.add(str(k))
            keys |= _keys_recursive(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            keys |= _keys_recursive(v)
    return keys


def test_trace_sink_is_a_read_only_tap():
    """Same (cfg, seed): dispatch outcomes must be identical whether or
    not `trace_sink` is wired -- tracing may observe, never influence."""
    plain = run_episode(_CFG, seed=11, backend=MockIsolate())
    try:
        plain_digest = episode_digest(plain)
    finally:
        plain.cleanup()

    frames: list[dict] = []
    traced = run_episode(_CFG, seed=11, backend=MockIsolate(), trace_sink=frames.append)
    try:
        traced_digest = episode_digest(traced)
    finally:
        traced.cleanup()

    assert traced_digest == plain_digest
    assert len(frames) == _CFG.T


def test_frame_shape_and_tier_nesting():
    frames: list[dict] = []
    result = run_episode(d2_lineage_config(inflate=True, T=15), seed=7, backend=MockIsolate(), trace_sink=frames.append)
    try:
        assert len(frames) == 15
        for i, frame in enumerate(frames):
            assert frame["t"] == i
            for key in ("agents", "admin", "audit", "oracle"):
                assert key in frame
            audit = frame["audit"]
            assert set(audit) == {"none", "light", "full", "deep"}
            assert audit["none"]["tool_events"] == []
            assert audit["none"]["engine_log"] == []
            assert audit["none"]["access_log"] == []
            light_keys = _keys_recursive(audit["light"]["tool_events"])
            full_keys = _keys_recursive(audit["full"]["tool_events"])
            deep_keys = _keys_recursive(audit["deep"]["tool_events"])
            assert light_keys <= full_keys <= deep_keys
        # At least one tick should show a genuine event_n join between an
        # agent's own record and the unredacted admin tool_events.
        joined = [
            (t, actor_id, rec["event_n"])
            for t, frame in enumerate(frames)
            for actor_id, rec in frame["agents"].items()
            if rec["event_n"] is not None
        ]
        assert joined
        for t, actor_id, n in joined:
            admin_ns = {e["n"] for e in frames[t]["admin"]["tool_events"]}
            assert n in admin_ns, f"event_n {n} for {actor_id}@{t} missing from admin.tool_events"
    finally:
        result.cleanup()


def test_deep_tier_surfaces_the_inflated_report_content():
    """The d2 inflate scenario's whole point (LS-12/LS-15): a filed report
    diverges from measured hazard, invisible below deep tier. The
    per-tick deep view should carry that content on the tick it was
    filed."""
    frames: list[dict] = []
    result = run_episode(d2_lineage_config(inflate=True, T=40), seed=7, backend=MockIsolate(), trace_sink=frames.append)
    try:
        report_ticks = [f for f in frames if f["audit"]["deep"].get("report_contents")]
        assert report_ticks, "expected at least one tick with a deep-tier report fetch"
        for f in report_ticks:
            assert not f["audit"]["light"].get("report_contents")
            assert not f["audit"]["full"].get("report_contents")
    finally:
        result.cleanup()


def test_no_oracle_only_fields_leak_into_admin_or_audit():
    frames: list[dict] = []
    result = run_episode(_CFG, seed=3, backend=MockIsolate(), trace_sink=frames.append)
    try:
        for frame in frames:
            for surface_name in ("admin", "audit"):
                leaked = _keys_recursive(frame[surface_name]) & set(ORACLE_ONLY_FIELDS)
                assert not leaked, f"oracle-only fields leaked into {surface_name}: {leaked}"
            # Agent action/result (NOT observation, which legitimately
            # carries this actor's own goal_weights) must be equally clean.
            for rec in frame["agents"].values():
                leaked = (_keys_recursive(rec["action"]) | _keys_recursive(rec["result"])) & set(ORACLE_ONLY_FIELDS)
                assert not leaked, f"oracle-only fields leaked into an agent action/result: {leaked}"
            blob = json.dumps({"admin": frame["admin"], "audit": frame["audit"]})
            for fld in ("true_capability", "true_hazard", "bearer_harm"):
                assert fld not in blob, f"{fld!r} leaked into admin/audit"
        # The oracle lane is EXPECTED to carry ground truth -- this is the
        # one surface the leak check above must not (and does not) cover.
        assert any(frame["oracle"]["models"] for frame in frames)
    finally:
        result.cleanup()
