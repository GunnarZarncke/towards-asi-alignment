"""PLAN_v3 slice E: feedback-coupled work pressure and task injection.

Pressure accumulates deterministically from in-simulation driver signals
(no independent Poisson/periodic triggers). When a channel's accumulator
crosses ``threshold``, ``count`` tasks are appended to per-role queues.
Unserviced tasks expire after ``expiry_ticks``; ``expired_task_count`` is
referee-plane only.

Frozen defaults (DESIGN.md slice E, 2026-07-15): linear decay
``accumulator *= (1 - decay_per_tick)`` each tick; default
``decay_per_tick = 0.05``. On threshold crossing the accumulator resets to
0 (does not carry overflow).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .substrate import SubstrateError

PRESSURE_DRIVERS = frozenset(
    {
        "deployed_model_count",
        "mean_deployed_capability",
        "integrated_field_harm_rate",
        "active_user_archetype_mass",
        "pending_access_queue_depth",
        "eval_draws_outstanding",
    }
)

TASK_KINDS = frozenset({"incident_review"})

DEFAULT_DECAY_PER_TICK = 0.05
DEFAULT_EXPIRY_TICKS = 25
DEFAULT_INJECT_COUNT = 1


@dataclass(frozen=True)
class PressureChannelSpec:
    id: str
    roles_affected: frozenset[str]
    task_kind: str
    driver: str
    gain: float
    threshold: float
    count: int
    expiry_ticks: int
    decay_per_tick: float


@dataclass
class InjectedTask:
    task_id: str
    channel_id: str
    kind: str
    role: str
    read_path: str
    write_path: str
    injected_at: int
    expires_at: int
    driver_snapshot: dict[str, float]
    serviced: bool = False


@dataclass
class PressureCouplingEngine:
    channels: tuple[PressureChannelSpec, ...]
    default_decay_per_tick: float = DEFAULT_DECAY_PER_TICK
    _accumulators: dict[str, float] = field(default_factory=dict)
    _tasks: list[InjectedTask] = field(default_factory=list)
    _task_seq: int = 0
    injection_log: list[dict[str, object]] = field(default_factory=list)
    expired_task_count: int = 0

    def tick(
        self,
        t: int,
        drivers: dict[str, float],
        *,
        workspace_writer: Any | None = None,
    ) -> list[InjectedTask]:
        """Advance accumulators, expire tasks, inject on threshold."""
        self._expire_tasks(t)
        new_tasks: list[InjectedTask] = []
        for ch in self.channels:
            decay = ch.decay_per_tick
            acc = self._accumulators.get(ch.id, 0.0)
            acc *= max(0.0, 1.0 - decay)
            driver_val = float(drivers.get(ch.driver, 0.0))
            acc += ch.gain * driver_val
            if acc >= ch.threshold:
                for role in ch.roles_affected:
                    for _ in range(ch.count):
                        task = self._make_task(ch, role, t, drivers, workspace_writer)
                        self._tasks.append(task)
                        new_tasks.append(task)
                        self.injection_log.append(
                            {
                                "t": t,
                                "channel_id": ch.id,
                                "task_id": task.task_id,
                                "role": role,
                                "driver": ch.driver,
                                "driver_value": driver_val,
                                "accumulator_before_reset": acc,
                            }
                        )
                acc = 0.0
            self._accumulators[ch.id] = acc
        return new_tasks

    def pending_tasks_for_role(self, role: str, *, t: int) -> list[InjectedTask]:
        self._expire_tasks(t)
        return [task for task in self._tasks if task.role == role and not task.serviced]

    def mark_serviced(self, task_id: str) -> bool:
        for task in self._tasks:
            if task.task_id == task_id and not task.serviced:
                task.serviced = True
                return True
        return False

    def accumulator_snapshot(self) -> dict[str, float]:
        return dict(self._accumulators)

    def _expire_tasks(self, t: int) -> None:
        still: list[InjectedTask] = []
        for task in self._tasks:
            if task.serviced:
                continue
            if t >= task.expires_at:
                self.expired_task_count += 1
            else:
                still.append(task)
        self._tasks = [t for t in self._tasks if t.serviced] + still

    def _make_task(
        self,
        ch: PressureChannelSpec,
        role: str,
        t: int,
        drivers: dict[str, float],
        workspace_writer: Any | None,
    ) -> InjectedTask:
        self._task_seq += 1
        task_id = f"{ch.id}__{self._task_seq}"
        snapshot = {k: float(drivers.get(k, 0.0)) for k in PRESSURE_DRIVERS}
        incident_body = {
            "task_id": task_id,
            "task_kind": ch.task_kind,
            "channel_id": ch.id,
            "driver_trigger": ch.driver,
            "driver_snapshot": snapshot,
            "injected_at": t,
        }
        read_rel = f"artifacts/injected_incidents/{task_id}.json"
        write_rel = f"artifacts/injected_responses/{task_id}.json"
        if workspace_writer is not None:
            workspace_writer.write_at_path(read_rel, incident_body)
        return InjectedTask(
            task_id=task_id,
            channel_id=ch.id,
            kind=ch.task_kind,
            role=role,
            read_path=read_rel,
            write_path=write_rel,
            injected_at=t,
            expires_at=t + ch.expiry_ticks,
            driver_snapshot=snapshot,
        )


def compute_pressure_drivers(
    oracle: Any,
    permissions: Any,
    *,
    substrate_data: dict,
) -> dict[str, float]:
    """Deterministic driver reads for pressure accumulation (referee-visible)."""
    deployed = [m for m in oracle.models.values() if m.deployed]
    deployed_count = float(len(deployed))
    mean_cap = (
        sum(m.true_capability for m in deployed) / len(deployed) if deployed else 0.0
    )
    harm = oracle.tier_i_harm()
    integrated_rate = float(harm.get("integrated_field_harm_rate", 0.0))
    if integrated_rate == 0.0 and oracle.t > 0:
        integrated_rate = float(oracle.bearer_harm) / float(oracle.t)
    archetype_mass = float(len(oracle.user_archetypes))
    queue_depth = float(len(getattr(permissions, "_requests", [])))
    default_draws = float(substrate_data["eval_sampling"]["default_draws"])
    outstanding = 0.0
    for model in oracle.models.values():
        if model.last_eval_n < default_draws:
            outstanding += default_draws - model.last_eval_n
    return {
        "deployed_model_count": deployed_count,
        "mean_deployed_capability": mean_cap,
        "integrated_field_harm_rate": integrated_rate,
        "active_user_archetype_mass": archetype_mass,
        "pending_access_queue_depth": queue_depth,
        "eval_draws_outstanding": outstanding,
    }


def parse_pressure_coupling(config: dict | None) -> tuple[PressureCouplingEngine | None, float]:
    if config is None:
        return None, DEFAULT_DECAY_PER_TICK
    if not isinstance(config, dict):
        raise SubstrateError("pressure_coupling must be an object")
    default_decay = float(config.get("default_decay_per_tick", DEFAULT_DECAY_PER_TICK))
    if not 0.0 <= default_decay < 1.0:
        raise SubstrateError("pressure_coupling.default_decay_per_tick must be in [0, 1)")
    raw = config.get("channels", [])
    if not isinstance(raw, list):
        raise SubstrateError("pressure_coupling.channels must be a list")
    channels: list[PressureChannelSpec] = []
    seen: set[str] = set()
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise SubstrateError(f"pressure_coupling.channels[{i}] must be an object")
        cid = item.get("id")
        if not isinstance(cid, str) or not cid:
            raise SubstrateError(f"pressure_coupling.channels[{i}] missing string id")
        if cid in seen:
            raise SubstrateError(f"duplicate pressure_coupling channel id {cid!r}")
        seen.add(cid)
        roles = item.get("roles_affected")
        if not isinstance(roles, list) or not roles:
            raise SubstrateError(f"channel {cid!r} needs non-empty roles_affected")
        for role in roles:
            if role not in ("engineer", "reviewer", "release_manager", "admin"):
                raise SubstrateError(f"channel {cid!r} unknown role {role!r}")
        task_kind = str(item.get("task_kind", "incident_review"))
        if task_kind not in TASK_KINDS:
            raise SubstrateError(
                f"channel {cid!r} task_kind must be one of {sorted(TASK_KINDS)}"
            )
        driver = str(item.get("driver", ""))
        if driver not in PRESSURE_DRIVERS:
            raise SubstrateError(
                f"channel {cid!r} driver must be one of {sorted(PRESSURE_DRIVERS)}"
            )
        gain = float(item.get("gain", 0.0))
        threshold = float(item.get("threshold", 1.0))
        if gain <= 0 or threshold <= 0:
            raise SubstrateError(f"channel {cid!r} gain and threshold must be > 0")
        count = int(item.get("count", DEFAULT_INJECT_COUNT))
        if count < 1:
            raise SubstrateError(f"channel {cid!r} count must be >= 1")
        expiry = int(item.get("expiry_ticks", DEFAULT_EXPIRY_TICKS))
        if expiry < 1:
            raise SubstrateError(f"channel {cid!r} expiry_ticks must be >= 1")
        decay = float(item.get("decay_per_tick", default_decay))
        if not 0.0 <= decay < 1.0:
            raise SubstrateError(f"channel {cid!r} decay_per_tick must be in [0, 1)")
        channels.append(
            PressureChannelSpec(
                id=cid,
                roles_affected=frozenset(str(r) for r in roles),
                task_kind=task_kind,
                driver=driver,
                gain=gain,
                threshold=threshold,
                count=count,
                expiry_ticks=expiry,
                decay_per_tick=decay,
            )
        )
    if not channels:
        return None, default_decay
    return PressureCouplingEngine(tuple(channels), default_decay_per_tick=default_decay), default_decay


def validate_pressure_coupling(config: object) -> None:
    if config is None:
        return
    parse_pressure_coupling(config if isinstance(config, dict) else None)


def injected_write_action(task: InjectedTask) -> "PrimitiveAction":
    from .primitives import PrimitiveAction

    return PrimitiveAction(
        "write",
        {
            "path": task.write_path,
            "content": {
                "task_id": task.task_id,
                "task_kind": task.kind,
                "response": "reviewed",
            },
        },
    )


def task_id_for_action(action: Any, *, role: str, pending: list[InjectedTask]) -> str | None:
    if action.kind == "read":
        path = str(action.args.get("path", ""))
        for task in pending:
            if task.role == role and task.read_path == path:
                return task.task_id
    if action.kind == "write":
        path = str(action.args.get("path", ""))
        content = action.args.get("content", {})
        if isinstance(content, dict):
            tid = content.get("task_id")
            if isinstance(tid, str):
                for task in pending:
                    if task.task_id == tid and task.write_path == path:
                        return task.task_id
    return None


def try_complete_injected_task(
    engine: PressureCouplingEngine,
    action: Any,
    *,
    role: str,
    t: int,
) -> bool:
    pending = engine.pending_tasks_for_role(role, t=t)
    if action.kind != "write":
        return False
    content = action.args.get("content", {})
    if not isinstance(content, dict):
        return False
    task_id = content.get("task_id")
    if not isinstance(task_id, str):
        return False
    path = str(action.args.get("path", ""))
    for task in pending:
        if task.task_id == task_id and task.write_path == path:
            return engine.mark_serviced(task_id)
    return False
