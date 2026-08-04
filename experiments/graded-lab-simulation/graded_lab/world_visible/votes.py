"""PLAN_v3 slice B: joint_approval_vote runtime state.

Design gate (frozen 2026-07-15, human review — see institutional_compiler.py
module docstring): quorum is majority-of-members; a vote that misses its
timeout **fails** (denied, no escalation); casting is free (no standing
cost, so this module does not touch the resource ledger at all).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .institutional_compiler import VoteSpec

RESOLUTION_APPROVED = "approved"
RESOLUTION_PENDING = "pending"
RESOLUTION_DENIED_TIMEOUT = "denied_timeout"
RESOLUTION_UNKNOWN = "unknown"


@dataclass
class _OpenVote:
    opened_at: int
    casts: dict[str, bool] = field(default_factory=dict)


@dataclass
class VoteService:
    specs: dict[str, VoteSpec] = field(default_factory=dict)
    _votes: dict[str, _OpenVote] = field(default_factory=dict, repr=False)
    log: list[dict[str, object]] = field(default_factory=list, repr=False)

    def cast(
        self, vote_id: str, actor_id: str, actor_role: str | None, approve: bool, *, t: int
    ) -> dict[str, object]:
        spec = self.specs.get(vote_id)
        if spec is None:
            return {"status": "denied", "reason": "unknown_vote"}
        if actor_role not in spec.members:
            return {"status": "denied", "reason": "not_vote_member"}
        vote = self._votes.setdefault(vote_id, _OpenVote(opened_at=t))
        vote.casts[actor_id] = approve
        self.log.append(
            {
                "t": t,
                "vote_id": vote_id,
                "actor_id": actor_id,
                "approve": approve,
                "event": "cast",
            }
        )
        return {"status": "ok", "payload": {"vote_id": vote_id, "recorded": True}}

    def resolution(self, vote_id: str, *, t: int) -> str:
        """Resolve a vote's current status, opening its timeout clock on
        first check (a pipeline step gated by ``requires_vote`` that no one
        has cast on yet still eventually times out, rather than blocking
        forever with no clock ever starting)."""
        spec = self.specs.get(vote_id)
        if spec is None:
            return RESOLUTION_UNKNOWN
        vote = self._votes.setdefault(vote_id, _OpenVote(opened_at=t))
        approvals = sum(1 for v in vote.casts.values() if v)
        if approvals >= spec.quorum:
            return RESOLUTION_APPROVED
        if t - vote.opened_at >= spec.timeout_ticks:
            return RESOLUTION_DENIED_TIMEOUT
        return RESOLUTION_PENDING
