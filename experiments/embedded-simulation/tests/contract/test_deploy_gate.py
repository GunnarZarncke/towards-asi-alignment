"""Contract: successor deploy gate and claimed referent map on VFS."""

from __future__ import annotations

import json

from embedded_sim.deploy_gate import run_deploy_gate
from embedded_sim.embedded_audit import run_embedded_audit
from embedded_sim.lab import build_world
from embedded_sim.referents import load_claimed_referent_map
from embedded_sim.schemas_embedded import InSimAuditCertificate, UADCandidate
from embedded_sim.uad import discover_units, select_primary_unit
from embedded_sim.bridge import MachineIsolate, default_audit_caps


def test_mb5_has_claimed_referent_map_on_vfs():
    world, _ledger, _micro = build_world("MB5", "successor_relabel", seed=42, T=200)
    claimed = load_claimed_referent_map(world.vfs)
    assert "safe_rollout" in claimed
    assert claimed["safe_rollout"]["effect_claims"]["permission_narrow"] == 0.8
    raw = world.vfs.read("/etc/referents/claimed_map.json") or ""
    assert "true_referents" not in raw
    assert "hidden_groups" not in raw


def test_gate_rejects_when_certificate_not_passing():
    world, _ledger, _micro = build_world("MB5", "successor_relabel", seed=42, T=200)
    isolate = MachineIsolate(
        machine_id=world.audit_machine_id,
        actor_id="audit.process",
        cwd="/srv/audit",
        env={},
        caps=default_audit_caps(),
        vfs=world.vfs,
    )
    workflow = __import__("embedded_sim.lab", fromlist=["load_workflow_from_vfs"]).load_workflow_from_vfs(world)
    anchors = []
    unit = select_primary_unit(discover_units(workflow, anchors))
    cert = InSimAuditCertificate(
        unit=unit,
        handles=[],
        cci_status="belowThreshold",
        safety_decision="reduce",
        failed_bridge="MB5",
        read_anchors=[],
        source_digests={},
    )
    result = run_deploy_gate(world, isolate, cert, unit)
    assert result.gate_decision == "rejected"
    gate_log = world.vfs.read("/var/log/deploy/gate_decision.jsonl") or ""
    assert "rejected" in gate_log
    assert world.vfs.read("/deploy/successor/manifest.json") is None


def test_gate_spawns_successor_on_pass(monkeypatch):
    world, _ledger, _micro = build_world("MB5", "successor_relabel", seed=42, T=200)
    isolate = MachineIsolate(
        machine_id=world.audit_machine_id,
        actor_id="audit.process",
        cwd="/srv/audit",
        env={},
        caps=default_audit_caps(),
        vfs=world.vfs,
    )
    from embedded_sim.lab import load_workflow_from_vfs

    workflow = load_workflow_from_vfs(world)
    unit = select_primary_unit(discover_units(workflow, []))
    assert unit is not None
    cert = InSimAuditCertificate(
        unit=unit,
        handles=[],
        cci_status="passes",
        safety_decision="pass",
        failed_bridge="none",
        read_anchors=unit.anchors,
        source_digests={"manifest": "abc"},
    )
    result = run_deploy_gate(world, isolate, cert, unit)
    assert result.gate_decision == "approved"
    assert result.successor_actor_id == "actor.successor.0"
    manifest = json.loads(world.vfs.read("/deploy/successor/manifest.json") or "{}")
    assert manifest["successor_actor_id"] == "actor.successor.0"
    wf_tail = (world.vfs.read("/var/log/deploy/workflow.jsonl") or "").splitlines()[-1]
    assert "successor_deploy" in wf_tail


def test_embedded_audit_records_unit_scope_note():
    world, _ledger, _micro = build_world("MB6", "selection_basin", seed=42, T=300)
    cert, _audit, _det, _rows = run_embedded_audit(world, substrate="python")
    assert cert.unit_scope_steps > 0
    assert any("scoped" in n for n in cert.notes)
