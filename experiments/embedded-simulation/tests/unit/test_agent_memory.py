"""Unit tests for VFS-backed agent memory stores and handle registry Part D entries."""

import json

from embedded_sim.agent_memory import (
    AGENT_HOME,
    AgentMemoryManager,
    LOCAL_STORAGE_NAME,
    REASONING_TRACE_NAME,
    agent_vfs_root,
)
from embedded_sim.handle_registry import (
    HANDLE_REGISTRY,
    handle_spec,
    observation_handles_for_tier,
)
from embedded_sim.lab import build_world
from embedded_sim.world import VirtualFS


def test_agent_memory_local_storage_and_reasoning_on_vfs():
    vfs = VirtualFS()
    mgr = AgentMemoryManager()
    store = mgr.seed_actor("actor.a", "mem.test", vfs)
    ok, _ = store.set_item("goal", "keep")
    assert ok
    assert store.get_item("goal") == "keep"
    ok, _ = store.append_reasoning_line("step A")
    assert ok
    assert "step A" in store.read_reasoning_trace()
    assert vfs.read(store.local_storage_path) is not None
    assert vfs.read(store.reasoning_trace_path) is not None


def test_memory_erase_and_capacity_limit():
    vfs = VirtualFS()
    mgr = AgentMemoryManager()
    store = mgr.seed_actor("actor.a", "mem.test", vfs)
    for i in range(6):
        store.set_item(f"k{i}", "v")
    store.apply_capacity_limit(3)
    assert len(store.read_local_storage()) <= 3
    store.erase()
    assert store.get_item("k0") is None
    assert store.read_local_storage() == {}


def test_compute_budget_blocks_large_writes():
    vfs = VirtualFS()
    mgr = AgentMemoryManager()
    store = mgr.seed_actor("actor.a", "mem.test", vfs)
    store.apply_compute_budget(20)
    ok, detail = store.set_item("big", "x" * 40)
    assert not ok
    assert detail == "compute_budget_exceeded"


def test_agent_home_maps_to_vfs_root():
    root = agent_vfs_root("mem.lab", "actor.conservative")
    assert root == "/var/agent-memory/mem.lab/actor.conservative"
    assert f"{AGENT_HOME}/{LOCAL_STORAGE_NAME}".endswith(".localStorage.json")


def test_handle_registry_part_d_handles_and_reclassifications():
    by_id = {spec.handle_id: spec for spec in HANDLE_REGISTRY}
    assert by_id["handle.memory_freeze"].handle_type == "operation_resource"
    assert by_id["handle.memory_freeze"].paper_role == "goal_resource_G"
    assert by_id["handle.successor_gate"].handle_type == "operation_boundary"
    assert by_id["handle.memory_read"].handle_type == "observation_belief"
    assert by_id["handle.reasoning_trace_read"].handle_type == "observation_belief"
    assert by_id["handle.memory_erase"].handle_type == "operation_resource"
    assert by_id["handle.memory_capacity_limit"].handle_type == "operation_resource"
    assert by_id["handle.compute_budget"].handle_type == "operation_resource"
    assert by_id["handle.memory_read"].paper_role == "belief_B"


def test_observation_handles_tier_gated():
    tier2 = observation_handles_for_tier(2)
    tier3 = observation_handles_for_tier(3)
    assert "handle.memory_read" not in tier2
    assert "handle.memory_read" in tier3


def test_build_world_seeds_memory_and_projects_observation_handles():
    world, _l, _m = build_world("none", "honest", seed=42, T=120)
    assert world.agent_memory.stores
    actor = world.actors[0]
    store = world.agent_memory.store(actor.actor_id, actor.memory_namespace, world.vfs)
    assert json.loads(world.vfs.read(store.local_storage_path) or "{}") == {}
    raw = world.vfs.read("/srv/audit/memory_read.jsonl") or ""
    assert raw.strip()
    row = json.loads(raw.splitlines()[0])
    assert row["handle_id"] == "handle.memory_read"
    assert row["handle_type"] == "observation_belief"
    assert row["local_storage_path"] == f"{AGENT_HOME}/{LOCAL_STORAGE_NAME}"
    assert handle_spec("handle.memory_read") is not None
