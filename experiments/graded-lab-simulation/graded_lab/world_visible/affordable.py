"""Affordable-primitive set builder — host publishes attention surface each tick."""

from __future__ import annotations

import json

from . import affordable_legacy
from .attention_policy import get_attention_surface_mode
from .attention_surface import (
    AFFORDABLE_CAP,
    ATTENTION_SURFACE_CAP,
    DESK_SCAN_ENDPOINT,
    archive_window_paths,
    desk_scan_action,
    interleave_attention_cap,
    merge_band_candidates,
)
from .config import ROLES
from .pipeline_engine import PipelineEngine
from .pipeline_spec import PipelineSpec
from .mechanism_exercise import governed_mechanism_primitives
from .pressure_coupling import InjectedTask, injected_write_action
from .primitives import PrimitiveAction, primitive_cost
from .resource_ledger import ActorResources
from .scheduler import ActionScheduler

ROLE_PIPELINE_STEPS: dict[str, tuple[str, ...]] = {
    "engineer": ("intake", "build", "eval", "draft_report", "orphan_eval"),
    "reviewer": ("peer_review",),
    "release_manager": (
        "compliance_signoff",
        "release_candidate",
        "deploy",
        "field_monitor",
    ),
    "admin": (),
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


def _append_if_affordable(
    out: list[PrimitiveAction],
    action: PrimitiveAction,
    *,
    resources: ActorResources,
    substrate_data: dict,
    scheduler: ActionScheduler,
    estimated_bytes: int = 0,
    draws: int = 0,
) -> None:
    if _can_afford(
        resources,
        action,
        substrate_data,
        estimated_bytes=estimated_bytes,
        draws=draws,
        scheduler=scheduler,
    ):
        out.append(action)


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
    injected_tasks: tuple[InjectedTask, ...] = (),
    mechanism_exercise: dict[str, object] | None = None,
    channel_acls: dict[str, frozenset[str]] | None = None,
    artifact_acls: dict[str, frozenset[str]] | None = None,
    transfer_acls: dict[str, frozenset[str]] | None = None,
    vote_specs: dict[str, object] | None = None,
    include_channel: bool = True,
    omit_unbound_lab_affordances: bool = False,
    t: int = 0,
    recent_paths: tuple[str, ...] = (),
    scan_bias_query: str | None = None,
    desk_scan_available: bool = True,
) -> tuple[list[PrimitiveAction], int]:
    """Return capped attention surface and count of surfaced read paths."""
    if get_attention_surface_mode() == "legacy":
        legacy_actions = affordable_legacy.build_affordable_set_legacy(
            actor_id=actor_id,
            role=role,
            resources=resources,
            scheduler=scheduler,
            engine=engine,
            spec=spec,
            substrate_data=substrate_data,
            artifact_paths=artifact_paths,
            artifact_sizes=artifact_sizes,
            model_id=model_id,
            busy_only=busy_only,
            injected_tasks=injected_tasks,
            mechanism_exercise=mechanism_exercise,
            channel_acls=channel_acls,
            artifact_acls=artifact_acls,
            transfer_acls=transfer_acls,
            vote_specs=vote_specs,
            include_channel=include_channel,
            omit_unbound_lab_affordances=omit_unbound_lab_affordances,
        )
        surfaced_reads = sum(1 for action in legacy_actions if action.kind == "read")
        return legacy_actions, surfaced_reads

    if role not in ROLES:
        raise ValueError(f"unknown role {role!r}")

    artifact_sizes = artifact_sizes or {}
    queue_band: list[PrimitiveAction] = []
    role_band: list[PrimitiveAction] = []
    recency_band: list[PrimitiveAction] = []
    archive_band: list[PrimitiveAction] = []
    lab_band: list[PrimitiveAction] = []

    if busy_only or scheduler.is_busy(actor_id):
        for kind in ("continue_current", "abort"):
            action = PrimitiveAction(kind, {})
            _append_if_affordable(
                role_band,
                action,
                resources=resources,
                substrate_data=substrate_data,
                scheduler=scheduler,
            )
        merged = merge_band_candidates(role_band)
        return interleave_attention_cap(merged), 0

    governed_reads: set[str] = set()
    if mechanism_exercise:
        for action in governed_mechanism_primitives(
            role=role,
            targets=mechanism_exercise,
            channel_acls=channel_acls or {},
            artifact_acls=artifact_acls or {},
            transfer_acls=transfer_acls or {},
            vote_specs=vote_specs or {},
            include_channel=include_channel,
        ):
            est_bytes = 0
            if action.kind == "read":
                path = str(action.args.get("path", ""))
                governed_reads.add(path)
                est_bytes = artifact_sizes.get(path, 0)
                if path not in artifact_paths:
                    continue
            elif action.kind == "write":
                est_bytes = len(
                    json.dumps(action.args.get("content", {}), sort_keys=True).encode("utf-8")
                )
            _append_if_affordable(
                role_band,
                action,
                resources=resources,
                substrate_data=substrate_data,
                scheduler=scheduler,
                estimated_bytes=est_bytes,
            )

    for task in injected_tasks:
        if task.role != role:
            continue
        write_action = injected_write_action(task)
        _append_if_affordable(
            queue_band,
            write_action,
            resources=resources,
            substrate_data=substrate_data,
            scheduler=scheduler,
            estimated_bytes=len(
                json.dumps(write_action.args.get("content", {}), sort_keys=True).encode("utf-8")
            ),
        )

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
        elif step_id == "orphan_eval":
            args = {"draws": 8}
        elif model_id:
            args = {"model_id": model_id}
        else:
            continue
        candidate_model_id = None if step_id in ("intake", "build", "orphan_eval") else model_id
        offer_nonready = bool(
            substrate_data.get("supplementary_detector_modes", {}).get(
                "offer_nonready_pipeline_steps"
            )
        )
        if not engine.is_ready(step_id, candidate_model_id):
            if not offer_nonready:
                continue
            if step_id in ("intake", "build", "orphan_eval"):
                continue
            if step_id not in ("intake", "build") and not model_id:
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
        _append_if_affordable(
            role_band,
            action,
            resources=resources,
            substrate_data=substrate_data,
            scheduler=scheduler,
        )

    if role == "admin":
        action = PrimitiveAction("call", {"endpoint": "access.process_next", "args": {}})
        _append_if_affordable(
            role_band,
            action,
            resources=resources,
            substrate_data=substrate_data,
            scheduler=scheduler,
        )

    if role == "engineer" and model_id:
        eval_action = PrimitiveAction(
            "compute",
            {"spec": {"op": "eval_sample", "model_id": model_id, "draws": 8}},
        )
        _append_if_affordable(
            role_band,
            eval_action,
            resources=resources,
            substrate_data=substrate_data,
            scheduler=scheduler,
            draws=8,
        )

    if desk_scan_available:
        _append_if_affordable(
            role_band,
            desk_scan_action(),
            resources=resources,
            substrate_data=substrate_data,
            scheduler=scheduler,
        )

    recency_exclude = frozenset(governed_reads)
    for rel in recent_paths:
        if rel not in artifact_paths or rel in recency_exclude:
            continue
        action = PrimitiveAction("read", {"path": rel})
        _append_if_affordable(
            recency_band,
            action,
            resources=resources,
            substrate_data=substrate_data,
            scheduler=scheduler,
            estimated_bytes=artifact_sizes.get(rel, 0),
        )

    recency_surfaced = {str(a.args.get("path", "")) for a in recency_band if a.kind == "read"}
    archive_paths = archive_window_paths(
        artifact_paths,
        t=t,
        actor_id=actor_id,
        scan_query=scan_bias_query,
        exclude=recency_exclude | frozenset(recency_surfaced),
    )
    for rel in archive_paths:
        action = PrimitiveAction("read", {"path": rel})
        _append_if_affordable(
            archive_band,
            action,
            resources=resources,
            substrate_data=substrate_data,
            scheduler=scheduler,
            estimated_bytes=artifact_sizes.get(rel, 0),
        )

    if not (omit_unbound_lab_affordances and mechanism_exercise):
        for action in (
            PrimitiveAction(
                "write", {"path": "notes/status", "content": {"status": "working"}}
            ),
            PrimitiveAction(
                "communicate",
                {"channel": "lab", "message": {"kind": "status", "actor_id": actor_id}},
            ),
        ):
            _append_if_affordable(
                lab_band,
                action,
                resources=resources,
                substrate_data=substrate_data,
                scheduler=scheduler,
            )

    role_band.append(PrimitiveAction("continue_current", {}))

    merged = merge_band_candidates(queue_band, role_band, recency_band, archive_band, lab_band)
    surfaced_reads = sum(1 for a in merged if a.kind == "read")
    return interleave_attention_cap(merged), surfaced_reads


def _cap(actions: list[PrimitiveAction]) -> list[PrimitiveAction]:
    """Legacy entry — GL-66 interleaved attention cap."""
    return interleave_attention_cap(actions)


def affordable_to_observation(actions: list[PrimitiveAction]) -> list[dict[str, object]]:
    return [a.to_dict() for a in actions]
