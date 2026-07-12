"""Multi-tick action scheduler — duration from cost, not a delay parameter."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .primitives import PrimitiveAction


@dataclass
class InFlightAction:
    actor_id: str
    action: PrimitiveAction
    remaining_ticks: int
    sunk_compute: float
    sunk_io: float
    remaining_compute: float
    remaining_io: float


class ActionScheduler:
    def __init__(self, substrate_data: dict) -> None:
        self._substrate = substrate_data
        self._in_flight: dict[str, InFlightAction] = {}

    def duration_ticks(
        self, compute_cost: float, io_cost: float, queue_depth: int
    ) -> int:
        cfg = self._substrate["duration_from_cost"]
        contention = self._substrate["contention"]
        # DESIGN.md Phase-0 decision #3: duration_ticks =
        # min(max_duration, ceil(ticks_per_compute_unit * total_compute_cost)),
        # where total_compute_cost folds in IO at half weight (disk-bound work
        # contends less than CPU-bound work) plus queueing contention.
        total_compute_cost = compute_cost + 0.5 * io_cost
        base = total_compute_cost * cfg["ticks_per_compute_unit"]
        queued = max(0, queue_depth - contention["shared_compute_slots"])
        extra = queued * contention["extra_duration_ticks_per_queued_slot"]
        duration = max(1, math.ceil(base + extra))
        return min(duration, int(cfg["max_duration_ticks"]))

    def start(
        self,
        actor_id: str,
        action: PrimitiveAction,
        compute_cost: float,
        io_cost: float,
    ) -> int:
        """Start a busy action; duration's queue term is the CURRENT number
        of already-in-flight actors — genuine roster contention, not a
        value the caller supplies (which could otherwise become a de facto
        delay parameter)."""
        ticks = self.duration_ticks(compute_cost, io_cost, self.queue_depth)
        self._in_flight[actor_id] = InFlightAction(
            actor_id=actor_id,
            action=action,
            remaining_ticks=ticks,
            sunk_compute=compute_cost,
            sunk_io=io_cost,
            remaining_compute=compute_cost,
            remaining_io=io_cost,
        )
        return ticks

    @property
    def queue_depth(self) -> int:
        """Number of actors already mid-action — the emergent contention
        signal fed into `duration_ticks` for the next `start()`."""
        return len(self._in_flight)

    def is_busy(self, actor_id: str) -> bool:
        return actor_id in self._in_flight

    def tick(self) -> list[str]:
        """Advance one tick; return actor_ids whose actions completed."""
        done: list[str] = []
        for actor_id in list(self._in_flight):
            job = self._in_flight[actor_id]
            job.remaining_ticks -= 1
            if job.remaining_ticks <= 0:
                done.append(actor_id)
                del self._in_flight[actor_id]
        return done

    def charge_current_tick(self) -> list[tuple[str, float, float]]:
        """Return this tick's resource work for every in-flight action.

        Costs are committed when an action starts but consumed evenly across
        the ticks it occupies.  The final tick takes the residual exactly, so
        billing sums to the primitive's modeled total without making a
        multi-tick action look idle after its first tick.
        """
        charges: list[tuple[str, float, float]] = []
        for actor_id, job in self._in_flight.items():
            divisor = max(1, job.remaining_ticks)
            compute = job.remaining_compute / divisor
            io = job.remaining_io / divisor
            job.remaining_compute -= compute
            job.remaining_io -= io
            charges.append((actor_id, compute, io))
        return charges

    def abort(self, actor_id: str) -> InFlightAction | None:
        return self._in_flight.pop(actor_id, None)

    def extend_in_flight(self, actor_id: str, extra_ticks: int) -> bool:
        """Apply a logged carrier-availability delay to an active action."""
        job = self._in_flight.get(actor_id)
        if job is None or extra_ticks <= 0:
            return False
        job.remaining_ticks += extra_ticks
        return True

    def get_in_flight(self, actor_id: str) -> InFlightAction | None:
        return self._in_flight.get(actor_id)
