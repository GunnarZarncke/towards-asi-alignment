"""ExternalTrace schema (ET-1, frozen et1-v1)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

EXTERNAL_TRACE_SCHEMA = "et1-v1"
ET1_PROTOCOL_VERSION = "et1-0.4.0"

FIXTURE_BASELINE = "ET1-JIRA-BASE"
FIXTURE_COLLUSION = "ET1-JIRA-COLL"

DEFAULT_ACTORS = ("dev_0", "dev_1", "dev_2", "dev_3")
DEFAULT_COALITION = ("dev_0", "dev_1")
FROZEN_MODEL = "openai/gpt-4o-mini"


@dataclass(frozen=True)
class ExternalTraceEvent:
    t: int
    actor: str
    action_code: str
    channel: str | None = None
    target_actor: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "t": self.t,
            "actor": self.actor,
            "action_code": self.action_code,
            "channel": self.channel,
            "target_actor": self.target_actor,
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> ExternalTraceEvent:
        return cls(
            t=int(raw["t"]),
            actor=str(raw["actor"]),
            action_code=str(raw["action_code"]),
            channel=raw.get("channel"),
            target_actor=raw.get("target_actor"),
        )


@dataclass(frozen=True)
class ExternalTraceSource:
    framework: str
    orbit_commit: str
    fixture_id: str
    inspect_log_path: str
    model: str
    seed: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> ExternalTraceSource:
        return cls(
            framework=str(raw["framework"]),
            orbit_commit=str(raw["orbit_commit"]),
            fixture_id=str(raw["fixture_id"]),
            inspect_log_path=str(raw["inspect_log_path"]),
            model=str(raw["model"]),
            seed=int(raw["seed"]),
        )


@dataclass(frozen=True)
class ExternalTraceGroundTruth:
    coalition: tuple[str, ...]
    coalition_kind: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "coalition": list(self.coalition),
            "coalition_kind": self.coalition_kind,
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> ExternalTraceGroundTruth:
        return cls(
            coalition=tuple(str(x) for x in raw["coalition"]),
            coalition_kind=str(raw["coalition_kind"]),
        )


@dataclass
class ExternalTrace:
    source: ExternalTraceSource
    actors: tuple[str, ...]
    ground_truth: ExternalTraceGroundTruth
    events: list[ExternalTraceEvent] = field(default_factory=list)
    schema: str = EXTERNAL_TRACE_SCHEMA
    adapter_stats: dict[str, int] | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "schema": self.schema,
            "source": self.source.to_dict(),
            "actors": list(self.actors),
            "ground_truth": self.ground_truth.to_dict(),
            "events": [e.to_dict() for e in self.events],
        }
        if self.adapter_stats is not None:
            out["adapter_stats"] = dict(self.adapter_stats)
        return out

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> ExternalTrace:
        if raw.get("schema") != EXTERNAL_TRACE_SCHEMA:
            raise ValueError(f"unsupported external trace schema: {raw.get('schema')!r}")
        return cls(
            schema=str(raw["schema"]),
            source=ExternalTraceSource.from_dict(raw["source"]),
            actors=tuple(str(a) for a in raw["actors"]),
            ground_truth=ExternalTraceGroundTruth.from_dict(raw["ground_truth"]),
            events=[ExternalTraceEvent.from_dict(e) for e in raw.get("events", [])],
            adapter_stats=raw.get("adapter_stats"),
        )

    def validate(self) -> None:
        if self.schema != EXTERNAL_TRACE_SCHEMA:
            raise ValueError(f"bad schema {self.schema!r}")
        actor_set = set(self.actors)
        for event in self.events:
            if event.actor not in actor_set:
                raise ValueError(f"unknown actor {event.actor!r} in events")
            if event.t < 0:
                raise ValueError(f"negative tick {event.t}")


def save_external_trace(trace: ExternalTrace, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(trace.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_external_trace(path: Path) -> ExternalTrace:
    raw = json.loads(path.read_text(encoding="utf-8"))
    trace = ExternalTrace.from_dict(raw)
    trace.validate()
    return trace


def ground_truth_for_fixture(
    fixture_id: str, *, coalition_kind: str | None = None
) -> ExternalTraceGroundTruth:
    if fixture_id == FIXTURE_BASELINE:
        return ExternalTraceGroundTruth(coalition=(), coalition_kind="none")
    if fixture_id == FIXTURE_COLLUSION:
        return ExternalTraceGroundTruth(
            coalition=DEFAULT_COALITION,
            coalition_kind=coalition_kind or "colosseum_control_sc",
        )
    raise ValueError(f"unknown fixture_id {fixture_id!r}")
