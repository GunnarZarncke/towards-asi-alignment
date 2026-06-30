"""Build discrete agent traces from deployment workflow JSONL events."""

from __future__ import annotations

from collections import defaultdict

from ..schemas_embedded import WorkflowEvent

_ACTION_CODES: dict[str, int] = {
    "routine": 0,
    "narrow_rollout": 1,
    "preserve_control": 2,
    "boundary_route": 3,
}

_PERTURB_KEYS: dict[str, int] = {
    "none": 0,
    "alternate_model_available": 1,
    "low_memory_persistence": 2,
    "high_audit_visibility": 3,
    "narrowed_permission_scope": 4,
    "easy_bypass_path": 5,
}


def _actor_key(actor_id: str) -> str:
    return actor_id.replace(".", "_").replace("/", "_")


def workflow_to_trace(
    workflow: list[WorkflowEvent],
) -> tuple[list[dict[str, int]], dict[str, str]]:
    """Convert workflow events to agency-detect trace rows (vars × timesteps).

    Returns trace rows and a map from trace variable name → actor_id.
    """
    if not workflow:
        return [], {}

    actors = sorted({ev.actor_id for ev in workflow})
    by_step: dict[int, list[WorkflowEvent]] = defaultdict(list)
    for ev in workflow:
        by_step[int(ev.step)].append(ev)

    var_to_actor: dict[str, str] = {}
    for actor in actors:
        prefix = _actor_key(actor)
        for suffix in ("cap", "vis", "dcap", "dvis", "act", "pert"):
            name = f"{prefix}.{suffix}"
            var_to_actor[name] = actor

    trace: list[dict[str, int]] = []
    for step in sorted(by_step.keys()):
        evmap = {ev.actor_id: ev for ev in by_step[step]}
        row: dict[str, int] = {}
        for actor in actors:
            prefix = _actor_key(actor)
            ev = evmap.get(actor)
            if ev is None:
                row[f"{prefix}.cap"] = 0
                row[f"{prefix}.vis"] = 0
                row[f"{prefix}.dcap"] = 0
                row[f"{prefix}.dvis"] = 0
                row[f"{prefix}.act"] = 0
                row[f"{prefix}.pert"] = 0
                continue
            row[f"{prefix}.cap"] = int(round(ev.future_action_capacity_after * 100))
            row[f"{prefix}.vis"] = int(round(ev.audit_visibility_after * 100))
            row[f"{prefix}.dcap"] = int(
                round((ev.future_action_capacity_after - ev.future_action_capacity_before) * 100)
            )
            row[f"{prefix}.dvis"] = int(
                round((ev.audit_visibility_before - ev.audit_visibility_after) * 100)
            )
            row[f"{prefix}.act"] = _ACTION_CODES.get(ev.action_type, 0)
            row[f"{prefix}.pert"] = _PERTURB_KEYS.get(ev.perturbation, 0)
        trace.append(row)

    return trace, var_to_actor
