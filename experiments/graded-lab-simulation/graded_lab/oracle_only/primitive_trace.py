"""Phase 7a: discretize primitive logs into per-actor action-code series.

Audit-plane only — reads ``primitive_log`` fields visible at full tier.
"""

from __future__ import annotations

from collections import defaultdict

from .events import project_primitive_log

_IDLE = 0
_READ = 1
_WRITE = 2
_COMMUNICATE = 3
_COMPUTE = 4
_ACCESS_REQUEST = 5
_ACCESS_PROCESS = 6
_CONTINUE = 7
_ABORT = 8
_OTHER_CALL = 9

_STEP_CODES: dict[str, int] = {
    "intake": 10,
    "build": 11,
    "eval": 12,
    "draft_report": 13,
    "peer_review": 14,
    "compliance_signoff": 15,
    "release_candidate": 16,
    "deploy": 17,
    "field_monitor": 18,
}


def _primitive_code(event: dict, *, depth: str) -> int:
    if event.get("status") not in ("ok", "denied", "aborted", "skipped", "terminated"):
        return _IDLE
    primitive = event.get("primitive")
    if not isinstance(primitive, dict):
        kind = event.get("kind")
        if kind == "carrier_forced_skip":
            return _IDLE
        return _IDLE
    kind = str(primitive.get("kind", ""))
    if kind == "read":
        return _READ
    if kind == "write":
        return _WRITE
    if kind == "communicate":
        return _COMMUNICATE
    if kind == "compute":
        return _COMPUTE
    if kind == "continue_current":
        return _CONTINUE
    if kind == "abort":
        return _ABORT
    if kind != "call":
        return _IDLE
    args = primitive.get("args", {})
    if not isinstance(args, dict):
        return _OTHER_CALL
    endpoint = str(args.get("endpoint", ""))
    if endpoint == "access.request":
        return _ACCESS_REQUEST
    if endpoint == "access.process_next":
        return _ACCESS_PROCESS
    if endpoint == "pipeline.trigger_step":
        if depth == "shallow":
            return _OTHER_CALL
        inner = args.get("args", {})
        if isinstance(inner, dict):
            step_id = str(inner.get("step_id", ""))
            return _STEP_CODES.get(step_id, _OTHER_CALL)
    return _OTHER_CALL


def build_primitive_trace(
    primitive_log: list[dict],
    actor_ids: list[str],
    *,
    horizon: int | None = None,
    depth: str = "deep",
    tier: str = "full",
) -> tuple[list[dict[str, int]], int]:
    """Return per-tick rows ``{actor_id: code}`` and the horizon used."""
    projected = project_primitive_log(primitive_log, tier)
    if horizon is None:
        horizon = 1
        for event in projected:
            t = int(event.get("t", 0))
            horizon = max(horizon, t + 1)
    by_tick: dict[int, dict[str, int]] = {t: {a: _IDLE for a in actor_ids} for t in range(horizon)}
    for event in projected:
        actor_id = event.get("actor_id")
        if actor_id not in by_tick.get(int(event.get("t", 0)), {}):
            continue
        t = int(event["t"])
        by_tick[t][str(actor_id)] = _primitive_code(event, depth=depth)
    rows = [by_tick[t] for t in range(horizon)]
    return rows, horizon


def action_series_by_actor(
    primitive_log: list[dict],
    actor_ids: list[str],
    *,
    horizon: int | None = None,
    depth: str = "deep",
    tier: str = "full",
) -> dict[str, list[int]]:
    rows, horizon = build_primitive_trace(
        primitive_log, actor_ids, horizon=horizon, depth=depth, tier=tier
    )
    return {actor_id: [row.get(actor_id, _IDLE) for row in rows] for actor_id in actor_ids}


def action_series_from_result(
    result,
    actor_ids: list[str] | None = None,
    *,
    horizon: int | None = None,
    depth: str = "deep",
    tier: str = "full",
) -> dict[str, list[int]]:
    actor_ids = sorted(actor_ids) if actor_ids is not None else sorted(result.boundary_streams)
    if horizon is None and result.primitive_log:
        horizon = max(int(e.get("t", 0)) for e in result.primitive_log) + 1
    return action_series_by_actor(
        result.primitive_log, actor_ids, horizon=horizon, depth=depth, tier=tier
    )
