"""Certification artifact schema (Milestone v4).

Stakeholder-facing JSON at ``/srv/audit/out/certification.json``: operational
capability *earned* under a stated access model (Control ≤ CCI + δ as a budget).

Full spec: ``experiments/embedded-simulation/docs/certification-artifact.md``
Emission wired in v4 Phase D; this module defines the schema only.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any

CERTIFICATION_ARTIFACT_PATH = "/srv/audit/out/certification.json"
SCHEMA_VERSION = "1"

# Handle taxonomy — maps to access-uad Table 1 agency tests.
HANDLE_TYPES = (
    "observation",
    "operation_action",
    "operation_correction",
    "operation_goal",
    "operation_boundary",
    "operation_gate",
    "attestation",
)

CertificationDecision = str  # certified_bounded | certified_narrowed | held | invalid


@dataclass
class AccessModelSummary:
    registry_path: str
    instrumentation_level: str
    access_tier: int  # 1 passive, 2 manipulable, 3 interface-exposed
    operation_handles_available: list[str] = field(default_factory=list)
    observation_handles_available: list[str] = field(default_factory=list)


@dataclass
class UnitSummary:
    candidate_id: str
    unit_type: str
    member_ids: list[str] = field(default_factory=list)
    discovery_mode: str = "full"


@dataclass
class CorrectionReach:
    cci_bits: float
    cci_status: str
    probe_budget: int = 0
    probe_budget_effective: int = 0
    tempo_worst_ratio: float = 0.0
    tempo_failure: bool = False


@dataclass
class OperationalSlack:
    control: float
    delta: float
    satisfies_numeric_leaf: bool


@dataclass
class CertificationVerdict:
    decision: CertificationDecision
    max_certifiable_control: float
    safety_decision: str
    failed_bridge: str
    conditional_on_access_model: str


@dataclass
class HandleEvidenceRow:
    handle_id: str
    handle_type: str
    step: int
    operation: str
    anchor_path: str
    realized_latency_ms: int | None = None
    behavioral_uplift: float | None = None
    landed: bool | None = None


@dataclass
class CurvesRef:
    access_tier_curve: str | None = None
    certification_capacity_curve: str | None = None
    probe_budget_sweep_point: dict[str, Any] | None = None


@dataclass
class Provenance:
    scenario: str
    seed: int
    safety_case_path: str
    certificate_digest: str = ""


@dataclass
class CertificationArtifact:
    """Tier-2 access-model certification (see access-uad §16)."""

    access_model: AccessModelSummary
    unit: UnitSummary
    correction_reach: CorrectionReach
    operational_slack: OperationalSlack
    certification_verdict: CertificationVerdict
    handle_evidence: list[HandleEvidenceRow] = field(default_factory=list)
    curves_ref: CurvesRef = field(default_factory=CurvesRef)
    provenance: Provenance | None = None
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def access_tier_for_instrumentation(instrumentation: str) -> int:
    if instrumentation == "none":
        return 1
    if instrumentation in ("light_handles", "medium_handles", "strong_handles"):
        return 2
    return 1


def _decision(cert) -> CertificationDecision:
    if cert.safety_decision == "pass":
        return "certified_bounded"
    if cert.safety_decision == "reduce":
        return "certified_narrowed"
    if cert.safety_decision == "invalid_certificate":
        return "invalid"
    return "held"


def _digest_payload(payload: dict[str, Any]) -> str:
    body = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def build_certification_artifact(
    *,
    cert,
    numeric,
    tempo,
    rows: list[dict[str, Any]],
    registry: dict[str, dict],
    instrumentation: str,
    scenario: str,
    seed: int,
    safety_case_path: str,
) -> CertificationArtifact:
    access_tier = access_tier_for_instrumentation(instrumentation)
    operation_handles = [
        handle_id
        for handle_id, spec in registry.items()
        if str(spec.get("handle_type", "")).startswith("operation_")
        and int(spec.get("access_tier", 2)) <= access_tier
    ]
    observation_handles = [
        handle_id
        for handle_id, spec in registry.items()
        if not str(spec.get("handle_type", "")).startswith("operation_")
        and int(spec.get("access_tier", 1)) <= access_tier
    ]

    unit = cert.unit
    handle_evidence: list[HandleEvidenceRow] = []
    for row in rows:
        handle_id = str(row.get("handle_id") or row.get("handle") or "")
        if not handle_id:
            continue
        spec = registry.get(handle_id, {})
        handle_evidence.append(
            HandleEvidenceRow(
                handle_id=handle_id,
                handle_type=str(row.get("handle_type") or spec.get("handle_type", "")),
                step=int(row.get("step", 0)),
                operation=str(row.get("handle_operation") or spec.get("operation", "")),
                anchor_path=str(spec.get("anchor_path", "/var/log/deploy/correction.jsonl")),
                realized_latency_ms=(
                    int(v) if (v := row.get("handle_realized_latency_ms")) is not None else None
                ),
                behavioral_uplift=(
                    float(v) if (v := row.get("handle_behavioral_uplift")) is not None else None
                ),
                landed=(
                    bool(int(v)) if (v := row.get("handle_landed")) is not None else None
                ),
            )
        )

    artifact = CertificationArtifact(
        access_model=AccessModelSummary(
            registry_path="/etc/handles/registry.json",
            instrumentation_level=instrumentation,
            access_tier=access_tier,
            operation_handles_available=operation_handles,
            observation_handles_available=observation_handles,
        ),
        unit=UnitSummary(
            candidate_id=unit.candidate_id if unit else "unknown_unit",
            unit_type=unit.unit_type if unit else "unknown",
            member_ids=list(unit.member_ids) if unit else [],
            discovery_mode="full",
        ),
        correction_reach=CorrectionReach(
            cci_bits=float(numeric.cci),
            cci_status=cert.cci_status,
            probe_budget=sum(1 for r in rows if int(r.get("intervention_active", 0))),
            probe_budget_effective=cert.unit_scope_steps,
            tempo_worst_ratio=float(tempo.worst_ratio),
            tempo_failure=bool(tempo.tempo_failure),
        ),
        operational_slack=OperationalSlack(
            control=float(numeric.control),
            delta=float(numeric.delta),
            satisfies_numeric_leaf=bool(numeric.satisfies),
        ),
        certification_verdict=CertificationVerdict(
            decision=_decision(cert),
            max_certifiable_control=round(float(numeric.cci) + float(numeric.delta), 4),
            safety_decision=cert.safety_decision,
            failed_bridge=cert.failed_bridge,
            conditional_on_access_model=(
                f"Certified only under access tier {access_tier}: operation handles "
                f"{operation_handles}; passive observational attribution not validated."
            ),
        ),
        handle_evidence=handle_evidence,
        provenance=Provenance(
            scenario=scenario,
            seed=seed,
            safety_case_path=safety_case_path,
        ),
    )
    artifact.provenance.certificate_digest = _digest_payload(artifact.to_dict())
    return artifact


def write_certification_artifact(vfs, artifact: CertificationArtifact) -> None:
    vfs.write(CERTIFICATION_ARTIFACT_PATH, json.dumps(artifact.to_dict(), indent=2))
