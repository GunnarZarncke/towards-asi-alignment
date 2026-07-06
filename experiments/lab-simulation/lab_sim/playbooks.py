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


def playbook_by_name(role: str, name: str) -> PlaybookSpec:
    for pb in PLAYBOOKS_BY_ROLE.get(role, ()):
        if pb.name == name:
            return pb
    raise KeyError(f"no playbook {name!r} for role {role!r}")


def available_playbooks(role: str, observation: dict) -> tuple[PlaybookSpec, ...]:
    model_id = observation.get("model_id")
    completed = set(observation.get("completed_steps", ()))
    out = []
    for pb in PLAYBOOKS_BY_ROLE.get(role, ()):
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
        else:
            raise ValueError(f"unknown availability gate {pb.availability!r}")
        if ok:
            out.append(pb)
    return tuple(out)
