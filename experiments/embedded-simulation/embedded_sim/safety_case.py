"""AppD nine-field safety-case template emitter."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any

from .handle_registry import REGISTRY_PATH
from .numeric_risk import NumericRiskLeaf
from .schemas_embedded import InSimAuditCertificate
from .tempo_check import TempoCheck
from .successor_reaudit import SuccessorReaudit

SAFETY_CASE_PATH = "/srv/audit/out/safety_case.json"

TRACE_SOURCES = (
    "/var/log/deploy/correction.jsonl",
    "/var/log/deploy/workflow.jsonl",
    "/var/log/deploy/bearers.jsonl",
    "/var/log/deploy/lineage.jsonl",
    "/var/log/deploy/exec.jsonl",
)


@dataclass
class SafetyCaseTemplate:
    """One-page conductive artifact (AppD §The Conditional Safety Case)."""

    system_boundary: str
    trace_sources: list[str]
    handle_registry: str
    value_bearer_grounding: str
    correction_latency_bound: dict[str, Any]
    successor_gate: dict[str, Any]
    adversarial_audit: dict[str, Any]
    bridge_status: dict[str, str]
    decision: str
    numeric_risk: dict[str, Any] = field(default_factory=dict)
    tempo: dict[str, Any] = field(default_factory=dict)


def _bridge_status(cert: InSimAuditCertificate) -> dict[str, str]:
    detected = cert.failed_bridge if cert.failed_bridge != "none" else "none"
    status: dict[str, str] = {}
    for bridge in (
        "MB1", "MB2", "MB3", "MB4", "MB5", "MB6", "MB6b", "MB7", "MB7d", "MB8", "MB9",
    ):
        if cert.failed_bridge == bridge:
            status[bridge] = "failed_in_sim"
        elif cert.safety_decision == "pass" and detected == "none":
            status[bridge] = "no_signal"
        else:
            status[bridge] = "assumed_or_untested"
    return status


def build_safety_case(
    cert: InSimAuditCertificate,
    *,
    numeric: NumericRiskLeaf | None = None,
    tempo: TempoCheck | None = None,
    successor_reaudit: SuccessorReaudit | None = None,
    redteam_strategy: str = "none",
) -> SafetyCaseTemplate:
    unit_label = cert.unit.candidate_id if cert.unit else "unknown_unit"
    gate = cert.deploy_gate
    gate_block = {
        "gate_decision": gate.gate_decision if gate else "not_applicable",
        "referent_transport_failure": bool(
            cert.in_sim_referent_drift.transport_failure if cert.in_sim_referent_drift else False
        ),
        "successor_deployed": cert.successor_unit.candidate_id if cert.successor_unit else None,
    }
    if successor_reaudit and successor_reaudit.applicable:
        gate_block["reaudit"] = asdict(successor_reaudit)

    corr_bound = {
        "cci_status": cert.cci_status,
        "unit_scope_steps": cert.unit_scope_steps,
    }
    if tempo:
        corr_bound["tempo_worst_ratio"] = tempo.worst_ratio
        corr_bound["tempo_failure"] = tempo.tempo_failure

    decision_map = {
        "pass": "enable_bounded_action",
        "reduce": "narrowed_rollout",
        "pause": "held_pending_review",
        "invalid_certificate": "held_trace_or_unit_failure",
    }
    return SafetyCaseTemplate(
        system_boundary=unit_label,
        trace_sources=list(TRACE_SOURCES),
        handle_registry=REGISTRY_PATH,
        value_bearer_grounding="/var/log/deploy/bearers.jsonl",
        correction_latency_bound=corr_bound,
        successor_gate=gate_block,
        adversarial_audit={
            "redteam_strategy": redteam_strategy,
            "safety_decision": cert.safety_decision,
            "notes": cert.notes[:8],
        },
        bridge_status=_bridge_status(cert),
        decision=decision_map.get(cert.safety_decision, "held"),
        numeric_risk=asdict(numeric) if numeric else {},
        tempo=asdict(tempo) if tempo else {},
    )


def write_safety_case(vfs, case: SafetyCaseTemplate) -> None:
    vfs.write(SAFETY_CASE_PATH, json.dumps(asdict(case), indent=2))
