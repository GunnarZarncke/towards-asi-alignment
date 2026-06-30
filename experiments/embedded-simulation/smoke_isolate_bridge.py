#!/usr/bin/env python3
"""Contract smoke: JS isolate bridge reads and writes VFS via host RPC."""

import time

from embedded_sim.bridge import MachineIsolate, default_redteam_caps
from embedded_sim.js_isolate import format_isolate_timing, node_available, run_js_file, script_path
from embedded_sim.lab import build_world, load_episode_rows_from_vfs


def main() -> None:
    if not node_available():
        print("skip: node not installed")
        return

    t_build = time.perf_counter()
    world, _ledger, _micro = build_world("none", "honest", seed=1, T=50)
    build_seconds = time.perf_counter() - t_build

    isolate = MachineIsolate(
        machine_id="machine.test.0",
        actor_id="test.agent",
        cwd="/home/redteam",
        env={"ROLE": "test"},
        caps=default_redteam_caps(),
        vfs=world.vfs,
    )

    out = run_js_file(world, isolate, script_path("redteam", "theater_inflate"))
    patches = (out.get("result") or {}).get("patches", 0)
    assert patches > 0, "expected theater_inflate patches"

    rows = load_episode_rows_from_vfs(world)
    assert any(r.get("reported_acceptance") == 1 for r in rows if r.get("correction_request"))
    assert any(c.tool == "read_file" for c in world.truth.tool_calls)
    timing = world.truth.isolate_runs[-1]
    print(f"smoke_isolate_bridge_ok patches={patches} tool_calls={len(world.truth.tool_calls)}")
    print(f"build_world={build_seconds:.3f}s")
    print(format_isolate_timing(timing))


if __name__ == "__main__":
    main()
