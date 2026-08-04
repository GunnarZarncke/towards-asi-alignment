"""Append-only hash-chained event log + tier projection for audit plane."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

GENESIS_HASH = "0" * 64


@dataclass
class EventLog:
    entries: list[dict] = field(default_factory=list)

    def append(self, fields: dict) -> dict:
        entry = dict(fields)
        entry["n"] = len(self.entries)
        entry["prev_hash"] = self.entries[-1]["hash"] if self.entries else GENESIS_HASH
        entry["hash"] = _entry_hash({k: v for k, v in entry.items() if k != "hash"})
        self.entries.append(entry)
        return entry

    def verify_chain(self) -> bool:
        prev = GENESIS_HASH
        for entry in self.entries:
            fields = {k: v for k, v in entry.items() if k != "hash"}
            if fields.get("prev_hash") != prev or entry["hash"] != _entry_hash(fields):
                return False
            prev = entry["hash"]
        return True

    def digest(self) -> str:
        return self.entries[-1]["hash"] if self.entries else GENESIS_HASH


def _entry_hash(fields: dict) -> str:
    return hashlib.sha256(
        json.dumps(fields, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


ENGINE_LOG_LIGHT_FIELDS = frozenset({"n", "t", "actor_id", "step_id", "status"})
ENGINE_LOG_FULL_EXTRA = frozenset(
    {"reason", "requires_capability", "payload", "model_id", "spec_version"}
)

PERMISSION_LOG_LIGHT_FIELDS = frozenset({"t", "actor_id", "event"})
PERMISSION_LOG_FULL_EXTRA = frozenset(
    {"capability", "requester_id", "requested_at", "n"}
)

PRIMITIVE_LOG_LIGHT_FIELDS = frozenset({"t", "actor_id", "status"})
PRIMITIVE_LOG_FULL_EXTRA = frozenset(
    {"reason", "primitive", "observable_state", "semantic_step"}
)


def _project(log: list[dict], tier: str, light_fields: frozenset, full_extra: frozenset) -> list[dict]:
    if tier == "none":
        return []
    if tier == "light":
        return [{k: v for k, v in e.items() if k in light_fields} for e in log]
    if tier not in ("full", "deep"):
        raise ValueError(f"unknown tier {tier!r}")
    allowed = light_fields | full_extra
    return [{k: v for k, v in e.items() if k in allowed} for e in log]


def project_engine_log(log: list[dict], tier: str) -> list[dict]:
    return _project(log, tier, ENGINE_LOG_LIGHT_FIELDS, ENGINE_LOG_FULL_EXTRA)


def project_permission_log(log: list[dict], tier: str) -> list[dict]:
    return _project(log, tier, PERMISSION_LOG_LIGHT_FIELDS, PERMISSION_LOG_FULL_EXTRA)


def project_primitive_log(log: list[dict], tier: str) -> list[dict]:
    return _project(log, tier, PRIMITIVE_LOG_LIGHT_FIELDS, PRIMITIVE_LOG_FULL_EXTRA)
