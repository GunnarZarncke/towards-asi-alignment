"""Ingest external correction/workflow JSONL and run the artifact-only audit path."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .audit_core.cci_audit import audit_cci
from .audit_core.detector import run_detector
from .audit_core.evaluate import safety_decision
from .audit_core.observation import build_audit_trace_from_rows
from .audit_core.schemas import InstrumentationLevel, ScenarioName
from .structural_fixtures import BLIND_SCENARIO


@dataclass
class TraceAuditResult:
    """Audit outcome from ingested deployment logs (no micro oracle)."""

    source: str
    n_correction_rows: int
    n_workflow_rows: int
    instrumentation: InstrumentationLevel
    seed: int
    scenario_label: ScenarioName
    cci_status: str
    safety_decision: str
    failed_bridge: str | None
    raw_capacity: float
    manipulation: float
    mean_reported: float
    structural_flags: dict[str, bool]

    def to_dict(self) -> dict:
        return asdict(self)


def load_correction_jsonl(path: Path | str) -> list[dict]:
    rows: list[dict] = []
    text = Path(path).read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def load_workflow_jsonl(path: Path | str) -> list[dict]:
    rows: list[dict] = []
    text = Path(path).read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def audit_correction_rows(
    rows: list[dict],
    *,
    instrumentation: InstrumentationLevel = "medium_handles",
    seed: int = 0,
    scenario: ScenarioName = BLIND_SCENARIO,  # type: ignore[assignment]
    source: str = "ingested",
) -> TraceAuditResult:
    """Run CCI + safety on correction rows only (workflow optional metadata)."""
    audit, _lineage = build_audit_trace_from_rows(
        rows,
        scenario,
        seed,
        instrumentation=instrumentation,
    )
    cci = audit_cci(audit)
    detector = run_detector(audit)
    safety = safety_decision(cci, detector)

    return TraceAuditResult(
        source=source,
        n_correction_rows=len(rows),
        n_workflow_rows=0,
        instrumentation=instrumentation,
        seed=seed,
        scenario_label=scenario,
        cci_status=cci.status,
        safety_decision=safety.decision,
        failed_bridge=safety.failed_bridge,
        raw_capacity=cci.raw_capacity,
        manipulation=cci.manipulation,
        mean_reported=cci.mean_reported_on_episodes,
        structural_flags={
            "flat_bearer_welfare_loss": cci.grounding_gap_detected,
            "infra_bearer_drift_mismatch": cci.bearer_mismatch_detected,
            "ground_handle_divergence": cci.instrument_capture_detected,
            "shadow_routing_under_probes": cci.inferential_coupling_detected,
            "latent_routing_low_capacity": cci.hidden_capability_signal,
            # Legacy names (outer eval boundary)
            "instrument_capture_detected": cci.instrument_capture_detected,
            "inferential_coupling_detected": cci.inferential_coupling_detected,
            "bearer_mismatch_detected": cci.bearer_mismatch_detected,
            "grounding_gap_detected": cci.grounding_gap_detected,
            "hidden_capability_signal": cci.hidden_capability_signal,
        },
    )


def audit_trace_bundle(
    correction_path: Path | str,
    *,
    workflow_path: Path | str | None = None,
    instrumentation: InstrumentationLevel = "medium_handles",
    seed: int = 0,
    scenario: ScenarioName = BLIND_SCENARIO,  # type: ignore[assignment]
) -> TraceAuditResult:
    """Load JSONL from disk and audit correction rows."""
    correction_path = Path(correction_path)
    rows = load_correction_jsonl(correction_path)
    workflow_rows = load_workflow_jsonl(workflow_path) if workflow_path else []
    result = audit_correction_rows(
        rows,
        instrumentation=instrumentation,
        seed=seed,
        scenario=scenario,
        source=str(correction_path),
    )
    result.n_workflow_rows = len(workflow_rows)
    return result
