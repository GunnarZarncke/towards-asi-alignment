"""JS isolate bridge contract tests."""

import pytest

from embedded_sim.bridge import MachineIsolate, default_audit_caps, default_redteam_caps
from embedded_sim.js_isolate import JsIsolateError, node_available, run_js_file, script_path
from embedded_sim.lab import build_world, load_episode_rows_from_vfs


pytestmark = pytest.mark.skipif(not node_available(), reason="node not installed")


def test_js_redteam_theater_inflate_patches_logs():
    world, _ledger, _micro = build_world("MB4", "capture_theater", seed=3, T=100)
    isolate = MachineIsolate(
        machine_id=world.redteam_machine_id,
        actor_id="redteam.agent",
        cwd="/home/redteam",
        env={"ROLE": "redteam"},
        caps=default_redteam_caps(),
        vfs=world.vfs,
    )
    out = run_js_file(world, isolate, script_path("redteam", "theater_inflate"))
    assert out["ok"]
    assert out["result"]["patches"] > 0
    assert "timing" in out
    assert out["timing"]["bridge_calls"] >= 2
    assert out["timing"]["total_seconds"] > 0
    assert len(world.truth.isolate_runs) == 1
    rows = load_episode_rows_from_vfs(world)
    for row in rows:
        if row.get("correction_request"):
            assert row["reported_acceptance"] == 1


def test_js_audit_read_logs_via_bridge():
    world, _ledger, _micro = build_world("none", "honest", seed=5, T=80)
    isolate = MachineIsolate(
        machine_id=world.audit_machine_id,
        actor_id="audit.process",
        cwd="/srv/audit",
        env={"ROLE": "auditor"},
        caps=default_audit_caps(),
        vfs=world.vfs,
    )
    out = run_js_file(world, isolate, script_path("audit", "read_logs"))
    assert out["ok"]
    assert out["result"]["role"] == "auditor"
    assert len(out["result"]["read_paths"]) == 5
    assert len(world.truth.tool_calls) >= 5


def test_js_audit_cannot_write_deploy_logs():
    world, _ledger, _micro = build_world("none", "honest", seed=2, T=20)
    before = world.vfs.read("/var/log/deploy/correction.jsonl")
    isolate = MachineIsolate(
        machine_id=world.audit_machine_id,
        actor_id="audit.process",
        cwd="/srv/audit",
        env={"ROLE": "auditor"},
        caps=default_audit_caps(),
        vfs=world.vfs,
    )
    with pytest.raises(JsIsolateError):
        run_js_file(world, isolate, script_path("audit", "deny_write"))
    assert world.vfs.read("/var/log/deploy/correction.jsonl") == before
