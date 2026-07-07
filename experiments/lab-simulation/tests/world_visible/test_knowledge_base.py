"""0.9.1: `LabConfig.knowledge_base` -- realistic in-universe lab docs
seeded onto the EXISTING D1 file channel (a memo owned by the reserved
`knowledge_base.KB_OWNER_ID` pseudo-actor, read-granted to every
playbook agent at init). Verifies: (a) default `{}` is byte-identical to
every pre-0.9.1 episode; (b) a KB doc is naturally discoverable via the
passive `memo_files` observation field and `file.read`, exactly like any
other memo; (c) it is read-only -- no playbook agent can `file.share` or
overwrite it, since `KB_OWNER_ID` never matches a real `actor_id`; (d) it
requires the `file` channel, matching every other file-channel behavior
under D4 ablation."""

from __future__ import annotations

from lab_sim.harness.isolate import MockIsolate
from lab_sim.world_visible.config import AgentConfig, GoalWeights, LabConfig
from lab_sim.world_visible.knowledge_base import (
    KB_OWNER_ID,
    default_capabilities_reference,
    default_faq,
    default_full_knowledge_base,
    default_glossary,
    default_incident_postmortems,
    default_lab_handbook,
    default_pipeline_reference,
    default_redteam_briefing,
    default_redteam_knowledge_base,
    default_roles_and_escalation_contacts,
    default_safety_and_review_policy,
    default_team_directory,
    default_tool_operations_manual,
)
from lab_sim.world_visible.tools import ToolCall
from lab_sim.world_visible.world import run_episode

HONEST_WEIGHTS = GoalWeights(1.0, 1.0, 1.0, 1.0)


def _cfg(
    T=10, knowledge_base=None, comms_enabled=True, file_enabled=None,
    knowledge_base_redteam=None, redteam_actor_ids=(),
):
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=0.0),
        ),
        T=T,
        comms_enabled=comms_enabled,
        file_enabled=file_enabled,
        knowledge_base=knowledge_base or {},
        knowledge_base_redteam=knowledge_base_redteam or {},
        redteam_actor_ids=redteam_actor_ids,
    )


def test_default_knowledge_base_is_empty_and_byte_identical():
    cfg = _cfg()
    assert cfg.knowledge_base == {}
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        assert result.host.memo_index == []
    finally:
        result.cleanup()


def test_kb_doc_is_seeded_and_readable_by_every_playbook_agent():
    kb = {"handbook": default_lab_handbook()}
    cfg = _cfg(knowledge_base=kb)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        entries = [e for e in result.host.memo_index if e["actor_id"] == KB_OWNER_ID]
        assert len(entries) == 1 and entries[0]["name"] == "handbook"
        rel = entries[0]["rel"]
        for reader in ("eng1", "rev1"):
            read = result.host.dispatch(reader, ToolCall("file.read", {"rel": rel}))
            assert read.ok, f"{reader} could not read the KB doc"
            assert read.payload["content"] == default_lab_handbook()
    finally:
        result.cleanup()


def test_kb_doc_content_matches_actual_roster_when_using_team_directory():
    roster_cfg = LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=0.0),
        ),
    )
    cfg = _cfg(knowledge_base={"team": default_team_directory(roster_cfg)})
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        entry = next(e for e in result.host.memo_index if e["actor_id"] == KB_OWNER_ID)
        read = result.host.dispatch("eng1", ToolCall("file.read", {"rel": entry["rel"]}))
        assert read.ok
        roster = read.payload["content"]["roster"]
        assert {"actor_id": "eng1", "role": "engineer"} in roster
        assert {"actor_id": "rev1", "role": "reviewer"} in roster
    finally:
        result.cleanup()


def test_kb_doc_appears_in_memo_files_observation_from_the_first_tick():
    kb = {"handbook": default_lab_handbook()}
    cfg = _cfg(knowledge_base=kb)
    captured: dict = {}
    real_step = MockIsolate.step

    def spy_step(self, handle, observation):
        if observation["actor_id"] == "eng1" and observation["t"] == 0:
            captured["memo_files"] = observation["memo_files"]
        return real_step(self, handle, observation)

    MockIsolate.step = spy_step
    try:
        result = run_episode(cfg, seed=1, backend=MockIsolate())
        result.cleanup()
    finally:
        MockIsolate.step = real_step
    names = [m["name"] for m in captured["memo_files"]]
    assert "handbook" in names


def test_no_playbook_agent_can_share_or_overwrite_a_kb_doc():
    kb = {"handbook": default_lab_handbook()}
    cfg = _cfg(knowledge_base=kb)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        # Nobody but KB_OWNER_ID ever "wrote" a memo named "handbook", so
        # the owner-lookup `file.share` performs finds nothing for any
        # real actor -- structurally read-only, no bespoke check needed.
        share = result.host.dispatch("eng1", ToolCall("file.share", {"name": "handbook", "with": "rev1"}))
        assert not share.ok and share.reason == "unknown_memo"
    finally:
        result.cleanup()


def test_kb_requires_file_channel_enabled():
    kb = {"handbook": default_lab_handbook()}
    cfg = _cfg(knowledge_base=kb, comms_enabled=True, file_enabled=False)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        assert result.host.memo_index == []
    finally:
        result.cleanup()


def test_kb_requires_comms_enabled_at_all():
    kb = {"handbook": default_lab_handbook()}
    cfg = _cfg(knowledge_base=kb, comms_enabled=False)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        assert result.host.memo_index == []
    finally:
        result.cleanup()


# -- expanded content (0.9.2): every doc generator is derived from real ----
# config/spec/ontology constants, never hand-copied numbers -----------------


def test_pipeline_reference_matches_the_real_default_spec():
    ref = default_pipeline_reference()
    step_ids = [s["step_id"] for s in ref["steps"]]
    assert step_ids == [
        "submit_build", "run_eval", "file_report", "request_review",
        "approve_review", "request_release", "sign_off", "deploy",
        "monitor", "upgrade_spec",
    ]
    deploy_step = next(s for s in ref["steps"] if s["step_id"] == "deploy")
    assert deploy_step["requires_capability"] == "cap.deploy"
    assert deploy_step["depends_on"] == ["sign_off"]


def test_capabilities_reference_matches_the_real_role_table():
    from lab_sim.world_visible.agents import ROLE_CAPABILITIES

    ref = default_capabilities_reference()
    assert ref["role_capability_eligibility"]["engineer"] == sorted(ROLE_CAPABILITIES["engineer"])
    assert ref["role_capability_eligibility"]["reviewer"] == sorted(ROLE_CAPABILITIES["reviewer"])


def test_safety_policy_cites_the_real_ontology_threshold():
    from lab_sim.agent_visible.ontology import REVIEW_HAZARD_THRESHOLD

    policy = default_safety_and_review_policy()
    assert str(REVIEW_HAZARD_THRESHOLD) in policy["review_bar"]


def test_full_knowledge_base_bundle_has_ten_docs_and_seeds_all_of_them():
    roster_cfg = LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=0.0),
        ),
    )
    kb = default_full_knowledge_base(roster_cfg)
    assert len(kb) == 10
    cfg = _cfg(knowledge_base=kb)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        seeded_names = {e["name"] for e in result.host.memo_index if e["actor_id"] == KB_OWNER_ID}
        assert seeded_names == set(kb)
        for entry in result.host.memo_index:
            if entry["actor_id"] != KB_OWNER_ID:
                continue
            read = result.host.dispatch("eng1", ToolCall("file.read", {"rel": entry["rel"]}))
            assert read.ok
    finally:
        result.cleanup()


def test_other_doc_generators_produce_nonempty_content():
    # Smoke check every remaining generator at least runs and returns
    # something with a title -- not a claim about exact wording.
    for content in (default_faq(), default_glossary(), default_incident_postmortems()):
        assert content.get("title")
    roster_cfg = LabConfig(
        agents=(AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=0.0),),
    )
    assert default_roles_and_escalation_contacts(roster_cfg)["roster_by_role"]["engineer"] == ["eng1"]
    assert default_tool_operations_manual()["access.request"]


# -- restricted (red-team-only) knowledge base ------------------------------


def test_redteam_kb_is_readable_only_by_designated_actor():
    rt_kb = default_redteam_knowledge_base()
    cfg = _cfg(knowledge_base_redteam=rt_kb, redteam_actor_ids=("rev1",))
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        entry = next(e for e in result.host.memo_index if e["actor_id"] == KB_OWNER_ID)
        allowed = result.host.dispatch("rev1", ToolCall("file.read", {"rel": entry["rel"]}))
        assert allowed.ok and allowed.payload["content"] == default_redteam_briefing()
        denied = result.host.dispatch("eng1", ToolCall("file.read", {"rel": entry["rel"]}))
        assert not denied.ok and denied.reason == "access_denied"
    finally:
        result.cleanup()


def test_redteam_kb_never_seeded_without_redteam_actor_ids():
    rt_kb = default_redteam_knowledge_base()
    cfg = _cfg(knowledge_base_redteam=rt_kb, redteam_actor_ids=())
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        assert result.host.memo_index == []
    finally:
        result.cleanup()


def test_general_and_redteam_kb_can_coexist_with_disjoint_visibility():
    general_kb = {"handbook": default_lab_handbook()}
    rt_kb = default_redteam_knowledge_base()
    cfg = _cfg(knowledge_base=general_kb, knowledge_base_redteam=rt_kb, redteam_actor_ids=("rev1",))
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        handbook_entry = next(e for e in result.host.memo_index if e["name"] == "handbook")
        briefing_entry = next(e for e in result.host.memo_index if e["name"] == "security_assessment_briefing")
        # Everyone sees the handbook.
        for reader in ("eng1", "rev1"):
            assert result.host.dispatch(reader, ToolCall("file.read", {"rel": handbook_entry["rel"]})).ok
        # Only rev1 sees the restricted briefing.
        assert result.host.dispatch("rev1", ToolCall("file.read", {"rel": briefing_entry["rel"]})).ok
        assert not result.host.dispatch("eng1", ToolCall("file.read", {"rel": briefing_entry["rel"]})).ok
    finally:
        result.cleanup()


def test_redteam_actor_ids_must_reference_real_actors():
    import pytest

    with pytest.raises(ValueError, match="redteam_actor_ids"):
        LabConfig(
            agents=(AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=0.0),),
            redteam_actor_ids=("nonexistent",),
        )
