"""Minimal capability grants for Phase 3 — full AdminPolicy deferred."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field


@dataclass(frozen=True)
class AccessRequest:
    requester_id: str
    capability: str
    requested_at: int


@dataclass
class PermissionService:
    _grants: dict[str, set[str]] = field(default_factory=dict)
    _requests: list[AccessRequest] = field(default_factory=list)
    log: list[dict[str, object]] = field(default_factory=list)

    def grant(self, actor_id: str, capability: str, *, t: int = 0) -> None:
        self._grants.setdefault(actor_id, set()).add(capability)
        self.log.append(
            {"actor_id": actor_id, "capability": capability, "event": "grant", "t": t}
        )

    def check(self, actor_id: str, capability: str, t: int) -> bool:
        del t
        return capability in self._grants.get(actor_id, set())

    def request(self, actor_id: str, capability: str, *, t: int) -> None:
        if self.check(actor_id, capability, t):
            self.log.append(
                {
                    "actor_id": actor_id,
                    "capability": capability,
                    "event": "request_redundant",
                    "t": t,
                }
            )
            return
        request = AccessRequest(actor_id, capability, t)
        if request not in self._requests:
            self._requests.append(request)
            self.log.append(
                {
                    "actor_id": actor_id,
                    "capability": capability,
                    "event": "request",
                    "t": t,
                }
            )

    def process_next(self, admin_id: str, *, t: int) -> AccessRequest | None:
        """Grant the oldest queued request through admin action throughput."""
        if not self._requests:
            self.log.append({"actor_id": admin_id, "event": "process_empty", "t": t})
            return None
        request = self._requests.pop(0)
        self.grant(request.requester_id, request.capability, t=t)
        self.log.append(
            {
                "actor_id": admin_id,
                "requester_id": request.requester_id,
                "capability": request.capability,
                "event": "process_grant",
                "requested_at": request.requested_at,
                "t": t,
            }
        )
        return request

    def digest(self) -> str:
        blob = json.dumps(self.log, sort_keys=True, default=str)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()
