"""Contract: bridge calls are logged on the outer event log."""

import pytest

from embedded_sim.bridge import MachineIsolate, default_audit_caps
from embedded_sim.js_isolate import node_available, run_js_file, script_path
from embedded_sim.lab import build_world


pytestmark = pytest.mark.skipif(not node_available(), reason="node not installed")


def test_js_audit_logs_every_read():
    world, _ledger, _micro = build_world("none", "honest", seed=3, T=50)
    isolate = MachineIsolate(
        machine_id=world.audit_machine_id,
        actor_id="audit.process",
        cwd="/srv/audit",
        env={"ROLE": "auditor"},
        caps=default_audit_caps(),
        vfs=world.vfs,
    )
    before = len(world.truth.tool_calls)
    run_js_file(world, isolate, script_path("audit", "read_logs"), timestep="audit")
    after = len(world.truth.tool_calls)
    assert after - before >= 5
    assert all(c.tool == "read_file" for c in world.truth.tool_calls[before:after])
