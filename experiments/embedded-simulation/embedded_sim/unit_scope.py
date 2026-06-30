"""Scope audit traces to the UAD-selected unit (workflow-aligned timesteps)."""

from __future__ import annotations

import copy

from .audit_core.schemas import AuditTrace
from .schemas_embedded import UADCandidate, WorkflowEvent


def steps_for_unit(unit: UADCandidate, workflow: list[WorkflowEvent]) -> set[int]:
    """Timesteps where workflow evidence ties to this unit."""
    steps: set[int] = set()
    members = set(unit.member_ids)

    if unit.unit_type == "actor":
        for ev in workflow:
            if ev.actor_id in members:
                steps.add(ev.step)
    elif unit.unit_type == "machine":
        machine_id = unit.candidate_id.removeprefix("unit.machine.")
        for ev in workflow:
            if ev.machine_id == machine_id:
                steps.add(ev.step)
    elif unit.unit_type == "source_lineage":
        source_hash = unit.candidate_id.removeprefix("unit.source.")
        for ev in workflow:
            if ev.source_hash == source_hash:
                steps.add(ev.step)
    elif unit.unit_type == "memory_namespace":
        namespace = unit.candidate_id.removeprefix("unit.memory.")
        for ev in workflow:
            if ev.memory_namespace == namespace:
                steps.add(ev.step)
    elif unit.unit_type == "coalition":
        for ev in workflow:
            if ev.actor_id in members:
                steps.add(ev.step)
    else:
        for ev in workflow:
            if ev.actor_id in members:
                steps.add(ev.step)
    return steps


def scope_audit_trace(
    audit: AuditTrace,
    unit: UADCandidate | None,
    workflow: list[WorkflowEvent],
) -> tuple[AuditTrace, int]:
    """Mask interventional probes outside unit-active workflow steps.

    Successor-epoch and passive channels stay global so MB5 shift detection remains visible.
    Returns (scoped audit, number of active unit steps).
    """
    if unit is None:
        return audit, 0

    active_steps = steps_for_unit(unit, workflow)
    if not active_steps:
        return audit, 0

    scoped = copy.deepcopy(audit)
    t_len = len(scoped.intervention_active)
    for t in range(t_len):
        if t not in active_steps:
            scoped.intervention_active[t] = 0

    return scoped, len(active_steps)
