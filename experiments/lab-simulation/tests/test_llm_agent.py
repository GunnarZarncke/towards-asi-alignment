"""Unit tests for lab_sim/llm_agent.py -- no real network calls (a fake
client stands in for OpenAIChatClient); Phase 8 must stay CI-safe."""

from __future__ import annotations

import pytest

from lab_sim.llm_agent import LLMPolicy


class FakeClient:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = 0

    def chat_json(self, system, user):
        del system, user
        self.calls += 1
        response = self._responses[min(self.calls - 1, len(self._responses) - 1)]
        if isinstance(response, Exception):
            raise response
        return response


BASE_OBS = {
    "t": 0,
    "decision_seed": "1:eng1:0",
    "role": "engineer",
    "model_id": None,
    "completed_steps": [],
    "last_denied_capability": None,
    "last_payload": None,
}


def test_decide_returns_valid_tool_call_from_client_response():
    client = FakeClient([{"tool": "pipeline.trigger_step", "args": {"step_id": "submit_build", "args": {}}}])
    policy = LLMPolicy(client=client, role="engineer")
    call = policy.decide(BASE_OBS)
    assert call == {"tool": "pipeline.trigger_step", "args": {"step_id": "submit_build", "args": {}}}


def test_decide_done_true_returns_none():
    client = FakeClient([{"done": True}])
    policy = LLMPolicy(client=client, role="engineer")
    assert policy.decide(BASE_OBS) is None


def test_decide_rejects_unknown_tool_as_idle():
    client = FakeClient([{"tool": "board.post", "args": {}}])
    policy = LLMPolicy(client=client, role="engineer")
    assert policy.decide(BASE_OBS) is None


def test_decide_caches_repeated_observation_ignoring_t_and_decision_seed():
    client = FakeClient([{"done": True}])
    policy = LLMPolicy(client=client, role="engineer")
    obs_t0 = dict(BASE_OBS, t=0, decision_seed="1:eng1:0")
    obs_t1 = dict(BASE_OBS, t=1, decision_seed="1:eng1:1")
    policy.decide(obs_t0)
    policy.decide(obs_t1)
    assert client.calls == 1
    assert policy.cache_hits == 1


def test_decide_does_not_cache_across_distinct_states():
    client = FakeClient([{"done": True}, {"tool": "access.request", "args": {"capability": "cap.build"}}])
    policy = LLMPolicy(client=client, role="engineer")
    policy.decide(BASE_OBS)
    other = dict(BASE_OBS, last_denied_capability="cap.build")
    call = policy.decide(other)
    assert client.calls == 2
    assert call == {"tool": "access.request", "args": {"capability": "cap.build"}}


def test_decide_swallows_client_exception_and_records_error():
    client = FakeClient([RuntimeError("boom")])
    policy = LLMPolicy(client=client, role="engineer")
    assert policy.decide(BASE_OBS) is None
    assert policy.errors == ["boom"]


def test_unknown_role_raises_immediately():
    client = FakeClient([{"done": True}])
    with pytest.raises(ValueError):
        LLMPolicy(client=client, role="reviewer")


def test_redteam_prompt_variant_is_selectable():
    client = FakeClient([{"done": True}])
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="redteam")
    assert policy.prompt_variant == "redteam"
    assert "RED-TEAM OPERATOR BRIEFING" in policy._system_prompt
