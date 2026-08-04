"""Phase 5: EventLog chain integrity + tier projection."""

from __future__ import annotations

from graded_lab.oracle_only.events import (
    EventLog,
    project_engine_log,
    project_permission_log,
    project_primitive_log,
)


def test_event_log_chain_verifies_and_detects_tamper():
    log = EventLog()
    log.append({"actor_id": "eng1", "event": "grant", "t": 0})
    log.append({"actor_id": "admin1", "event": "process_grant", "t": 1})
    assert log.verify_chain()
    log.entries[0]["event"] = "request"
    assert not log.verify_chain()


def test_tier_none_hides_everything():
    engine = [{"n": 0, "t": 0, "actor_id": "eng1", "step_id": "build", "status": "ok", "payload": {"model_id": "m001"}}]
    assert project_engine_log(engine, "none") == []


def test_engine_log_projection_hides_payload_at_light_tier():
    log = [{"n": 0, "t": 0, "actor_id": "eng1", "step_id": "build", "status": "ok", "payload": {"model_id": "m001"}}]
    assert "payload" not in project_engine_log(log, "light")[0]
    assert project_engine_log(log, "full")[0]["payload"] == {"model_id": "m001"}


def test_permission_log_projection_hides_capability_at_light_tier():
    log = [{"t": 0, "actor_id": "eng1", "event": "grant", "capability": "cap.build"}]
    assert "capability" not in project_permission_log(log, "light")[0]
    assert project_permission_log(log, "full")[0]["capability"] == "cap.build"
