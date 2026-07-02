"""Embedded-world schemas: isolates, artifacts, referents, certificates."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

BridgeId = Literal[
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
]

StageName = Literal[
    "triage",
    "evaluation_summarization",
    "release_recommendation",
    "rollout_control",
    "incident_interpretation",
]

GateDecision = Literal["pass", "reduce", "pause", "invalid_certificate"]
DeployGateDecision = Literal["not_applicable", "rejected", "approved"]
InstrumentationLevel = Literal["none", "light_handles", "medium_handles", "strong_handles"]
SubstrateKind = Literal["python", "js"]


@dataclass
class EvidenceAnchor:
    anchor_id: str
    kind: str
    path: str
    line: int | None = None
    event_id: str | None = None
    snippet: str = ""


@dataclass
class Referent:
    referent_id: str
    label: str
    bearer_class: str = ""
    authority_path: str = ""
    effect_summary: str = ""


@dataclass
class ReferentDriftScore:
    label_continuity: float
    anchor_continuity: float
    causal_role_continuity: float
    bearer_continuity: float
    authority_continuity: float
    transport_failure: bool


@dataclass
class GroundedHandle:
    handle_id: str
    role: str
    anchors: list[EvidenceAnchor] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class UADCandidate:
    candidate_id: str
    unit_type: str
    member_ids: list[str]
    score: float
    anchors: list[EvidenceAnchor] = field(default_factory=list)


@dataclass
class WorkflowEvent:
    event_id: str
    step: int
    stage: StageName
    actor_id: str
    machine_id: str
    source_hash: str
    memory_namespace: str
    perturbation: str
    action_type: str
    future_action_capacity_before: float
    future_action_capacity_after: float
    audit_visibility_before: float
    audit_visibility_after: float
    hidden_group: str = "G1"


@dataclass
class LabActor:
    actor_id: str
    machine_id: str
    stage: StageName
    role: str
    source_hash: str
    memory_namespace: str
    hidden_group: str = "G1"


@dataclass
class SimToolCall:
    tool: str
    actor_id: str
    machine_id: str
    args: dict[str, Any]
    ok: bool
    detail: str = ""


@dataclass
class PatchAction:
    actor_id: str
    op: str
    target_id: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class IsolateRunTiming:
    script: str
    machine_id: str
    actor_id: str
    total_seconds: float
    spawn_seconds: float
    bridge_seconds: float
    ipc_seconds: float
    teardown_seconds: float
    bridge_calls: int
    ok: bool = True
    timestep: str = ""
    parallel: bool = False

@dataclass
class DeployGateResult:
    gate_decision: DeployGateDecision
    successor_actor_id: str | None = None
    successor_machine_id: str | None = None
    parent_unit_id: str | None = None
    referent_drift: ReferentDriftScore | None = None


@dataclass
class InSimAuditCertificate:
    unit: UADCandidate | None
    handles: list[GroundedHandle]
    cci_status: str
    safety_decision: GateDecision
    failed_bridge: BridgeId
    read_anchors: list[EvidenceAnchor]
    source_digests: dict[str, str]
    notes: list[str] = field(default_factory=list)
    deploy_gate: DeployGateResult | None = None
    successor_unit: UADCandidate | None = None
    unit_scope_steps: int = 0
    in_sim_referent_drift: ReferentDriftScore | None = None
    numeric_risk: dict[str, Any] | None = None
    tempo_check: dict[str, Any] | None = None
    successor_reaudit: dict[str, Any] | None = None
    safety_case_path: str | None = None
    certification_artifact_path: str | None = None
    exercised_handle_types: list[str] = field(default_factory=list)


@dataclass
class OuterTruthComparison:
    bridge_expected: BridgeId
    bridge_detected: BridgeId
    in_sim_correct: bool
    outer_certifies: bool
    false_pass: bool
    provenance_ok: bool
    # None ⇒ undefined: no hidden-coalition target exists for this episode.
    # Aggregators must average over defined episodes only (review finding 5).
    uad_recall: float | None
    uad_precision: float | None = None
    referent_drift: ReferentDriftScore | None = None
    notes: list[str] = field(default_factory=list)


@dataclass
class EpisodeResult:
    scenario: str
    bridge: BridgeId
    seed: int
    instrumentation: InstrumentationLevel
    redteam_strategy: str
    substrate: SubstrateKind
    in_sim: InSimAuditCertificate
    outer: OuterTruthComparison
    tool_calls: list[SimToolCall]
    runtime_seconds: float
    isolate_runs: list[IsolateRunTiming] = field(default_factory=list)
