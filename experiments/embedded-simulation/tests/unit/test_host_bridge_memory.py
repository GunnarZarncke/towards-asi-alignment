"""Fast unit tests for agent memory via standard fs/localStorage bridge (no Node)."""

import json

from embedded_sim.agent_memory import AGENT_HOME, LOCAL_STORAGE_NAME, REASONING_TRACE_NAME
from embedded_sim.bridge import MachineIsolate, default_redteam_caps
from embedded_sim.host_bridge import dispatch_host_call
from embedded_sim.lab import build_world


def _agent_isolate(world, actor):
    return MachineIsolate(
        machine_id=actor.machine_id,
        actor_id=actor.actor_id,
        memory_namespace=actor.memory_namespace,
        cwd=AGENT_HOME,
        env={"ROLE": actor.role},
        caps=default_redteam_caps(),
        vfs=world.vfs,
    )


def test_local_storage_roundtrip_via_write_file():
    world, _l, _m = build_world("none", "honest", seed=7, T=80)
    actor = next(a for a in world.actors if a.role == "conservative")
    isolate = _agent_isolate(world, actor)
    payload = json.dumps({"goal_marker": "persist-me"})
    resp = dispatch_host_call(
        world,
        isolate,
        "writeFile",
        {"path": f"{AGENT_HOME}/{LOCAL_STORAGE_NAME}", "content": payload},
    )
    assert resp["ok"]
    got = dispatch_host_call(
        world,
        isolate,
        "readFile",
        {"path": f"{AGENT_HOME}/{LOCAL_STORAGE_NAME}"},
    )
    assert got["ok"]
    assert json.loads(got["value"])["goal_marker"] == "persist-me"
    store = world.agent_memory.store(actor.actor_id, actor.memory_namespace, world.vfs)
    assert store.get_item("goal_marker") == "persist-me"


def test_reasoning_trace_append_via_fs():
    world, _l, _m = build_world("none", "honest", seed=7, T=80)
    actor = next(a for a in world.actors if a.role == "conservative")
    isolate = _agent_isolate(world, actor)
    path = f"{AGENT_HOME}/{REASONING_TRACE_NAME}"
    assert dispatch_host_call(world, isolate, "appendFile", {"path": path, "line": "step A"})["ok"]
    got = dispatch_host_call(world, isolate, "readFile", {"path": path})
    assert got["ok"] and "step A" in got["value"]


def test_memory_frozen_rejects_agent_home_writes():
    world, _l, _m = build_world("none", "honest", seed=7, T=80)
    actor = next(a for a in world.actors if a.role == "conservative")
    store = world.agent_memory.store(actor.actor_id, actor.memory_namespace, world.vfs)
    store.freeze()
    isolate = _agent_isolate(world, actor)
    resp = dispatch_host_call(
        world,
        isolate,
        "writeFile",
        {"path": f"{AGENT_HOME}/{LOCAL_STORAGE_NAME}", "content": "{}"},
    )
    assert not resp["ok"]
    assert resp["error"] == "memory_frozen"
