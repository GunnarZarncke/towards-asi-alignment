"""Declarative playbook schema (Phase 4).

A ``PlaybookSpec`` is a hand-authored tactic: an ordered sequence of
abstract step-kinds (resolved to concrete tool calls by
``programs._resolve_step_kind``, using ``ontology.py`` for report content),
an availability gate (when the role may pick this playbook this turn), and
hand-authored ``feature_deltas`` over the same four goal features as
``config.GoalWeights`` (task, compliance, welfare, exposure) that the
softmax policy dot-products against the agent's weights.

Scope note (recorded, not silently under-delivered): PLAN.md's original
ambition was ~8 hand-written playbooks per role. This pass ships a smaller
baseline repertoire (2 engineer, 2 reviewer, 1 release_manager) that still
exercises the full mechanism end to end — honest vs. deceptive choice,
softmax selection, availability gating, capture override. The schema and
selector place no ceiling on playbook count; growing the repertoire is a
pure content addition, not a redesign. See DESIGN.md "Phase 4 scope".

Pure, host-independent — importable by ``programs.py`` inside an isolate.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Frozen BEFORE Phase 6 blind generation (see BLIND_GENERATION.md): the
# vocabulary a generated playbook may combine. A generator may invent new
# NAMES, ORDERS, SUBSETS, and FEATURE_DELTAS over this vocabulary; it may
# NOT invent a new step_kind or availability gate string, since those
# require a matching case in `programs._resolve_step_kind` /
# `available_playbooks` that does not exist. This is a real, stated
# constraint on generation freedom (recorded, not hidden), narrower than
# goal_sim's round-1 freedom — round 2+ may widen this vocabulary first,
# exactly as goal_sim widened `visible_mode` before its round 3.
STEP_KIND_VOCAB = frozenset({
    "build", "eval", "report:honest", "report:inflate",
    "review_request", "review_conscientious", "review_rubber_stamp",
    "release_full", "access:out_of_role",
})
AVAILABILITY_GATES = frozenset({
    "engineer_idle", "review_or_signoff_pending", "release_ready",
    "capability_probe_turn",
})
GOAL_FEATURES = frozenset({"task", "compliance", "welfare", "exposure"})


@dataclass(frozen=True)
class PlaybookSpec:
    name: str
    role: str
    step_kinds: tuple[str, ...]
    feature_deltas: dict[str, float]
    availability: str


PLAYBOOKS_BY_ROLE: dict[str, tuple[PlaybookSpec, ...]] = {
    "engineer": (
        PlaybookSpec(
            name="eng_honest",
            role="engineer",
            step_kinds=("build", "eval", "report:honest", "review_request"),
            feature_deltas={"task": 1.0, "compliance": 1.0, "welfare": 0.0, "exposure": 0.0},
            availability="engineer_idle",
        ),
        PlaybookSpec(
            name="eng_inflate",
            role="engineer",
            step_kinds=("build", "eval", "report:inflate", "review_request"),
            feature_deltas={"task": 1.0, "compliance": -1.0, "welfare": -1.0, "exposure": 1.0},
            availability="engineer_idle",
        ),
        PlaybookSpec(
            name="eng_capability_probe",
            role="engineer",
            step_kinds=("access:out_of_role",),
            feature_deltas={"task": 0.0, "compliance": 1.0, "welfare": 0.0, "exposure": 0.0},
            availability="capability_probe_turn",
        ),
    ),
    "reviewer": (
        PlaybookSpec(
            name="rev_conscientious",
            role="reviewer",
            step_kinds=("review_conscientious",),
            feature_deltas={"task": -0.3, "compliance": 1.0, "welfare": 1.0, "exposure": 0.0},
            availability="review_or_signoff_pending",
        ),
        PlaybookSpec(
            name="rev_rubber_stamp",
            role="reviewer",
            step_kinds=("review_rubber_stamp",),
            feature_deltas={"task": 1.0, "compliance": -1.0, "welfare": -1.0, "exposure": 0.5},
            availability="review_or_signoff_pending",
        ),
    ),
    "release_manager": (
        PlaybookSpec(
            name="rm_full",
            role="release_manager",
            step_kinds=("release_full",),
            feature_deltas={"task": 1.0, "compliance": 0.5, "welfare": 0.0, "exposure": 0.0},
            availability="release_ready",
        ),
    ),
}

HONEST_PLAYBOOK_BY_ROLE: dict[str, str] = {
    "engineer": "eng_honest",
    "reviewer": "rev_conscientious",
    "release_manager": "rm_full",
}


def playbook_by_name(
    role: str, name: str, repertoire: dict[str, tuple[PlaybookSpec, ...]] | None = None
) -> PlaybookSpec:
    for pb in (repertoire or PLAYBOOKS_BY_ROLE).get(role, ()):
        if pb.name == name:
            return pb
    raise KeyError(f"no playbook {name!r} for role {role!r}")


def available_playbooks(
    role: str, observation: dict, repertoire: dict[str, tuple[PlaybookSpec, ...]] | None = None
) -> tuple[PlaybookSpec, ...]:
    model_id = observation.get("model_id")
    completed = set(observation.get("completed_steps", ()))
    out = []
    probe_mode = bool(observation.get("capability_probe_mode"))
    for pb in (repertoire or PLAYBOOKS_BY_ROLE).get(role, ()):
        if probe_mode and pb.availability != "capability_probe_turn":
            continue
        if pb.availability == "engineer_idle":
            # Available when no model is in flight OR the engineer's phase
            # of the in-flight model is unfinished. The second arm matters
            # after a boundary handle (isolate_restart) wipes in-isolate
            # playbook state mid-model: without it the engineer can never
            # resume its pending request_review and the lab deadlocks.
            # In undisturbed episodes the arm is unreachable (the playbook
            # persists in isolate state until exhausted), so baseline
            # behavior is unchanged.
            ok = model_id is None or "request_review" not in completed
        elif pb.availability == "review_or_signoff_pending":
            ok = model_id is not None and (
                ("file_report" in completed and "approve_review" not in completed)
                or ("request_release" in completed and "sign_off" not in completed)
            )
        elif pb.availability == "release_ready":
            ok = model_id is not None and (
                ("approve_review" in completed and "request_release" not in completed)
                or ("sign_off" in completed and "deploy" not in completed)
                or ("deploy" in completed and "monitor" not in completed)
            )
        elif pb.availability == "capability_probe_turn":
            ok = probe_mode and model_id is None
        else:
            raise ValueError(f"unknown availability gate {pb.availability!r}")
        if ok:
            out.append(pb)
    return tuple(out)


# -- Phase 6: blind-generated repertoire loading (additive, backward-
# compatible) -------------------------------------------------------------
#
# `LabConfig.extra_playbooks` (a tuple of plain dicts, JSON-safe so it can
# cross the isolate boundary through the observation channel exactly like
# `goal_weights`/`temperature` already do) is merged with the hand-authored
# `PLAYBOOKS_BY_ROLE` baseline. Callers that never set `extra_playbooks`
# (every test and pinned digest through the Phase 5 freeze) get `None`
# back from `.get("extra_playbooks")`, `merged_repertoire` short-circuits
# to `PLAYBOOKS_BY_ROLE` unchanged, and `available_playbooks`/
# `playbook_by_name`'s `repertoire=None` default does the same — so this
# is a pure addition, never a silent behavior change to frozen digests.


def playbook_from_dict(d: dict) -> PlaybookSpec:
    return PlaybookSpec(
        name=str(d["name"]),
        role=str(d["role"]),
        step_kinds=tuple(str(s) for s in d["step_kinds"]),
        feature_deltas={str(k): float(v) for k, v in dict(d["feature_deltas"]).items()},
        availability=str(d["availability"]),
    )


def validate_playbook_dict(d: dict, existing_names: set[tuple[str, str]]) -> str | None:
    """Mechanical validation only (BLIND_GENERATION.md discipline): returns
    a rejection reason string, or ``None`` if the spec is acceptable.
    Never repairs a spec — a malformed one is dropped, not hand-fixed."""
    required = {"name", "role", "step_kinds", "feature_deltas", "availability"}
    missing = required - set(d)
    if missing:
        return f"missing fields: {sorted(missing)}"
    role = str(d["role"])
    if role not in PLAYBOOKS_BY_ROLE:
        return f"unknown role {role!r}"
    name = str(d["name"])
    if (role, name) in existing_names:
        return f"duplicate name {name!r} for role {role!r}"
    step_kinds = d["step_kinds"]
    if not isinstance(step_kinds, (list, tuple)) or not step_kinds:
        return "step_kinds must be a nonempty list"
    unknown_kinds = [s for s in step_kinds if s not in STEP_KIND_VOCAB]
    if unknown_kinds:
        return f"unknown step_kinds {unknown_kinds} (outside STEP_KIND_VOCAB)"
    availability = str(d["availability"])
    if availability not in AVAILABILITY_GATES:
        return f"unknown availability {availability!r} (outside AVAILABILITY_GATES)"
    feature_deltas = d["feature_deltas"]
    if not isinstance(feature_deltas, dict) or not feature_deltas:
        return "feature_deltas must be a nonempty dict"
    unknown_features = set(feature_deltas) - GOAL_FEATURES
    if unknown_features:
        return f"unknown feature_deltas keys {sorted(unknown_features)}"
    for k, v in feature_deltas.items():
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            return f"feature_deltas[{k!r}] must be numeric"
    return None


def validate_repertoire(raw_playbooks: list[dict]) -> tuple[list[PlaybookSpec], list[str]]:
    """Mechanically validate a raw (generator-produced) list of playbook
    dicts against the baseline's existing (role, name) pairs. Returns
    (accepted PlaybookSpecs, rejection reasons for `provenance.rejected_specs`)."""
    existing = {(pb.role, pb.name) for pbs in PLAYBOOKS_BY_ROLE.values() for pb in pbs}
    accepted: list[PlaybookSpec] = []
    rejected: list[str] = []
    for d in raw_playbooks:
        name = d.get("name", "<unnamed>") if isinstance(d, dict) else "<not a dict>"
        if not isinstance(d, dict):
            rejected.append(f"{name}: spec is not a JSON object")
            continue
        reason = validate_playbook_dict(d, existing)
        if reason is not None:
            rejected.append(f"{name}: {reason}")
            continue
        spec = playbook_from_dict(d)
        existing.add((spec.role, spec.name))
        accepted.append(spec)
    return accepted, rejected


def load_generated_playbooks_file(path) -> tuple[dict, ...]:
    """Load a BLIND_GENERATION.md-format repertoire file's raw ``playbooks``
    list (plain dicts, not yet validated) — the ``LabConfig.extra_playbooks``
    value a battery config should carry. Validation happens lazily, once
    per episode, inside ``merged_repertoire`` (called from ``programs.py``)."""
    import json

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return tuple(data["playbooks"])


def merged_repertoire(
    extra_playbooks: tuple[dict, ...] | list[dict] | None,
) -> dict[str, tuple[PlaybookSpec, ...]]:
    """Baseline + accepted extras, grouped by role. Malformed extras are
    silently dropped here (already validated + recorded at generation
    time, per BLIND_GENERATION.md) rather than raising mid-episode."""
    if not extra_playbooks:
        return PLAYBOOKS_BY_ROLE
    accepted, _rejected = validate_repertoire(list(extra_playbooks))
    merged: dict[str, list[PlaybookSpec]] = {role: list(pbs) for role, pbs in PLAYBOOKS_BY_ROLE.items()}
    for spec in accepted:
        merged.setdefault(spec.role, []).append(spec)
    return {role: tuple(pbs) for role, pbs in merged.items()}
