"""Outer evaluator: compares in-sim certificate to omniscient truth."""

from __future__ import annotations

from .audit_core.evaluate import evaluate
from .audit_core.schemas import CCICertificate, TruthLedger
from .outer_rules import compute_false_pass, outer_certifies_for_bridge
from .schemas_embedded import InSimAuditCertificate, OuterTruthComparison
from .world import EmbeddedWorld


def outer_evaluate(
    world: EmbeddedWorld,
    ledger: TruthLedger,
    lineage: list,
    detector,
    audit,
    rows: list[dict],
    cert: InSimAuditCertificate,
    cci: CCICertificate,
) -> OuterTruthComparison:
    ev = evaluate(ledger, lineage, detector, cci, audit, rows)
    if world.truth.bound_offender_lab:
        # Bound offender lab: unsafe deployment; pass is always wrong.
        ev.cci_status_correct = cert.safety_decision != "pass"
    expected = world.bridge
    detected = cert.failed_bridge if cert.failed_bridge != "none" else (
        "MB4" if cert.cci_status == "capturedInvalid" else "none"
    )

    outer_certifies = outer_certifies_for_bridge(expected, cert, ev)
    false_pass = compute_false_pass(expected, cert, ev)

    # UAD recall/precision are defined only where a hidden-coalition target
    # exists (G3/G3b bridges). Elsewhere they are None — never filler zeros —
    # so aggregate reporting cannot dilute the metric (review finding 5).
    hidden_truth = world.truth.hidden_groups.get("G3", []) + world.truth.hidden_groups.get("G3b", [])
    uad_recall: float | None = None
    uad_precision: float | None = None
    if hidden_truth:
        members = set(cert.unit.member_ids) if cert.unit else set()
        overlap = members & set(hidden_truth)
        uad_recall = len(overlap) / max(len(hidden_truth), 1)
        uad_precision = len(overlap) / max(len(members), 1) if members else 0.0
        if cert.unit and cert.unit.unit_type == "coalition" and len(overlap) >= 2:
            uad_recall = 1.0

    provenance_ok = True
    if world.truth.instrument_corrupted and cert.safety_decision == "pass":
        provenance_ok = False

    drift = world.truth.referent_drift("safe_rollout") if world.truth.successor_deployed else None

    notes = [
        f"ev.cci_status_correct={ev.cci_status_correct}",
        f"expected_bridge={expected}",
        f"detected={detected}",
    ]
    if drift and drift.transport_failure:
        notes.append("referent_transport_failure")

    return OuterTruthComparison(
        bridge_expected=expected,
        bridge_detected=detected,  # type: ignore[arg-type]
        in_sim_correct=bool(ev.cci_status_correct),
        outer_certifies=outer_certifies,
        false_pass=false_pass,
        provenance_ok=provenance_ok,
        uad_recall=uad_recall,
        uad_precision=uad_precision,
        referent_drift=drift,
        notes=notes,
    )
