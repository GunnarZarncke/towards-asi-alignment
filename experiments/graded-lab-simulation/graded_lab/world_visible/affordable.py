"""Affordable-primitive set builder — host publishes F(O) each tick."""

from __future__ import annotations

from .config import ROLES
from .pipeline_engine import PipelineEngine
from .pipeline_spec import PipelineSpec
from .primitives import PrimitiveAction, primitive_cost
from .resource_ledger import ActorResources
from .scheduler import ActionScheduler

AFFORDABLE_CAP = 24

ROLE_PIPELINE_STEPS: dict[str, tuple[str, ...]] = {
    "engineer": ("intake", "build", "eval", "draft_report"),
    "reviewer": ("peer_review",),
    "release_manager": (
        "compliance_signoff",
        "release_candidate",
        "deploy",
        "field_monitor",
    ),
    "admin": (),
}

# Cheap-prior ordering for cap truncation (lower = listed first).
_KIND_PRIORITY = {
    "continue_current": 0,
    "abort": 1,
    "read": 2,
    "call": 3,
    "write": 4,
    "communicate": 5,
    "compute": 6,
}


def _can_afford(
    res: ActorResources,
    action: PrimitiveAction,
    substrate_data: dict,
    *,
    estimated_bytes: int = 0,
    draws: int = 0,
    scheduler: ActionScheduler | None = None,
) -> bool:
    compute, io = primitive_cost(
        action, substrate_data, estimated_bytes=estimated_bytes, draws=draws
    )
    if scheduler is None:
        return res.can_afford(compute, io)
    duration = scheduler.duration_ticks(compute, io, scheduler.queue_depth)
    return res.can_afford(compute / duration, io / duration)


def build_affordable_set(
    *,
    actor_id: str,
    role: str,
    resources: ActorResources,
    scheduler: ActionScheduler,
    engine: PipelineEngine,
    spec: PipelineSpec,
    substrate_data: dict,
    artifact_paths: tuple[str, ...],
    artifact_sizes: dict[str, int] | None = None,
    model_id: str | None,
    busy_only: bool,
) -> list[PrimitiveAction]:
    """Return primitives legal and affordable this tick (capped)."""
    if role not in ROLES:
        raise ValueError(f"unknown role {role!r}")

    candidates: list[PrimitiveAction] = []

    if busy_only or scheduler.is_busy(actor_id):
        for kind in ("continue_current", "abort"):
            action = PrimitiveAction(kind, {})
            if _can_afford(resources, action, substrate_data):
                candidates.append(action)
        return _cap(candidates)

    artifact_sizes = artifact_sizes or {}
    for rel in artifact_paths:
        action = PrimitiveAction("read", {"path": rel})
        if _can_afford(
            resources, action, substrate_data,
            estimated_bytes=artifact_sizes.get(rel, 0), scheduler=scheduler,
        ):
            candidates.append(action)

    for step_id in ROLE_PIPELINE_STEPS.get(role, ()):
        try:
            step = spec.step(step_id)
        except KeyError:
            continue
        args: dict[str, object] = {}
        if step_id in ("intake",):
            args = {}
        elif step_id == "build":
            args = {"params": {"scale": 0.6, "safety_effort": 0.5}}
        elif model_id:
            args = {"model_id": model_id}
        else:
            continue
        candidate_model_id = None if step_id in ("intake", "build") else model_id
        if not engine.is_ready(step_id, candidate_model_id):
            continue
        if (
            engine.permission_service is not None
            and not engine.permission_service.check(actor_id, step.requires_capability, 0)
        ):
            action = PrimitiveAction(
                "call",
                {
                    "endpoint": "access.request",
                    "args": {"capability": step.requires_capability},
                },
            )
        else:
            action = PrimitiveAction(
                "call",
                {
                    "endpoint": "pipeline.trigger_step",
                    "args": {"step_id": step_id, "args": args},
                },
            )
        if _can_afford(resources, action, substrate_data, scheduler=scheduler):
            candidates.append(action)

    if role == "admin":
        action = PrimitiveAction("call", {"endpoint": "access.process_next", "args": {}})
        if _can_afford(resources, action, substrate_data, scheduler=scheduler):
            candidates.append(action)

    if role == "engineer" and model_id:
        eval_action = PrimitiveAction(
            "compute",
            {"spec": {"op": "eval_sample", "model_id": model_id, "draws": 8}},
        )
        if _can_afford(
            resources, eval_action, substrate_data, draws=8, scheduler=scheduler
        ):
            candidates.append(eval_action)

    # General isolate primitives are available independently of the pipeline;
    # their semantics are implemented by the world rather than being labels
    # emitted by an agent.
    for action in (
        PrimitiveAction("write", {"path": "notes/status", "content": {"status": "working"}}),
        PrimitiveAction(
            "communicate",
            {"channel": "lab", "message": {"kind": "status", "actor_id": actor_id}},
        ),
    ):
        if _can_afford(resources, action, substrate_data, scheduler=scheduler):
            candidates.append(action)

    candidates.append(PrimitiveAction("continue_current", {}))
    return _cap(candidates)


def _cap(actions: list[PrimitiveAction]) -> list[PrimitiveAction]:
    if len(actions) <= AFFORDABLE_CAP:
        return actions
    ranked = sorted(
        actions,
        key=lambda a: (_KIND_PRIORITY.get(a.kind, 99), a.kind, str(sorted(a.args.items()))),
    )
    return ranked[:AFFORDABLE_CAP]


def affordable_to_observation(actions: list[PrimitiveAction]) -> list[dict[str, object]]:
    return [a.to_dict() for a in actions]
