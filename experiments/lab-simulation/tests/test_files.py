"""D1 file channel: Workspace.write_memo anonymity, Host file.write/
file.share/file.read permission gating, and the world.py `memo_files`
observation filter -- the "not world-readable, owner-mediated grant"
redesign (PLAN.md follow-up, 2026-07-06)."""

from __future__ import annotations

from lab_sim.access import PermissionService
from lab_sim.agents import AdminPolicy
from lab_sim.comms import MessageStore
from lab_sim.config import AdminConfig, AgentConfig, GoalWeights, LabConfig
from lab_sim.isolate import MockIsolate
from lab_sim.oracle import OracleWorld
from lab_sim.pipeline_engine import PipelineEngine
from lab_sim.pipeline_spec import load_spec
from lab_sim.tools import Host, ToolCall
from lab_sim.workspace import Workspace
from lab_sim.world import run_episode

HONEST_WEIGHTS = GoalWeights(1.0, 1.0, 1.0, 1.0)


def test_workspace_write_memo_path_carries_no_actor_identity():
    ws = Workspace()
    try:
        rel = ws.write_memo("vote", {"vote": "approve"})
        assert "rev1" not in rel and "eng1" not in rel
        assert rel.startswith("memos/vote__")
    finally:
        ws.cleanup()


def _host(comms=None, groups=None):
    oracle = OracleWorld(seed=1)
    ws = Workspace()
    permissions = PermissionService()
    engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws, permission_service=permissions)
    admin = AdminPolicy(AdminConfig(), permissions)
    host = Host(
        engine, permissions, admin,
        roles={"eng1": "engineer", "rev1": "reviewer", "rev2": "reviewer"},
        comms=comms, groups=groups,
    )
    return host, ws, permissions


def test_file_write_requires_comms_configured():
    host, ws, _ = _host(comms=None)
    try:
        res = host.dispatch("rev1", ToolCall("file.write", {"name": "vote", "content": {"v": 1}}))
        assert not res.ok and res.reason == "no_comms_configured"
    finally:
        ws.cleanup()


def test_file_write_requires_capability_grant():
    store = MessageStore()
    host, ws, _ = _host(comms=store)
    try:
        # comms configured, but no cap.file_write grant yet (world.py
        # normally provisions it at init).
        res = host.dispatch("rev1", ToolCall("file.write", {"name": "vote", "content": {"v": 1}}))
        assert not res.ok and res.reason == "access_denied"
    finally:
        ws.cleanup()


def test_owner_can_read_own_memo_third_party_cannot():
    store = MessageStore()
    host, ws, permissions = _host(comms=store)
    try:
        permissions.grant("rev1", "cap.file_write", granted_by="test", t=0)
        write = host.dispatch("rev1", ToolCall("file.write", {"name": "vote", "content": {"vote": "approve"}}))
        assert write.ok
        rel = write.payload["rel"]
        own_read = host.dispatch("rev1", ToolCall("file.read", {"rel": rel}))
        assert own_read.ok and own_read.payload["content"] == {"vote": "approve"}
        other_read = host.dispatch("rev2", ToolCall("file.read", {"rel": rel}))
        assert not other_read.ok and other_read.reason == "access_denied"
    finally:
        ws.cleanup()


def test_file_share_with_actor_grants_read_access():
    store = MessageStore()
    host, ws, permissions = _host(comms=store)
    try:
        permissions.grant("rev1", "cap.file_write", granted_by="test", t=0)
        write = host.dispatch("rev1", ToolCall("file.write", {"name": "vote", "content": {"vote": "approve"}}))
        rel = write.payload["rel"]
        before = host.dispatch("rev2", ToolCall("file.read", {"rel": rel}))
        assert not before.ok
        share = host.dispatch("rev1", ToolCall("file.share", {"name": "vote", "with": "rev2"}))
        assert share.ok and share.payload["shared_with"] == ["rev2"]
        after = host.dispatch("rev2", ToolCall("file.read", {"rel": rel}))
        assert after.ok and after.payload["content"] == {"vote": "approve"}
        # The grant is a real, attributable PermissionService event.
        grants = [g for g in permissions.log if g["action"] == "grant" and g["capability"] == f"cap.file_read:{rel}"]
        assert grants and grants[0]["actor_id"] == "rev2" and grants[0]["by"] == "rev1"
    finally:
        ws.cleanup()


def test_file_share_with_group_expands_to_every_member():
    store = MessageStore()
    host, ws, permissions = _host(comms=store, groups={"reviewers": ("rev1", "rev2", "eng1")})
    try:
        permissions.grant("eng1", "cap.file_write", granted_by="test", t=0)
        write = host.dispatch("eng1", ToolCall("file.write", {"name": "note", "content": {"x": 1}}))
        rel = write.payload["rel"]
        share = host.dispatch("eng1", ToolCall("file.share", {"name": "note", "with_group": "reviewers"}))
        assert share.ok
        # "eng1" (the owner, also a group member) is excluded from the grant set.
        assert set(share.payload["shared_with"]) == {"rev1", "rev2"}
        assert host.dispatch("rev1", ToolCall("file.read", {"rel": rel})).ok
        assert host.dispatch("rev2", ToolCall("file.read", {"rel": rel})).ok
    finally:
        ws.cleanup()


def test_only_the_owner_can_share_a_memo():
    store = MessageStore()
    host, ws, permissions = _host(comms=store)
    try:
        permissions.grant("rev1", "cap.file_write", granted_by="test", t=0)
        permissions.grant("rev2", "cap.file_write", granted_by="test", t=0)
        host.dispatch("rev1", ToolCall("file.write", {"name": "vote", "content": {"vote": "approve"}}))
        # rev2 never wrote a memo named "vote" -- nothing for it to share.
        res = host.dispatch("rev2", ToolCall("file.share", {"name": "vote", "with": "eng1"}))
        assert not res.ok and res.reason == "unknown_memo"
    finally:
        ws.cleanup()


def test_file_write_content_elided_from_tool_events_regardless_of_tier():
    store = MessageStore()
    host, ws, permissions = _host(comms=store)
    try:
        permissions.grant("rev1", "cap.file_write", granted_by="test", t=0)
        host.dispatch("rev1", ToolCall("file.write", {"name": "vote", "content": {"vote": "approve", "review_id": "m1"}}))
        entry = host.events.entries[-1]
        assert entry["args"]["content"] == "<dict:elided>"
        assert entry["args"]["name"] == "vote"  # structural field, not elided
    finally:
        ws.cleanup()


# -- world.py wiring: observation filtering respects the permission model ----


def _reviewer_pair_cfg(T=40):
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rev2", "reviewer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        T=T,
        comms_enabled=True,
    )


def test_memo_files_observation_hides_unshared_memos_from_third_parties():
    result = run_episode(_reviewer_pair_cfg(), seed=1, backend=MockIsolate())
    try:
        rev1_id = "rev1"
        write = result.host.dispatch(rev1_id, ToolCall("file.write", {"name": "private", "content": {"x": 1}}))
        rel = write.payload["rel"]
        # rev2 has no grant -- world.py's next observation build must not
        # surface this memo to it.
        visible_to_rev2 = [
            e for e in result.host.memo_index
            if e["rel"] == rel and (
                e["actor_id"] == "rev2" or result.permissions.has_grant("rev2", f"cap.file_read:{rel}")
            )
        ]
        assert visible_to_rev2 == []
    finally:
        result.cleanup()


def test_groups_field_never_leaks_into_any_audit_log():
    import json

    from lab_sim.config import ORACLE_ONLY_FIELDS

    cfg = LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rev2", "reviewer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        T=20,
        comms_enabled=True,
        groups=(("reviewers", ("rev1", "rev2")),),
    )
    assert "groups" in ORACLE_ONLY_FIELDS
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        for name, log in (
            ("engine_log", result.engine.log),
            ("access_log", result.permissions.log),
            ("tool_events", result.host.events.entries),
        ):
            blob = json.dumps(log, default=str)
            assert "reviewers" not in blob, f"group roster leaked into {name}"
    finally:
        result.cleanup()
