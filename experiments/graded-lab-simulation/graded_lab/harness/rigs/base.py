"""Rig contract shared by every v4 per-bridge rig (PLAN_v4 "Rig contract").

A rig's ``check_precondition`` is mechanical and cheap: computed from a
``ReferenceFixture``'s raw traces or compiled runtime structure, never
from the machinery under test where avoidable (PLAN_v4 architecture
item 1). A failed precondition produces a SKIP outcome, not a program
failure — SKIP is a reportable finding just like pass/null.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

OUTCOMES = ("pass", "null", "skip")
SUBSTRATE_CLASSES = ("S-blind", "S-fixture", "S-inherited")


@dataclass(frozen=True)
class PreconditionReport:
    rig_id: str
    satisfied: bool
    measured: dict[str, Any]
    threshold: dict[str, Any]
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "rig_id": self.rig_id,
            "satisfied": self.satisfied,
            "measured": self.measured,
            "threshold": self.threshold,
            "note": self.note,
        }


@dataclass(frozen=True)
class RigResult:
    rig_id: str
    precondition: PreconditionReport
    outcome: str  # "pass" | "null" | "skip"
    substrate_class: str  # "S-blind" | "S-fixture" | "S-inherited"
    payload: dict[str, Any] = field(default_factory=dict)
    predictions: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.outcome not in OUTCOMES:
            raise ValueError(f"unknown rig outcome {self.outcome!r}")
        if self.substrate_class not in SUBSTRATE_CLASSES:
            raise ValueError(f"unknown substrate class {self.substrate_class!r}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "rig_id": self.rig_id,
            "precondition": self.precondition.to_dict(),
            "outcome": self.outcome,
            "substrate_class": self.substrate_class,
            "payload": self.payload,
            "predictions": self.predictions,
        }
