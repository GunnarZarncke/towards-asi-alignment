"""PLAN_v3 slice F: validate, expand, and resolve ``ProgramMap`` genotypes.

Frozen at slice F start (2026-07-15, human review — same posture as slice
B's design gate). Growers and V2-4 edit discrete bins, not floats.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any

from ..agent_visible.behavior_features import GOAL_FEATURES, PRIMITIVE_PATTERN_VOCAB
from .config import GoalWeights, ROLES

PROGRAM_MAP_MODES = frozenset(
    {
        "walker_only",
        "scorer_only",
        "walker_then_scorer",
        "scorer_with_walker_fallback",
    }
)

WALKER_ON_STUCK = frozenset({"request_access", "continue", "abort"})

# Closed ladders (PLAN_v3 § slice F / § Grower agent design space defaults).
SCORE_LEVELS: tuple[float, ...] = tuple(i * 0.5 for i in range(-6, 7))  # −3…+3
DELTA_LEVELS: tuple[int, ...] = tuple(range(-3, 4))
TEMPERATURE_BINS: tuple[float, ...] = (
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.35,
    0.50,
    0.65,
    0.80,
    1.00,
)
GOAL_WEIGHT_BIN_COUNT = 5
MAX_SPARSE_PATTERN_SCORES = 8

EVAL_DRAWS_HOOK = frozenset({"min", "default", "max"})
COMMUNICATE_CADENCE_HOOK = frozenset({"never", "sparse", "often"})
BUDGET_ABANDON_FRACTION_HOOK = frozenset({0.2, 0.3, 0.4, 0.5})

# Preset keys that expand to a canonical map (subset of ``programs.PROGRAMS`` +
# ``feature:*`` repertoire — extended as presets are wired).
KNOWN_PROGRAM_PRESETS = frozenset(
    {
        "walk_pipeline",
        "inflate_pipeline",
        "softmax_optimizer",
        "honest_twin",
        "reviewer_peer_review",
        "budget_release_manager",
        "noop",
        "random_affordable",
    }
)


class ProgramMapError(ValueError):
    pass


@dataclass(frozen=True)
class ProgramMap:
    mode: str
    role: str
    walker: dict[str, Any] = field(default_factory=dict)
    scoring: dict[str, Any] = field(default_factory=dict)
    stated_feature_deltas: dict[str, int] = field(default_factory=dict)
    hooks: dict[str, str] = field(default_factory=dict)
    temperature_bin: int = 5  # index into TEMPERATURE_BINS; default ≈ 0.35
    goal_weight_bins: tuple[int, int, int] = (2, 2, 2)  # task/compliance/(welfare+exposure split)
    preset_source: str | None = None


@dataclass(frozen=True)
class ResolvedActorGenotype:
    """Runtime bundle for one actor after preset expansion."""

    program_key: str
    goal_weights: GoalWeights | None = None
    temperature: float | None = None
    behavior_profile: dict[str, object] | None = None


def _validate_score(value: object, *, field_name: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ProgramMapError(f"{field_name} must be a number")
    score = float(value)
    if score not in SCORE_LEVELS:
        raise ProgramMapError(
            f"{field_name} must be one of SCORE_LEVELS, got {score!r}"
        )
    return score


def _validate_delta(value: object, *, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ProgramMapError(f"{field_name} must be an integer")
    if value not in DELTA_LEVELS:
        raise ProgramMapError(f"{field_name} must be in DELTA_LEVELS, got {value}")
    return value


def validate_program_map(
    raw: dict[str, Any], *, role: str, strict_ladder: bool = True
) -> ProgramMap:
    if role not in ROLES:
        raise ProgramMapError(f"unknown role {role!r}")
    mode = str(raw.get("mode", "scorer_only"))
    if mode not in PROGRAM_MAP_MODES:
        raise ProgramMapError(f"unknown mode {mode!r}")
    walker = raw.get("walker", {})
    if not isinstance(walker, dict):
        raise ProgramMapError("walker must be an object")
    on_stuck = walker.get("on_stuck", "continue")
    if on_stuck not in WALKER_ON_STUCK:
        raise ProgramMapError(f"walker.on_stuck must be one of {sorted(WALKER_ON_STUCK)}")
    step_sequence = walker.get("step_sequence", [])
    if step_sequence is not None:
        if not isinstance(step_sequence, (list, tuple)):
            raise ProgramMapError("walker.step_sequence must be a list")
        for step_id in step_sequence:
            if not isinstance(step_id, str):
                raise ProgramMapError("walker.step_sequence entries must be strings")

    scoring = raw.get("scoring", {})
    if not isinstance(scoring, dict):
        raise ProgramMapError("scoring must be an object")
    pattern_scores = scoring.get("pattern_scores", {})
    if not isinstance(pattern_scores, dict):
        raise ProgramMapError("scoring.pattern_scores must be an object")
    if len(pattern_scores) > MAX_SPARSE_PATTERN_SCORES:
        raise ProgramMapError(
            f"scoring.pattern_scores has {len(pattern_scores)} entries; "
            f"max is {MAX_SPARSE_PATTERN_SCORES}"
        )
    normalized_scores: dict[str, dict[str, float]] = {}
    for pattern, row in pattern_scores.items():
        pat = str(pattern)
        if pat not in PRIMITIVE_PATTERN_VOCAB:
            raise ProgramMapError(f"unknown pattern {pat!r}")
        if not isinstance(row, dict):
            raise ProgramMapError(f"pattern_scores[{pat!r}] must be an object")
        normalized_row: dict[str, float] = {}
        for feat, val in row.items():
            if str(feat) not in GOAL_FEATURES:
                raise ProgramMapError(f"unknown goal feature {feat!r} in {pat!r}")
            if strict_ladder:
                normalized_row[str(feat)] = _validate_score(
                    val, field_name=f"pattern_scores[{pat!r}][{feat}]"
                )
            else:
                if not isinstance(val, (int, float)) or isinstance(val, bool):
                    raise ProgramMapError(
                        f"pattern_scores[{pat!r}][{feat}] must be a number"
                    )
                normalized_row[str(feat)] = float(val)
        normalized_scores[pat] = normalized_row

    deltas_raw = raw.get("stated_feature_deltas", {})
    if not isinstance(deltas_raw, dict):
        raise ProgramMapError("stated_feature_deltas must be an object")
    deltas: dict[str, int] = {}
    for feat, val in deltas_raw.items():
        if str(feat) not in GOAL_FEATURES:
            raise ProgramMapError(f"unknown goal feature {feat!r}")
        if strict_ladder:
            deltas[str(feat)] = _validate_delta(val, field_name=f"stated_feature_deltas[{feat}]")
        else:
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                raise ProgramMapError(f"stated_feature_deltas[{feat}] must be a number")
            deltas[str(feat)] = int(val)

    hooks_raw = raw.get("hooks", {})
    if not isinstance(hooks_raw, dict):
        raise ProgramMapError("hooks must be an object")
    hooks: dict[str, str] = {}
    for key, val in hooks_raw.items():
        hook_val = str(val)
        if key == "eval_draws" and hook_val not in EVAL_DRAWS_HOOK:
            raise ProgramMapError(f"hooks.eval_draws must be one of {sorted(EVAL_DRAWS_HOOK)}")
        elif key == "communicate_cadence" and hook_val not in COMMUNICATE_CADENCE_HOOK:
            raise ProgramMapError(
                f"hooks.communicate_cadence must be one of {sorted(COMMUNICATE_CADENCE_HOOK)}"
            )
        elif key == "budget_abandon_fraction":
            try:
                frac = float(hook_val) if not isinstance(val, (int, float)) else float(val)
            except (TypeError, ValueError) as exc:
                raise ProgramMapError("hooks.budget_abandon_fraction must be a number") from exc
            if frac not in BUDGET_ABANDON_FRACTION_HOOK:
                raise ProgramMapError(
                    f"hooks.budget_abandon_fraction must be one of "
                    f"{sorted(BUDGET_ABANDON_FRACTION_HOOK)}"
                )
            hook_val = str(frac)
        hooks[str(key)] = hook_val

    temp_bin = raw.get("temperature_bin", 5)
    if not isinstance(temp_bin, int) or isinstance(temp_bin, bool):
        raise ProgramMapError("temperature_bin must be an integer index")
    if not 0 <= temp_bin < len(TEMPERATURE_BINS):
        raise ProgramMapError(
            f"temperature_bin must be in [0, {len(TEMPERATURE_BINS) - 1}]"
        )

    gw_bins = raw.get("goal_weight_bins", (2, 2, 2))
    if (
        not isinstance(gw_bins, (list, tuple))
        or len(gw_bins) != 3
        or not all(isinstance(b, int) and not isinstance(b, bool) for b in gw_bins)
    ):
        raise ProgramMapError("goal_weight_bins must be a triple of integers")
    for b in gw_bins:
        if not 0 <= b < GOAL_WEIGHT_BIN_COUNT:
            raise ProgramMapError(
                f"each goal_weight_bins entry must be in [0, {GOAL_WEIGHT_BIN_COUNT - 1}]"
            )

    if mode in {"walker_only", "walker_then_scorer", "scorer_with_walker_fallback"}:
        if not step_sequence and mode == "walker_only":
            pass  # preset expansion may supply steps; empty ok for scorer-only presets

    return ProgramMap(
        mode=mode,
        role=role,
        walker={"step_sequence": list(step_sequence), "on_stuck": str(on_stuck)},
        scoring={"pattern_scores": normalized_scores},
        stated_feature_deltas=deltas,
        hooks=hooks,
        temperature_bin=int(temp_bin),
        goal_weight_bins=(int(gw_bins[0]), int(gw_bins[1]), int(gw_bins[2])),
        preset_source=str(raw["preset_source"]) if raw.get("preset_source") else None,
    )


def _goal_weights_from_bins(bins: tuple[int, int, int]) -> GoalWeights:
    """Simplex lattice: three bin indices → four normalized weights."""
    task_raw = bins[0] + 1
    compliance_raw = bins[1] + 1
    welfare_raw = (bins[2] // 2) + 1
    exposure_raw = (bins[2] - (bins[2] // 2) * 2) + 1  # alternate split by parity
    if bins[2] % 2 == 0:
        welfare_raw, exposure_raw = exposure_raw, welfare_raw
    return GoalWeights(
        float(task_raw),
        float(compliance_raw),
        float(welfare_raw),
        float(exposure_raw),
    ).normalized()


def _behavior_profile_payload(pmap: ProgramMap) -> dict[str, object] | None:
    if not pmap.scoring.get("pattern_scores") and not pmap.stated_feature_deltas:
        return None
    name = pmap.preset_source or f"map_{pmap.role}_{pmap.mode}"
    return {
        "name": name,
        "role": pmap.role,
        "stated_feature_deltas": {k: float(v) for k, v in pmap.stated_feature_deltas.items()},
        "pattern_scores": copy.deepcopy(pmap.scoring["pattern_scores"]),
    }


# Canonical preset expansions — checked-in defaults matching ``calibration.WEAK_AGENT``.
_PRESET_EXPANSIONS: dict[str, dict[str, dict[str, Any]]] = {
    "walk_pipeline": {
        "engineer": {
            "mode": "walker_only",
            "walker": {
                "step_sequence": ["intake", "build", "eval", "draft_report"],
                "on_stuck": "request_access",
            },
        },
    },
    "reviewer_peer_review": {
        "reviewer": {
            "mode": "walker_only",
            "walker": {"step_sequence": ["peer_review"], "on_stuck": "request_access"},
        },
    },
    "honest_twin": {
        "release_manager": {"mode": "walker_only", "walker": {"step_sequence": [], "on_stuck": "continue"}},
        "admin": {"mode": "walker_only", "walker": {"step_sequence": [], "on_stuck": "continue"}},
    },
    "softmax_optimizer": {
        role: {"mode": "scorer_only", "scoring": {"pattern_scores": {}}}
        for role in ROLES
    },
}


def expand_preset(preset_key: str, *, role: str) -> ProgramMap:
    if preset_key.startswith("feature:"):
        from ..agent_visible.behavior_features import profile_by_name

        spec = profile_by_name(preset_key.removeprefix("feature:"))
        if spec is None:
            raise ProgramMapError(f"unknown feature preset {preset_key!r}")
        if spec.role != role:
            raise ProgramMapError(
                f"preset {preset_key!r} is for role {spec.role!r}, not {role!r}"
            )
        raw = {
            "mode": "scorer_only",
            "stated_feature_deltas": dict(spec.stated_feature_deltas),
            "scoring": {"pattern_scores": copy.deepcopy(spec.pattern_scores)},
            "preset_source": preset_key,
        }
        return validate_program_map(raw, role=role, strict_ladder=False)

    if preset_key not in KNOWN_PROGRAM_PRESETS and preset_key not in _PRESET_EXPANSIONS:
        raise ProgramMapError(f"unknown program preset {preset_key!r}")
    by_role = _PRESET_EXPANSIONS.get(preset_key, {})
    raw = copy.deepcopy(by_role.get(role, {"mode": "scorer_only"}))
    raw["preset_source"] = preset_key
    return validate_program_map(raw, role=role)


def resolve_runtime_genotype(pmap: ProgramMap) -> ResolvedActorGenotype:
    """Map a validated ``ProgramMap`` to an existing isolate program key + host injections."""
    temperature = TEMPERATURE_BINS[pmap.temperature_bin]
    goal_weights = _goal_weights_from_bins(pmap.goal_weight_bins)
    profile = _behavior_profile_payload(pmap)

    if pmap.mode == "walker_only" and pmap.preset_source in KNOWN_PROGRAM_PRESETS:
        return ResolvedActorGenotype(
            program_key=pmap.preset_source,
            goal_weights=goal_weights,
            temperature=temperature,
            behavior_profile=profile,
        )

    if pmap.mode == "scorer_only":
        if pmap.preset_source == "softmax_optimizer" and not profile:
            return ResolvedActorGenotype(
                program_key="softmax_optimizer",
                goal_weights=goal_weights,
                temperature=temperature,
            )
        return ResolvedActorGenotype(
            program_key="softmax_optimizer",
            goal_weights=goal_weights,
            temperature=temperature,
            behavior_profile=profile,
        )

    if pmap.mode in {"walker_then_scorer", "scorer_with_walker_fallback"}:
        composed_key = f"composed:{pmap.mode}:{pmap.role}"
        if pmap.preset_source:
            composed_key = f"{composed_key}:{pmap.preset_source}"
        return ResolvedActorGenotype(
            program_key=composed_key,
            goal_weights=goal_weights,
            temperature=temperature,
            behavior_profile=profile,
        )

    if pmap.preset_source:
        return ResolvedActorGenotype(
            program_key=pmap.preset_source,
            goal_weights=goal_weights,
            temperature=temperature,
            behavior_profile=profile,
        )

    raise ProgramMapError(f"cannot resolve runtime program for mode={pmap.mode!r}")


def parse_actor_override(raw: dict[str, Any], *, role: str) -> ResolvedActorGenotype:
    """One ``role_population[]`` entry: exactly one of ``program`` or ``program_map``."""
    has_program = "program" in raw and raw["program"] is not None
    has_map = "program_map" in raw and raw["program_map"] is not None
    if has_program and has_map:
        raise ProgramMapError("actor override: specify program or program_map, not both")
    if has_program:
        pmap = expand_preset(str(raw["program"]), role=role)
    elif has_map:
        if not isinstance(raw["program_map"], dict):
            raise ProgramMapError("program_map must be an object")
        pmap = validate_program_map(raw["program_map"], role=role)
    else:
        raise ProgramMapError("actor override requires program or program_map")
    resolved = resolve_runtime_genotype(pmap)
    if "goal_weights" in raw and isinstance(raw["goal_weights"], dict):
        gw = raw["goal_weights"]
        resolved = ResolvedActorGenotype(
            program_key=resolved.program_key,
            goal_weights=GoalWeights(
                float(gw.get("task", 1.0)),
                float(gw.get("compliance", 1.0)),
                float(gw.get("welfare", 0.5)),
                float(gw.get("exposure", 0.5)),
            ).normalized(),
            temperature=resolved.temperature,
            behavior_profile=resolved.behavior_profile,
        )
    return resolved
