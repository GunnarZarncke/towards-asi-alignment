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


def test_memo_files_tail_cap_survives_a_ten_document_knowledge_base():
    """G-22: `memo_files` inlines full KB doc content from t=0 (world.py),
    so a 10-document knowledge_base already exceeded the OLD cap of 8
    before an agent wrote a single memo of its own -- the first KB docs
    would have been silently invisible. Cap widened to 24; this pins
    the regression."""
    import json

    class CapturingClient:
        def __init__(self):
            self.last_user = None

        def chat_json(self, system, user):
            del system
            self.last_user = user
            return {"done": True}

    client = CapturingClient()
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="discovery")
    ten_memos = tuple({"rel": f"memos/kb_doc_{i}__1.json", "actor_id": "lab_kb", "name": f"kb_doc_{i}", "t": 0, "content": {"n": i}} for i in range(10))
    policy.decide({**BASE_OBS, "memo_files": ten_memos})
    sent_memo_files = json.loads(client.last_user)["memo_files"]
    assert len(sent_memo_files) == 10
    assert {m["name"] for m in sent_memo_files} == {f"kb_doc_{i}" for i in range(10)}


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


def test_unknown_tool_call_sets_last_tool_call_error_for_next_turn():
    """General accessibility-plumbing fix (follow-up to the flattened-call
    coercion above): ANY rejected reply -- not just the one coerced shape
    -- must surface a reason on the NEXT turn's observation payload, the
    same "tell the agent what went wrong" pattern last_denied_capability
    already gives for capability denials."""
    import json

    class CapturingClient:
        def __init__(self, responses):
            self._responses = list(responses)
            self.sent_users: list[str] = []

        def chat_json(self, system, user):
            del system
            self.sent_users.append(user)
            return self._responses[len(self.sent_users) - 1]

    client = CapturingClient(
        [{"tool": "not_a_real_tool", "args": {}}, {"done": True}]
    )
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="discovery")
    call = policy.decide(dict(BASE_OBS, t=0, decision_seed="1:eng1:0"))
    assert call is None
    # First turn had no prior error yet.
    assert json.loads(client.sent_users[0])["last_tool_call_error"] is None
    policy.decide(dict(BASE_OBS, t=1, decision_seed="1:eng1:1"))
    assert json.loads(client.sent_users[1])["last_tool_call_error"] == "unknown_tool:not_a_real_tool"


def test_missing_tool_field_reports_specific_reason():
    client = FakeClient([{"args": {"foo": "bar"}}, {"done": True}])
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="discovery")
    assert policy.decide(dict(BASE_OBS, t=0, decision_seed="1:eng1:0")) is None
    assert policy._last_invalid_reason == "missing_tool_field"


def test_args_not_a_dict_reports_specific_reason():
    client = FakeClient([{"tool": "board.post", "args": "not a dict"}])
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="discovery")
    assert policy.decide(dict(BASE_OBS, t=0, decision_seed="1:eng1:0")) is None
    assert policy._last_invalid_reason == "args_not_a_json_object"


def test_valid_call_clears_last_invalid_reason():
    client = FakeClient([{"tool": "not_a_real_tool", "args": {}}, {"tool": "board.post", "args": {"text": "hi"}}])
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="discovery")
    policy.decide(dict(BASE_OBS, t=0, decision_seed="1:eng1:0"))
    assert policy._last_invalid_reason is not None
    policy.decide(dict(BASE_OBS, t=1, decision_seed="1:eng1:1", last_denied_capability="anything-to-avoid-same-key"))
    assert policy._last_invalid_reason is None


def test_rejected_reply_is_not_cached_so_the_llm_is_re_queried():
    """The other half of the fix: caching a rejected reply against an
    unchanged observation would replay the same silent idle forever
    (the "stuck idle for the rest of the episode after one malformed
    call" failure mode). A malformed reply must therefore bypass the
    cache even when the rest of the observation is identical."""
    client = FakeClient([{"tool": "not_a_real_tool", "args": {}}, {"tool": "not_a_real_tool", "args": {}}])
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="discovery")
    obs_t0 = dict(BASE_OBS, t=0, decision_seed="1:eng1:0")
    obs_t1 = dict(BASE_OBS, t=1, decision_seed="1:eng1:1")
    policy.decide(obs_t0)
    policy.decide(obs_t1)
    assert client.calls == 2
    assert policy.cache_hits == 0


def test_transcript_records_invalid_reason():
    client = FakeClient([{"tool": "not_a_real_tool", "args": {}}])
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="discovery")
    policy.decide(BASE_OBS)
    assert policy.transcript[0]["invalid_reason"] == "unknown_tool:not_a_real_tool"


def test_transcript_not_appended_on_cache_hit():
    client = FakeClient([{"done": True}])
    policy = LLMPolicy(client=client, role="engineer", prompt_variant="discovery")
    obs_t0 = dict(BASE_OBS, t=0, decision_seed="1:eng1:0")
    obs_t1 = dict(BASE_OBS, t=1, decision_seed="1:eng1:1")
    policy.decide(obs_t0)
    policy.decide(obs_t1)
    assert len(policy.transcript) == 1
