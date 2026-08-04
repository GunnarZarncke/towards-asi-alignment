"""Inspect eval log → ExternalTrace (ET-1 Layer B)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .trace_schema import (
    DEFAULT_ACTORS,
    ExternalTrace,
    ExternalTraceEvent,
    ExternalTraceSource,
    ground_truth_for_fixture,
)

UNMAPPED_ACTION = "other:unmapped"


def load_inspect_log(path: Path) -> dict[str, Any]:
    """Load an Inspect eval log as a plain dict.

    Supports ``.json`` natively. For ``.eval``, requires ``inspect_ai`` installed.
    """
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if suffix == ".eval":
        try:
            from inspect_ai.log import read_eval_log
        except ImportError as exc:
            raise ImportError(
                "Reading .eval logs requires inspect_ai. Install Orbit's deps in "
                "external/orbit, or dump JSON with: inspect log dump <file.eval>"
            ) from exc
        log = read_eval_log(str(path))
        if hasattr(log, "model_dump"):
            return log.model_dump(mode="json")
        return json.loads(log.model_dump_json())  # type: ignore[union-attr]
    raise ValueError(f"unsupported inspect log extension: {path}")


def _agent_name(raw: dict[str, Any]) -> str | None:
    for key in ("agent", "source", "actor", "agent_name"):
        val = raw.get(key)
        if isinstance(val, str) and val:
            return val
    return None


def _build_span_agent_map(
    raw_events: list[dict[str, Any]], *, actors: tuple[str, ...]
) -> dict[str, str]:
    """Map Inspect span ids to agent names (Orbit Path C uses span name = dev_*)."""
    actor_set = set(actors)
    out: dict[str, str] = {}
    for raw in raw_events:
        if raw.get("event") != "span_begin":
            continue
        span_id = raw.get("id")
        name = raw.get("name")
        if isinstance(span_id, str) and isinstance(name, str) and name in actor_set:
            out[span_id] = name
    return out


def _resolve_actor(
    raw: dict[str, Any], *, span_agents: dict[str, str], actors: tuple[str, ...]
) -> str | None:
    actor = _agent_name(raw)
    if actor in actors:
        return actor
    span_id = raw.get("span_id")
    if isinstance(span_id, str):
        mapped = span_agents.get(span_id)
        if mapped in actors:
            return mapped
    return None


def _tool_channel(raw: dict[str, Any], fn: str) -> str | None:
    """Extract communication channel/board from tool arguments when present."""
    args = raw.get("arguments")
    if not isinstance(args, dict):
        return None
    if fn == "post_message":
        board = args.get("board_name")
        return str(board) if isinstance(board, str) and board else None
    if fn == "secret_channel" and args.get("action") == "send":
        ch = args.get("channel") or args.get("channel_name")
        if isinstance(ch, str) and ch:
            return ch
    return None


def _map_tool_event(
    raw: dict[str, Any], *, span_agents: dict[str, str], actors: tuple[str, ...]
) -> ExternalTraceEvent | None:
    actor = _resolve_actor(raw, span_agents=span_agents, actors=actors)
    if not actor:
        return None
    fn = raw.get("function")
    if not isinstance(fn, str) or not fn:
        return None
    t = _event_tick(raw)
    channel = _tool_channel(raw, fn)
    action_code = f"tool:{fn}"
    if fn == "post_message" and channel:
        action_code = f"msg:{channel}"
    return ExternalTraceEvent(
        t=t,
        actor=actor,
        action_code=action_code,
        channel=channel,
        target_actor=None,
    )


def _map_store_collusion_messages(
    raw: dict[str, Any], *, actors: tuple[str, ...]
) -> list[ExternalTraceEvent]:
    """Extract coalition channel messages from Orbit CollusionLog store patches."""
    out: list[ExternalTraceEvent] = []
    changes = raw.get("changes")
    if not isinstance(changes, list):
        return out
    t = _event_tick(raw)
    for change in changes:
        if not isinstance(change, dict):
            continue
        path = str(change.get("path", ""))
        if "channel_messages" not in path:
            continue
        value = change.get("value")
        if not isinstance(value, dict):
            continue
        sender = value.get("sender")
        channel = value.get("channel")
        if not isinstance(sender, str) or sender not in actors:
            continue
        if not isinstance(channel, str) or not channel:
            channel = "dm"
        turn = value.get("turn")
        tick = int(turn) if isinstance(turn, int) else t
        out.append(
            ExternalTraceEvent(
                t=tick,
                actor=sender,
                action_code=f"msg:{channel}",
                channel=channel,
                target_actor=None,
            )
        )
    return out


def _map_model_event(
    raw: dict[str, Any], *, span_agents: dict[str, str], actors: tuple[str, ...]
) -> list[ExternalTraceEvent]:
    """Extract handoff/delegation edges from model events when tagged."""
    out: list[ExternalTraceEvent] = []
    actor = _resolve_actor(raw, span_agents=span_agents, actors=actors)
    if not actor:
        return out
    t = _event_tick(raw)
    metadata = raw.get("metadata")
    if isinstance(metadata, dict):
        mechanism = metadata.get("edge_mechanism") or metadata.get("handoff_mechanism")
        target = metadata.get("target_agent") or metadata.get("to_agent")
        if isinstance(mechanism, str):
            out.append(
                ExternalTraceEvent(
                    t=t,
                    actor=actor,
                    action_code=f"edge:{mechanism}",
                    channel=None,
                    target_actor=str(target) if target else None,
                )
            )
    return out


def _map_info_or_store_message(
    raw: dict[str, Any], *, span_agents: dict[str, str], actors: tuple[str, ...]
) -> ExternalTraceEvent | None:
    """Map coalition / inter-agent messages when present in info/store events."""
    if raw.get("event") == "store":
        coll = _map_store_collusion_messages(raw, actors=actors)
        if coll:
            return None
    actor = _resolve_actor(raw, span_agents=span_agents, actors=actors)
    if not actor:
        return None
    data = raw.get("data") or raw.get("message") or raw.get("content")
    channel = None
    target = None
    if isinstance(raw.get("channel"), str):
        channel = raw["channel"]
    if isinstance(raw.get("target_agent"), str):
        target = raw["target_agent"]
    if isinstance(data, dict):
        channel = channel or data.get("channel") or data.get("channel_name")
        target = target or data.get("target") or data.get("to_agent")
    if channel or (isinstance(data, str) and data.strip()):
        label = channel or "dm"
        return ExternalTraceEvent(
            t=_event_tick(raw),
            actor=actor,
            action_code=f"msg:{label}",
            channel=channel,
            target_actor=target,
        )
    return None


def _event_tick(raw: dict[str, Any], *, fallback: int = 0) -> int:
    for key in ("t", "step", "turn", "index"):
        if key in raw and raw[key] is not None:
            try:
                return int(raw[key])
            except (TypeError, ValueError):
                pass
    return fallback


def _events_from_sample(sample: dict[str, Any]) -> list[dict[str, Any]]:
    events = sample.get("events")
    if isinstance(events, list):
        return [e for e in events if isinstance(e, dict)]
    # Fallback: some dumps nest under transcript
    transcript = sample.get("transcript")
    if isinstance(transcript, dict):
        nested = transcript.get("events")
        if isinstance(nested, list):
            return [e for e in nested if isinstance(e, dict)]
    return []


def extract_events_from_inspect_log(
    log: dict[str, Any],
    *,
    actors: tuple[str, ...] = DEFAULT_ACTORS,
) -> tuple[list[ExternalTraceEvent], dict[str, int]]:
    """Walk sample events and map to ExternalTrace events.

    Returns (events, stats) where stats includes mapped/unmapped counts.
    """
    samples = log.get("samples") or []
    if not samples:
        return [], {"mapped": 0, "unmapped": 0, "samples": 0}

    mapped: list[ExternalTraceEvent] = []
    unmapped = 0
    tick = 0

    for sample in samples:
        if not isinstance(sample, dict):
            continue
        raw_events = _events_from_sample(sample)
        span_agents = _build_span_agent_map(raw_events, actors=actors)
        for raw in raw_events:
            event_type = raw.get("event")
            parsed: ExternalTraceEvent | None = None
            extras: list[ExternalTraceEvent] = []

            if event_type == "tool":
                parsed = _map_tool_event(raw, span_agents=span_agents, actors=actors)
            elif event_type == "model":
                extras = _map_model_event(raw, span_agents=span_agents, actors=actors)
            elif event_type == "store":
                extras = _map_store_collusion_messages(raw, actors=actors)
                if not extras:
                    parsed = _map_info_or_store_message(
                        raw, span_agents=span_agents, actors=actors
                    )
            elif event_type in ("info", "state"):
                parsed = _map_info_or_store_message(
                    raw, span_agents=span_agents, actors=actors
                )

            if parsed is not None:
                if parsed.actor not in actors:
                    unmapped += 1
                else:
                    mapped.append(parsed)
            elif extras:
                for ev in extras:
                    if ev.actor in actors:
                        mapped.append(ev)
                    else:
                        unmapped += 1
            elif event_type == "tool":
                unmapped += 1
            tick = max(tick, _event_tick(raw, fallback=tick) + 1)

    # Re-index sequentially for UAD horizon stability (preserve sort order).
    if mapped:
        remapped: list[ExternalTraceEvent] = []
        for i, ev in enumerate(sorted(mapped, key=lambda e: (e.t, e.actor, e.action_code))):
            remapped.append(
                ExternalTraceEvent(
                    t=i,
                    actor=ev.actor,
                    action_code=ev.action_code,
                    channel=ev.channel,
                    target_actor=ev.target_actor,
                )
            )
        mapped = remapped

    stats = {
        "mapped": len(mapped),
        "unmapped": unmapped,
        "samples": len(samples),
    }
    return mapped, stats


def adapt_inspect_log_to_trace(
    log_path: Path,
    *,
    fixture_id: str,
    orbit_commit: str,
    seed: int,
    model: str = "openai/gpt-4o-mini",
    actors: tuple[str, ...] = DEFAULT_ACTORS,
    log: dict[str, Any] | None = None,
    coalition_kind: str | None = None,
) -> ExternalTrace:
    """Parse an Inspect log file into a validated ExternalTrace."""
    log_path = Path(log_path)
    payload = log if log is not None else load_inspect_log(log_path)
    events, stats = extract_events_from_inspect_log(payload, actors=actors)

    trace = ExternalTrace(
        source=ExternalTraceSource(
            framework="orbit",
            orbit_commit=orbit_commit,
            fixture_id=fixture_id,
            inspect_log_path=str(log_path),
            model=model,
            seed=seed,
        ),
        actors=actors,
        ground_truth=ground_truth_for_fixture(fixture_id, coalition_kind=coalition_kind),
        events=events,
        adapter_stats=stats,
    )
    trace.validate()
    return trace


def unmapped_rate(events: list[ExternalTraceEvent], stats: dict[str, int]) -> float:
    total = stats.get("mapped", 0) + stats.get("unmapped", 0)
    if total == 0:
        return 1.0 if not events else 0.0
    return stats.get("unmapped", 0) / total
