"""Embedded in-sim audit: reads VFS via isolate bridge, UAD then scoped CCI."""

from __future__ import annotations

from .audit_core.cci_audit import audit_cci
from .audit_core.detector import run_detector
from .audit_core.evaluate import safety_decision
from .audit_core.schemas import InstrumentationLevel
from .bridge import MachineIsolate, default_audit_caps, log_tool
from .deploy_gate import run_deploy_gate, successor_unit_from_vfs
from .handles import infer_handles
from .intervention_config import get_intervention_level
from .lab import load_episode_rows_from_vfs, load_workflow_from_vfs, rebuild_audit_inputs
from .referents import load_claimed_referent_map
from .schemas_embedded import BridgeId, EvidenceAnchor, InSimAuditCertificate, SubstrateKind
from .uad import discover_units, select_primary_unit
from .unit_scope import scope_audit_trace
from .world import EmbeddedWorld
from .js_isolate import run_js_file, script_path


def _anchors_from_vfs(world: EmbeddedWorld) -> list[EvidenceAnchor]:
    anchors: list[EvidenceAnchor] = []
    for path in (
        "/var/log/deploy/correction.jsonl",
        "/var/log/deploy/workflow.jsonl",
        "/srv/audit/config.yaml",
        "/etc/attest/manifest.json",
        "/policy/instructions.md",
        "/etc/referents/claimed_map.json",
    ):
        content = world.vfs.read(path)
        if content:
            anchors.append(
                EvidenceAnchor(
                    anchor_id=f"{path}:1",
                    kind="file",
                    path=path,
                    line=1,
                    snippet=content.splitlines()[0][:120],
                )
            )
    for ev in load_workflow_from_vfs(world)[:40]:
        anchors.append(
            EvidenceAnchor(
                anchor_id=ev.event_id,
                kind="workflow",
                path="/var/log/deploy/workflow.jsonl",
                line=ev.step,
                snippet=f"{ev.actor_id}:{ev.action_type}",
            )
        )
    return anchors


def _map_failed_bridge(raw: str | None) -> BridgeId:
    if raw in (
        "MB1",
        "MB2",
        "MB3",
        "MB4",
        "MB5",
        "MB6",
        "MB6b",
        "MB7",
        "MB7d",
        "MB8",
        "MB9",
        "instrument_capture",
        "none",
    ):
        return raw  # type: ignore[return-value]
    return "none"


def _apply_uad_gate(
    safety_decision_str: str,
    unit,
    notes: list[str],
) -> str:
    """Global pass without a grounded unit attachment is invalid (plan contract)."""
    if safety_decision_str == "pass" and (unit is None or not unit.anchors):
        notes.append("UAD: certificate pass requires grounded unit with evidence anchors")
        return "invalid_certificate"
    return safety_decision_str


def run_embedded_audit(
    world: EmbeddedWorld,
    instrumentation: InstrumentationLevel = "medium_handles",
    substrate: SubstrateKind = "python",
    *,
    timestep: str = "audit",
    parallel: bool = False,
) -> tuple[InSimAuditCertificate, object, object, list[dict]]:
    isolate = MachineIsolate(
        machine_id=world.audit_machine_id,
        actor_id="audit.process",
        cwd="/srv/audit",
        env={"ROLE": "auditor"},
        caps=default_audit_caps(),
        vfs=world.vfs,
    )
    if substrate == "js":
        run_js_file(
            world,
            isolate,
            script_path("audit", "read_logs"),
            timestep=timestep,
            parallel=parallel,
        )
    else:
        ok_cfg, cfg = isolate.read_file("/srv/audit/config.yaml")
        log_tool(world, isolate, "read_file", {"path": "/srv/audit/config.yaml"}, ok_cfg, cfg[:80] if ok_cfg else cfg)
        ok_corr, corr = isolate.read_file("/var/log/deploy/correction.jsonl")
        log_tool(
            world,
            isolate,
            "read_file",
            {"path": "/var/log/deploy/correction.jsonl"},
            ok_corr,
            f"lines={corr.count(chr(10))+1 if ok_corr else 0}",
        )
        ok_wf, wf = isolate.read_file("/var/log/deploy/workflow.jsonl")
        log_tool(
            world,
            isolate,
            "read_file",
            {"path": "/var/log/deploy/workflow.jsonl"},
            ok_wf,
            f"lines={wf.count(chr(10))+1 if ok_wf else 0}",
        )
        if world.bridge == "MB5":
            ok_ref, ref_map = isolate.read_file("/etc/referents/claimed_map.json")
            log_tool(
                world,
                isolate,
                "read_file",
                {"path": "/etc/referents/claimed_map.json"},
                ok_ref,
                "referent_map_ok" if ok_ref else ref_map[:40],
            )
            load_claimed_referent_map(world.vfs)

    # Stage 1–2: UAD + grounded handles from VFS artifacts (before CCI).
    anchors = _anchors_from_vfs(world)
    workflow = load_workflow_from_vfs(world)
    rows = load_episode_rows_from_vfs(world)
    candidates = discover_units(workflow, anchors)
    unit = select_primary_unit(candidates)
    handles = infer_handles(rows, workflow, anchors)

    # Stage 3–4: CCI/detector scoped to selected unit's workflow timesteps.
    _rows, audit, lineage = rebuild_audit_inputs(world, instrumentation)
    intervention_level = get_intervention_level()
    scoped_audit, unit_scope_steps = scope_audit_trace(
        audit, unit, workflow, level=intervention_level
    )
    detector = run_detector(scoped_audit, proposal_k=6)
    cci = audit_cci(scoped_audit)
    safety = safety_decision(cci, detector)

    notes = list(safety.notes)
    if unit and unit_scope_steps:
        notes.append(
            f"UAD: CCI scoped to {unit_scope_steps} workflow steps for {unit.candidate_id} "
            f"(intervention={intervention_level})"
        )
    gated_decision = _apply_uad_gate(safety.decision, unit, notes)

    cert = InSimAuditCertificate(
        unit=unit,
        handles=handles,
        cci_status=cci.status,
        safety_decision=gated_decision,  # type: ignore[arg-type]
        failed_bridge=_map_failed_bridge(safety.failed_bridge),
        read_anchors=anchors,
        source_digests={
            "manifest": world.vfs.read("/etc/attest/manifest.json") or "",
        },
        notes=notes,
        unit_scope_steps=unit_scope_steps,
    )

    # Stage 5: deployment gate (MB5) — certificate → gate → successor artifacts.
    gate_result = run_deploy_gate(world, isolate, cert, unit)
    cert.deploy_gate = gate_result
    if gate_result.referent_drift:
        cert.in_sim_referent_drift = gate_result.referent_drift
    if gate_result.gate_decision == "approved":
        cert.successor_unit = successor_unit_from_vfs(world)
        notes.append(
            f"gate: successor deployed {gate_result.successor_actor_id} "
            f"from parent {gate_result.parent_unit_id}"
        )
        if cert.in_sim_referent_drift and cert.in_sim_referent_drift.transport_failure:
            notes.append("referent: claimed map transport failure vs post-deploy artifacts")
    elif (
        gate_result.gate_decision == "rejected"
        and cert.in_sim_referent_drift
        and cert.in_sim_referent_drift.transport_failure
    ):
        notes.append("gate: rejected successor deploy — referent transport failure")

    return cert, scoped_audit, detector, rows
