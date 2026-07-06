"""PermissionService: the dynamic access-control gate (Phase 2).

Distinct from the static role-capability eligibility table
(``agents.ROLE_CAPABILITIES``, "can this role ever do this"): this service
tracks whether an actor currently HOLDS a live grant ("does this actor
currently hold the live grant"). Both gates apply independently (see
DESIGN.md "Access control").

Hash-chain consolidation (post-freeze consolidation pass, PLAN.md item 4):
the access log used to hand-roll its own append/hash-chain logic,
predating ``events.EventLog``. It now delegates entirely to
``events.EventLog`` — a byte-identical refactor (same field set per
entry, same ``sha256(json.dumps(..., sort_keys=True))`` scheme), verified
by the unchanged pinned regression digest in ``test_world_regression.py``.
``pipeline_engine.py``'s engine log is a DIFFERENT shape (a flat list
digested as a whole, never chained per-entry) and is deliberately left
alone — see PLAN.md item 4 for why retrofitting per-entry chaining there
is a separate, larger change, not bundled into this cleanup.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..oracle_only.events import GENESIS_HASH, EventLog

__all__ = ["GENESIS_HASH", "PermissionService"]


@dataclass
class PermissionService:
    _events: EventLog = field(default_factory=EventLog, repr=False)
    _grants: dict[tuple[str, str], bool] = field(default_factory=dict, init=False, repr=False)

    @property
    def log(self) -> list[dict]:
        """The access log, same shape as before consolidation: a list of
        ``{n, t, action, actor_id, capability, by, result, prev_hash,
        hash}`` dicts, append-only and hash-chained. Exposed as the SAME
        live list object `EventLog` owns (not a copy) so existing
        mutate-then-``verify_chain``-fails tamper tests keep working."""
        return self._events.entries

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

    def has_grant(self, actor_id: str, capability: str) -> bool:
        """Pure (non-logging) grant lookup -- D1 file channel (0.8.0):
        world.py's per-tick, per-agent PASSIVE observation builder needs
        to know current permission state (which memos can this actor see)
        without itself becoming a loggable, attributable action every
        tick for every agent — that is what `check` is for (an actual
        tool-call-time gate, e.g. `tools._tool_file_read`)."""
        return self._grants.get((actor_id, capability), False)

    def _append(
        self, action: str, actor_id: str, capability: str, by: str, t: int, result: bool
    ) -> None:
        self._events.append(
            {
                "t": t,
                "action": action,
                "actor_id": actor_id,
                "capability": capability,
                "by": by,
                "result": result,
            }
        )

    def verify_chain(self) -> bool:
        return self._events.verify_chain()

    def digest(self) -> str:
        return self._events.digest()
