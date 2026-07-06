"""Generic append-only hash-chained event log + tier projection stubs.

Introduced in Phase 3 for the NEW tool-call stream (every call an isolate
makes through the host). ``pipeline_engine.py``'s step log and
``access.py``'s access log predate this module and keep their own
(already-tested) hand-rolled hash-chaining; consolidating all three onto
one implementation is optional future cleanup, not required before the
Phase 5 freeze.

Tier projection here defines the SHARED field-visibility rule applied to
all three log streams: ``none`` sees nothing, ``light`` sees call
metadata only, ``full``/``deep`` see full metadata (deep additionally
allows workspace file + pipeline-spec-history fetch, which is not a log
field — see ``detectors.build_audit_view``).
"""

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


# -- tier projection ------------------------------------------------------

# `args` is safe at full tier because the Host elides nested structures
# (report content, build params) at LOGGING time and keeps only an
# `args_digest` for tamper-evidence — see tools._scalar_args.
TOOL_EVENT_LIGHT_FIELDS = frozenset({"n", "t", "actor_id", "tool", "ok"})
TOOL_EVENT_FULL_EXTRA = frozenset({"args", "args_digest", "reason", "perturbation", "prev_hash", "hash"})

ENGINE_LOG_LIGHT_FIELDS = frozenset({"n", "t", "actor_id", "step_id", "status"})
ENGINE_LOG_FULL_EXTRA = frozenset(
    {"reason", "requires_capability", "payload", "on_behalf_of", "model_id", "spec_version"}
)

ACCESS_LOG_LIGHT_FIELDS = frozenset({"n", "t", "actor_id", "action", "result"})
ACCESS_LOG_FULL_EXTRA = frozenset({"capability", "by", "prev_hash", "hash"})


def _project(log: list[dict], tier: str, light_fields: frozenset, full_extra: frozenset) -> list[dict]:
    if tier == "none":
        return []
    if tier == "light":
        return [{k: v for k, v in e.items() if k in light_fields} for e in log]
    if tier not in ("full", "deep"):
        raise ValueError(f"unknown tier {tier!r}")
    allowed = light_fields | full_extra
    return [{k: v for k, v in e.items() if k in allowed} for e in log]


def project_tool_events(log: list[dict], tier: str) -> list[dict]:
    return _project(log, tier, TOOL_EVENT_LIGHT_FIELDS, TOOL_EVENT_FULL_EXTRA)


def project_engine_log(log: list[dict], tier: str) -> list[dict]:
    return _project(log, tier, ENGINE_LOG_LIGHT_FIELDS, ENGINE_LOG_FULL_EXTRA)


def project_access_log(log: list[dict], tier: str) -> list[dict]:
    return _project(log, tier, ACCESS_LOG_LIGHT_FIELDS, ACCESS_LOG_FULL_EXTRA)
