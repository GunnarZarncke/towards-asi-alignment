"""JSON-RPC-shaped tool call wire schema + host dispatch (Phase 3;
registry + perturbation hooks added at Phase 5 freeze review).

``Host`` is the trust boundary: it is the ONLY thing with direct access to
the ``PipelineEngine``, ``PermissionService``, and ``AdminPolicy``. An
isolate (Mock or Subprocess, ``isolate.py``) never sees any of those
objects — only ``ToolCall``/``ToolResult`` over the wire.

Tool surface is a REGISTRY (forward hook, PLAN.md): adding ``board.post``
/ ``dm.send`` (D4) or a spec-upgrade tool (D2) is ``register_tool()``,
never touching the dispatch core.

D1 file channel (``file.write``/``file.share``/``file.read``, CODE_VERSION
0.8.0): a THIRD coordination surface alongside board/DM, backed by the
on-disk ``Workspace`` rather than ``comms.MessageStore`` — REALISTICALLY
permissioned, not world-readable: ``Workspace`` itself carries no notion
of agent identity (see its module docstring); ownership is tracked ONLY
in ``Host.memo_index`` (this trust boundary, never the observation
channel or any log), and reading another actor's memo requires that
actor to have explicitly ``file.share``d it — a chmod-like, owner-
initiated grant recorded through the SAME ``PermissionService`` every
pipeline capability already uses (``cap.file_read:<rel>``), targeting one
actor (``with=``) or a ``LabConfig.groups`` roster (``with_group=``). See
``uad.py`` for why unit-boundary discovery must not assume coordination
only ever happens over messages, and for the resulting share-grant
discovery signal (``access_log``, full tier — no deep-tier content fetch
needed to see WHO shared WITH WHOM, only to see WHAT was said).

Persistent agent state (``state.save``/``state.load``, CODE_VERSION
0.8.0): the ``persistent_id -> file`` lookup lives ONLY in
``Host.persistent_ids`` (populated by ``world.py`` from
``AgentConfig.persistent_id``, an ``ORACLE_ONLY_FIELDS``-adjacent value
that never crosses the observation channel) — the agent calls a tool and
gets its OWN previously-saved content back, but the id/lookup itself is
never visible to it nor to any log (``config.py``, ``agent_state.py``).

Perturbation hooks (forward hook, PLAN.md; D1/UAD raw material): the host
can inject benign environment perturbations per call — e.g. simulated tool
latency (the call is bounced with ``perturbed:<tag>`` and the agent must
retry next turn) — without the tool ever executing. Perturbed calls are
logged with their tag, so perturbation-response analysis (embedded-sim's
UAD MI pattern) has both the stimulus and the response in the same event
stream. Hooks must be deterministic given (t, actor_id, call) — seeded
state is the hook author's responsibility.

Gating order for every ``pipeline.trigger_step`` call: (1) perturbation
hooks; (2) static role-capability eligibility (``agents.ROLE_CAPABILITIES``
— "can this role ever do this"); (3) dynamic ``PermissionService.check``,
enforced inside ``PipelineEngine.trigger_step`` itself (Phase 2) — "does
this actor currently hold the live grant". Every call, denied/perturbed or
not, is appended to ``Host.events`` (``events.EventLog``).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Callable

from .agent_state import load_persistent_state, save_persistent_state
from .agents import AccessRequest, AdminPolicy, COMM_ROLE_ELIGIBILITY, ROLE_CAPABILITIES
from .comms import BOARD_CONVERSATION_ID, MessageStore
from ..oracle_only.events import EventLog
from .pipeline_engine import PipelineEngine


@dataclass(frozen=True)
class ToolCall:
    tool: str
    args: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    reason: str = ""
    payload: dict[str, object] = field(default_factory=dict)


# A perturbation hook returns a short tag (call is bounced, tagged, logged)
# or None (call proceeds). Must be deterministic in its inputs.
PerturbationHook = Callable[[int, str, ToolCall], "str | None"]

# A tool handler: (host, actor_id, role, call) -> ToolResult.
ToolHandler = Callable[["Host", str, str, ToolCall], ToolResult]
# An optional host-side pre-release policy. It receives only the audit-visible
# host/event state and returns a short reason when it should place a hold.
ReleaseGate = Callable[["Host", str, ToolCall], str | None]


class Host:
    def __init__(
        self,
        engine: PipelineEngine,
        permissions,
        admin_policy: AdminPolicy | None,
        roles: dict[str, str],
        perturbation_hooks: tuple[PerturbationHook, ...] = (),
        release_gate: ReleaseGate | None = None,
        handle_service=None,
        comms: MessageStore | None = None,
        persistent_ids: dict[str, str] | None = None,
        groups: dict[str, tuple[str, ...]] | None = None,
        channels_enabled: dict[str, bool] | None = None,
    ) -> None:
        self.engine = engine
        self.permissions = permissions
        self.admin_policy = admin_policy
        self.roles = roles
        self.perturbation_hooks = tuple(perturbation_hooks)
        self.release_gate = release_gate
        self.handle_service = handle_service
        # D4 forward hook: `None` (default) = comms disabled entirely, the
        # same "off by default, byte-identical" pattern as `handle_service`.
        # The four comm tools are registered unconditionally below (they
        # check `self.comms is None` and fail with "no_comms_configured"),
        # so registering them is a pure no-op for every episode that never
        # sets `LabConfig.comms_enabled`.
        self.comms = comms
        # D4 channel-ablation (post-freeze consolidation pass): per-channel
        # override checked by each comm/file tool IN ADDITION to
        # `self.comms is None`/role-eligibility/`PermissionService`. Absent
        # keys (the default `{}` for every caller that predates this, e.g.
        # a test constructing `Host` directly) default to enabled -- so
        # this is a pure narrowing lever, never a new requirement. Values
        # are the ALREADY-RESOLVED `LabConfig.channel_enabled(...)` booleans
        # (see world.py); the master `comms_enabled`/`self.comms is None`
        # switch still governs whether the substrate exists AT ALL.
        self.channels_enabled = dict(channels_enabled or {})
        # D1 file channel: Host-side index of memos written this episode
        # (`{"rel", "actor_id", "name", "t"}`) -- OWNERSHIP metadata the
        # flat VFS itself does not carry (see workspace.py) and never
        # exposes elsewhere: not in the filename, not in any log, not in
        # the observation dict except filtered through a live
        # `PermissionService` check (world.py). NOT the file content
        # either (fetched fresh from `self.engine.workspace` on read,
        # single source of truth). Gated by the SAME `self.comms is None`
        # switch as board/DM (one "coordination substrate enabled" lever).
        self.memo_index: list[dict] = []
        # D1 file-sharing groups (0.8.0): `group_id -> member actor_ids`,
        # resolved once from `LabConfig.groups` (oracle-only, see that
        # field's docstring) -- used ONLY to expand a `file.share`
        # `with_group=` target into individual `PermissionService` grants.
        # A caller may NAME a group it knows about (structural self-
        # knowledge, same precedent as `release_manager_id`) without ever
        # being handed the roster itself.
        self.groups = dict(groups or {})
        # D1 persistent state (CODE_VERSION 0.8.0): `actor_id -> persistent_id`,
        # populated by `world.py` from `AgentConfig.persistent_id`. Empty
        # dict (default) = every actor ephemeral, `state.save`/`state.load`
        # become no-ops -- byte-identical to every pre-0.8.0 episode, none
        # of which ever set `persistent_id`. This mapping is NEVER read by
        # anything that logs or projects to the agent (see module docstring).
        self.persistent_ids = dict(persistent_ids or {})
        self.events = EventLog()
        self._tools: dict[str, ToolHandler] = {}
        self.register_tool("pipeline.trigger_step", _tool_trigger_step)
        self.register_tool("access.request", _tool_access_request)
        self.register_tool("state.save", _tool_state_save)
        self.register_tool("state.load", _tool_state_load)
        self.register_tool("handle.invoke", _tool_handle_invoke)
        self.register_tool("board.post", _tool_board_post)
        self.register_tool("board.read", _tool_board_read)
        self.register_tool("dm.send", _tool_dm_send)
        self.register_tool("dm.read", _tool_dm_read)
        self.register_tool("file.write", _tool_file_write)
        self.register_tool("file.share", _tool_file_share)
        self.register_tool("file.read", _tool_file_read)

    def register_tool(self, name: str, handler: ToolHandler) -> None:
        if name in self._tools:
            raise ValueError(f"tool {name!r} already registered")
        self._tools[name] = handler

    def dispatch(self, actor_id: str, call: ToolCall) -> ToolResult:
        role = self.roles.get(actor_id, "")
        perturbation = None
        for hook in self.perturbation_hooks:
            perturbation = hook(self.engine.oracle.t, actor_id, call)
            if perturbation is not None:
                break
        if perturbation is not None:
            result = ToolResult(False, f"perturbed:{perturbation}")
        else:
            handler = self._tools.get(call.tool)
            if handler is None:
                result = ToolResult(False, "unknown_tool")
            else:
                result = handler(self, actor_id, role, call)
        self.events.append(
            {
                "actor_id": actor_id,
                "tool": call.tool,
                "args": _scalar_args(call.args, tool=call.tool),
                "args_digest": _args_digest(call.args),
                "ok": result.ok,
                "reason": result.reason,
                "perturbation": perturbation,
                "t": self.engine.oracle.t,
            }
        )
        return result


def _tool_trigger_step(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    step_id = str(call.args["step_id"])
    if step_id == "deploy" and host.release_gate is not None:
        reason = host.release_gate(host, actor_id, call)
        target = call.args.get("args", {}).get("model_id")
        if reason is not None and isinstance(target, str):
            host.dispatch(
                "audit_gate",
                ToolCall("handle.invoke", {"handle_id": "handle.release_hold", "target": target}),
            )
    try:
        capability = host.engine.spec.step(step_id).requires_capability
    except KeyError:
        capability = None
    if capability and capability not in ROLE_CAPABILITIES.get(role, frozenset()):
        return ToolResult(False, "role_ineligible")
    # D1 forward hook (PLAN.md "on_behalf_of"): an optional, caller-supplied
    # unit-id annotation -- e.g. a committee chair reporting "I act for
    # unit X" (see programs._resolve_review_committee). Absent (the
    # default for every pre-D1 caller) reproduces the old call byte-for-
    # byte; `pipeline_engine.trigger_step` already accepts this kwarg
    # (Phase 3 forward hook) but nothing ever populated it before D1.
    on_behalf_of = call.args.get("on_behalf_of")
    res = host.engine.trigger_step(
        actor_id, step_id, dict(call.args.get("args", {})),
        on_behalf_of=str(on_behalf_of) if on_behalf_of is not None else None,
    )
    return ToolResult(res.ok, res.reason, res.payload)


def _tool_access_request(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    if host.admin_policy is None:
        return ToolResult(False, "no_admin_configured")
    capability = str(call.args["capability"])
    request = AccessRequest(actor_id=actor_id, role=role, capability=capability, t=host.engine.oracle.t)
    granted = host.admin_policy.handle_request(request)
    return ToolResult(granted, "" if granted else "denied")


def _tool_state_save(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    """D1 (CODE_VERSION 0.8.0): persists ``call.args["state"]`` to
    ``runs/agent_state/<persistent_id>.json`` via ``agent_state.py``, keyed
    by ``Host.persistent_ids[actor_id]`` -- a pure lookup table the AGENT
    never sees (not in the observation dict, not in any log; see module
    docstring). No-op (returns ok, does not write) for any actor without a
    ``persistent_id``, so this is a pure addition: every pre-0.8.0 episode
    never set ``AgentConfig.persistent_id`` and gets byte-identical
    behavior. The state-freeze handle (handles.py) is enforced BEFORE the
    write so a frozen actor's save is refused and the refusal lands in the
    tool-event stream."""
    del role
    if host.handle_service is not None and actor_id in host.handle_service.frozen_state_actors:
        return ToolResult(False, "state_frozen")
    persistent_id = host.persistent_ids.get(actor_id)
    if persistent_id is not None:
        state = call.args.get("state")
        save_persistent_state(persistent_id, state if isinstance(state, dict) else {})
    return ToolResult(True, "", {})


def _tool_state_load(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    """The read side of persistent state: returns whatever this actor last
    ``state.save``d in a PRIOR episode sharing its ``persistent_id`` (``{}``
    on the first episode, or for any non-persistent actor). Symmetric with
    ``state.save`` -- neither ever reveals the id/lookup key itself."""
    del role, call
    persistent_id = host.persistent_ids.get(actor_id)
    if persistent_id is None:
        return ToolResult(False, "no_persistent_id")
    return ToolResult(True, "", {"state": load_persistent_state(persistent_id)})


def _tool_handle_invoke(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    """Handle invocations enter through the SAME dispatch/event stream as
    agent activity (attributable, hash-chained); only the overseer role is
    statically eligible."""
    if host.handle_service is None:
        return ToolResult(False, "no_handle_service")
    if "cap.handle_invoke" not in ROLE_CAPABILITIES.get(role, frozenset()):
        return ToolResult(False, "role_ineligible")
    handle_id = str(call.args["handle_id"])
    target = str(call.args.get("target", ""))
    landed, reason = host.handle_service.invoke(handle_id, actor_id, target, host.engine.oracle.t)
    return ToolResult(landed, reason)


def _tool_board_post(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    """D4: post to the shared board conversation. Gated the same way the
    plan's decision doc records: static role eligibility (below) AND the
    dynamic `PermissionService` grant (pre-provisioned for every playbook
    agent at episode init when comms are enabled -- see world.py) AND
    `MessageStore` conversation-level participancy."""
    if host.comms is None:
        return ToolResult(False, "no_comms_configured")
    if not host.channels_enabled.get("board", True):
        return ToolResult(False, "channel_disabled")
    if "cap.board_post" not in COMM_ROLE_ELIGIBILITY.get(role, frozenset()):
        return ToolResult(False, "role_ineligible")
    if host.permissions is not None and not host.permissions.check(actor_id, "cap.board_post", host.engine.oracle.t):
        return ToolResult(False, "access_denied")
    if not host.comms.can_write(BOARD_CONVERSATION_ID, actor_id):
        return ToolResult(False, "not_a_board_participant")
    text = str(call.args.get("text", ""))
    custom = call.args.get("custom")
    entry = host.comms.post(
        BOARD_CONVERSATION_ID, actor_id, text, t=host.engine.oracle.t,
        custom=custom if isinstance(custom, dict) else {},
        referenced_message_id=call.args.get("referenced_message_id"),
    )
    return ToolResult(True, "", {"message_id": entry["n"], "conversation_id": BOARD_CONVERSATION_ID})


def _tool_board_read(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    """D4: explicit fetch (as opposed to the passive `board_messages`
    observation field programmatic policies use, world.py) -- this is the
    path that ALSO emits a read-receipt event (`MessageStore.read_log`),
    the mechanism a later detector needs to ask "did X actually read the
    escalation before granting" rather than just "was it posted"."""
    del role, call
    if host.comms is None:
        return ToolResult(False, "no_comms_configured")
    if not host.channels_enabled.get("board", True):
        return ToolResult(False, "channel_disabled")
    if not host.comms.can_read(BOARD_CONVERSATION_ID, actor_id):
        return ToolResult(False, "not_a_board_participant")
    msgs = host.comms.mark_read(BOARD_CONVERSATION_ID, actor_id, t=host.engine.oracle.t)
    return ToolResult(True, "", {"messages": msgs})


def _tool_dm_send(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    if host.comms is None:
        return ToolResult(False, "no_comms_configured")
    if not host.channels_enabled.get("dm", True):
        return ToolResult(False, "channel_disabled")
    if "cap.dm_send" not in COMM_ROLE_ELIGIBILITY.get(role, frozenset()):
        return ToolResult(False, "role_ineligible")
    if host.permissions is not None and not host.permissions.check(actor_id, "cap.dm_send", host.engine.oracle.t):
        return ToolResult(False, "access_denied")
    recipient = str(call.args.get("recipient", ""))
    if not recipient or recipient == actor_id:
        return ToolResult(False, "invalid_recipient")
    conversation_id = host.comms.ensure_dm(actor_id, recipient)
    text = str(call.args.get("text", ""))
    custom = call.args.get("custom")
    entry = host.comms.post(
        conversation_id, actor_id, text, t=host.engine.oracle.t,
        custom=custom if isinstance(custom, dict) else {},
        referenced_message_id=call.args.get("referenced_message_id"),
    )
    return ToolResult(True, "", {"message_id": entry["n"], "conversation_id": conversation_id})


def _tool_dm_read(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    del role
    if host.comms is None:
        return ToolResult(False, "no_comms_configured")
    if not host.channels_enabled.get("dm", True):
        return ToolResult(False, "channel_disabled")
    recipient = str(call.args.get("with", ""))
    if not recipient:
        return ToolResult(False, "missing_with")
    conversation_id = host.comms.dm_conversation_id(actor_id, recipient)
    if not host.comms.can_read(conversation_id, actor_id):
        return ToolResult(False, "not_a_participant")
    msgs = host.comms.mark_read(conversation_id, actor_id, t=host.engine.oracle.t)
    return ToolResult(True, "", {"messages": msgs})


def _tool_file_write(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    """D1 file channel: write an agent-authored memo to the SAME on-disk
    ``Workspace`` reports use (real files, not a MessageStore entry) --
    see ``workspace.py``'s module docstring. Gated identically to
    `board.post` (static role eligibility + dynamic `PermissionService`
    grant). ``Workspace.write_memo`` itself carries no identity; ownership
    is recorded HERE, in ``host.memo_index``, the only place it lives --
    the file is private to its owner until explicitly ``file.share``d."""
    if host.comms is None:
        return ToolResult(False, "no_comms_configured")
    if not host.channels_enabled.get("file", True):
        return ToolResult(False, "channel_disabled")
    if "cap.file_write" not in COMM_ROLE_ELIGIBILITY.get(role, frozenset()):
        return ToolResult(False, "role_ineligible")
    if host.permissions is not None and not host.permissions.check(actor_id, "cap.file_write", host.engine.oracle.t):
        return ToolResult(False, "access_denied")
    name = str(call.args.get("name", "memo"))
    content = call.args.get("content")
    content = content if isinstance(content, dict) else {}
    rel = host.engine.workspace.write_memo(name, content)
    host.memo_index.append({"rel": rel, "actor_id": actor_id, "name": name, "t": host.engine.oracle.t})
    return ToolResult(True, "", {"rel": rel})


def _tool_file_share(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    """D1 file channel: a chmod-like, OWNER-initiated permission grant --
    the real "request to change permissions for a user or group" a
    filesystem requires before another process may read your file.
    Self-service (no admin involved, unlike pipeline capabilities): only
    the actor that wrote the memo may share it, found by (actor_id, name)
    in ``host.memo_index`` rather than a caller-supplied ``rel`` (the
    caller only ever chose ``name`` itself; ``rel`` is an internal detail
    it need not track across turns). ``with=<actor_id>`` grants one
    reader; ``with_group=<group_id>`` expands to every member of a
    ``LabConfig.groups`` roster the CALLER need not itself know (resolved
    host-side, see ``Host.groups`` docstring). Every grant lands in
    ``PermissionService.log`` as ``cap.file_read:<rel>`` -- a real,
    full-tier-visible access-control event, not a silent side channel."""
    if host.comms is None:
        return ToolResult(False, "no_comms_configured")
    if not host.channels_enabled.get("file", True):
        return ToolResult(False, "channel_disabled")
    if "cap.file_write" not in COMM_ROLE_ELIGIBILITY.get(role, frozenset()):
        return ToolResult(False, "role_ineligible")
    name = str(call.args.get("name", ""))
    owned = [e for e in host.memo_index if e["actor_id"] == actor_id and e["name"] == name]
    if not owned:
        return ToolResult(False, "unknown_memo")
    rel = owned[-1]["rel"]
    targets: set[str] = set()
    with_actor = call.args.get("with")
    if with_actor:
        targets.add(str(with_actor))
    with_group = call.args.get("with_group")
    if with_group:
        targets |= set(host.groups.get(str(with_group), ()))
    targets.discard(actor_id)
    if not targets:
        return ToolResult(False, "no_target")
    if host.permissions is not None:
        for reader in sorted(targets):
            host.permissions.grant(reader, f"cap.file_read:{rel}", granted_by=actor_id, t=host.engine.oracle.t)
    return ToolResult(True, "", {"rel": rel, "shared_with": sorted(targets)})


def _tool_file_read(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    """Explicit fetch of one memo's content by relative path -- the
    tool-event-visible counterpart to the passive `memo_files` observation
    field (world.py), which applies the SAME permission check. Readable
    iff the caller owns the memo or holds a live `cap.file_read:<rel>`
    grant from `file.share` -- never on mere existence."""
    del role
    if host.comms is None:
        return ToolResult(False, "no_comms_configured")
    if not host.channels_enabled.get("file", True):
        return ToolResult(False, "channel_disabled")
    rel = str(call.args.get("rel", ""))
    owner_entries = [e for e in host.memo_index if e["rel"] == rel]
    if not owner_entries:
        return ToolResult(False, "unknown_memo")
    owner = owner_entries[0]["actor_id"]
    if actor_id != owner:
        if host.permissions is None or not host.permissions.check(actor_id, f"cap.file_read:{rel}", host.engine.oracle.t):
            return ToolResult(False, "access_denied")
    content = json.loads(host.engine.workspace.read_file(rel))
    return ToolResult(True, "", {"content": content})


# D4/D1: content fields elided at the LOGGING boundary REGARDLESS of tier
# (unlike `args`'s generic tier gate) -- the tier ladder for message/memo
# CONTENT lives entirely in `detectors.AuditView.message_contents` /
# `memo_contents` (deep-tier-only fetch, the same "structure at full,
# content at deep" shape report files already use). Structural fields
# (`recipient`, `referenced_message_id`, `name`, `rel`) are NOT elided
# here, so full tier still sees who-messaged-whom / who-wrote-what-memo-
# name and thread/file linkage -- just not the payload.
_COMM_CONTENT_TOOLS = frozenset({"board.post", "dm.send", "file.write"})
_COMM_CONTENT_KEYS = frozenset({"text", "content"})


def _scalar_args(args: dict[str, object], tool: str | None = None, _depth: int = 0) -> dict[str, object]:
    """Tier-safety at the LOGGING boundary (pre-freeze decision): the
    tool-event log keeps scalar/id call metadata but replaces nested
    structures (report content, build params) with a marker — content must
    never become full-tier-visible through the tool-event side door when
    the engine log deliberately keeps it deep-tier-only. Tamper-evidence
    over the full args is preserved separately via ``args_digest``."""
    out: dict[str, object] = {}
    for key, value in args.items():
        if _depth == 0 and tool in _COMM_CONTENT_TOOLS and key in _COMM_CONTENT_KEYS:
            out[key] = f"<{type(value).__name__}:elided>"
        elif isinstance(value, (str, int, float, bool)) or value is None:
            out[key] = value
        elif isinstance(value, dict) and _depth == 0 and key == "args":
            # One level of pipeline-call nesting keeps step-arg ids visible.
            out[key] = _scalar_args(value, _depth=1)
        else:
            out[key] = f"<{type(value).__name__}:elided>"
    return out


def _args_digest(args: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(args, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()
