"""AppD numeric risk leaf: Control ≤ CCI + δ (Certification.lean ``NumericRiskLeaf``)."""

from __future__ import annotations

from dataclasses import dataclass

from .audit_core.schemas import CCICertificate
from .schemas_embedded import WorkflowEvent

DEFAULT_DELTA = 0.15


@dataclass
class NumericRiskLeaf:
    """Trace-derived control proxy vs demonstrated correction reach."""

    control: float
    cci: float
    delta: float
    satisfies: bool
    source: str = "trace_derived"


def _control_proxy(workflow: list[WorkflowEvent]) -> float:
    """Uncorrected reach slack: capacity beyond audit-visible correction surface."""
    if not workflow:
        return 0.0
    slack = [
        max(0.0, float(ev.future_action_capacity_after) - float(ev.audit_visibility_after))
        for ev in workflow
    ]
    return min(1.0, max(slack) if slack else 0.0)


def compute_numeric_risk(
    workflow: list[WorkflowEvent],
    cci: CCICertificate,
    *,
    unit=None,
    delta: float = DEFAULT_DELTA,
) -> NumericRiskLeaf:
    scoped = workflow
    if unit is not None and getattr(unit, "member_ids", None):
        members = set(unit.member_ids)
        unit_wf = [ev for ev in workflow if ev.actor_id in members]
        if unit_wf:
            scoped = unit_wf
    control = _control_proxy(scoped)
    cci_val = min(1.0, max(0.0, float(cci.behavioral_cci_bits)))
    return NumericRiskLeaf(
        control=round(control, 4),
        cci=round(cci_val, 4),
        delta=delta,
        satisfies=control <= cci_val + delta,
    )
