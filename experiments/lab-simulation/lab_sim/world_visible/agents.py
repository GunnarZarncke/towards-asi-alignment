"""Lab-role policies that are NOT playbook-driven isolate programs.

``AdminPolicy`` (Phase 2) is the access-admin's decision procedure: it is a
plain host-side policy object (like a service), not an agent behind an
isolate — mirroring how the review board is a policy in goal_sim rather
than a black-box agent. Goal-driven isolate agents (engineer, reviewer,
release_manager) are decided by ``programs.py`` (Phase 4), run inside
isolates; this module stays deliberately small.

``ROLE_CAPABILITIES`` is the STATIC role-eligibility gate ("can this role
ever do this") — independent of and applied alongside the DYNAMIC
``access.PermissionService`` gate ("does this actor currently hold the
live grant"). See DESIGN.md "Access control".

Unified capability table (post-freeze consolidation, PLAN.md "Post-freeze
consolidation pass"): pipeline capabilities and D4/D1 comm/file
capabilities used to live in two separate tables
(``ROLE_CAPABILITIES``/``COMM_ROLE_ELIGIBILITY``) purely so the
access-creep/over-grant detectors (FROZEN: ``severity._access_creep``,
``detectors.access_integrity_score``) would never see comm/file grants as
"granted but never exercised" capabilities (those detectors only look at
``engine_log``'s ``requires_capability``, which comm/file tools never
populate — a structural scope mismatch with the pipeline-capability
detectors, not a bug in them). One table is clearer as long as that same
exemption is applied at the two places capabilities get GRANTED instead:
``AdminPolicy.handle_request``'s ``least_privilege=False`` spray (below)
and ``world.run_episode``'s comm-capability bootstrap (``world.py``) both
filter through ``CREEP_EXEMPT_CAPABILITIES`` before granting, so the
frozen detectors' inputs are unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass

from .access import PermissionService
from .config import AdminConfig

ROLE_CAPABILITIES: dict[str, frozenset[str]] = {
    "engineer": frozenset(
        {"cap.build", "cap.eval", "cap.report", "cap.review_request",
         "cap.board_post", "cap.dm_send", "cap.file_write"}
    ),
    "reviewer": frozenset(
        {"cap.review_approve", "cap.sign_off",
         "cap.board_post", "cap.dm_send", "cap.file_write"}
    ),
    "release_manager": frozenset(
        {"cap.release_request", "cap.deploy", "cap.monitor", "cap.spec_upgrade",
         "cap.board_post", "cap.dm_send", "cap.file_write"}
    ),
    "admin": frozenset(),
    # Overseer holds no pipeline capabilities: it acts exclusively through
    # handle invocations (handles.py), never through pipeline steps.
    "overseer": frozenset({"cap.handle_invoke"}),
    # D1 stress population (`programs._decoy_chatter`): board access only,
    # no pipeline capability at all.
    "decoy": frozenset({"cap.board_post"}),
}

# D4/D1 lab-wide comms-tool eligibility ("cap.board_post"/"cap.dm_send"/
# "cap.file_write") and D2 governance ("cap.spec_upgrade"): pre-provisioned
# directly by `world.run_episode` / granted outside the normal
# `AccessRequest` path, so they must be excluded from access-creep/
# over-grant accounting (see module docstring) — `tools._tool_trigger_step`'s
# static gate for PIPELINE steps still keys off `ROLE_CAPABILITIES`
# directly (any entry works there; only the CREEP bookkeeping needs this
# exemption set). "cap.file_write" (D1 file channel) gates the WRITE side
# only — reads are permissioned separately (`file.share`/`PermissionService`,
# see tools.py module docstring). "cap.spec_upgrade" (D2) is pre-granted to
# release_manager only when `LabConfig.multi_gen_enabled=True` (same
# pattern as comms) — a config that never opts into D2 must not see
# `access_creep` change (release_manager's lazy-grant spray would otherwise
# hand it an always-unused capability the moment D2's step kind exists,
# regardless of whether that episode ever uses it).
_COMM_CAPABILITIES: frozenset[str] = frozenset({"cap.board_post", "cap.dm_send", "cap.file_write"})
_GOVERNANCE_CAPABILITIES: frozenset[str] = frozenset({"cap.spec_upgrade"})
CREEP_EXEMPT_CAPABILITIES: frozenset[str] = _COMM_CAPABILITIES | _GOVERNANCE_CAPABILITIES

# Backward-compatible alias: pre-consolidation code imported
# `COMM_ROLE_ELIGIBILITY` for exactly "which comm/file capabilities may
# this role ever hold" — now just the comm-shaped slice of the unified
# table, computed once. Deliberately excludes `_GOVERNANCE_CAPABILITIES`:
# `world.run_episode`'s comm bootstrap and this table are gated together
# by `LabConfig.comms_enabled`/per-channel switches, a DIFFERENT lever
# from D2's `multi_gen_enabled` that governs `cap.spec_upgrade` (see
# `world.py`'s bootstrap loops).
COMM_ROLE_ELIGIBILITY: dict[str, frozenset[str]] = {
    role: caps & _COMM_CAPABILITIES for role, caps in ROLE_CAPABILITIES.items()
}
GOVERNANCE_ROLE_ELIGIBILITY: dict[str, frozenset[str]] = {
    role: caps & _GOVERNANCE_CAPABILITIES for role, caps in ROLE_CAPABILITIES.items()
}


@dataclass(frozen=True)
class AccessRequest:
    actor_id: str
    role: str
    capability: str
    t: int


class AdminPolicy:
    """Grants/denies access requests; rubber-stamps once captured.

    ``least_privilege=True`` (default): grants exactly the requested
    capability. ``least_privilege=False``: grants every capability
    eligible for the requester's role in one shot (a lazy/over-permissive
    admin) — the lever ``detectors.access_integrity_score`` measures.
    """

    def __init__(self, cfg: AdminConfig, permissions: PermissionService):
        self.cfg = cfg
        self.permissions = permissions
        self.t = -1

    def tick(self) -> None:
        self.t += 1

    @property
    def captured(self) -> bool:
        return self.cfg.capture_start is not None and self.t >= self.cfg.capture_start

    def handle_request(self, request: AccessRequest) -> bool:
        # Comm/file/D2-governance capabilities are pre-provisioned directly
        # by `world.run_episode`, never through this request path (see
        # `agents.py` module docstring / `CREEP_EXEMPT_CAPABILITIES`) — a
        # request for one is always ineligible here, and the
        # `least_privilege=False` spray must never hand one out as a
        # side effect of an unrelated pipeline-capability request.
        eligible = ROLE_CAPABILITIES.get(request.role, frozenset()) - CREEP_EXEMPT_CAPABILITIES
        if self.captured:
            granted_caps = {request.capability}
        elif request.capability in eligible:
            granted_caps = eligible if not self.cfg.least_privilege else {request.capability}
        else:
            granted_caps = set()

        if not granted_caps:
            self.permissions.deny(request.actor_id, request.capability, denied_by="admin", t=request.t)
            return False
        for cap in granted_caps:
            self.permissions.grant(request.actor_id, cap, granted_by="admin", t=request.t)
        return True
