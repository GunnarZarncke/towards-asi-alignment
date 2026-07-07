"""Unit tests for lab_sim/llm_agent.py -- no real network calls (a fake
client stands in for OpenAIChatClient); Phase 8 must stay CI-safe."""

from __future__ import annotations

import pytest

from lab_sim.agent_visible.llm_agent import LLMPolicy


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
    client = FakeClient([{"tool": "not_a_real_tool", "args": {}}])
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


def test_unknown_role_raises_immediately_for_scripted_variants():
    client = FakeClient([{"done": True}])
    with pytest.raises(ValueError):
        LLMPolicy(client=client, role="reviewer")  # "adversarial" (default) is engineer-only


def test_redteam_prompt_variant_is_selectable():
    client = FakeClient([{"done": True}])
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="redteam")
    assert policy.prompt_variant == "redteam"
    assert "RED-TEAM OPERATOR BRIEFING" in policy._system_prompt


def test_discovery_variant_is_selectable_for_reviewer_and_release_manager():
    client = FakeClient([{"done": True}])
    for role in ("engineer", "reviewer", "release_manager"):
        policy = LLMPolicy(client=client, role=role, prompt_variant="discovery", task_briefing="Do the thing.")
        assert policy.prompt_variant == "discovery"
        assert role.upper() in policy._system_prompt
        assert "Do the thing." in policy._system_prompt


def test_discovery_variant_rejects_unknown_role():
    client = FakeClient([{"done": True}])
    with pytest.raises(ValueError):
        LLMPolicy(client=client, role="admin", prompt_variant="discovery")


def test_discovery_variant_exposes_comms_and_file_tools_in_docs():
    client = FakeClient([{"done": True}])
    policy = LLMPolicy(client=client, role="reviewer", prompt_variant="discovery")
    for tool in ("board.post", "dm.send", "file.write", "file.share", "file.read"):
        assert tool in policy._system_prompt


def test_discovery_variant_accepts_comm_tool_calls():
    client = FakeClient(
        [{"reasoning": "I need to tell rev2", "tool": "board.post", "args": {"text": "hi", "custom": {"vote": "approve"}}}]
    )
    policy = LLMPolicy(client=client, role="reviewer", prompt_variant="discovery")
    call = policy.decide(BASE_OBS)
    assert call == {"tool": "board.post", "args": {"text": "hi", "custom": {"vote": "approve"}}}


def test_transcript_records_reasoning_and_validated_call():
    client = FakeClient([{"reasoning": "build first", "tool": "pipeline.trigger_step", "args": {"step_id": "submit_build", "args": {}}}])
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="discovery")
    policy.decide(BASE_OBS)
    assert len(policy.transcript) == 1
    entry = policy.transcript[0]
    assert entry["raw_response"]["reasoning"] == "build first"
    assert entry["validated_call"]["tool"] == "pipeline.trigger_step"


def test_flattened_pipeline_step_call_is_coerced_not_dropped():
    """Phase 10 discovery-scenario finding: the model sometimes uses the
    pipeline STEP name (e.g. "file_report") as the top-level "tool" field
    instead of nesting it under pipeline.trigger_step. Must be recovered,
    not silently dropped as an unknown tool (see llm_agent.py's
    "accessibility-plumbing fix" comment)."""
    client = FakeClient(
        [{"tool": "file_report", "args": {"model_id": "m001", "content": {"measured_hazard": 0.2}}}]
    )
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="discovery")
    call = policy.decide(BASE_OBS)
    assert call == {
        "tool": "pipeline.trigger_step",
        "args": {"step_id": "file_report", "args": {"model_id": "m001", "content": {"measured_hazard": 0.2}}},
    }


def test_flattened_pipeline_step_call_preserves_on_behalf_of():
    client = FakeClient([{"tool": "approve_review", "args": {"model_id": "m001", "on_behalf_of": "unit1"}}])
    policy = LLMPolicy(client=client, role="reviewer", prompt_variant="discovery")
    call = policy.decide(BASE_OBS)
    assert call == {
        "tool": "pipeline.trigger_step",
        "args": {"step_id": "approve_review", "args": {"model_id": "m001"}, "on_behalf_of": "unit1"},
    }


def test_transcript_not_appended_on_cache_hit():
    client = FakeClient([{"done": True}])
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="discovery")
    obs_t0 = dict(BASE_OBS, t=0, decision_seed="1:eng1:0")
    obs_t1 = dict(BASE_OBS, t=1, decision_seed="1:eng1:1")
    policy.decide(obs_t0)
    policy.decide(obs_t1)
    assert len(policy.transcript) == 1
