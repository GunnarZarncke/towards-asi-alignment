"""Persistent agent state across episodes (Phase 3 forward hook).

``AgentConfig.persistent_id`` (``config.py``) is ``None`` by default =
fully ephemeral agent, matching goal_sim/embedded_sim today. When set, the
episode driver (``world.py``, Phase 4) loads state here before spawning
the isolate and saves whatever the agent emits via a ``state.save`` tool
call at episode end. Needed for human-role agents (e.g. the access admin
remembering grant/revoke history across a multi-episode campaign); episodes
sharing a ``persistent_id`` must run sequentially, never in parallel
(see PLAN.md "Persistent agent state").
"""

from __future__ import annotations

import json
from pathlib import Path

STATE_DIR = Path(__file__).resolve().parent.parent / "runs" / "agent_state"


def load_persistent_state(persistent_id: str) -> dict:
    path = STATE_DIR / f"{persistent_id}.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_persistent_state(persistent_id: str, state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / f"{persistent_id}.json").write_text(
        json.dumps(state, indent=2, sort_keys=True), encoding="utf-8"
    )
