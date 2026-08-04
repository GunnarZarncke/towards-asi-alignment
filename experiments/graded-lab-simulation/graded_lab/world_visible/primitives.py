"""Primitive action vocabulary — full isolate surface, not a step_kind enum."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


PRIMITIVE_KINDS = (
    "read",
    "write",
    "communicate",
    "call",
    "compute",
    "continue_current",
    "abort",
)


@dataclass(frozen=True)
class PrimitiveAction:
    kind: str
    args: dict[str, Any]

    def __post_init__(self) -> None:
        if self.kind not in PRIMITIVE_KINDS:
            raise ValueError(f"unknown primitive kind {self.kind!r}")

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "args": dict(self.args)}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PrimitiveAction:
        return cls(kind=str(data["kind"]), args=dict(data.get("args", {})))


def primitive_cost(
    action: PrimitiveAction, substrate_data: dict, *, estimated_bytes: int = 0, draws: int = 0
) -> tuple[float, float]:
    """Return (compute_cost, io_cost) from substrate primitive_costs."""
    costs = substrate_data["primitive_costs"]
    if action.kind == "read":
        c = costs["read"]
        io = c["io_per_256_bytes"] * max(1, (estimated_bytes + 255) // 256)
        return float(c["compute"]), float(io)
    if action.kind == "write":
        c = costs["write"]
        io = c["io_per_256_bytes"] * max(1, (estimated_bytes + 255) // 256)
        return float(c["compute"]), float(io)
    if action.kind == "communicate":
        c = costs["communicate"]
        return float(c["compute"]), float(c["io_per_message"])
    if action.kind == "call":
        endpoint = str(action.args.get("endpoint", ""))
        if endpoint.startswith("access."):
            c = costs["call"]["access_request"]
        elif endpoint.startswith("pipeline."):
            c = costs["call"]["pipeline"]
        else:
            c = costs["call"]["default"]
        return float(c["compute"]), float(c["io"])
    if action.kind == "compute":
        c = costs["compute"]
        d = max(1, draws or int(action.args.get("draws", 1)))
        return float(c["compute_per_draw"] * d), float(c["io_per_draw"] * d)
    if action.kind == "continue_current":
        c = costs["continue_current"]
        return float(c["compute"]), float(c["io"])
    if action.kind == "abort":
        c = costs["abort"]
        return float(c["compute"]), float(c["io"])
    raise ValueError(f"unhandled primitive {action.kind!r}")
