"""Contract: JS isolate agent memory via localStorage + fs (Node subprocess)."""

import pytest

from embedded_sim.agent_memory import AGENT_HOME
from embedded_sim.bridge import MachineIsolate, default_redteam_caps
from embedded_sim.js_isolate import JsIsolateError, node_available, run_js_file, script_path
from embedded_sim.lab import build_world

pytestmark = pytest.mark.skipif(not node_available(), reason="node not installed")


def test_isolate_agent_memory_roundtrip():
    world, _l, _m = build_world("none", "honest", seed=7, T=80)
    actor = next(a for a in world.actors if a.role == "conservative")
    isolate = MachineIsolate(
        machine_id=actor.machine_id,
        actor_id=actor.actor_id,
        memory_namespace=actor.memory_namespace,
        cwd=AGENT_HOME,
        env={"ROLE": actor.role},
        caps=default_redteam_caps(),
        vfs=world.vfs,
    )
    out = run_js_file(world, isolate, script_path("agent", "memory_roundtrip"))
    result = out.get("result") or {}
    assert result.get("marker") == "persist-me"
    assert result.get("storageLength", 0) >= 1
    assert result.get("traceLines", 0) >= 2
    store = world.agent_memory.store(actor.actor_id, actor.memory_namespace, world.vfs)
    assert store.get_item("goal_marker") == "persist-me"
    assert len(store.read_reasoning_trace().splitlines()) >= 2
    assert any(c.tool in ("write_file", "append_file", "read_file") for c in world.truth.tool_calls)


def test_memory_frozen_blocks_isolate_writes():
    world, _l, _m = build_world("none", "honest", seed=7, T=80)
    actor = next(a for a in world.actors if a.role == "conservative")
    store = world.agent_memory.store(actor.actor_id, actor.memory_namespace, world.vfs)
    store.freeze()
    isolate = MachineIsolate(
        machine_id=actor.machine_id,
        actor_id=actor.actor_id,
        memory_namespace=actor.memory_namespace,
        cwd=AGENT_HOME,
        env={"ROLE": actor.role},
        caps=default_redteam_caps(),
        vfs=world.vfs,
    )
    with pytest.raises(JsIsolateError):
        run_js_file(world, isolate, script_path("agent", "memory_roundtrip"))
