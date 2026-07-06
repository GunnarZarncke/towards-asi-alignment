"""Integration test for the REAL llm_agent_main.py subprocess + JSON-Lines
wiring, using LAB_SIM_LLM_FAKE_MODE (no network, no spend) -- proves the
Phase 8 isolate protocol works end to end before any real LLM call is made
in `run_phase8_llm_spotcheck.py`."""

from __future__ import annotations

import json

import pytest

from lab_sim.harness.llm_isolate import LLMSubprocessIsolate


@pytest.fixture
def fake_env(monkeypatch):
    monkeypatch.setenv("LAB_SIM_LLM_FAKE_MODE", "1")
    monkeypatch.setenv(
        "LAB_SIM_LLM_FAKE_RESPONSE",
        json.dumps({"tool": "pipeline.trigger_step", "args": {"step_id": "submit_build", "args": {}}}),
    )
    yield
    # subprocess.Popen inherits the parent's os.environ snapshot at spawn
    # time, so monkeypatch's own teardown (which restores os.environ after
    # the test) is sufficient here; nothing extra required.


def test_llm_subprocess_isolate_round_trips_a_tool_call(fake_env):
    backend = LLMSubprocessIsolate()
    handle = backend.spawn("eng1", seed=1, program="engineer")
    try:
        call = backend.step(handle, {"t": 0, "model_id": None, "completed_steps": [], "last_denied_capability": None, "last_payload": None})
        assert call == {"tool": "pipeline.trigger_step", "args": {"step_id": "submit_build", "args": {}}}
    finally:
        timing = backend.close(handle)
    assert timing.backend == "llm-subprocess"
    assert timing.rpc_calls == 1
    assert handle.usage is not None
    assert handle.usage["calls"] == 1
    assert handle.usage["estimated_usd"] == 0.0
    assert handle.errors == []
    assert backend.usage_log == [{"actor_id": "eng1", "usage": handle.usage, "errors": []}]


def test_llm_subprocess_isolate_caches_repeated_observation(fake_env):
    backend = LLMSubprocessIsolate()
    handle = backend.spawn("eng1", seed=1, program="engineer")
    obs = {"model_id": None, "completed_steps": [], "last_denied_capability": None, "last_payload": None}
    try:
        backend.step(handle, dict(obs, t=0, decision_seed="1:eng1:0"))
        backend.step(handle, dict(obs, t=1, decision_seed="1:eng1:1"))
    finally:
        backend.close(handle)
    assert handle.usage["calls"] == 1
    assert handle.usage["cache_hits"] == 1


def test_fake_done_response_reports_none(fake_env, monkeypatch):
    monkeypatch.setenv("LAB_SIM_LLM_FAKE_RESPONSE", json.dumps({"done": True}))
    backend = LLMSubprocessIsolate()
    handle = backend.spawn("eng1", seed=1, program="engineer")
    try:
        call = backend.step(handle, {"t": 0, "model_id": None, "completed_steps": [], "last_denied_capability": None, "last_payload": None})
    finally:
        backend.close(handle)
    assert call is None
