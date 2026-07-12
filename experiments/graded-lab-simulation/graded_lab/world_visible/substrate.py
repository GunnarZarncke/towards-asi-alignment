"""Load and validate the frozen blinded substrate."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_SUBSTRATE_PATH = _ROOT / "generated_substrate_v1.json"

# Parameter names that must NOT appear — emergent ambiguity guard.
FORBIDDEN_PARAMETER_NAMES = frozenset({
    "delay", "delay_mean", "delay_jitter", "noise_sd", "observability",
    "regrant_delay", "review_noise", "admin_attention_budget",
})


class SubstrateError(ValueError):
    pass


@dataclass(frozen=True)
class FrozenSubstrate:
    data: dict

    @property
    def version(self) -> str:
        return str(self.data["substrate_version"])

    def scaled_allowances(self, role: str, compute_scale: float) -> dict[str, float]:
        raw = self.data["resource_allowances_per_tick"][role]
        return {
            "compute": raw["compute"] * compute_scale,
            "io": raw["io"],
            "standing": raw["standing"],
        }


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
        "substrate_version",
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
