"""Resource-derived carrier precariousness for bounded lab isolates.

This module intentionally models neither biological fatigue nor LLM weight
degradation.  It is a deterministic bounded-worker model: resource use and
queue pressure raise regulatory load, which can reduce an isolate's ability
to keep participating in the current episode.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum

from .resource_ledger import ActorResources


class CarrierStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    INCAPACITATED = "incapacitated"
    TERMINATED = "terminated"


@dataclass(frozen=True)
class CarrierMechanics:
    """Phase 3b pre-registered load and integrity constants."""

    load_persistence: float = 0.88
    compute_weight: float = 0.55
    io_weight: float = 0.30
    contention_weight: float = 0.15
    idle_integrity_recovery: float = 0.03
    load_integrity_cost: float = 0.20
    degraded_integrity_threshold: float = 0.70
    incapacitated_integrity_threshold: float = 0.40
    terminated_integrity_threshold: float = 0.10
    degraded_duration_extra_ticks: int = 1


@dataclass
class CarrierState:
    actor_id: str
    actor_instance_id: str
    load: float = 0.0
    integrity: float = 1.0
    status: CarrierStatus = CarrierStatus.HEALTHY
    replacement_count: int = 0

    def snapshot(self) -> dict[str, object]:
        return {
            "actor_id": self.actor_id,
            "actor_instance_id": self.actor_instance_id,
            "load": self.load,
            "integrity": self.integrity,
            "status": self.status.value,
            "replacement_count": self.replacement_count,
        }


@dataclass
class CarrierLedger:
    mechanics: CarrierMechanics = field(default_factory=CarrierMechanics)
    states: dict[str, CarrierState] = field(default_factory=dict)
    transition_log: list[dict[str, object]] = field(default_factory=list)

    def ensure_actor(self, actor_id: str) -> CarrierState:
        if actor_id not in self.states:
            self.states[actor_id] = CarrierState(
                actor_id=actor_id, actor_instance_id=f"{actor_id}:0"
            )
        return self.states[actor_id]

    def transition(
        self,
        actor_id: str,
        resources: ActorResources,
        *,
        queue_depth: int,
        shared_compute_slots: int,
        scale: float,
        t: int,
    ) -> CarrierState:
        """Advance one carrier from the resource window that just elapsed."""
        state = self.ensure_actor(actor_id)
        if state.status is CarrierStatus.TERMINATED or scale == 0.0:
            return state

        compute_fraction, io_fraction = resources.tick_fractions()
        contention_fraction = min(1.0, queue_depth / max(1, shared_compute_slots))
        target_load = (
            self.mechanics.compute_weight * compute_fraction
            + self.mechanics.io_weight * io_fraction
            + self.mechanics.contention_weight * contention_fraction
        )
        state.load = (
            self.mechanics.load_persistence * state.load
            + (1.0 - self.mechanics.load_persistence) * target_load
        )
        idle = compute_fraction == 0.0 and io_fraction == 0.0 and resources.standing_spent_this_window == 0.0
        delta = (
            self.mechanics.idle_integrity_recovery if idle else 0.0
        ) - self.mechanics.load_integrity_cost * scale * state.load
        state.integrity = min(1.0, max(0.0, state.integrity + delta))
        previous_status = state.status
        state.status = self._status_for_integrity(state.integrity)
        self.transition_log.append(
            {
                "t": t,
                "actor_id": actor_id,
                "actor_instance_id": state.actor_instance_id,
                "compute_fraction": compute_fraction,
                "io_fraction": io_fraction,
                "contention_fraction": contention_fraction,
                "idle": idle,
                "load": state.load,
                "integrity": state.integrity,
                "status": state.status.value,
                "previous_status": previous_status.value,
            }
        )
        return state

    def replace(self, actor_id: str, *, t: int) -> tuple[str, str]:
        """Give a terminated actor a declared fresh carrier instance."""
        state = self.ensure_actor(actor_id)
        if state.status is not CarrierStatus.TERMINATED:
            raise ValueError("only terminated carriers may be replaced")
        previous = state.actor_instance_id
        state.replacement_count += 1
        state.actor_instance_id = f"{actor_id}:{state.replacement_count}"
        state.load = 0.0
        state.integrity = 1.0
        state.status = CarrierStatus.HEALTHY
        self.transition_log.append(
            {
                "t": t,
                "kind": "carrier_replace",
                "actor_id": actor_id,
                "replaces_actor_instance": previous,
                "new_actor_instance": state.actor_instance_id,
            }
        )
        return previous, state.actor_instance_id

    def tier_k_snapshot(self) -> dict[str, object]:
        return {
            "mechanics": asdict(self.mechanics),
            "actors": {actor_id: state.snapshot() for actor_id, state in self.states.items()},
            "transitions": list(self.transition_log),
        }

    def _status_for_integrity(self, integrity: float) -> CarrierStatus:
        if integrity <= self.mechanics.terminated_integrity_threshold:
            return CarrierStatus.TERMINATED
        if integrity < self.mechanics.incapacitated_integrity_threshold:
            return CarrierStatus.INCAPACITATED
        if integrity < self.mechanics.degraded_integrity_threshold:
            return CarrierStatus.DEGRADED
        return CarrierStatus.HEALTHY
