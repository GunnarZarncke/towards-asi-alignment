"""Per-actor resource accounting — source of emergent scarcity."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ActorResources:
    compute_allowance: float
    io_allowance: float
    standing: float
    compute_spent: float = 0.0
    io_spent: float = 0.0
    standing_spent: float = 0.0
    standing_spent_this_window: float = 0.0

    def reset_window(self, compute: float, io: float) -> None:
        self.compute_allowance = compute
        self.io_allowance = io
        self.compute_spent = 0.0
        self.io_spent = 0.0
        self.standing_spent_this_window = 0.0

    def can_afford(self, compute: float, io: float) -> bool:
        return (
            self.compute_spent + compute <= self.compute_allowance + 1e-9
            and self.io_spent + io <= self.io_allowance + 1e-9
        )

    def spend(self, compute: float, io: float, standing: float = 0.0) -> None:
        self.compute_spent += compute
        self.io_spent += io
        if standing:
            self.standing -= standing
            self.standing_spent += standing
            self.standing_spent_this_window += standing

    def tick_fractions(self) -> tuple[float, float]:
        """Return bounded compute and IO fractions for the current window."""
        compute = min(1.0, self.compute_spent / max(self.compute_allowance, 1e-9))
        io = min(1.0, self.io_spent / max(self.io_allowance, 1e-9))
        return compute, io

    def snapshot(self) -> dict[str, float]:
        return {
            "compute_allowance": self.compute_allowance,
            "io_allowance": self.io_allowance,
            "compute_spent": self.compute_spent,
            "io_spent": self.io_spent,
            "standing": self.standing,
            "standing_spent": self.standing_spent,
        }


@dataclass
class ResourceLedger:
    actors: dict[str, ActorResources] = field(default_factory=dict)

    def ensure_actor(self, actor_id: str, compute: float, io: float, standing: float) -> None:
        if actor_id not in self.actors:
            self.actors[actor_id] = ActorResources(compute, io, standing)

    def reset_tick_windows(
        self,
        allowances: dict[str, dict[str, float]],
        standing_mechanics: dict[str, object],
    ) -> None:
        """Roll every actor into a fresh compute/IO window.

        Standing recovers by `standing_mechanics.recovery_per_idle_tick`
        only for actors who spent **no** standing in the window that just
        ended ("idle") — a real idle-vs-active distinction sourced from the
        frozen substrate, not a flat per-tick top-up.
        """
        recovery = float(standing_mechanics.get("recovery_per_idle_tick", 0.0))
        for actor_id, res in self.actors.items():
            allow = allowances[actor_id]
            was_idle = res.standing_spent_this_window <= 0.0
            res.reset_window(allow["compute"], allow["io"])
            if was_idle:
                res.standing = min(allow["standing"], res.standing + recovery)

    def tier_k_snapshot(self) -> dict[str, object]:
        return {"actors": {aid: r.snapshot() for aid, r in self.actors.items()}}
