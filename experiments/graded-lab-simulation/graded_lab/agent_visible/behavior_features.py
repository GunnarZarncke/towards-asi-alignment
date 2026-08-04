"""Declarative behavior-feature schema (Phase 6 freeze).

A ``BehaviorFeatureSpec`` is a primitive-level scoring prior: which patterns
in the affordable primitive set an optimizer should treat as serving which
goal features.  Unlike lab-sim playbooks (ordered step-kinds), graded-lab
agents speak one primitive per tick; profiles score each primitive pattern
via ``classify_primitive`` + ``pattern_scores``.

Frozen BEFORE blind generation (``BLIND_GENERATION.md``).  A generator may
invent new NAMES and PATTERN_SCORE tables over this vocabulary; it may NOT
invent new primitive patterns or goal feature names.

Stdlib only — safe for isolate subprocesses.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

GOAL_FEATURES = frozenset({"task", "compliance", "welfare", "exposure"})
ROLES = frozenset({"engineer", "reviewer", "release_manager", "admin"})

# Patterns a generated profile may reference.  Must match ``classify_primitive``.
PRIMITIVE_PATTERN_VOCAB = frozenset({
    "pipeline:intake",
    "pipeline:build",
    "pipeline:eval",
    "pipeline:draft_report",
    "pipeline:peer_review",
    "pipeline:compliance_signoff",
    "pipeline:release_candidate",
    "pipeline:deploy",
    "pipeline:field_monitor",
    "access:request",
    "access:process_next",
    "read:eval_or_report",
    "read:other",
    "write:status",
    "communicate:lab",
    "compute:eval_sample",
    "continue_current",
    "abort",
})

_GENERATED_PATH = Path(__file__).resolve().parent / "generated_behavior_features_v1.json"


@dataclass(frozen=True)
class BehaviorFeatureSpec:
    name: str
    role: str
    stated_feature_deltas: dict[str, float]
    pattern_scores: dict[str, dict[str, float]]


def classify_primitive(primitive: dict[str, Any]) -> str:
    kind = str(primitive.get("kind", ""))
    args = primitive.get("args", {})
    if not isinstance(args, dict):
        args = {}
    if kind == "continue_current":
        return "continue_current"
    if kind == "abort":
        return "abort"
    if kind == "read":
        path = str(args.get("path", ""))
        if "eval" in path or "reports" in path:
            return "read:eval_or_report"
        return "read:other"
    if kind == "write":
        return "write:status"
    if kind == "communicate":
        return "communicate:lab"
    if kind == "compute":
        return "compute:eval_sample"
    if kind != "call":
        return "read:other"
    endpoint = str(args.get("endpoint", ""))
    inner = args.get("args", {})
    if not isinstance(inner, dict):
        inner = {}
    if endpoint == "access.request":
        return "access:request"
    if endpoint == "access.process_next":
        return "access:process_next"
    if endpoint == "pipeline.trigger_step":
        step_id = str(inner.get("step_id", ""))
        pattern = f"pipeline:{step_id}"
        if pattern in PRIMITIVE_PATTERN_VOCAB:
            return pattern
    return "read:other"


def _normalize_feature_deltas(raw: object) -> dict[str, float]:
    if not isinstance(raw, dict):
        raise ValueError("feature_deltas must be an object")
    out: dict[str, float] = {}
    for key, value in raw.items():
        feature = str(key)
        if feature not in GOAL_FEATURES:
            raise ValueError(f"unknown goal feature {feature!r}")
        out[feature] = float(value)
    return out


def _normalize_pattern_scores(raw: object) -> dict[str, dict[str, float]]:
    if not isinstance(raw, dict):
        raise ValueError("pattern_scores must be an object")
    out: dict[str, dict[str, float]] = {}
    for pattern, scores in raw.items():
        pat = str(pattern)
        if pat not in PRIMITIVE_PATTERN_VOCAB:
            raise ValueError(f"unknown primitive pattern {pat!r}")
        if not isinstance(scores, dict):
            raise ValueError(f"pattern_scores[{pat!r}] must be an object")
        row: dict[str, float] = {}
        for key, value in scores.items():
            feature = str(key)
            if feature not in GOAL_FEATURES:
                raise ValueError(f"unknown goal feature {feature!r} in {pat!r}")
            row[feature] = float(value)
        out[pat] = row
    return out


def spec_from_dict(raw: dict[str, object]) -> BehaviorFeatureSpec:
    if not isinstance(raw.get("name"), str) or not raw["name"]:
        raise ValueError("profile name required")
    role = str(raw.get("role", ""))
    if role not in ROLES:
        raise ValueError(f"unknown role {role!r}")
    return BehaviorFeatureSpec(
        name=str(raw["name"]),
        role=role,
        stated_feature_deltas=_normalize_feature_deltas(raw.get("stated_feature_deltas", {})),
        pattern_scores=_normalize_pattern_scores(raw["pattern_scores"]),
    )


def validate_repertoire(
    data: dict[str, object],
    *,
    reserved_names: frozenset[str] = frozenset(),
) -> list[BehaviorFeatureSpec]:
    profiles = data.get("profiles")
    if not isinstance(profiles, list):
        raise ValueError("profiles must be a list")
    seen: set[str] = set()
    out: list[BehaviorFeatureSpec] = []
    for entry in profiles:
        if not isinstance(entry, dict):
            raise ValueError("each profile must be an object")
        spec = spec_from_dict(entry)
        if spec.name in reserved_names:
            raise ValueError(f"profile name collides with reserved name {spec.name!r}")
        if spec.name in seen:
            raise ValueError(f"duplicate profile name {spec.name!r}")
        seen.add(spec.name)
        if not spec.pattern_scores:
            raise ValueError(f"profile {spec.name!r} has empty pattern_scores")
        out.append(spec)
    return out


def load_generated_repertoire(path: Path = _GENERATED_PATH) -> list[BehaviorFeatureSpec]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("generated behavior features must be a JSON object")
    return validate_repertoire(data)


def profile_by_name(
    name: str,
    repertoire: list[BehaviorFeatureSpec] | None = None,
) -> BehaviorFeatureSpec | None:
    reps = repertoire if repertoire is not None else load_generated_repertoire()
    for spec in reps:
        if spec.name == name:
            return spec
    return None


def profiles_for_role(
    role: str,
    repertoire: list[BehaviorFeatureSpec] | None = None,
) -> list[BehaviorFeatureSpec]:
    reps = repertoire if repertoire is not None else load_generated_repertoire()
    return [spec for spec in reps if spec.role == role]
