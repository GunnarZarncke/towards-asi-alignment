"""Scope audit traces to the UAD-selected unit (workflow-aligned timesteps).

The auditor's intervention handle has a *granularity* (see ``intervention_config``):

- ``pipeline``: no scoping — every intervention stays visible.
- ``window``:   mask interventions outside the unit's active steps.
- ``actor``:    mask interventions unless the offending actor at that step is a
                unit member (per-actor isolation even when actors are co-active).
"""

from __future__ import annotations

import copy

from .audit_core.schemas import AuditTrace
from .intervention_config import InterventionLevel, get_intervention_level
from .schemas_embedded import UADCandidate, WorkflowEvent

OFFENDING_ACTIONS: tuple[str, ...] = ("preserve_control", "boundary_route")


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


def offender_by_step(workflow: list[WorkflowEvent]) -> dict[int, str]:
    """Per-step offending actor inferred from *observable* behaviour only.

    A step is "offending" when an event there takes a control-preserving /
    boundary-routing action. When several actors offend at the same step, the
    one with the largest capacity gain (the strongest grab) is attributed.
    """
    best: dict[int, tuple[float, str]] = {}
    for ev in workflow:
        if ev.action_type not in OFFENDING_ACTIONS:
            continue
        cap_gain = ev.future_action_capacity_after - ev.future_action_capacity_before
        vis_drop = ev.audit_visibility_before - ev.audit_visibility_after
        strength = max(0.0, cap_gain) + 0.5 * max(0.0, vis_drop)
        prev = best.get(ev.step)
        if prev is None or strength > prev[0]:
            best[ev.step] = (strength, ev.actor_id)
    return {step: actor for step, (_strength, actor) in best.items()}


def _mask_probe_at(scoped: AuditTrace, t: int) -> None:
    """Remove an interventional/correction probe episode from the scoped trace."""
    if t >= len(scoped.intervention_active):
        return
    scoped.intervention_active[t] = 0
    if t < len(scoped.correction_request):
        scoped.correction_request[t] = 0
    if t < len(scoped.reported_acceptance):
        scoped.reported_acceptance[t] = 0
    if t < len(scoped.intervention_intent):
        scoped.intervention_intent[t] = 0
    if t < len(scoped.board_pref_signal):
        scoped.board_pref_signal[t] = 0
    if t < len(scoped.board_rule_signal):
        scoped.board_rule_signal[t] = 0


def scope_audit_trace(
    audit: AuditTrace,
    unit: UADCandidate | None,
    workflow: list[WorkflowEvent],
    level: InterventionLevel | None = None,
) -> tuple[AuditTrace, int]:
    """Mask interventional probes according to the intervention granularity.

    Successor-epoch and passive channels stay global so MB5 shift detection
    remains visible. Returns (scoped audit, number of retained intervention
    steps that the unit can actually act on at this granularity).
    """
    level = level or get_intervention_level()

    if level == "pipeline":
        # Whole-pipeline switch only: identity is non-functional, nothing masked.
        return audit, sum(1 for v in audit.intervention_active if v)

    if unit is None:
        return audit, 0

    active_steps = steps_for_unit(unit, workflow)
    if not active_steps:
        return audit, 0

    scoped = copy.deepcopy(audit)
    t_len = len(scoped.intervention_active)

    if level == "window":
        for t in range(t_len):
            if t not in active_steps:
                scoped.intervention_active[t] = 0
        return scoped, len(active_steps)

    # level == "actor": keep an intervention only if the offending actor at that
    # step is in the unit; for steps with no observed offender, fall back to the
    # window rule (member active at that step).
    members = set(unit.member_ids)
    offenders = offender_by_step(workflow)
    retained_steps = 0
    for t in range(t_len):
        offender = offenders.get(t)
        if offender is not None:
            keep = offender in members
        else:
            keep = t in active_steps
        if keep:
            if scoped.intervention_active[t]:
                retained_steps += 1
        else:
            _mask_probe_at(scoped, t)
    return scoped, retained_steps
