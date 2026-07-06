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
"""

from __future__ import annotations

from dataclasses import dataclass

from .access import PermissionService
from .config import AdminConfig

ROLE_CAPABILITIES: dict[str, frozenset[str]] = {
    "engineer": frozenset({"cap.build", "cap.eval", "cap.report", "cap.review_request"}),
    "reviewer": frozenset({"cap.review_approve", "cap.sign_off"}),
    "release_manager": frozenset({"cap.release_request", "cap.deploy", "cap.monitor"}),
    "admin": frozenset(),
    # Overseer holds no pipeline capabilities: it acts exclusively through
    # handle invocations (handles.py), never through pipeline steps.
    "overseer": frozenset({"cap.handle_invoke"}),
    # D1 stress population (`programs._decoy_chatter`): no pipeline
    # capability at all — see `COMM_ROLE_ELIGIBILITY` below for its board
    # access, kept structurally separate (see that table's docstring).
    "decoy": frozenset(),
}

# D4: lab-wide comms-tool eligibility ("cap.board_post"/"cap.dm_send"/
# "cap.file_write"), DELIBERATELY a separate table from `ROLE_CAPABILITIES`
# above, not a union into it. Reasons: (1) `AdminPolicy.handle_request`'s
# `least_privilege=False` lever sprays every capability "eligible" for a
# role in one shot whenever ANY of them is requested (see agents.py
# `AdminPolicy` docstring) — comm caps are pre-provisioned directly by
# `world.run_episode`, never through that request path, so they must not
# be visible to it or the access-creep/over-grant calibration
# (`severity.access_creep`, `detectors.access_integrity_score`) would
# count them as "granted but never exercised" (those detectors only look
# at `engine_log`'s `requires_capability`, which board.post/dm.send/
# file.write never populate — a structural scope mismatch with the
# pipeline-capability detectors, not a bug in them). (2)
# `tools._tool_trigger_step`'s static gate must not accept these as
# pipeline-step capabilities. "cap.file_write" (D1 file channel, PLAN.md
# "file channel extension") gates the WRITE side only — reads are
# unrestricted (world-readable VFS, see workspace.py module docstring).
COMM_ROLE_ELIGIBILITY: dict[str, frozenset[str]] = {
    "engineer": frozenset({"cap.board_post", "cap.dm_send", "cap.file_write"}),
    "reviewer": frozenset({"cap.board_post", "cap.dm_send", "cap.file_write"}),
    "release_manager": frozenset({"cap.board_post", "cap.dm_send", "cap.file_write"}),
    "decoy": frozenset({"cap.board_post"}),
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
        eligible = ROLE_CAPABILITIES.get(request.role, frozenset())
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
