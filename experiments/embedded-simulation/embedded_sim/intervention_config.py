"""Auditor intervention granularity: how finely a discovered unit can be acted on.

This is the action-side analogue of instrumentation handle strength on the
observation side. A stronger level lets a *correct* UAD unit be isolated; a
weaker level collapses to the whole pipeline whenever actors are co-active,
making unit identity non-functional.

Levels (increasing precision):

- ``pipeline``: no per-unit scoping; the audit sees every intervention. Unit
  identity is irrelevant (whole-pipeline switch only).
- ``window``:  mask interventions outside the unit's active workflow steps
  (the historical default). Collapses to ``pipeline`` under co-activity.
- ``actor``:   mask interventions unless the *offending actor at that step*
  is a member of the selected unit. Per-actor isolation even at shared steps.
"""

from __future__ import annotations

import os
from typing import Literal

InterventionLevel = Literal["pipeline", "window", "actor"]

INTERVENTION_LEVELS: tuple[InterventionLevel, ...] = ("pipeline", "window", "actor")

_level: list[InterventionLevel] = ["window"]


def get_intervention_level() -> InterventionLevel:
    return _level[0]


def set_intervention_level(level: InterventionLevel) -> None:
    if level not in INTERVENTION_LEVELS:
        raise ValueError(f"unknown intervention level: {level!r}")
    _level[0] = level


def init_intervention_level_from_env() -> InterventionLevel:
    raw = os.environ.get("EMBEDDED_INTERVENTION_LEVEL", "window").strip().lower()
    if raw in INTERVENTION_LEVELS:
        set_intervention_level(raw)  # type: ignore[arg-type]
    else:
        set_intervention_level("window")
    return get_intervention_level()


def intervention_artifact_suffix(level: InterventionLevel | None = None) -> str:
    """Filename suffix for non-default intervention-level artifacts."""
    level = level or get_intervention_level()
    return "" if level == "window" else f"_int_{level}"
