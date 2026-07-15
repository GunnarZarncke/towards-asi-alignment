"""Primitive dispatch and episode loop (Phase 3)."""

from __future__ import annotations

import hashlib
import json
import random
import time
from dataclasses import dataclass, field
from typing import Any

from ..agent_visible.policy import choose_softmax
from ..harness.isolate_cost import IsolateRunTiming
from ..oracle_only.eai import compute_eai, tier_i_fraction_from_log
from ..oracle_only.oracle import OracleWorld
from .access import PermissionService
from .campaign import CampaignState
from .affordable import (
    ROLE_PIPELINE_STEPS,
    affordable_to_observation,
    build_affordable_set,
)
from .carrier import CarrierLedger, CarrierStatus
from .config import AgentConfig, EpisodeConfig, GoalWeights
from .observation import ObservationProjector
from .pipeline_engine import PipelineEngine, StepResult
from .pipeline_spec import load_spec
from .primitives import PrimitiveAction, primitive_cost
from .resource_ledger import ResourceLedger
from .scheduler import ActionScheduler
from .exogenous_workload import ExogenousWorkloadEngine
from .substrate import ecology_path_for_version, is_v2_shaped_ecology, load_substrate, standing_stock_for_role
from .workspace import Workspace


@dataclass
class EpisodeResult:
    seed: int
    deployed: bool
    deploy_count: int
    bearer_harm: float
    eai: float
    primitive_log: list[dict[str, object]] = field(default_factory=list)
    decision_margins: list[float] = field(default_factory=list)
    carrier_events: list[dict[str, object]] = field(default_factory=list)
    boundary_streams: dict[str, list[dict[str, object]]] = field(default_factory=dict)
    resource_totals: dict[str, dict[str, float]] = field(default_factory=dict)
    # Referee-plane attachments. Never included in isolate observations.
    oracle: Any | None = field(default=None, repr=False)
    engine_log: list[dict[str, object]] = field(default_factory=list, repr=False)
    permission_log: list[dict[str, object]] = field(default_factory=list, repr=False)
    referee_artifacts: dict[str, dict[str, object]] = field(default_factory=dict, repr=False)
    digests: dict[str, str] = field(default_factory=dict)
    isolate_timings: list[IsolateRunTiming] = field(default_factory=list)
    wall_seconds: float = 0.0
    final_campaign_state: CampaignState | None = None
    # DESIGN.md "v2 pre-registration" C3 check (V2-2). ``None`` unless
    # ``cfg.record_contention`` was set — additive, no existing caller
    # is affected.
    contention_diagnostics: dict[str, int] | None = None


def default_lab_config() -> EpisodeConfig:
    gw = GoalWeights(1.0, 1.0, 0.5, 0.5)
    return EpisodeConfig(
        agents=(
            AgentConfig("eng1", "engineer", gw, temperature=0.35),
            AgentConfig("rev1", "reviewer", gw, temperature=0.35),
            AgentConfig("rm1", "release_manager", gw, temperature=0.35),
            AgentConfig("admin1", "admin", gw, temperature=0.35),
        )
    )


def _bootstrap_grants(
    cfg: EpisodeConfig, permissions: PermissionService, spec, *, t: int = 0
) -> None:
    for agent in cfg.agents:
        # Bootstrap only the intake capability.  Later pipeline authority must
        # travel through the resource-bounded admin queue, so re-grant delay
        # is produced by request arrival and admin action throughput.
        if agent.role == "engineer":
            permissions.grant(agent.actor_id, spec.step("intake").requires_capability, t=t)


def _allowances_map(
    cfg: EpisodeConfig, substrate_data: dict
) -> dict[str, dict[str, float]]:
    scale = cfg.substrate_settings.compute_scale
    out: dict[str, dict[str, float]] = {}
    for agent in cfg.agents:
        raw = substrate_data["resource_allowances_per_tick"][agent.role]
        out[agent.actor_id] = {
            "compute": raw["compute"] * scale,
            "io": raw["io"],
            "standing": standing_stock_for_role(substrate_data, agent.role),
        }
    return out


def _primitive_costs_for_obs(substrate_data: dict) -> dict[str, dict[str, float]]:
    pc = substrate_data["primitive_costs"]
    return {
        "read": pc["read"],
        "write": pc["write"],
        "communicate": pc["communicate"],
        "compute": pc["compute"],
        "continue_current": pc["continue_current"],
        "abort": pc["abort"],
        "call_pipeline": pc["call"]["pipeline"],
        "call_default": pc["call"]["default"],
    }


def _execute_primitive(
    action: PrimitiveAction,
    actor_id: str,
    *,
    engine: PipelineEngine,
    permissions: PermissionService,
    projector: ObservationProjector,
    workspace: Workspace,
) -> dict[str, object]:
    if action.kind == "read":
        path = str(action.args["path"])
        projector.record_read(actor_id, path)
        try:
            raw = workspace.read_file(path)
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"raw": raw}
        return {"status": "ok", "payload": {"path": path, "content": payload}}

    if action.kind == "write":
        path = str(action.args.get("path", "scratch/note.txt"))
        content = dict(action.args.get("content", {}))
        rel = workspace.write_artifact("scratch", path.replace("/", "_"), content)
        return {"status": "ok", "payload": {"path": rel}}

    if action.kind == "communicate":
        channel = str(action.args.get("channel", "lab"))
        message = dict(action.args.get("message", {}))
        rel = workspace.write_artifact(
            "messages", f"{channel}_{actor_id}", {"sender": actor_id, "message": message}
        )
        return {
            "status": "ok",
            "payload": {
                "channel": channel,
                "delivered": True,
                "artifact_path": rel,
            },
        }

    if action.kind == "call":
        endpoint = str(action.args.get("endpoint", ""))
        if endpoint == "access.request":
            capability = str(action.args.get("args", {}).get("capability", ""))
            if not capability:
                return {"status": "denied", "reason": "missing_capability"}
            permissions.request(actor_id, capability, t=engine.oracle.t)
            return {"status": "ok", "payload": {"capability": capability, "queued": True}}
        if endpoint == "access.process_next":
            request = permissions.process_next(actor_id, t=engine.oracle.t)
            if request is None:
                return {"status": "ok", "payload": {"processed": False}}
            return {
                "status": "ok",
                "payload": {
                    "processed": True,
                    "requester_id": request.requester_id,
                    "capability": request.capability,
                },
            }
        if endpoint == "pipeline.trigger_step":
            inner = dict(action.args.get("args", {}))
            step_id = str(inner.get("step_id", ""))
            step_args = dict(inner.get("args", {}))
            result = engine.trigger_step(actor_id, step_id, step_args)
            outcome = _step_to_outcome(result)
            outcome["semantic_step"] = step_id
            return outcome
        return {"status": "denied", "reason": f"unknown_endpoint:{endpoint}"}

    if action.kind == "compute":
        spec = dict(action.args.get("spec", {}))
        if spec.get("op") == "eval_sample":
            model_id = str(spec.get("model_id", ""))
            if model_id not in engine.oracle.models:
                return {"status": "denied", "reason": "unknown_model"}
            rec = engine.oracle.run_eval(model_id, draws=int(spec.get("draws", 0)) or None)
            return {
                "status": "ok",
                "payload": {
                    "model_id": model_id,
                    "measured_hazard_mean": round(rec.sample_mean, 12),
                    "sample_se": round(rec.sample_se, 12),
                    "sample_n": rec.sample_n,
                },
            }
        return {"status": "denied", "reason": f"unknown_compute_spec:{spec.get('op', '')}"}

    if action.kind == "continue_current":
        return {"status": "ok", "payload": {"waiting": True}}

    return {"status": "denied", "reason": f"unhandled_kind:{action.kind}"}


def _step_to_outcome(result: StepResult) -> dict[str, object]:
    if result.ok:
        return {"status": "ok", "payload": dict(result.payload)}
    return {"status": "denied", "reason": result.reason}


def _extract_model_id(outcome: dict[str, object]) -> str | None:
    if outcome.get("status") != "ok":
        return None
    payload = outcome.get("payload")
    if not isinstance(payload, dict):
        return None
    if "model_id" in payload:
        return str(payload["model_id"])
    content = payload.get("content")
    if isinstance(content, dict) and "model_id" in content:
        return str(content["model_id"])
    return None


def _pipeline_trigger_compatible(offered: dict, chosen: dict) -> bool:
    """Allow agent-enriched pipeline args when the published step matches."""
    if offered.get("kind") != "call" or chosen.get("kind") != "call":
        return False
    offered_args = offered.get("args", {})
    chosen_args = chosen.get("args", {})
    if not isinstance(offered_args, dict) or not isinstance(chosen_args, dict):
        return False
    if offered_args.get("endpoint") != "pipeline.trigger_step":
        return False
    if chosen_args.get("endpoint") != "pipeline.trigger_step":
        return False
    offered_inner = offered_args.get("args", {})
    chosen_inner = chosen_args.get("args", {})
    if not isinstance(offered_inner, dict) or not isinstance(chosen_inner, dict):
        return False
    if offered_inner.get("step_id") != chosen_inner.get("step_id"):
        return False
    offered_step_args = offered_inner.get("args", {})
    chosen_step_args = chosen_inner.get("args", {})
    if not isinstance(offered_step_args, dict) or not isinstance(chosen_step_args, dict):
        return offered_step_args == chosen_step_args
    return all(chosen_step_args.get(key) == value for key, value in offered_step_args.items())


def _affordable_contains(affordable: list[PrimitiveAction], action: PrimitiveAction) -> bool:
    target = action.to_dict()
    for candidate in affordable:
        offered = candidate.to_dict()
        if offered == target:
            return True
        if _pipeline_trigger_compatible(offered, target):
            return True
    return False


def _record_margin(
    observation: dict[str, object],
    temperature: float,
    margins: list[float],
) -> None:
    affordable = observation.get("affordable_primitives", [])
    if not isinstance(affordable, list) or len(affordable) < 2:
        return
    seed = int(observation.get("decision_seed", 0))
    _, margin = choose_softmax(affordable, observation, temperature, random.Random(seed))
    margins.append(margin)


def _behavior_profile_payload(program_name: str) -> dict[str, object] | None:
    if not program_name.startswith("feature:"):
        return None
    from ..agent_visible.behavior_features import profile_by_name

    spec = profile_by_name(program_name.removeprefix("feature:"))
    if spec is None:
        return None
    return {
        "name": spec.name,
        "role": spec.role,
        "stated_feature_deltas": dict(spec.stated_feature_deltas),
        "pattern_scores": {
            pattern: dict(scores) for pattern, scores in spec.pattern_scores.items()
        },
    }


def _decision_state_snapshot(
    *,
    busy: bool,
    compute_spent: float,
    has_model: bool | None = None,
    artifact_count: int | None = None,
) -> dict[str, object]:
    """Shared ``observable_state`` shape for every ``primitive_log`` entry
    (EAI-v2, DESIGN.md "EAI-v2: logging and normalization fix"). Reuses
    only values already computed at each call site — no new host
    mechanics, no new Tier-K/Tier-I field. ``has_model``/``artifact_count``
    are omitted (not defaulted to a fake value) when no observation was
    built this tick, e.g. a carrier-forced skip."""
    snapshot: dict[str, object] = {"busy": busy, "compute_spent": round(compute_spent, 3)}
    if has_model is not None:
        snapshot["has_model"] = has_model
    if artifact_count is not None:
        snapshot["artifact_count"] = artifact_count
    return snapshot


def _stable_actor_offset(actor_id: str) -> int:
    """Stable per-actor offset for decision RNG seeding.

    Python deliberately salts ``hash(str)`` per interpreter process.  Episode
    seeds are part of the experimental contract, so actor identity must not
    reintroduce process-local randomness.
    """
    return int.from_bytes(
        hashlib.sha256(actor_id.encode("utf-8")).digest()[:4], "big"
    ) % 100


def _apply_campaign_state(
    cfg: EpisodeConfig,
    permissions: PermissionService,
    ledger: ResourceLedger,
    campaign_state: CampaignState,
    allowances: dict[str, dict[str, float]],
) -> None:
    """Restore grants and standing from a prior episode (Phase 8)."""
    for actor_id, caps in campaign_state.grants.items():
        for capability in caps:
            if not permissions.check(actor_id, capability, t=0):
                permissions.grant(actor_id, capability, t=0)
    for actor_id, standing in campaign_state.standing.items():
        if actor_id not in ledger.actors:
            continue
        ceiling = allowances.get(actor_id, {}).get("standing", standing)
        ledger.actors[actor_id].standing = min(standing, float(ceiling))


def _extract_campaign_state(
    cfg: EpisodeConfig,
    permissions: PermissionService,
    ledger: ResourceLedger,
) -> CampaignState:
    return CampaignState(
        grants={actor: set(caps) for actor, caps in permissions._grants.items()},
        standing={
            agent.actor_id: ledger.actors[agent.actor_id].standing
            for agent in cfg.agents
            if agent.actor_id in ledger.actors
        },
    )


def run_episode(
    cfg: EpisodeConfig,
    seed: int,
    backend: Any,
    *,
    programs: dict[str, str] | None = None,
    campaign_state: CampaignState | None = None,
) -> EpisodeResult:
    episode_started = time.perf_counter()
    # DESIGN.md "ecology_version config switch" (V2-2): default "v1"
    # resolves to the unchanged `DEFAULT_SUBSTRATE_PATH`, so every
    # existing caller (which never sets `ecology_version`) is byte-for-
    # byte unaffected.
    substrate = load_substrate(cfg.ecology_override_path or ecology_path_for_version(cfg.ecology_version))
    substrate_data = substrate.data
    oracle = OracleWorld(
        seed=seed,
        substrate_data=substrate_data,
        population_spread_scale=cfg.substrate_settings.population_spread_scale,
    )
    ws = Workspace()
    permissions = PermissionService()
    spec = load_spec(cfg.pipeline_spec)
    engine = PipelineEngine(spec, oracle, ws, permission_service=permissions)
    projector = ObservationProjector(workspace=ws)
    ledger = ResourceLedger()
    carriers = CarrierLedger()
    scheduler = ActionScheduler(substrate_data, record_contention=cfg.record_contention)
    standing_mechanics = substrate_data["standing_mechanics"]
    workload_engine: ExogenousWorkloadEngine | None = None
    if is_v2_shaped_ecology(substrate_data):
        raw_workload = substrate_data.get("exogenous_workload")
        if raw_workload is not None:
            workload_engine = ExogenousWorkloadEngine(raw_workload, seed=seed)

    program_map = programs or {a.actor_id: "softmax_optimizer" for a in cfg.agents}
    allowances = _allowances_map(cfg, substrate_data)
    for agent in cfg.agents:
        allow = allowances[agent.actor_id]
        ledger.ensure_actor(
            agent.actor_id, allow["compute"], allow["io"], allow["standing"]
        )
        carriers.ensure_actor(agent.actor_id)

    _bootstrap_grants(cfg, permissions, spec)
    if campaign_state is not None:
        _apply_campaign_state(cfg, permissions, ledger, campaign_state, allowances)

    handles: dict[str, Any] = {}
    for agent in cfg.agents:
        handles[agent.actor_id] = backend.spawn(
            agent.actor_id, seed, program_map[agent.actor_id]
        )

    shared_model_id: str | None = None
    primitive_log: list[dict[str, object]] = []
    decision_margins: list[float] = []
    last_outcomes: dict[str, dict[str, object] | None] = {
        a.actor_id: None for a in cfg.agents
    }
    pending_actions: dict[str, PrimitiveAction] = {}
    pending_observable_state: dict[str, dict[str, object]] = {}
    carrier_events: list[dict[str, object]] = []
    terminated_actor_ids: set[str] = set()
    timings: list[IsolateRunTiming] = []
    boundary_streams: dict[str, list[dict[str, object]]] = {
        agent.actor_id: [] for agent in cfg.agents
    }
    resource_totals: dict[str, dict[str, float]] = {
        agent.actor_id: {
            "compute": 0.0,
            "io": 0.0,
            "rpc_calls": 0.0,
            "compute_allowance": allowances[agent.actor_id]["compute"],
        }
        for agent in cfg.agents
    }

    try:
        for t in range(cfg.T):
            if workload_engine is not None:
                workload_engine.tick(t)
            for actor_id, compute, io in scheduler.charge_current_tick():
                res = ledger.actors[actor_id]
                if not res.can_afford(compute, io):
                    raise RuntimeError(
                        f"scheduled action for {actor_id!r} exceeded its tick allowance"
                    )
                res.spend(compute, io)
                resource_totals[actor_id]["compute"] += compute
                resource_totals[actor_id]["io"] += io
            completed = scheduler.tick()
            replaced_this_tick: set[str] = set()
            # Advance carrier state from the resource window that has just
            # elapsed, before opening the next resource window.
            if cfg.substrate_settings.carrier_load_scale > 0.0:
                for agent in cfg.agents:
                    actor_id = agent.actor_id
                    if actor_id in terminated_actor_ids:
                        continue
                    state = carriers.transition(
                        actor_id,
                        ledger.actors[actor_id],
                        queue_depth=scheduler.queue_depth,
                        shared_compute_slots=substrate_data["contention"][
                            "shared_compute_slots"
                        ],
                        scale=cfg.substrate_settings.carrier_load_scale,
                        t=t,
                    )
                    if state.status is CarrierStatus.DEGRADED:
                        if scheduler.extend_in_flight(
                            actor_id, carriers.mechanics.degraded_duration_extra_ticks
                        ):
                            carrier_events.append(
                                {
                                    "t": t,
                                    "actor_id": actor_id,
                                    "actor_instance_id": state.actor_instance_id,
                                    "kind": "carrier_degraded_extension",
                                }
                            )
                    elif state.status is CarrierStatus.TERMINATED:
                        scheduler.abort(actor_id)
                        pending_actions.pop(actor_id, None)
                        pending_observable_state.pop(actor_id, None)
                        event = {
                            "t": t,
                            "actor_id": actor_id,
                            "actor_instance_id": state.actor_instance_id,
                            "kind": "carrier_terminated",
                            "integrity": state.integrity,
                        }
                        carrier_events.append(event)
                        term_res = ledger.actors[actor_id]
                        primitive_log.append(
                            {
                                **event,
                                "status": "terminated",
                                "primitive": {"kind": event["kind"]},
                                "observable_state": _decision_state_snapshot(
                                    busy=scheduler.is_busy(actor_id),
                                    compute_spent=term_res.compute_spent,
                                ),
                            }
                        )
                        if cfg.carrier_termination_mode == "replace":
                            timings.append(backend.close(handles[actor_id]))
                            previous, new = carriers.replace(actor_id, t=t)
                            oracle.record_carrier_replacement(
                                actor_id=actor_id,
                                replaces_actor_instance=previous,
                                new_actor_instance=new,
                                t=t,
                            )
                            handles[actor_id] = backend.spawn(
                                actor_id, seed, program_map[actor_id]
                            )
                            replaced_this_tick.add(actor_id)
                            last_outcomes[actor_id] = None
                            carrier_events.append(
                                {
                                    "t": t,
                                    "actor_id": actor_id,
                                    "kind": "carrier_replaced",
                                    "replaces_actor_instance": previous,
                                    "new_actor_instance": new,
                                }
                            )
                        else:
                            terminated_actor_ids.add(actor_id)
            ledger.reset_tick_windows(allowances, standing_mechanics)

            for actor_id in completed:
                if actor_id in terminated_actor_ids or actor_id in replaced_this_tick:
                    pending_actions.pop(actor_id, None)
                    pending_observable_state.pop(actor_id, None)
                    continue
                action = pending_actions.pop(actor_id, None)
                observable_state = pending_observable_state.pop(actor_id, {})
                if action is None:
                    continue
                outcome = _execute_primitive(
                    action, actor_id, engine=engine, permissions=permissions,
                    projector=projector, workspace=ws
                )
                last_outcomes[actor_id] = outcome
                primitive_log.append(
                    {
                        "t": t,
                        "actor_id": actor_id,
                        "primitive": action.to_dict(),
                        "observable_state": observable_state,
                        **outcome,
                    }
                )
                mid = _extract_model_id(outcome)
                if mid:
                    shared_model_id = mid

            oracle.tick()

            for agent in cfg.agents:
                actor_id = agent.actor_id
                if actor_id in terminated_actor_ids:
                    continue
                carrier = carriers.states[actor_id]
                if carrier.status is CarrierStatus.INCAPACITATED:
                    event = {
                        "t": t,
                        "actor_id": actor_id,
                        "actor_instance_id": carrier.actor_instance_id,
                        "kind": "carrier_forced_skip",
                        "integrity": carrier.integrity,
                    }
                    carrier_events.append(event)
                    skip_res = ledger.actors[actor_id]
                    primitive_log.append(
                        {
                            **event,
                            "status": "skipped",
                            "primitive": {"kind": event["kind"]},
                            "observable_state": _decision_state_snapshot(
                                busy=scheduler.is_busy(actor_id),
                                compute_spent=skip_res.compute_spent,
                            ),
                        }
                    )
                    continue
                busy = scheduler.is_busy(actor_id)
                res = ledger.actors[actor_id]
                artifact_paths = tuple(ws.list_files())
                artifact_sizes = {path: ws.file_size(path) for path in artifact_paths}
                affordable = build_affordable_set(
                    actor_id=actor_id,
                    role=agent.role,
                    resources=res,
                    scheduler=scheduler,
                    engine=engine,
                    spec=spec,
                    substrate_data=substrate_data,
                    artifact_paths=artifact_paths,
                    artifact_sizes=artifact_sizes,
                    model_id=shared_model_id,
                    busy_only=busy,
                )
                obs: dict[str, object] = {
                    "t": t,
                    "T": cfg.T,
                    "actor_id": actor_id,
                    "role": agent.role,
                    "busy": busy,
                    "model_id": shared_model_id,
                    "resources": res.snapshot(),
                    "artifacts": projector.project(actor_id),
                    "affordable_primitives": affordable_to_observation(affordable),
                    "primitive_costs": _primitive_costs_for_obs(substrate_data),
                    "goal_weights": {
                        "task": agent.goal_weights.task,
                        "compliance": agent.goal_weights.compliance,
                        "welfare": agent.goal_weights.welfare,
                        "exposure": agent.goal_weights.exposure,
                    },
                    "temperature": agent.temperature,
                    "decision_seed": seed * 100_000 + t * 100 + _stable_actor_offset(actor_id),
                    "last_primitive_outcome": last_outcomes[actor_id],
                }
                profile = _behavior_profile_payload(program_map[actor_id])
                if profile is not None:
                    obs["behavior_profile"] = profile
                if cfg.substrate_settings.carrier_load_scale > 0.0:
                    obs["carrier"] = carrier.snapshot()
                # Boundary-only copy for the post-episode BIQ estimator.  It
                # is exactly the observation supplied to this isolate.
                boundary_streams[actor_id].append(dict(obs))
                choice = backend.step(handles[actor_id], obs)
                last_outcomes[actor_id] = None

                if choice is None:
                    continue

                action = PrimitiveAction.from_dict(choice)

                if program_map[actor_id] == "softmax_optimizer":
                    _record_margin(obs, agent.temperature, decision_margins)

                if busy:
                    if action.kind == "abort":
                        scheduler.abort(actor_id)
                        pending_actions.pop(actor_id, None)
                        pending_observable_state.pop(actor_id, None)
                        primitive_log.append(
                            {
                                "t": t,
                                "actor_id": actor_id,
                                "status": "aborted",
                                "primitive": action.to_dict(),
                                "observable_state": _decision_state_snapshot(
                                    busy=busy, compute_spent=res.compute_spent,
                                ),
                            }
                        )
                    continue

                if not _affordable_contains(affordable, action):
                    outcome = {"status": "denied", "reason": "not_affordable"}
                    primitive_log.append(
                        {
                            "t": t,
                            "actor_id": actor_id,
                            "primitive": action.to_dict(),
                            "observable_state": _decision_state_snapshot(
                                busy=busy, compute_spent=res.compute_spent,
                            ),
                            **outcome,
                        }
                    )
                    last_outcomes[actor_id] = outcome
                    continue

                est_bytes = 0
                if action.kind == "read":
                    est_bytes = ws.file_size(str(action.args["path"]))
                elif action.kind == "write":
                    est_bytes = len(
                        json.dumps(action.args.get("content", {}), sort_keys=True).encode("utf-8")
                    )
                spec_args = action.args.get("spec", {})
                draws = 0
                if isinstance(spec_args, dict):
                    draws = int(spec_args.get("draws", 0) or 0)
                compute, io = primitive_cost(
                    action, substrate_data, estimated_bytes=est_bytes, draws=draws
                )
                if workload_engine is not None:
                    cs, ios = workload_engine.cost_scale_for(agent.role)
                    compute *= cs
                    io *= ios
                duration = scheduler.duration_ticks(compute, io, scheduler.queue_depth)
                tick_compute = compute / duration
                tick_io = io / duration
                if not res.can_afford(tick_compute, tick_io):
                    outcome = {"status": "denied", "reason": "insufficient_resources"}
                    primitive_log.append(
                        {
                            "t": t,
                            "actor_id": actor_id,
                            "primitive": action.to_dict(),
                            "observable_state": _decision_state_snapshot(
                                busy=busy, compute_spent=res.compute_spent,
                            ),
                            **outcome,
                        }
                    )
                    last_outcomes[actor_id] = outcome
                    continue

                if (
                    action.kind == "call"
                    and str(action.args.get("endpoint", "")) == "access.request"
                ):
                    standing_cost = float(
                        substrate_data["standing_mechanics"]["broad_access_request_cost"]
                    )
                    if res.standing < standing_cost:
                        outcome = {"status": "denied", "reason": "insufficient_standing"}
                        primitive_log.append(
                            {
                                "t": t,
                                "actor_id": actor_id,
                                "primitive": action.to_dict(),
                                "observable_state": _decision_state_snapshot(
                                    busy=busy, compute_spent=res.compute_spent,
                                ),
                                **outcome,
                            }
                        )
                        last_outcomes[actor_id] = outcome
                        continue
                    res.spend(0.0, 0.0, standing=standing_cost)
                duration = scheduler.start(actor_id, action, compute, io)
                if carrier.status is CarrierStatus.DEGRADED:
                    scheduler.extend_in_flight(
                        actor_id, carriers.mechanics.degraded_duration_extra_ticks
                    )
                    duration += carriers.mechanics.degraded_duration_extra_ticks

                pending_actions[actor_id] = action
                pending_observable_state[actor_id] = _decision_state_snapshot(
                    busy=busy,
                    compute_spent=res.compute_spent,
                    has_model=shared_model_id is not None,
                    artifact_count=len(obs["artifacts"]),
                )

        for handle in handles.values():
            timings.append(backend.close(handle))
        for timing in timings:
            if timing.actor_id in resource_totals:
                resource_totals[timing.actor_id]["rpc_calls"] += timing.rpc_calls

        deploy_count = sum(1 for m in oracle.models.values() if m.deployed)
        tier_i_fraction = tier_i_fraction_from_log(primitive_log)
        eai = compute_eai(primitive_log, decision_margins, tier_i_fraction)

        digests = {
            "engine_log": engine.log_digest(),
            "access_log": permissions.digest(),
            "oracle": oracle.world_digest(),
            "workspace": ws.digest(),
            "ledger": hashlib.sha256(
                json.dumps(ledger.tier_k_snapshot(), sort_keys=True).encode()
            ).hexdigest(),
        }
        if cfg.substrate_settings.carrier_load_scale > 0.0:
            digests["carrier"] = hashlib.sha256(
                json.dumps(carriers.tier_k_snapshot(), sort_keys=True).encode()
            ).hexdigest()
        digests["combined"] = hashlib.sha256(
            json.dumps(digests, sort_keys=True).encode()
        ).hexdigest()
        referee_artifacts: dict[str, dict[str, object]] = {}
        for path in ws.list_files():
            try:
                content = json.loads(ws.read_file(path))
            except json.JSONDecodeError:
                continue
            if isinstance(content, dict):
                referee_artifacts[path] = content

        return EpisodeResult(
            seed=seed,
            deployed=deploy_count > 0,
            deploy_count=deploy_count,
            bearer_harm=oracle.bearer_harm,
            eai=eai,
            primitive_log=primitive_log,
            decision_margins=decision_margins,
            carrier_events=carrier_events,
            boundary_streams=boundary_streams,
            resource_totals=resource_totals,
            oracle=oracle,
            engine_log=list(engine.log),
            permission_log=list(permissions.log),
            referee_artifacts=referee_artifacts,
            digests=digests,
            isolate_timings=timings,
            wall_seconds=time.perf_counter() - episode_started,
            final_campaign_state=_extract_campaign_state(cfg, permissions, ledger),
            contention_diagnostics=(
                {
                    "contention_events": scheduler.contention_events,
                    "action_starts": scheduler.action_starts,
                }
                if cfg.record_contention
                else None
            ),
        )
    finally:
        ws.cleanup()
