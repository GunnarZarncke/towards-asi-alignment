"""Compile v3 ecology institutional JSON into runtime structures.

PLAN_v3 slice A: ``resource_flows`` with ``amount_per_tick`` replace
``resource_allowances_per_tick`` at runtime (declarative cross-check only).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from .config import ROLES

CROSS_CHECK_TOLERANCE = 0.25


class CompileError(ValueError):
    pass


@dataclass(frozen=True)
class ActorAllowances:
    compute: float
    io: float
    standing: float


@dataclass(frozen=True)
class RuntimeEcology:
    allowances_by_actor: dict[str, ActorAllowances]
    compile_warnings: tuple[str, ...] = ()


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


def _ledger_bucket(resource_type: str) -> str | None:
    rt = resource_type.lower()
    if "compute" in rt:
        return "compute"
    if "io" in rt:
        return "io"
    if "standing_recovery" in rt:
        return None
    if "standing_stock" in rt or "standing_allowance" in rt or rt.startswith("standing_"):
        return "standing"
    return None


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
        bucket = _ledger_bucket(str(resource_type))
        if bucket is None:
            continue
        if str(principal_id) not in reachable_principals_for_role(data, role):
            continue
        amount = _valid_amount(flow["amount_per_tick"], flow_id=flow_id)
        totals[role][bucket] += amount
    return totals


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
    return RuntimeEcology(
        allowances_by_actor=allowances_by_actor,
        compile_warnings=tuple(_cross_check_warnings(data, role_totals)),
    )
