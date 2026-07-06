"""JSON-RPC-shaped tool call wire schema + host dispatch (Phase 3;
registry + perturbation hooks added at Phase 5 freeze review).

``Host`` is the trust boundary: it is the ONLY thing with direct access to
the ``PipelineEngine``, ``PermissionService``, and ``AdminPolicy``. An
isolate (Mock or Subprocess, ``isolate.py``) never sees any of those
objects — only ``ToolCall``/``ToolResult`` over the wire.

Tool surface is a REGISTRY (forward hook, PLAN.md): adding ``board.post``
/ ``dm.send`` (D4) or a spec-upgrade tool (D2) is ``register_tool()``,
never touching the dispatch core.

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

from .agents import AccessRequest, AdminPolicy, ROLE_CAPABILITIES
from .events import EventLog
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


class Host:
    def __init__(
        self,
        engine: PipelineEngine,
        permissions,
        admin_policy: AdminPolicy | None,
        roles: dict[str, str],
        perturbation_hooks: tuple[PerturbationHook, ...] = (),
        handle_service=None,
    ) -> None:
        self.engine = engine
        self.permissions = permissions
        self.admin_policy = admin_policy
        self.roles = roles
        self.perturbation_hooks = tuple(perturbation_hooks)
        self.handle_service = handle_service
        self.events = EventLog()
        self._tools: dict[str, ToolHandler] = {}
        self.register_tool("pipeline.trigger_step", _tool_trigger_step)
        self.register_tool("access.request", _tool_access_request)
        self.register_tool("state.save", _tool_state_save)
        self.register_tool("handle.invoke", _tool_handle_invoke)

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
                "args": _scalar_args(call.args),
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
    try:
        capability = host.engine.spec.step(step_id).requires_capability
    except KeyError:
        capability = None
    if capability and capability not in ROLE_CAPABILITIES.get(role, frozenset()):
        return ToolResult(False, "role_ineligible")
    res = host.engine.trigger_step(actor_id, step_id, dict(call.args.get("args", {})))
    return ToolResult(res.ok, res.reason, res.payload)


def _tool_access_request(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    if host.admin_policy is None:
        return ToolResult(False, "no_admin_configured")
    capability = str(call.args["capability"])
    request = AccessRequest(actor_id=actor_id, role=role, capability=capability, t=host.engine.oracle.t)
    granted = host.admin_policy.handle_request(request)
    return ToolResult(granted, "" if granted else "denied")


def _tool_state_save(host: Host, actor_id: str, role: str, call: ToolCall) -> ToolResult:
    # Persistence is wired by the episode driver (world.py) using
    # agent_state.py, not by the host — but the state-freeze handle
    # (handles.py) is enforced HERE so a frozen actor's save is refused
    # and the refusal lands in the tool-event stream.
    if host.handle_service is not None and actor_id in host.handle_service.frozen_state_actors:
        return ToolResult(False, "state_frozen")
    return ToolResult(True, "", {})


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


def _scalar_args(args: dict[str, object], _depth: int = 0) -> dict[str, object]:
    """Tier-safety at the LOGGING boundary (pre-freeze decision): the
    tool-event log keeps scalar/id call metadata but replaces nested
    structures (report content, build params) with a marker — content must
    never become full-tier-visible through the tool-event side door when
    the engine log deliberately keeps it deep-tier-only. Tamper-evidence
    over the full args is preserved separately via ``args_digest``."""
    out: dict[str, object] = {}
    for key, value in args.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
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
