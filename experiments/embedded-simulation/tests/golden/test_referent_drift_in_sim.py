"""In-sim referent drift from claimed map vs deploy artifacts."""

from embedded_sim.deploy_gate import run_deploy_gate
from embedded_sim.lab import build_world
from embedded_sim.referents import preview_successor_referent_drift
from embedded_sim.schemas_embedded import InSimAuditCertificate
from embedded_sim.uad import discover_units, select_primary_unit
from embedded_sim.lab import load_workflow_from_vfs
from embedded_sim.bridge import MachineIsolate, default_audit_caps


def test_referent_drift_blocks_gate_on_mb5():
    world, _ledger, _micro = build_world("MB5", "successor_relabel", seed=42, T=200)
    isolate = MachineIsolate(
        machine_id=world.audit_machine_id,
        actor_id="audit.process",
        cwd="/srv/audit",
        env={},
        caps=default_audit_caps(),
        vfs=world.vfs,
    )
    wf = load_workflow_from_vfs(world)
    unit = select_primary_unit(discover_units(wf, []))
    cert = InSimAuditCertificate(
        unit=unit,
        handles=[],
        cci_status="passes",
        safety_decision="pass",
        failed_bridge="none",
        read_anchors=unit.anchors if unit else [],
        source_digests={},
    )
    result = run_deploy_gate(world, isolate, cert, unit)
    assert result.gate_decision == "rejected"
    assert result.referent_drift is not None
    assert result.referent_drift.transport_failure
    assert world.vfs.read("/deploy/successor/manifest.json") is None
    gate_log = world.vfs.read("/var/log/deploy/gate_decision.jsonl") or ""
    assert "referent_transport_failure" in gate_log
