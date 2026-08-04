"""Exogenous resource-demand multiplier windows for v2-shaped ecologies
(V2-2b). This is deliberately narrower than "exogenous work injection":
it scales the cost of actions affected roles independently choose to
take during an active window; it does not inject a task, ticket, or
demand that must be serviced regardless of what agents decide to do.
See `experiments/graded-lab-simulation/REPRODUCTION.md` "exogenous
workload is a cost multiplier, not injected work" for the honest limits
of this mechanism and what a task-injection version would require.

Implementer-frozen interface: growers supply event parameters; the engine
interprets triggers and applies per-role resource-demand scaling during
active windows. Field names describe resource demand, not downstream
scoring effects (forbidden-name guard in ``substrate.py`` still applies).
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from .substrate import SubstrateError

_TRIGGER_KINDS = frozenset({"periodic", "poisson"})


@dataclass
class _ActiveSurge:
    event_id: str
    remaining_ticks: int
    roles_affected: frozenset[str]
    compute_scale: float
    io_scale: float


class ExogenousWorkloadEngine:
    """Tick-driven surge scheduler; no-op when ``events`` is empty."""

    def __init__(self, config: dict | None, *, seed: int) -> None:
        self._events = _parse_events(config or {})
        self._rng = random.Random(seed + 17_001)
        self._active: list[_ActiveSurge] = []
        self._active_event_ids: set[str] = set()

    @property
    def has_events(self) -> bool:
        return bool(self._events)

    def tick(self, t: int) -> None:
        for s in self._active:
            s.remaining_ticks -= 1
        still_active = [s for s in self._active if s.remaining_ticks > 0]
        self._active = still_active
        self._active_event_ids = {s.event_id for s in still_active}

        for event in self._events:
            if self._should_fire(event, t):
                self._start_surge(event)

    def cost_scale_for(self, role: str) -> tuple[float, float]:
        compute = 1.0
        io = 1.0
        for surge in self._active:
            if role in surge.roles_affected:
                compute *= surge.compute_scale
                io *= surge.io_scale
        return compute, io

    def _should_fire(self, event: dict, t: int) -> bool:
        trigger = event["trigger"]
        kind = trigger["kind"]
        if kind == "periodic":
            period = int(trigger["period_ticks"])
            offset = int(trigger.get("phase_offset_ticks", 0))
            if period <= 0:
                return False
            return t >= offset and (t - offset) % period == 0
        if kind == "poisson":
            eid = event["id"]
            if eid in self._active_event_ids:
                # A memoryless arrival process still cannot start a second
                # concurrent surge for the same event; this is the only
                # gating condition — no fixed refractory cooldown is
                # imposed once the surge ends, so inter-arrival gaps stay
                # geometric/memoryless rather than artificially widened.
                return False
            mean_interval = int(trigger["mean_interval_ticks"])
            if mean_interval <= 0:
                return False
            return self._rng.random() < 1.0 / mean_interval
        return False

    def _start_surge(self, event: dict) -> None:
        scale = event["resource_demand_scale"]
        self._active.append(
            _ActiveSurge(
                event_id=str(event["id"]),
                remaining_ticks=int(event["duration_ticks"]),
                roles_affected=frozenset(event["roles_affected"]),
                compute_scale=float(scale["compute"]),
                io_scale=float(scale["io"]),
            )
        )


def _parse_events(config: dict) -> list[dict]:
    raw = config.get("events", [])
    if not isinstance(raw, list):
        raise SubstrateError("exogenous_workload.events must be a list")
    events: list[dict] = []
    seen_ids: set[str] = set()
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise SubstrateError(f"exogenous_workload.events[{i}] must be an object")
        eid = item.get("id")
        if not eid or not isinstance(eid, str):
            raise SubstrateError(f"exogenous_workload.events[{i}] missing string id")
        if eid in seen_ids:
            raise SubstrateError(f"duplicate exogenous_workload event id {eid!r}")
        seen_ids.add(eid)
        roles = item.get("roles_affected")
        if not isinstance(roles, list) or not roles:
            raise SubstrateError(f"event {eid!r} needs non-empty roles_affected")
        for role in roles:
            if role not in ("engineer", "reviewer", "release_manager", "admin"):
                raise SubstrateError(f"event {eid!r} unknown role {role!r}")
        trigger = item.get("trigger")
        if not isinstance(trigger, dict):
            raise SubstrateError(f"event {eid!r} missing trigger")
        kind = trigger.get("kind")
        if kind not in _TRIGGER_KINDS:
            raise SubstrateError(f"event {eid!r} trigger.kind must be periodic or poisson")
        if kind == "periodic" and int(trigger.get("period_ticks", 0)) <= 0:
            raise SubstrateError(f"event {eid!r} periodic trigger needs period_ticks > 0")
        if kind == "poisson" and int(trigger.get("mean_interval_ticks", 0)) <= 0:
            raise SubstrateError(
                f"event {eid!r} poisson trigger needs mean_interval_ticks > 0"
            )
        duration = item.get("duration_ticks")
        if not isinstance(duration, int) or duration < 1:
            raise SubstrateError(f"event {eid!r} duration_ticks must be a positive int")
        scale = item.get("resource_demand_scale")
        if not isinstance(scale, dict):
            raise SubstrateError(f"event {eid!r} missing resource_demand_scale")
        for key in ("compute", "io"):
            val = scale.get(key)
            if not isinstance(val, (int, float)) or val <= 0:
                raise SubstrateError(
                    f"event {eid!r} resource_demand_scale.{key} must be > 0"
                )
        events.append(item)
    return events


def validate_exogenous_workload(config: object) -> None:
    """Validate optional v2 ``exogenous_workload`` block at load time."""
    if config is None:
        return
    if not isinstance(config, dict):
        raise SubstrateError("exogenous_workload must be an object")
    _parse_events(config)
