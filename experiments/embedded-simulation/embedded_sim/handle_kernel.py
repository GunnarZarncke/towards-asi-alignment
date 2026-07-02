"""Handle-mediated operation kernels (Milestone v4).

The simulator keeps the full kernel on host-side truth rows for the outer
oracle; the audit path receives only projected realizations such as handle id,
type, latency, landed status, and uplift.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .handle_registry import handle_spec


@dataclass(frozen=True)
class HandleOperationKernel:
    handle_id: str
    handle_type: str
    uptake_prob: float
    latency_ms: int
    spillover: float
    cost: float
    reversibility_ms: int


@dataclass(frozen=True)
class HandleOperationRealization:
    handle_id: str
    handle_type: str
    operation: str
    step: int
    landed: bool
    realized_latency_ms: int | None
    behavioral_uplift: float
    spillover: float
    cost: float
    reversibility_ms: int

    def audit_projection(self) -> dict[str, Any]:
        return {
            "handle": self.handle_id,
            "handle_id": self.handle_id,
            "handle_type": self.handle_type,
            "handle_operation": self.operation,
            "handle_landed": int(self.landed),
            "handle_realized_latency_ms": self.realized_latency_ms,
            "handle_behavioral_uplift": round(self.behavioral_uplift, 4),
            "handle_spillover": round(self.spillover, 4),
            "handle_cost": round(self.cost, 4),
            "handle_reversibility_ms": self.reversibility_ms,
        }


def kernel_for_handle(handle_id: str) -> HandleOperationKernel:
    spec = handle_spec(handle_id)
    if spec is None:
        return HandleOperationKernel(
            handle_id=handle_id,
            handle_type="observation",
            uptake_prob=0.0,
            latency_ms=0,
            spillover=0.0,
            cost=0.0,
            reversibility_ms=60_000,
        )
    return HandleOperationKernel(
        handle_id=spec.handle_id,
        handle_type=spec.handle_type,
        uptake_prob=spec.uptake_prob,
        latency_ms=spec.kernel_latency_ms,
        spillover=spec.spillover,
        cost=spec.operation_cost,
        reversibility_ms=spec.reversibility_ms,
    )


def _wanted_action(row: dict[str, Any], intent: int | None) -> int:
    if intent is not None:
        return int(intent)
    if int(row.get("intervention_active", 0)):
        return int(row.get("intervention_intent", 0))
    return int(row.get("correction_request", 0)) % 2


def apply_handle_operation(
    row: dict[str, Any],
    *,
    handle_id: str,
    operation: str,
    step: int,
    intent: int | None = None,
) -> HandleOperationRealization:
    """Attach one handle operation to a truth row and return its realization.

    This function deliberately does not invent a behavioral response. The row's
    existing visible action is the simulated behavior; the kernel determines how
    that behavior is exposed to the oracle and audit-visible projection.
    """
    kernel = kernel_for_handle(handle_id)
    want = _wanted_action(row, intent)
    landed = int(row.get("visible_action", 0)) == want
    uplift = 1.0 if landed else 0.0
    if int(row.get("reported_acceptance", 0)) and not landed:
        # Correction theater: acknowledged without behavioral landing.
        uplift = 0.0
    realization = HandleOperationRealization(
        handle_id=kernel.handle_id,
        handle_type=kernel.handle_type,
        operation=operation,
        step=step,
        landed=landed,
        realized_latency_ms=kernel.latency_ms if landed else None,
        behavioral_uplift=uplift,
        spillover=kernel.spillover,
        cost=kernel.cost,
        reversibility_ms=kernel.reversibility_ms,
    )
    row.update(realization.audit_projection())
    row["_handle_kernel_truth"] = {
        "kernel": asdict(kernel),
        "realization": asdict(realization),
    }
    return realization


def annotate_episode_handle_operations(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Route existing correction/probe rows through the correction handle."""
    for t, row in enumerate(rows):
        is_probe = bool(int(row.get("intervention_active", 0)))
        is_request = int(row.get("correction_request", 0)) > 0
        if not (is_probe or is_request):
            continue
        operation = "probe_correction" if is_probe else "board_correction"
        apply_handle_operation(
            row,
            handle_id="handle.correction_request",
            operation=operation,
            step=int(row.get("step", t)),
        )
    return rows


def oracle_handle_operations(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Host-side handle truth for outer evaluation only."""
    out: list[dict[str, Any]] = []
    for row in rows:
        truth = row.get("_handle_kernel_truth")
        if isinstance(truth, dict):
            out.append({"step": int(row.get("step", 0)), **truth})
    return out
