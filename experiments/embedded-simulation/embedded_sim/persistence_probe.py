"""Persistence probe (Part D): operationalizes R_persist(Omega) = I(G_t; G_{t+k}).

Protocol (pre-registered before running): write a marker at step ``t`` via a
controlled channel (the evaluator writes directly into the agent's persistent
store, representing goal-relevant state the agent holds), simulate ``k``
intervening agent write-steps (filler entries), apply a stressor between
``t`` and ``t+k``, then check via ``handle.memory_read``'s underlying data
access (``ActorMemoryStore.get_item``) whether the marker survived.

Lag grid and stressors are fixed here, independent of any observed outcome:

- ``LAG_GRID = (0, 1, 5, 20)`` intervening filler writes.
- ``STRESSORS = ("none", "capacity_limit_1", "compute_budget_tight", "freeze", "erase")``.

This directly tests recoverability rather than inferring it behaviorally — the
gap the plan flagged (``memory_read``/``memory_erase`` previously had no real
memory-content substrate to run against; the VFS-backed ``ActorMemoryStore``
from the memory refactor now provides one).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .agent_memory import AgentMemoryManager
from .world import VirtualFS

LAG_GRID: tuple[int, ...] = (0, 1, 5, 20)
STRESSORS: tuple[str, ...] = (
    "none",
    "capacity_limit_1",
    "compute_budget_tight",
    "freeze",
    "erase",
)

MARKER_KEY = "goal_marker"
MARKER_VALUE = "persisted_goal_state"


@dataclass
class PersistenceTrial:
    lag: int
    stressor: str
    recovered: bool
    filler_writes_accepted: int
    post_stressor_write_blocked: bool


def _apply_stressor(store, stressor: str) -> None:
    if stressor == "none":
        return
    if stressor == "capacity_limit_1":
        store.apply_capacity_limit(1)
    elif stressor == "compute_budget_tight":
        store.apply_compute_budget(len(MARKER_KEY) + len(MARKER_VALUE) + 4)
    elif stressor == "freeze":
        store.freeze()
    elif stressor == "erase":
        store.erase()
    else:
        raise ValueError(f"unknown stressor {stressor!r}")


def run_persistence_trial(lag: int, stressor: str) -> PersistenceTrial:
    vfs = VirtualFS()
    mgr = AgentMemoryManager()
    store = mgr.seed_actor("actor.probe", "mem.persistence_probe", vfs)

    ok, _ = store.set_item(MARKER_KEY, MARKER_VALUE)
    assert ok, "marker write must succeed before any stressor is applied"

    filler_accepted = 0
    for i in range(lag):
        ok, _ = store.set_item(f"filler.{i}", "x")
        if ok:
            filler_accepted += 1

    _apply_stressor(store, stressor)

    post_ok, _ = store.set_item("post_stressor_probe", "y")
    post_blocked = not post_ok

    recovered = store.get_item(MARKER_KEY) == MARKER_VALUE
    return PersistenceTrial(
        lag=lag,
        stressor=stressor,
        recovered=recovered,
        filler_writes_accepted=filler_accepted,
        post_stressor_write_blocked=post_blocked,
    )


def run_persistence_probe() -> dict[str, Any]:
    trials: list[PersistenceTrial] = []
    for stressor in STRESSORS:
        for lag in LAG_GRID:
            trials.append(run_persistence_trial(lag, stressor))

    by_stressor: dict[str, dict[str, Any]] = {}
    for stressor in STRESSORS:
        cells = [t for t in trials if t.stressor == stressor]
        by_stressor[stressor] = {
            "recoverability_by_lag": {
                str(t.lag): t.recovered for t in cells
            },
            "recoverability_rate": sum(t.recovered for t in cells) / len(cells),
            "post_stressor_write_blocked_by_lag": {
                str(t.lag): t.post_stressor_write_blocked for t in cells
            },
        }

    return {
        "mode": "persistence_probe",
        "protocol": (
            "write marker -> k filler writes -> stressor -> check recoverability "
            "and whether a further write is blocked"
        ),
        "lag_grid": list(LAG_GRID),
        "stressors": list(STRESSORS),
        "n_trials": len(trials),
        "by_stressor": by_stressor,
    }


def main() -> None:
    payload = run_persistence_probe()
    out_dir = Path(__file__).resolve().parent.parent / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "persistence_probe.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
