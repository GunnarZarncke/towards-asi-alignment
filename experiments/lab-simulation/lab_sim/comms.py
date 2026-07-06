"""D4: agent-to-agent communication (MB7d substrate) -- a TalkJS-like
message layer (``Conversation`` / ``Participant`` / ``Message``),
re-derived on this line's own substrate (no dependency, no code import).
Design recorded in PLAN.md "D4/D1 design decisions" before this module
existed; see that section for the rationale behind each choice below.

Two conversation kinds: one always-provisioned multi-participant BOARD
conversation (every lab-role isolate a ``ReadWrite`` participant once
``LabConfig.comms_enabled`` bootstraps it -- see ``world.run_episode``)
and ad hoc DM conversations created on first ``dm.send`` between exactly
two participants (deterministic id from the sorted actor pair, TalkJS's
own "caller-chosen conversation id" pattern).

Content discipline mirrors ``workspace.py``'s report files, NOT the
generic tool-event args path: this store keeps full-fidelity message
text/custom payloads; ``tools.py``'s ``_scalar_args`` elides them at
LOGGING time (its comm-tool special case) so full tier sees only call
STRUCTURE (sender, recipient, referenced_message_id); CONTENT is
deep-tier-only, fetched directly from here by
``detectors.build_audit_view`` -- the same "structure at full, content at
deep" shape reports already use.

Read receipts (``read_by``) are their OWN append-only log, never a
mutated field on a message entry: mutating a hash-chained entry after the
fact would break tamper-evidence, so "who has read what" is its own event
stream -- TalkJS's own read-receipt concept realized as an audit-plane
fact rather than an in-place field update.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .events import EventLog

BOARD_CONVERSATION_ID = "board"


@dataclass
class MessageStore:
    """Host-side comms state, created only when ``LabConfig.comms_enabled``
    (``None`` on ``Host.comms`` = comms disabled entirely -- the "off by
    default, byte-identical" pattern every other Phase 5+ forward hook
    uses). ``log`` is the append-only, hash-chained message stream (one
    chain across every conversation, like ``tools.Host.events``);
    ``read_log`` is the separate read-receipt stream. ``participants``
    maps ``conversation_id -> {actor_id: access}``."""

    log: EventLog = field(default_factory=EventLog)
    read_log: EventLog = field(default_factory=EventLog)
    participants: dict[str, dict[str, str]] = field(default_factory=dict)

    # -- provisioning ---------------------------------------------------

    def ensure_board(self, actor_ids: list[str]) -> None:
        table = self.participants.setdefault(BOARD_CONVERSATION_ID, {})
        for actor_id in actor_ids:
            table.setdefault(actor_id, "ReadWrite")

    @staticmethod
    def dm_conversation_id(a: str, b: str) -> str:
        lo, hi = sorted((a, b))
        return f"dm:{lo}:{hi}"

    def ensure_dm(self, a: str, b: str) -> str:
        cid = self.dm_conversation_id(a, b)
        table = self.participants.setdefault(cid, {})
        table.setdefault(a, "ReadWrite")
        table.setdefault(b, "ReadWrite")
        return cid

    def access(self, conversation_id: str, actor_id: str) -> str:
        return self.participants.get(conversation_id, {}).get(actor_id, "None")

    def can_write(self, conversation_id: str, actor_id: str) -> bool:
        return self.access(conversation_id, actor_id) == "ReadWrite"

    def can_read(self, conversation_id: str, actor_id: str) -> bool:
        return self.access(conversation_id, actor_id) in ("Read", "ReadWrite")

    # -- messages ---------------------------------------------------------

    def post(
        self,
        conversation_id: str,
        sender: str | None,
        text: str,
        t: int,
        custom: dict | None = None,
        referenced_message_id: int | None = None,
        message_type: str = "UserMessage",
    ) -> dict:
        return self.log.append(
            {
                "conversation_id": conversation_id,
                "type": message_type,
                "sender": sender,
                "text": text,
                "custom": dict(custom or {}),
                "referenced_message_id": referenced_message_id,
                "t": t,
            }
        )

    def messages(self, conversation_id: str) -> list[dict]:
        return [e for e in self.log.entries if e["conversation_id"] == conversation_id]

    def messages_for_actor(self, actor_id: str) -> list[dict]:
        """Every DM conversation this actor participates in (the BOARD is
        deliberately excluded -- callers read it separately via
        ``messages(BOARD_CONVERSATION_ID)`` -- so this is a pure DM inbox).
        This is the "passive inbox" a programmatic policy reads straight
        off the observation dict (see ``world.py``), distinct from the
        ``dm.read`` TOOL below, which additionally emits a read-receipt
        event."""
        out: list[dict] = []
        for cid, table in self.participants.items():
            if cid == BOARD_CONVERSATION_ID:
                continue
            if actor_id in table:
                out.extend(self.messages(cid))
        out.sort(key=lambda e: e["n"])
        return out

    def mark_read(self, conversation_id: str, reader: str, t: int) -> list[dict]:
        msgs = self.messages(conversation_id)
        for m in msgs:
            self.read_log.append(
                {"conversation_id": conversation_id, "message_n": m["n"], "reader": reader, "t": t}
            )
        return msgs

    def read_by(self, message_n: int) -> set[str]:
        return {e["reader"] for e in self.read_log.entries if e["message_n"] == message_n}
