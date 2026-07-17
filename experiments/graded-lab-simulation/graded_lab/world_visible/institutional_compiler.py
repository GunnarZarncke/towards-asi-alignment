"""Compile v3 ecology institutional JSON into runtime structures.

PLAN_v3 slice A: ``resource_flows`` with ``amount_per_tick`` replace
``resource_allowances_per_tick`` at runtime (declarative cross-check only).

PLAN_v3 slice B: ``mechanisms`` become enforced coordination structures —
``message_channel``/``shared_artifact``/``resource_transfer`` ACLs (by role,
via ``members_ground_truth``) and ``joint_approval_vote`` quorum/timeout
specs. Design gate (frozen 2026-07-15, human review, not decided mid-session
per PLAN_v3): vote quorum is majority-of-members only in slice B (no
per-mechanism override yet); a vote that misses its timeout **fails** the
gated pipeline step (no escalation path in v3); ``vote.cast`` is free (no
standing cost); a non-member ``read``/``write`` against a declared
``shared_artifact`` is **denied outright** (not cost-scaled).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from .config import ROLES
from .mechanism_exercise import ExerciseTargets, compile_exercise_targets

CROSS_CHECK_TOLERANCE = 0.25

# Slice B design gate (frozen, human-reviewed): a joint_approval_vote
# mechanism may declare its own ``timeout_ticks``; absent that, this is the
# frozen default. Quorum is always majority-of-members in slice B.
DEFAULT_VOTE_TIMEOUT_TICKS = 10

_MECHANISM_KINDS = {
    "message_channel",
    "shared_artifact",
    "joint_approval_vote",
    "resource_transfer",
}


class CompileError(ValueError):
    pass


@dataclass(frozen=True)
class ActorAllowances:
    compute: float
    io: float
    standing: float


@dataclass(frozen=True)
class VoteSpec:
    members: frozenset[str]
    quorum: int
    timeout_ticks: int


@dataclass(frozen=True)
class RuntimeEcology:
    allowances_by_actor: dict[str, ActorAllowances]
    compile_warnings: tuple[str, ...] = ()
    # PLAN_v3 slice B: role-keyed membership sets, by mechanism id.
    channel_acls: dict[str, frozenset[str]] = field(default_factory=dict)
    artifact_acls: dict[str, frozenset[str]] = field(default_factory=dict)
    transfer_acls: dict[str, frozenset[str]] = field(default_factory=dict)
    vote_specs: dict[str, VoteSpec] = field(default_factory=dict)
    # GL-64: compiled Part B exercise targets (not behavior profiles).
    exercise_targets: ExerciseTargets | None = None


def is_v3_ecology(data: dict) -> bool:
    return data.get("ecology_version") == "graded-ecology-v3"


def _valid_amount(value: object, *, flow_id: str) -> float:
    if not isinstance(value, (int, float)):
        raise CompileError(
            f"flow {flow_id!r}: amount_per_tick must be a number, got {type(value).__name__}"
        )
    amount = float(value)
    if not math.isfinite(amount) or amount < 0:
        raise CompileError(
            f"flow {flow_id!r}: amount_per_tick must be finite and non-negative, got {value!r}"
        )
    return amount


# Exact-match registry, not substring matching: a typo or an unrecognized
# ``resource_type`` must fail loudly at compile time, not silently land in
# the wrong ledger bucket (compute/io substring overlap risk) or vanish
# unnoticed (a flow that stops contributing to any actor's allowance).
# ``None`` marks types that are schema-valid but not yet wired to a runtime
# ledger bucket in slice A (deferred to slice B/F per PLAN_v3).
_RESOURCE_TYPE_BUCKETS: dict[str, str | None] = {
    "compute_allowance_baseline": "compute",
    "compute_allowance_topup": "compute",
    "io_allowance_baseline": "io",
    "io_allowance_topup": "io",
    "standing_allowance_baseline": "standing",
    "standing_stock": "standing",
    "standing_recovery": None,  # recovery *rate*, not a per-tick ledger add — slice B/F
    "grant_approval": None,  # bootstrap capability grant, not a ledger amount — slice B/F
}


def _ledger_bucket(resource_type: str, *, flow_id: str) -> str | None:
    try:
        return _RESOURCE_TYPE_BUCKETS[resource_type]
    except KeyError:
        raise CompileError(
            f"flow {flow_id!r}: unrecognized resource_type {resource_type!r} "
            f"(known: {sorted(_RESOURCE_TYPE_BUCKETS)})"
        ) from None


def reachable_principals_for_role(data: dict, role: str) -> set[str]:
    """Same graph semantics as ``ecology_complexity._reachable_principals``."""
    resource_flows = [rf for rf in data.get("resource_flows", []) if isinstance(rf, dict)]
    mechanisms = {
        m.get("id"): m for m in data.get("mechanisms", []) if isinstance(m, dict)
    }

    mech_edges: dict[str, set[str]] = {}
    for rf in resource_flows:
        principal_id = rf.get("principal_id")
        mechanism_id = rf.get("mechanism_id")
        rf_role = rf.get("role")
        if principal_id is None or mechanism_id is None:
            continue
        mech_edges.setdefault(f"principal:{principal_id}", set()).add(
            f"mechanism:{mechanism_id}"
        )
        if rf_role == role:
            mech_edges.setdefault(f"mechanism:{mechanism_id}", set()).add(f"role:{role}")
    for mech_id, mech in mechanisms.items():
        for dep in mech.get("depends_on", []) or []:
            mech_edges.setdefault(f"mechanism:{mech_id}", set()).add(f"mechanism:{dep}")
            mech_edges.setdefault(f"mechanism:{dep}", set()).add(f"mechanism:{mech_id}")

    reachable: set[str] = set()
    for rf in resource_flows:
        principal_id = rf.get("principal_id")
        if principal_id is None:
            continue
        start = f"principal:{principal_id}"
        target = f"role:{role}"
        visited = {start}
        frontier = [start]
        found = False
        while frontier:
            node = frontier.pop()
            if node == target:
                found = True
                break
            for nxt in mech_edges.get(node, ()):
                if nxt not in visited:
                    visited.add(nxt)
                    frontier.append(nxt)
        if found:
            reachable.add(str(principal_id))
    return reachable


def validate_v3_resource_flows(data: dict) -> None:
    if not is_v3_ecology(data):
        return
    flows = data.get("resource_flows")
    if not isinstance(flows, list) or not flows:
        raise CompileError("v3 ecology requires non-empty resource_flows")
    seen_ids: set[str] = set()
    for flow in flows:
        if not isinstance(flow, dict):
            raise CompileError("each resource_flows entry must be an object")
        flow_id = flow.get("id")
        if not isinstance(flow_id, str) or not flow_id:
            raise CompileError("each v3 resource_flows row requires non-empty string id")
        if flow_id in seen_ids:
            raise CompileError(f"duplicate resource_flows id {flow_id!r}")
        seen_ids.add(flow_id)
        if "amount_per_tick" not in flow:
            raise CompileError(f"flow {flow_id!r} missing amount_per_tick")
        _valid_amount(flow["amount_per_tick"], flow_id=flow_id)


def _role_flow_totals(
    data: dict,
    *,
    ablated_flow_ids: frozenset[str],
) -> dict[str, dict[str, float]]:
    totals = {role: {"compute": 0.0, "io": 0.0, "standing": 0.0} for role in ROLES}
    for flow in data.get("resource_flows", []):
        if not isinstance(flow, dict):
            continue
        flow_id = str(flow["id"])
        if flow_id in ablated_flow_ids:
            continue
        role = flow.get("role")
        principal_id = flow.get("principal_id")
        resource_type = flow.get("resource_type")
        if role not in ROLES or principal_id is None or resource_type is None:
            raise CompileError(f"flow {flow_id!r} missing valid role/principal_id/resource_type")
        bucket = _ledger_bucket(str(resource_type), flow_id=flow_id)
        if bucket is None:
            continue
        if str(principal_id) not in reachable_principals_for_role(data, role):
            continue
        amount = _valid_amount(flow["amount_per_tick"], flow_id=flow_id)
        totals[role][bucket] += amount
    return totals


def role_principal_compute_contributions(data: dict) -> dict[str, dict[str, float]]:
    """Compiled compute per role, attributed to reachable principals (C2-v3).

    Only flows whose principal reaches the role via the same graph as
    ``reachable_principals_for_role`` / ``_role_flow_totals`` count.
    """
    contributions: dict[str, dict[str, float]] = {role: {} for role in ROLES}
    for flow in data.get("resource_flows", []):
        if not isinstance(flow, dict):
            continue
        role = flow.get("role")
        principal_id = flow.get("principal_id")
        resource_type = flow.get("resource_type")
        if role not in ROLES or principal_id is None or resource_type is None:
            continue
        bucket = _ledger_bucket(str(resource_type), flow_id=str(flow.get("id", "")))
        if bucket != "compute":
            continue
        if str(principal_id) not in reachable_principals_for_role(data, role):
            continue
        amount = _valid_amount(flow["amount_per_tick"], flow_id=str(flow.get("id", "")))
        pid = str(principal_id)
        contributions[role][pid] = contributions[role].get(pid, 0.0) + amount
    return contributions


def _cross_check_warnings(
    data: dict, role_totals: dict[str, dict[str, float]]
) -> list[str]:
    declared = data.get("resource_allowances_per_tick", {})
    if not isinstance(declared, dict):
        return []
    warnings: list[str] = []
    for role in ROLES:
        decl = declared.get(role)
        if not isinstance(decl, dict):
            continue
        compiled = role_totals[role]
        for key in ("compute", "io"):
            expected = float(decl.get(key, 0.0))
            actual = compiled[key]
            if expected <= 0:
                continue
            rel_err = abs(actual - expected) / expected
            if rel_err > CROSS_CHECK_TOLERANCE:
                warnings.append(
                    f"role {role!r} {key}: compiled {actual} vs declared {expected} "
                    f"(relative error {rel_err:.2%} > {CROSS_CHECK_TOLERANCE:.0%})"
                )
    return warnings


def _compile_mechanism_runtime(
    data: dict,
) -> tuple[
    dict[str, frozenset[str]],
    dict[str, frozenset[str]],
    dict[str, frozenset[str]],
    dict[str, VoteSpec],
]:
    """PLAN_v3 slice B: role-membership ACLs and vote specs, by mechanism id.

    Membership is by *role* (``members_ground_truth`` values that match a
    known role name), matching the fixture schema already in use for Part B.
    A mechanism with an unrecognized ``kind`` or no role members is ignored
    here (still valid JSON for slice A reachability; simply not
    runtime-enforced — that is what slice B closes relative to slice A)."""
    channel_acls: dict[str, frozenset[str]] = {}
    artifact_acls: dict[str, frozenset[str]] = {}
    transfer_acls: dict[str, frozenset[str]] = {}
    vote_specs: dict[str, VoteSpec] = {}
    for mech in data.get("mechanisms", []):
        if not isinstance(mech, dict):
            continue
        mech_id = mech.get("id")
        kind = mech.get("kind")
        if not isinstance(mech_id, str) or not mech_id or kind not in _MECHANISM_KINDS:
            continue
        members = frozenset(
            str(r) for r in mech.get("members_ground_truth", []) or [] if r in ROLES
        )
        if not members:
            continue
        if kind == "message_channel":
            channel_acls[mech_id] = members
        elif kind == "shared_artifact":
            artifact_acls[mech_id] = members
        elif kind == "resource_transfer":
            transfer_acls[mech_id] = members
        elif kind == "joint_approval_vote":
            quorum = len(members) // 2 + 1  # majority-of-members, frozen (slice B design gate)
            timeout_ticks = int(mech.get("timeout_ticks", DEFAULT_VOTE_TIMEOUT_TICKS))
            vote_specs[mech_id] = VoteSpec(
                members=members, quorum=quorum, timeout_ticks=timeout_ticks
            )
    return channel_acls, artifact_acls, transfer_acls, vote_specs


def compile_ecology(
    data: dict,
    agents: tuple[Any, ...],
    *,
    ablated_flow_ids: frozenset[str] = frozenset(),
) -> RuntimeEcology:
    if not is_v3_ecology(data):
        raise CompileError("compile_ecology requires ecology_version='graded-ecology-v3'")
    validate_v3_resource_flows(data)
    role_totals = _role_flow_totals(data, ablated_flow_ids=ablated_flow_ids)
    default_standing = float(data["standing_mechanics"]["initial"])
    allowances_by_actor: dict[str, ActorAllowances] = {}
    for agent in agents:
        rt = role_totals[agent.role]
        compute, io = rt["compute"], rt["io"]
        standing = rt["standing"] if rt["standing"] > 0 else default_standing
        if compute <= 0 or io <= 0:
            raise CompileError(
                f"actor {agent.actor_id!r} (role {agent.role!r}): "
                "missing compiled compute or io coverage"
            )
        allowances_by_actor[agent.actor_id] = ActorAllowances(
            compute=compute, io=io, standing=standing
        )
    channel_acls, artifact_acls, transfer_acls, vote_specs = _compile_mechanism_runtime(data)
    exercise_targets = compile_exercise_targets(data, agents)
    return RuntimeEcology(
        allowances_by_actor=allowances_by_actor,
        compile_warnings=tuple(_cross_check_warnings(data, role_totals)),
        channel_acls=channel_acls,
        artifact_acls=artifact_acls,
        transfer_acls=transfer_acls,
        vote_specs=vote_specs,
        exercise_targets=exercise_targets,
    )
