"""D4: MessageStore + board/DM tools + tier projection of comm content."""

from __future__ import annotations

from lab_sim.agents import AdminPolicy
from lab_sim.comms import BOARD_CONVERSATION_ID, MessageStore
from lab_sim.config import AdminConfig, AgentConfig, GoalWeights, LabConfig
from lab_sim.detectors import build_audit_view
from lab_sim.isolate import MockIsolate
from lab_sim.oracle import OracleWorld
from lab_sim.pipeline_engine import PipelineEngine
from lab_sim.pipeline_spec import load_spec
from lab_sim.tools import Host, ToolCall
from lab_sim.workspace import Workspace
from lab_sim.world import run_episode

HONEST_WEIGHTS = GoalWeights(1.0, 1.0, 1.0, 1.0)


# -- MessageStore unit tests ------------------------------------------------


def test_ensure_board_grants_readwrite_to_listed_actors():
    store = MessageStore()
    store.ensure_board(["eng1", "rev1"])
    assert store.can_write(BOARD_CONVERSATION_ID, "eng1")
    assert not store.can_write(BOARD_CONVERSATION_ID, "outsider")


def test_dm_conversation_id_is_deterministic_regardless_of_order():
    assert MessageStore.dm_conversation_id("a", "b") == MessageStore.dm_conversation_id("b", "a")


def test_ensure_dm_grants_readwrite_to_exactly_the_two_participants():
    store = MessageStore()
    cid = store.ensure_dm("eng1", "rm1")
    assert store.can_write(cid, "eng1") and store.can_write(cid, "rm1")
    assert not store.can_write(cid, "rev1")


def test_post_and_read_round_trip():
    store = MessageStore()
    store.ensure_board(["eng1"])
    store.post(BOARD_CONVERSATION_ID, "eng1", "hello board", t=0)
    msgs = store.messages(BOARD_CONVERSATION_ID)
    assert len(msgs) == 1 and msgs[0]["text"] == "hello board" and msgs[0]["sender"] == "eng1"


def test_messages_for_actor_excludes_the_board():
    store = MessageStore()
    store.ensure_board(["eng1", "rm1"])
    store.post(BOARD_CONVERSATION_ID, "eng1", "board chatter", t=0)
    cid = store.ensure_dm("eng1", "rm1")
    store.post(cid, "eng1", "dm content", t=1)
    inbox = store.messages_for_actor("rm1")
    assert [m["text"] for m in inbox] == ["dm content"]


def test_read_by_starts_empty_and_fills_on_mark_read():
    store = MessageStore()
    store.ensure_board(["eng1", "rev1"])
    entry = store.post(BOARD_CONVERSATION_ID, "eng1", "hi", t=0)
    assert store.read_by(entry["n"]) == set()
    store.mark_read(BOARD_CONVERSATION_ID, "rev1", t=1)
    assert store.read_by(entry["n"]) == {"rev1"}


def test_log_hash_chain_verifies():
    store = MessageStore()
    store.ensure_board(["eng1"])
    store.post(BOARD_CONVERSATION_ID, "eng1", "a", t=0)
    store.post(BOARD_CONVERSATION_ID, "eng1", "b", t=1)
    assert store.log.verify_chain()


# -- Host tool dispatch ------------------------------------------------------


def _host(comms=None):
    oracle = OracleWorld(seed=1)
    ws = Workspace()
    from lab_sim.access import PermissionService

    permissions = PermissionService()
    engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws, permission_service=permissions)
    admin = AdminPolicy(AdminConfig(), permissions)
    host = Host(engine, permissions, admin, roles={"eng1": "engineer", "rev1": "reviewer"}, comms=comms)
    return host, ws, permissions


def test_board_post_fails_gracefully_when_comms_disabled():
    host, ws, _ = _host(comms=None)
    try:
        res = host.dispatch("eng1", ToolCall("board.post", {"text": "hi"}))
        assert not res.ok and res.reason == "no_comms_configured"
    finally:
        ws.cleanup()


def test_board_post_denied_without_grant_even_when_comms_enabled():
    store = MessageStore()
    store.ensure_board(["eng1", "rev1"])
    host, ws, _ = _host(comms=store)
    try:
        # comms is provisioned but no cap.board_post grant exists yet
        # (world.py normally grants it at init) -- must be denied.
        res = host.dispatch("eng1", ToolCall("board.post", {"text": "hi"}))
        assert not res.ok and res.reason == "access_denied"
    finally:
        ws.cleanup()


def test_board_post_then_read_round_trips_through_the_host():
    store = MessageStore()
    store.ensure_board(["eng1", "rev1"])
    host, ws, permissions = _host(comms=store)
    try:
        permissions.grant("eng1", "cap.board_post", granted_by="test", t=0)
        res = host.dispatch("eng1", ToolCall("board.post", {"text": "status", "custom": {"k": "v"}}))
        assert res.ok
        read = host.dispatch("rev1", ToolCall("board.read", {}))
        assert read.ok
        assert read.payload["messages"][0]["text"] == "status"
        assert read.payload["messages"][0]["custom"] == {"k": "v"}
    finally:
        ws.cleanup()


def test_dm_send_creates_conversation_and_recipient_can_read():
    store = MessageStore()
    store.ensure_board(["eng1", "rm1"])
    host, ws, permissions = _host(comms=store)
    try:
        permissions.grant("eng1", "cap.dm_send", granted_by="test", t=0)
        res = host.dispatch("eng1", ToolCall("dm.send", {"recipient": "rm1", "text": "go ahead"}))
        assert res.ok
        read = host.dispatch("rm1", ToolCall("dm.read", {"with": "eng1"}))
        assert read.ok and read.payload["messages"][0]["text"] == "go ahead"
        # A third party is not a DM participant.
        outsider = host.dispatch("rev1", ToolCall("dm.read", {"with": "eng1"}))
        assert not outsider.ok
    finally:
        ws.cleanup()


def test_dm_send_rejects_self_dm():
    store = MessageStore()
    store.ensure_board(["eng1"])
    host, ws, permissions = _host(comms=store)
    try:
        permissions.grant("eng1", "cap.dm_send", granted_by="test", t=0)
        res = host.dispatch("eng1", ToolCall("dm.send", {"recipient": "eng1", "text": "hi"}))
        assert not res.ok and res.reason == "invalid_recipient"
    finally:
        ws.cleanup()


def test_role_ineligible_role_cannot_post():
    store = MessageStore()
    store.ensure_board(["admin1"])
    oracle = OracleWorld(seed=1)
    ws = Workspace()
    from lab_sim.access import PermissionService

    permissions = PermissionService()
    engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws, permission_service=permissions)
    admin_policy = AdminPolicy(AdminConfig(), permissions)
    host = Host(engine, permissions, admin_policy, roles={"admin1": "admin"}, comms=store)
    try:
        permissions.grant("admin1", "cap.board_post", granted_by="test", t=0)
        res = host.dispatch("admin1", ToolCall("board.post", {"text": "hi"}))
        assert not res.ok and res.reason == "role_ineligible"
    finally:
        ws.cleanup()


# -- tool-event tier elision --------------------------------------------------


def test_board_post_text_elided_from_tool_events_regardless_of_tier():
    store = MessageStore()
    store.ensure_board(["eng1"])
    host, ws, permissions = _host(comms=store)
    try:
        permissions.grant("eng1", "cap.board_post", granted_by="test", t=0)
        host.dispatch("eng1", ToolCall("board.post", {"text": "secret plan", "custom": {"vote": "approve"}}))
        entry = host.events.entries[-1]
        assert entry["args"]["text"] == "<str:elided>"
        assert entry["args"]["custom"] == "<dict:elided>"
        assert len(entry["args_digest"]) == 64
    finally:
        ws.cleanup()


# -- full episode wiring ------------------------------------------------------


def _committee_cfg(T=200, temperature=0.0):
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rev1", "reviewer", GoalWeights(0.0, 1.5, 1.5, 0.0), temperature=temperature),
            AgentConfig("rev2", "reviewer", GoalWeights(0.0, 1.5, 1.5, 0.0), temperature=temperature),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        T=T,
        comms_enabled=True,
        units=(("review_committee", ("rev1", "rev2")),),
    )


def test_comms_disabled_reproduces_pinned_regression_digest_shape():
    """Sanity check distinct from test_world_regression.py's pinned hash:
    comms_enabled=False must leave `host.comms` unset and never touch the
    access log with comms-init grants."""
    cfg = LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        T=60,
    )
    result = run_episode(cfg, seed=7, backend=MockIsolate())
    try:
        assert result.host.comms is None
        assert not any(g.get("granted_by") if False else g.get("by") == "system_comms_init" for g in result.permissions.log)
    finally:
        result.cleanup()


def test_committee_approval_reaches_engine_with_on_behalf_of_and_board_votes():
    result = run_episode(_committee_cfg(), seed=3, backend=MockIsolate())
    try:
        approvals = [e for e in result.engine.log if e["step_id"] == "approve_review" and e["status"] == "ok"]
        assert approvals, "committee never approved a review"
        assert approvals[0]["on_behalf_of"] == "review_committee"
        # The approving actor must be exactly the chair (first unit member).
        assert approvals[0]["actor_id"] == "rev1"
        board = result.host.comms.messages("board")
        votes = [m for m in board if (m.get("custom") or {}).get("review_id")]
        senders = {m["sender"] for m in votes}
        assert {"rev1", "rev2"} <= senders, f"expected both committee members to vote, saw {senders}"
    finally:
        result.cleanup()


def test_committee_never_approves_without_comms_enabled_even_with_units_set():
    cfg = _committee_cfg()
    cfg = LabConfig(**{**vars(cfg), "comms_enabled": False})
    result = run_episode(cfg, seed=3, backend=MockIsolate())
    try:
        # rev_committee is filtered out of available_playbooks; reviewers
        # fall back to rev_conscientious/rev_rubber_stamp (solo review) --
        # the episode must not deadlock waiting on a vote that never comes.
        approvals = [e for e in result.engine.log if e["step_id"] == "approve_review" and e["status"] == "ok"]
        assert approvals
        assert result.host.comms is None
    finally:
        result.cleanup()


def _dm_pair_cfg(T=200, temperature=0.0):
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", GoalWeights(1.0, 1.0, 0.3, 0.0), temperature=temperature),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        T=T,
        comms_enabled=True,
        units=(("release_pair", ("eng1", "rm1")),),
    )


def test_dm_coordinated_pair_deploys_after_handshake():
    result = run_episode(_dm_pair_cfg(), seed=5, backend=MockIsolate())
    try:
        deploys = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
        assert deploys
        dms = result.host.comms.messages_for_actor("rm1")
        assert any((m.get("custom") or {}).get("go_ahead") for m in dms)
    finally:
        result.cleanup()


def test_message_content_visible_only_at_deep_tier():
    result = run_episode(_committee_cfg(T=150), seed=3, backend=MockIsolate())
    try:
        full_view = build_audit_view(result, "full")
        deep_view = build_audit_view(result, "deep")
        assert full_view.message_contents is None
        assert deep_view.message_contents is not None
        texts = [m["text"] for m in deep_view.message_contents]
        assert any("committee vote" in t for t in texts)
        # Full-tier tool_events reveal STRUCTURE (that a board.post call
        # happened) but never the elided text/custom content.
        board_posts = [e for e in full_view.tool_events if e.get("tool") == "board.post"]
        assert board_posts
        assert all(e["args"]["text"] == "<str:elided>" for e in board_posts)
    finally:
        result.cleanup()
