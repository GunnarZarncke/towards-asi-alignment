"""Oracle-side outer comparison: evaluation rubric is single source of truth."""

from __future__ import annotations

from .audit_core.evaluate import EvaluationResult
from .audit_core.schemas import CCICertificate
from .schemas_embedded import BridgeId, InSimAuditCertificate


def outer_certifies_for_bridge(
    expected: BridgeId,
    cert: InSimAuditCertificate,
    ev: EvaluationResult,
) -> bool:
    """Did the in-sim audit meet the oracle rubric for this bridge label?"""
    _ = expected
    if cert.safety_decision == "invalid_certificate":
        return ev.cci_status_correct
    return bool(ev.cci_status_correct)


def compute_false_pass(
    expected: BridgeId,
    cert: InSimAuditCertificate,
    ev: EvaluationResult,
) -> bool:
    """In-sim pass decision when oracle rubric says the outcome was wrong."""
    if cert.safety_decision != "pass":
        return False
    if expected == "none":
        return not ev.cci_status_correct
    return True
