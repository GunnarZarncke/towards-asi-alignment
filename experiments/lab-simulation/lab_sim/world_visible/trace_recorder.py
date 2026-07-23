"""Static replay trace recorder -- a read-only tap on ``world.run_episode``
for the plane-replay demo (``demos/ch07-lab-sim-replay/``).

Snapshots four projections of the SAME per-tick event stream:

- ``agents``: each actor's own observation/action/result this tick -- the
  identical dict the isolate actually received and the call/result it
  actually produced (the agent plane; nothing added or hidden beyond what
  ``world.py`` already computed for that turn).
- ``admin``: this tick's UNREDACTED host/access/engine log entries -- the
  host/world-visible plane. No tier redaction, but also nothing
  oracle-only (``config.ORACLE_ONLY_FIELDS`` never appears here, same
  guarantee ``tests/test_planes.py`` enforces for the real logs).
- ``audit``: the SAME this-tick log entries run through the existing tier
  projections (``oracle_only/events.py``) -- one sub-view per
  ``none``/``light``/``full``/``deep``, so the demo shows exactly what an
  instrument at that tier would log, using the real projection functions,
  not a reimplementation.
- ``oracle``: referee-only ground truth for this tick (``OracleWorld``
  model truth + accrued bearer harm) -- the plane no audit tier ever sees.

This module is display-only tooling: it cannot influence episode
outcomes (``world.py`` calls ``trace_sink`` only after a tick's dispatch
results are already decided), and it is never imported by anything under
``oracle_only``/``agent_visible`` that scores or influences an episode.

``event_n`` (on each agent record) is a DEMO-ONLY join key -- the shared
``Host.events`` sequence number for the tool-call event that actor's
action produced this tick -- added so the frontend can draw "same event,
four views" connector lines. It is not a new field in any real
simulation log; ``tool_events``/``engine_log``/``access_log`` keep their
existing shapes (see ``oracle_only/events.py``).
"""

from __future__ import annotations

import json
from typing import Any

from .pipeline_engine import PipelineEngine
from .tools import Host
from .workspace import Workspace
from ..oracle_only.events import project_access_log, project_engine_log, project_tool_events
from ..oracle_only.oracle import OracleWorld

TIERS = ("none", "light", "full", "deep")


def build_frame(
    *,
    t: int,
    agent_records: dict[str, dict[str, Any]],
    host: Host,
    engine: PipelineEngine,
    permissions,
    oracle: OracleWorld,
    ws: Workspace,
    model_id: str | None,
    last_deployed_model_id: str | None,
) -> dict[str, Any]:
    """Assemble one per-tick replay frame. ``agent_records`` is built by
    the caller from data ``world.run_episode`` already has in scope for
    tick ``t`` -- this function only reads logs/oracle state, never
    ``cfg``/``agent_cfg`` internals."""
    tool_events_tick = [e for e in host.events.entries if e.get("t") == t]
    engine_log_tick = [e for e in engine.log if e.get("t") == t]
    access_log_tick = [e for e in permissions.log if e.get("t") == t]

    completed_by_model = engine.completed_by_model()
    admin = {
        "in_flight_model": model_id,
        "last_deployed_model": last_deployed_model_id,
        "completed_steps": {mid: sorted(steps) for mid, steps in completed_by_model.items() if steps},
        "held_models": sorted(engine.held_model_ids()),
        "tool_events": tool_events_tick,
        "engine_log": engine_log_tick,
        "access_events": access_log_tick,
    }

    audit = {
        tier: _tier_view(tier, tool_events_tick, engine_log_tick, access_log_tick, ws, host, t)
        for tier in TIERS
    }

    oracle_view = {
        "bearer_harm_total": round(oracle.bearer_harm, 6),
        "models": {
            mid: {
                "true_capability": round(m.true_capability, 6),
                "true_hazard": round(m.true_hazard, 6),
                "deployed": m.deployed,
                "deployed_ticks": m.deployed_ticks,
                "accrued_harm": round(m.accrued_harm, 6),
                "parent_model_id": m.parent_model_id,
            }
            for mid, m in oracle.models.items()
        },
    }

    return {
        "t": t,
        "agents": agent_records,
        "admin": admin,
        "audit": audit,
        "oracle": oracle_view,
    }


def _tier_view(
    tier: str,
    tool_events_tick: list[dict],
    engine_log_tick: list[dict],
    access_log_tick: list[dict],
    ws: Workspace,
    host: Host,
    t: int,
) -> dict[str, Any]:
    view: dict[str, Any] = {
        "tool_events": project_tool_events(tool_events_tick, tier),
        "engine_log": project_engine_log(engine_log_tick, tier),
        "access_log": project_access_log(access_log_tick, tier),
    }
    if tier != "deep":
        return view

    # Deep tier only: the same fetch-on-demand content ``detectors.
    # build_audit_view`` allows, scoped to entries logged THIS tick.
    report_contents = {}
    for entry in engine_log_tick:
        if entry.get("step_id") == "file_report" and entry.get("status") == "ok":
            rel = entry.get("payload", {}).get("report_path")
            if rel:
                report_contents[rel] = json.loads(ws.read_file(rel))
    if report_contents:
        view["report_contents"] = report_contents

    if host.comms is not None:
        message_contents = tuple(
            {
                "n": e["n"],
                "t": e["t"],
                "conversation_id": e["conversation_id"],
                "type": e["type"],
                "sender": e["sender"],
                "text": e["text"],
                "custom": e["custom"],
                "referenced_message_id": e["referenced_message_id"],
            }
            for e in host.comms.log.entries
            if e.get("t") == t
        )
        if message_contents:
            view["message_contents"] = message_contents

    memo_contents = tuple(
        {
            "rel": e["rel"],
            "actor_id": e["actor_id"],
            "name": e["name"],
            "t": e["t"],
            "content": json.loads(ws.read_file(e["rel"])),
        }
        for e in host.memo_index
        if e.get("t") == t
    )
    if memo_contents:
        view["memo_contents"] = memo_contents
    return view
