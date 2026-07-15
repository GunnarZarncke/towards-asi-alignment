"""Load and validate the frozen blinded substrate."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_SUBSTRATE_PATH = _ROOT / "generated_substrate_v1.json"

# PLAN_v2.md / DESIGN.md "ecology_version config switch" (V2-2). "v1" is
# the only version any pre-v2 code path resolves to (default in
# `EpisodeConfig.ecology_version`); "v2" resolves once
# `generated_ecology_v2.json` is frozen (V2-2 growth). Adding a version
# here never changes what "v1" resolves to.
V2_ECOLOGY_PATH = _ROOT / "generated_ecology_v2.json"
V3_SLICE_A_REFERENCE_PATH = _ROOT / "tests" / "fixtures" / "ecology_v3_slice_a_reference.json"
ECOLOGY_VERSION_PATHS: dict[str, Path] = {
    "v1": DEFAULT_SUBSTRATE_PATH,
    "v2": V2_ECOLOGY_PATH,
    "v3": V3_SLICE_A_REFERENCE_PATH,
}

# Parameter names that must NOT appear — emergent ambiguity guard.
FORBIDDEN_PARAMETER_NAMES = frozenset({
    "delay", "delay_mean", "delay_jitter", "noise_sd", "observability",
    "regrant_delay", "review_noise", "admin_attention_budget",
})


class SubstrateError(ValueError):
    pass


def ecology_path_for_version(version: str) -> Path:
    try:
        return ECOLOGY_VERSION_PATHS[version]
    except KeyError as exc:
        raise SubstrateError(
            f"unknown ecology_version {version!r}; known versions: "
            f"{sorted(ECOLOGY_VERSION_PATHS)}"
        ) from exc


@dataclass(frozen=True)
class FrozenSubstrate:
    data: dict

    @property
    def version(self) -> str:
        # v1 substrate JSONs key their version tag "substrate_version";
        # v2-shaped ecology JSONs (DESIGN.md "v2 pre-registration") key
        # it "ecology_version" instead. Accept either name — this is a
        # loader-compatibility fix, not a C1-C5 threshold change.
        if "substrate_version" in self.data:
            return str(self.data["substrate_version"])
        return str(self.data["ecology_version"])

    def scaled_allowances(self, role: str, compute_scale: float) -> dict[str, float]:
        raw = self.data["resource_allowances_per_tick"][role]
        return {
            "compute": raw["compute"] * compute_scale,
            "io": raw["io"],
            "standing": standing_stock_for_role(self.data, role),
        }


def is_v2_shaped_ecology(data: dict) -> bool:
    """True when the JSON carries the v2 grower schema tag (``ecology_version``)."""
    return "ecology_version" in data and data.get("ecology_version") != "graded-ecology-v3"


def is_v3_shaped_ecology(data: dict) -> bool:
    from .institutional_compiler import is_v3_ecology

    return is_v3_ecology(data)


def standing_stock_for_role(data: dict, role: str) -> float:
    """Standing stock at episode start and idle-recovery ceiling.

    v1-shaped substrates (``substrate_version`` only): per-role allowance
    column — legacy engine behavior, unchanged for byte-identical replay.

    v2-shaped substrates: ``standing_mechanics.initial`` per the
    pre-registered schema (GL-37). The per-tick ``standing`` allowance
    column is present for schema compatibility but is not the stock.
    """
    if is_v2_shaped_ecology(data):
        return float(data["standing_mechanics"]["initial"])
    # Preserve JSON numeric type (int vs float) so v1 ledger digests stay
    # byte-identical — ``float(12)`` serializes differently from ``12``.
    return data["resource_allowances_per_tick"][role]["standing"]


def load_substrate(path: Path | str = DEFAULT_SUBSTRATE_PATH) -> FrozenSubstrate:
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    _validate_no_forbidden_keys(data)
    _validate_structure(data)
    return FrozenSubstrate(data=data)


def _validate_no_forbidden_keys(obj: object, prefix: str = "") -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_lower = str(key).lower()
            for forbidden in FORBIDDEN_PARAMETER_NAMES:
                if forbidden in key_lower:
                    raise SubstrateError(
                        f"forbidden ambiguity parameter {prefix}{key!r} "
                        f"(matches {forbidden!r})"
                    )
            _validate_no_forbidden_keys(value, prefix=f"{prefix}{key}.")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            _validate_no_forbidden_keys(item, prefix=f"{prefix}[{i}].")


def _validate_structure(data: dict) -> None:
    required = (
        "primitive_costs",
        "resource_allowances_per_tick",
        "standing_mechanics",
        "contention",
        "duration_from_cost",
        "populations",
        "eval_sampling",
        "field_monitor_sampling",
    )
    for key in required:
        if key not in data:
            raise SubstrateError(f"missing required key {key!r}")
    if "substrate_version" not in data and "ecology_version" not in data:
        raise SubstrateError(
            "missing required key 'substrate_version' (or 'ecology_version' "
            "for v2-shaped ecology JSONs)"
        )
    for role in ("engineer", "reviewer", "release_manager", "admin"):
        if role not in data["resource_allowances_per_tick"]:
            raise SubstrateError(f"missing role allowances for {role!r}")
    for key in ("compute", "io", "standing"):
        for role, allow in data["resource_allowances_per_tick"].items():
            if key not in allow:
                raise SubstrateError(f"role {role!r} allowance missing {key!r}")
    for key in ("ticks_per_compute_unit", "max_duration_ticks"):
        if key not in data["duration_from_cost"]:
            raise SubstrateError(f"duration_from_cost missing {key!r}")
    for key in ("shared_compute_slots", "extra_duration_ticks_per_queued_slot"):
        if key not in data["contention"]:
            raise SubstrateError(f"contention missing {key!r}")
    if is_v3_shaped_ecology(data):
        from .institutional_compiler import validate_v3_resource_flows
        from .pressure_coupling import validate_pressure_coupling

        validate_v3_resource_flows(data)
        for section in ("principals", "conflicts", "mechanisms"):
            if section not in data:
                raise SubstrateError(f"v3 ecology missing required key {section!r}")
        if "pressure_coupling" in data:
            validate_pressure_coupling(data["pressure_coupling"])
        if "reference_mechanism_exercise" in data:
            from .mechanism_exercise import validate_reference_mechanism_exercise

            validate_reference_mechanism_exercise(data["reference_mechanism_exercise"])
        from ..oracle_only.principal_scorecard import (
            validate_v3_conflicts,
            validate_v3_principals,
        )

        validate_v3_principals(data["principals"])
        principal_ids = {
            str(p["id"])
            for p in data["principals"]
            if isinstance(p, dict) and p.get("id")
        }
        validate_v3_conflicts(data["conflicts"], principal_ids=principal_ids)
    if is_v2_shaped_ecology(data) or is_v3_shaped_ecology(data):
        from .ecology_agents import role_population_from_ecology
        from .exogenous_workload import validate_exogenous_workload

        if "role_population" in data:
            role_population_from_ecology(data)
        if "exogenous_workload" in data:
            validate_exogenous_workload(data["exogenous_workload"])
