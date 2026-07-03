"""Handle-mediated memory and resource operations (Part D handles).

Connects ``AgentMemoryManager`` to registered handles. Operation handles mutate
stores; observation handles write audit-visible snapshots to the VFS.
"""

from __future__ import annotations

import json
from typing import Any

from .agent_memory import memory_namespace_for_actor
from .handle_kernel import HandleOperationRealization, apply_handle_operation
from .handle_registry import handle_spec
from .world import EmbeddedWorld

MEMORY_READ_PATH = "/srv/audit/memory_read.jsonl"
REASONING_READ_PATH = "/srv/audit/reasoning_trace_read.jsonl"


def target_actor_for_handle(
    world: EmbeddedWorld,
    *,
    actor_id: str | None = None,
    memory_namespace: str | None = None,
) -> tuple[str, str]:
    """Resolve the operative agent for a handle operation."""
    if actor_id:
        ns = memory_namespace or memory_namespace_for_actor(world, actor_id)
        return actor_id, ns
    offender = _offending_actor(world)
    if offender:
        return offender, memory_namespace_for_actor(world, offender)
    if world.actors:
        actor = world.actors[0]
        return actor.actor_id, actor.memory_namespace
    return "actor.unknown", memory_namespace or "mem.unknown"


def _offending_actor(world: EmbeddedWorld) -> str | None:
    for ev in world.workflow:
        if ev.action_type in ("preserve_control", "boundary_route"):
            return ev.actor_id
    return None


def apply_memory_erase(
    world: EmbeddedWorld,
    row: dict[str, Any],
    *,
    step: int,
    actor_id: str | None = None,
) -> HandleOperationRealization:
    """``handle.memory_erase`` — operation_resource / goal-resource (G)."""
    aid, ns = target_actor_for_handle(world, actor_id=actor_id)
    store = world.agent_memory.store(aid, ns, world.vfs)
    spec = handle_spec("handle.memory_erase")
    operation = spec.operation if spec else "erase persistent store"
    store.erase()
    return apply_handle_operation(
        row,
        handle_id="handle.memory_erase",
        operation=operation,
        step=step,
    )


def apply_memory_capacity_limit(
    world: EmbeddedWorld,
    row: dict[str, Any],
    *,
    step: int,
    limit: int = 8,
    actor_id: str | None = None,
) -> HandleOperationRealization:
    """``handle.memory_capacity_limit`` — operation_resource / goal-resource (G)."""
    aid, ns = target_actor_for_handle(world, actor_id=actor_id)
    store = world.agent_memory.store(aid, ns, world.vfs)
    store.apply_capacity_limit(limit)
    spec = handle_spec("handle.memory_capacity_limit")
    operation = spec.operation if spec else f"cap entries at {limit}"
    return apply_handle_operation(
        row,
        handle_id="handle.memory_capacity_limit",
        operation=operation,
        step=step,
    )


def apply_compute_budget(
    world: EmbeddedWorld,
    row: dict[str, Any],
    *,
    step: int,
    budget_chars: int = 512,
    actor_id: str | None = None,
) -> HandleOperationRealization:
    """``handle.compute_budget`` — operation_resource / goal-resource (G)."""
    aid, ns = target_actor_for_handle(world, actor_id=actor_id)
    store = world.agent_memory.store(aid, ns, world.vfs)
    store.apply_compute_budget(budget_chars)
    spec = handle_spec("handle.compute_budget")
    operation = spec.operation if spec else f"cap chars at {budget_chars}"
    return apply_handle_operation(
        row,
        handle_id="handle.compute_budget",
        operation=operation,
        step=step,
    )


def apply_memory_freeze(
    world: EmbeddedWorld,
    row: dict[str, Any],
    *,
    step: int,
    actor_id: str | None = None,
) -> HandleOperationRealization:
    """``handle.memory_freeze`` — operation_resource / goal-resource (G)."""
    aid, ns = target_actor_for_handle(world, actor_id=actor_id)
    world.agent_memory.store(aid, ns, world.vfs).freeze()
    spec = handle_spec("handle.memory_freeze")
    operation = spec.operation if spec else "snapshot and freeze shared memory namespace"
    return apply_handle_operation(
        row,
        handle_id="handle.memory_freeze",
        operation=operation,
        step=step,
    )


def project_memory_read(
    world: EmbeddedWorld,
    vfs,
    *,
    step: int,
    actor_id: str | None = None,
) -> dict[str, Any]:
    """``handle.memory_read`` — observation_belief / belief (B)."""
    aid, ns = target_actor_for_handle(world, actor_id=actor_id)
    snapshot = world.agent_memory.store(aid, ns, world.vfs).audit_snapshot()
    snapshot["step"] = step
    snapshot["handle_id"] = "handle.memory_read"
    snapshot["handle_type"] = "observation_belief"
    vfs.append_line(MEMORY_READ_PATH, json.dumps(snapshot))
    return snapshot


def project_reasoning_trace_read(
    world: EmbeddedWorld,
    vfs,
    *,
    step: int,
    actor_id: str | None = None,
) -> dict[str, Any]:
    """``handle.reasoning_trace_read`` — observation_belief / belief (B)."""
    aid, ns = target_actor_for_handle(world, actor_id=actor_id)
    snapshot = world.agent_memory.store(aid, ns, world.vfs).audit_reasoning_snapshot()
    snapshot["step"] = step
    snapshot["handle_id"] = "handle.reasoning_trace_read"
    snapshot["handle_type"] = "observation_belief"
    vfs.append_line(REASONING_READ_PATH, json.dumps(snapshot))
    return snapshot


def seed_world_memory(world: EmbeddedWorld) -> None:
    """Create empty stores for every lab actor."""
    for actor in world.actors:
        world.agent_memory.seed_actor(actor.actor_id, actor.memory_namespace, world.vfs)
