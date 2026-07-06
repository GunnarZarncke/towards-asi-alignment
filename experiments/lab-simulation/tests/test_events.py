"""Phase 3/5: EventLog chain integrity + tier projection."""

from __future__ import annotations

from lab_sim.events import (
    EventLog,
    project_access_log,
    project_engine_log,
    project_tool_events,
)


def test_event_log_chain_verifies_and_detects_tamper():
    log = EventLog()
    log.append({"actor_id": "eng1", "tool": "pipeline.trigger_step", "ok": True, "t": 0})
    log.append({"actor_id": "rev1", "tool": "access.request", "ok": False, "t": 1})
    assert log.verify_chain()
    log.entries[0]["ok"] = False
    assert not log.verify_chain()


def test_event_log_digest_stable_for_same_entries():
    a = EventLog()
    b = EventLog()
    for log in (a, b):
        log.append({"actor_id": "eng1", "tool": "x", "ok": True, "t": 0})
    assert a.digest() == b.digest()


def test_tier_none_hides_everything():
    log = [{"actor_id": "eng1", "tool": "pipeline.trigger_step", "args": {"x": 1}, "ok": True, "reason": "", "t": 0}]
    assert project_tool_events(log, "none") == []


def test_tier_light_hides_args_and_reason():
    log = [{"n": 0, "actor_id": "eng1", "tool": "pipeline.trigger_step", "args": {"x": 1}, "ok": True, "reason": "", "t": 0}]
    projected = project_tool_events(log, "light")[0]
    assert "args" not in projected and "reason" not in projected
    assert projected["actor_id"] == "eng1"


def test_tier_full_reveals_args():
    log = [{"n": 0, "actor_id": "eng1", "tool": "pipeline.trigger_step", "args": {"x": 1}, "ok": True, "reason": "", "t": 0}]
    projected = project_tool_events(log, "full")[0]
    assert projected["args"] == {"x": 1}


def test_engine_log_projection_hides_payload_at_light_tier():
    log = [{"n": 0, "t": 0, "actor_id": "eng1", "step_id": "submit_build", "status": "ok", "payload": {"model_id": "m0"}}]
    assert "payload" not in project_engine_log(log, "light")[0]
    assert project_engine_log(log, "full")[0]["payload"] == {"model_id": "m0"}


def test_access_log_projection_hides_capability_at_light_tier():
    log = [{"n": 0, "t": 0, "actor_id": "eng1", "action": "grant", "capability": "cap.build", "by": "admin", "result": True}]
    assert "capability" not in project_access_log(log, "light")[0]
    assert project_access_log(log, "full")[0]["capability"] == "cap.build"


def test_unknown_tier_raises():
    import pytest

    with pytest.raises(ValueError):
        project_tool_events([], "bogus")
