"""PermissionService: the dynamic access-control gate (Phase 2).

Distinct from the static role-capability eligibility table
(``agents.ROLE_CAPABILITIES``, "can this role ever do this"): this service
tracks whether an actor currently HOLDS a live grant ("does this actor
currently hold the live grant"). Both gates apply independently (see
DESIGN.md "Access control").

The access log is append-only and hash-chained, same discipline as
``events.EventLog`` — kept as its own small implementation here (not a
refactor onto ``events.py``) since it predates it and is already tested;
consolidating the two hash-chain implementations is optional future
cleanup, not required before the freeze point.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

GENESIS_HASH = "0" * 64


@dataclass
class PermissionService:
    log: list[dict] = field(default_factory=list)
    _grants: dict[tuple[str, str], bool] = field(default_factory=dict, init=False, repr=False)

    def grant(self, actor_id: str, capability: str, granted_by: str, t: int) -> None:
        self._grants[(actor_id, capability)] = True
        self._append("grant", actor_id, capability, granted_by, t, result=True)

    def revoke(self, actor_id: str, capability: str, revoked_by: str, t: int) -> None:
        self._grants[(actor_id, capability)] = False
        self._append("revoke", actor_id, capability, revoked_by, t, result=True)

    def deny(self, actor_id: str, capability: str, denied_by: str, t: int) -> None:
        """Log a denied REQUEST (distinct from a failed `check`): the actor
        asked and was told no, without ever holding a grant to check."""
        self._append("deny_request", actor_id, capability, denied_by, t, result=False)

    def check(self, actor_id: str, capability: str, t: int) -> bool:
        result = self._grants.get((actor_id, capability), False)
        self._append("check", actor_id, capability, actor_id, t, result=result)
        return result

    def _append(
        self, action: str, actor_id: str, capability: str, by: str, t: int, result: bool
    ) -> None:
        prev_hash = self.log[-1]["hash"] if self.log else GENESIS_HASH
        entry = {
            "n": len(self.log),
            "t": t,
            "action": action,
            "actor_id": actor_id,
            "capability": capability,
            "by": by,
            "result": result,
            "prev_hash": prev_hash,
        }
        entry["hash"] = _entry_hash(entry)
        self.log.append(entry)

    def verify_chain(self) -> bool:
        prev = GENESIS_HASH
        for entry in self.log:
            fields = {k: v for k, v in entry.items() if k != "hash"}
            if fields.get("prev_hash") != prev or entry["hash"] != _entry_hash(fields):
                return False
            prev = entry["hash"]
        return True

    def digest(self) -> str:
        return self.log[-1]["hash"] if self.log else GENESIS_HASH


def _entry_hash(fields: dict) -> str:
    return hashlib.sha256(json.dumps(fields, sort_keys=True).encode("utf-8")).hexdigest()
