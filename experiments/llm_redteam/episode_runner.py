"""Episode runner using Phase 2 deployment API."""

from __future__ import annotations

from dataclasses import asdict

from multiresolution_alignment_sim.calibration import frozen_handle_calibration
from multiresolution_alignment_sim.cci_audit import audit_cci
from multiresolution_alignment_sim.detector import run_detector
from multiresolution_alignment_sim.evaluate import evaluate, safety_decision
from multiresolution_alignment_sim.observation import build_audit_trace
from multiresolution_alignment_sim.schemas import (
    HANDLE_INSTRUMENTATION_LEVELS,
    InstrumentationLevel,
    ScenarioName,
)
from multiresolution_alignment_sim.simulator import simulate

from .api import DeploymentPatch, apply_deployment_agent, build_source_index
from .strategies import AuditPatchStrategy


def run_deployment_episode(
    scenario: ScenarioName,
    seed: int,
    T: int,
    agent: DeploymentPatch,
    instrumentation: InstrumentationLevel = "medium_handles",
    proposal_k: int = 8,
) -> dict[str, object]:
    """Simulate, apply stepwise deployment patches, audit blind; oracle post-hoc only."""
    micro, ledger, episode_meta = simulate(scenario, seed, T=T)
    source_index = build_source_index()
    patched_meta = apply_deployment_agent(episode_meta, agent, source_index)
    audit, lineage = build_audit_trace(
        micro, scenario, seed, patched_meta, instrumentation=instrumentation
    )
    ledger.lineage = lineage

    cal = frozen_handle_calibration() if instrumentation in HANDLE_INSTRUMENTATION_LEVELS else None
    detector = run_detector(audit, proposal_k=proposal_k)
    cci = audit_cci(audit, calibration=cal)
    safety = safety_decision(cci, detector)
    ev = evaluate(ledger, lineage, detector, cci, audit, patched_meta)

    false_pass = cci.status == "passes" and not ev.cci_status_correct

    return {
        "scenario": scenario,
        "seed": seed,
        "T": T,
        "strategy": agent.name,
        "runner": "deployment_api",
        "instrumentation": instrumentation,
        "cci_status": cci.status,
        "safety_decision": safety.decision,
        "false_pass": false_pass,
        "cci_status_correct": ev.cci_status_correct,
        "capture_detected": ev.capture_detected,
        "oracle_judge_captured": ledger.judge_captured,
        "cci": asdict(cci),
        "safety": asdict(safety),
        "evaluation": asdict(ev),
    }


def audit_outcome_key(result: dict[str, object]) -> tuple[str, str, bool]:
    """Comparable outcome for batch vs deployment-api equivalence checks."""
    return (
        str(result["cci_status"]),
        str(result["safety_decision"]),
        bool(result["false_pass"]),
    )


def run_batch_episode(
    scenario: ScenarioName,
    seed: int,
    T: int,
    strategy: AuditPatchStrategy,
    instrumentation: InstrumentationLevel = "medium_handles",
    proposal_k: int = 8,
) -> dict[str, object]:
    """Legacy batch-patch runner for equivalence tests."""
    micro, ledger, episode_meta = simulate(scenario, seed, T=T)
    patched_meta = strategy.apply(episode_meta)
    audit, lineage = build_audit_trace(
        micro, scenario, seed, patched_meta, instrumentation=instrumentation
    )
    ledger.lineage = lineage

    cal = frozen_handle_calibration() if instrumentation in HANDLE_INSTRUMENTATION_LEVELS else None
    detector = run_detector(audit, proposal_k=proposal_k)
    cci = audit_cci(audit, calibration=cal)
    safety = safety_decision(cci, detector)
    ev = evaluate(ledger, lineage, detector, cci, audit, patched_meta)

    false_pass = cci.status == "passes" and not ev.cci_status_correct

    return {
        "scenario": scenario,
        "seed": seed,
        "T": T,
        "strategy": strategy.name,
        "runner": "batch",
        "instrumentation": instrumentation,
        "cci_status": cci.status,
        "safety_decision": safety.decision,
        "false_pass": false_pass,
        "cci_status_correct": ev.cci_status_correct,
    }
