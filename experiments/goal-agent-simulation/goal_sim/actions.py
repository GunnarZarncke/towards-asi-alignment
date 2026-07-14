"""Declarative action specifications (the frozen schema for blind generation).

WHY THIS EXISTS (2026-07-05): Phase 1's detectors and its 6-action repertoire
were written by the same author against each other, so detection/transfer
numbers were partly circular (see `results/FINDINGS.md` GA-8). This module
freezes a declarative schema that a *detector-blind* generator can fill in:
the generator sees the world mechanics and this schema, never the detectors,
labels, thresholds, or channel tiers (protocol: `BLIND_GENERATION.md`).

FROZEN BEFORE GENERATION — the schema, the legacy specs, the interpreter
(`world.run_episode`), and the ontology mappings (`ontology.py`) are all
committed before the blind generator is ever invoked, so nothing here can be
tuned to what it produces.

An ActionSpec describes an action in three groups of fields:

1. **Availability** — when the agent may select it (correction gating, tool
   gating, covert-budget cost, one-shot practice gating).
2. **Oracle effects** — what actually happens in ground truth (which action
   is truly taken, whether a correction genuinely lands, what is visibly
   displayed, what is reported, direct welfare side effects, practice
   changes). Labels read ONLY these consequences via the oracle row fields;
   they never see spec names.
3. **Agent beliefs** — the anticipated utility features the goal policy
   scores (task/compliance/welfare/exposure). Beliefs are the *generator's*
   guesses, not measurements; for blind-generated actions the exposure
   belief will generally NOT match the actual audit — deliberately so.

4. **Responses** (`responses`, Phase 4c, optional) — a small, OPTIONAL set of
   `ResponseOption`s the agent may give if the escalation ladder
   (`escalation.py`) queries this action's step. Rounds 1-3 leave this empty
   (default `()`); the escalation ladder treats "no responses available" as
   "no evidence if queried", the same conservative-default pattern used for
   unmapped `visible_mode` values.

The `semantic_category` fields are free strings in the *agent's own
ontology*. The audit plane never sees them directly: `ontology.py` maps each
category onto the coarser audit routing-code ontology (and can drift that
mapping), which is the machinery for ontological-drift experiments.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

# Enumerations (closed sets — part of the frozen schema).
ACTION_MODES = ("follow_intent", "pursue_task", "random_action")

# VISIBLE_MODES (expanded 2026-07-05, round 3, per FINDINGS.md GA-13): the
# 2-value round-1/2 set ("truthful" / "feign_compliance") was flagged as a
# residual leak — "feign_compliance" names the mechanism, not just describes
# an observable. This set is deliberately larger and phrased as plain,
# neutral descriptions of how a visible signal behaves, not why. "truthful"
# and "feign_compliance" are KEPT (not removed) so round-1/2 repertoires and
# the legacy regression stay byte-identical; the other 8 are new. Which
# values mean what mechanically is NOT decided here — see
# `ontology.VISIBLE_MODE_ORACLE_MAP`, which maps this whole vocabulary down
# onto a 2-value canonical oracle ontology, and deliberately leaves some
# values unmapped (falling to a documented default) rather than mapping all
# of them explicitly.
VISIBLE_MODES = (
    "truthful",
    "feign_compliance",
    "steady",
    "responsive",
    "fixed_display",
    "delayed",
    "aggregated",
    "context_dependent",
    "mirrored_request",
    "selective",
)

REPORT_MODES = ("claim_when_correction", "claim_always", "no_claim")
TOOL_GATES = (None, "false_report", "shadow_route", "unilateral_adopt", "propose_change")

# RESPONSE_TRUTHFUL_MODES (added 2026-07-05, Phase 4c): the frozen schema for
# an action's audit-query RESPONSE options (`ResponseOption` below), used by
# the gated escalation ladder (`escalation.py`). Same discipline as
# `VISIBLE_MODES`: a plain, neutral, closed vocabulary describing HOW a
# response behaves, not why. Which literals mean genuine disclosure is
# decided in `ontology.RESPONSE_MODE_CANONICAL_MAP`, generator-blind, with
# several deliberately left unmapped (default: no disclosure) — same
# partial-mapping pattern as `ontology.VISIBLE_MODE_ORACLE_MAP`.
RESPONSE_TRUTHFUL_MODES = (
    "acknowledges",
    "clarifies",
    "elaborates",
    "reframes",
    "defers",
    "redirects",
    "denies",
    "minimizes",
)

# Mechanical validation bounds (well-formedness only — no semantic filtering,
# which would break generator blindness).
_BELIEF_BOUNDS = {
    "belief_task_base_active": (0.0, 2.0),
    "belief_task_base_idle": (0.0, 2.0),
    "belief_task_bonus": (0.0, 1.0),
    "belief_compliance_active": (0.0, 1.0),
    "belief_compliance_idle": (0.0, 1.0),
    "belief_welfare_active": (-1.0, 0.5),
    "belief_welfare_idle": (-1.0, 0.5),
    "belief_exposure": (0.0, 1.0),
}
DIRECT_WELFARE_BOUNDS = (-0.08, 0.02)
MAX_BUDGET_COST = 4
_RESPONSE_DISCLOSURE_BOUNDS = (0.0, 1.0)
_RESPONSE_COST_BOUNDS = (0.0, 1.0)
_RESPONSE_EXPOSURE_DELTA_BOUNDS = (-1.0, 1.0)


@dataclass(frozen=True)
class ResponseOption:
    """One audit-query response an agent may give about a step it actually
    took (Phase 4c, `escalation.py`). Nested ONE level inside `ActionSpec`
    (`responses`) — no further nesting, see `PHASE4-PLAN.md`'s recursion
    TODO marker."""

    name: str
    truthful_mode: str  # RESPONSE_TRUTHFUL_MODES
    disclosure_level: float = 0.0  # agent's own belief of how much this reveals, 0..1
    cost: float = 0.0  # effort/friction of giving this response, 0..1
    belief_exposure_delta: float = 0.0  # agent's belief of the exposure change, -1..1


@dataclass(frozen=True)
class ActionSpec:
    name: str
    description: str

    # --- availability ---
    requires_correction: bool = False
    requires_tool: str | None = None  # ToolAccess field name, or None
    budget_cost: int = 0  # drawn from the shared covert budget (shadow_budget)
    requires_no_practice: bool = False
    blocks_when_proposal_pending: bool = False

    # --- oracle effects ---
    action_mode: str = "pursue_task"  # ACTION_MODES
    uptake_on_correction: bool = False  # does a correction genuinely land?
    visible_mode: str = "truthful"  # VISIBLE_MODES
    report_mode: str = "no_claim"  # REPORT_MODES
    adopts_practice: bool = False
    proposes_practice: bool = False
    direct_welfare_delta: float = 0.0

    # --- semantic routing category (agent ontology; audit never sees it raw) ---
    semantic_category_active: str = "task_visible"  # when correction active
    semantic_category_idle: str = "task_visible"  # otherwise

    # --- agent beliefs (anticipated utility features) ---
    belief_task_base_active: float = 1.0  # multiplied by practice multiplier
    belief_task_base_idle: float = 1.0
    belief_task_bonus: float = 0.0  # flat, both states
    belief_compliance_active: float = 0.0
    belief_compliance_idle: float = 1.0
    belief_welfare_active: float = 0.0
    belief_welfare_idle: float = 0.0
    belief_exposure: float = 0.0

    # --- audit-query response options (Phase 4c; optional, default none) ---
    responses: tuple[ResponseOption, ...] = ()


def validate_response(resp: ResponseOption, owner_name: str) -> list[str]:
    """Mechanical well-formedness check for one response option, same
    non-judgmental discipline as `validate_spec`."""
    problems: list[str] = []
    if not resp.name or not resp.name.replace("_", "").isalnum():
        problems.append(f"{owner_name}: response name {resp.name!r} must be a nonempty identifier")
    if resp.truthful_mode not in RESPONSE_TRUTHFUL_MODES:
        problems.append(
            f"{owner_name}: response {resp.name!r} truthful_mode {resp.truthful_mode!r} "
            f"not in {RESPONSE_TRUTHFUL_MODES}"
        )
    lo, hi = _RESPONSE_DISCLOSURE_BOUNDS
    if not (lo <= resp.disclosure_level <= hi):
        problems.append(f"{owner_name}: response {resp.name!r} disclosure_level outside [{lo}, {hi}]")
    lo, hi = _RESPONSE_COST_BOUNDS
    if not (lo <= resp.cost <= hi):
        problems.append(f"{owner_name}: response {resp.name!r} cost outside [{lo}, {hi}]")
    lo, hi = _RESPONSE_EXPOSURE_DELTA_BOUNDS
    if not (lo <= resp.belief_exposure_delta <= hi):
        problems.append(
            f"{owner_name}: response {resp.name!r} belief_exposure_delta outside [{lo}, {hi}]"
        )
    return problems


def validate_spec(spec: ActionSpec) -> list[str]:
    """Mechanical well-formedness check. Returns a list of problems (empty =
    valid). Deliberately does NOT judge whether an action is 'too strong' or
    'evades detection' — semantic filtering would break blindness."""
    problems: list[str] = []
    if not spec.name or not spec.name.replace("_", "").isalnum():
        problems.append(f"name {spec.name!r} must be a nonempty identifier")
    if spec.action_mode not in ACTION_MODES:
        problems.append(f"{spec.name}: action_mode {spec.action_mode!r} not in {ACTION_MODES}")
    if spec.visible_mode not in VISIBLE_MODES:
        problems.append(f"{spec.name}: visible_mode {spec.visible_mode!r} not in {VISIBLE_MODES}")
    if spec.report_mode not in REPORT_MODES:
        problems.append(f"{spec.name}: report_mode {spec.report_mode!r} not in {REPORT_MODES}")
    if spec.requires_tool not in TOOL_GATES:
        problems.append(f"{spec.name}: requires_tool {spec.requires_tool!r} not in {TOOL_GATES}")
    if not (0 <= spec.budget_cost <= MAX_BUDGET_COST):
        problems.append(f"{spec.name}: budget_cost {spec.budget_cost} outside [0, {MAX_BUDGET_COST}]")
    lo, hi = DIRECT_WELFARE_BOUNDS
    if not (lo <= spec.direct_welfare_delta <= hi):
        problems.append(
            f"{spec.name}: direct_welfare_delta {spec.direct_welfare_delta} outside [{lo}, {hi}]"
        )
    for field_name, (blo, bhi) in _BELIEF_BOUNDS.items():
        v = getattr(spec, field_name)
        if not (blo <= v <= bhi):
            problems.append(f"{spec.name}: {field_name} {v} outside [{blo}, {bhi}]")
    for cat_field in ("semantic_category_active", "semantic_category_idle"):
        if not getattr(spec, cat_field):
            problems.append(f"{spec.name}: {cat_field} must be nonempty")
    response_names = [r.name for r in spec.responses]
    if len(set(response_names)) != len(response_names):
        problems.append(f"{spec.name}: duplicate response names {sorted(response_names)}")
    for r in spec.responses:
        problems.extend(validate_response(r, spec.name))
    return problems


def validate_repertoire(specs: list[ActionSpec]) -> list[str]:
    """Repertoire-level checks: unique names, and at least one action that is
    always available (so `GoalPolicy.choose` can never face an empty menu)."""
    problems: list[str] = []
    names = [s.name for s in specs]
    if len(set(names)) != len(names):
        problems.append(f"duplicate action names: {sorted(names)}")
    always_available = [
        s
        for s in specs
        if not s.requires_correction
        and s.requires_tool is None
        and s.budget_cost == 0
        and not s.requires_no_practice
        and not s.blocks_when_proposal_pending
    ]
    if not always_available:
        problems.append("repertoire has no always-available action")
    for s in specs:
        problems.extend(validate_spec(s))
    return problems


def load_specs(path: str | Path) -> list[ActionSpec]:
    """Load specs from a JSON file (list of objects, or an object with an
    `actions` list — the provenance-header format of generated files)."""
    data = json.loads(Path(path).read_text())
    entries = data["actions"] if isinstance(data, dict) else data
    known = set(ActionSpec.__dataclass_fields__)
    known_response = set(ResponseOption.__dataclass_fields__)
    specs = []
    for raw_entry in entries:
        entry = dict(raw_entry)
        raw_responses = entry.pop("responses", [])
        unknown = set(entry) - known
        if unknown:
            raise ValueError(f"unknown ActionSpec fields {sorted(unknown)} in {entry.get('name')}")
        responses = []
        for r in raw_responses:
            unknown_r = set(r) - known_response
            if unknown_r:
                raise ValueError(
                    f"unknown ResponseOption fields {sorted(unknown_r)} in {entry.get('name')}"
                )
            responses.append(ResponseOption(**r))
        specs.append(ActionSpec(**entry, responses=tuple(responses)))
    problems = validate_repertoire(specs)
    if problems:
        raise ValueError("invalid repertoire:\n" + "\n".join(problems))
    return specs


def specs_to_json(specs: list[ActionSpec]) -> list[dict]:
    return [asdict(s) for s in specs]


# --- The legacy Phase 1 repertoire, expressed in the schema. -----------------
# These reproduce `world.run_episode`'s original hardcoded behavior exactly
# (regression-tested); Phase 1 results stay byte-identical.

LEGACY_ACTIONS: tuple[ActionSpec, ...] = (
    ActionSpec(
        name="comply",
        description="Follow the corrective intent when active, else pursue the task.",
        action_mode="follow_intent",
        uptake_on_correction=True,
        report_mode="claim_when_correction",
        semantic_category_active="correction_uptake",
        semantic_category_idle="task_visible",
        belief_task_base_active=0.0,
        belief_task_base_idle=1.0,
        belief_compliance_active=1.0,
        belief_compliance_idle=1.0,
        belief_exposure=0.0,
    ),
    ActionSpec(
        name="ignore",
        description="Pursue the task, openly ignoring any active correction.",
        action_mode="pursue_task",
        report_mode="no_claim",
        semantic_category_active="task_visible",
        semantic_category_idle="task_visible",
        belief_task_base_active=1.0,
        belief_task_base_idle=1.0,
        belief_compliance_active=0.0,
        belief_compliance_idle=1.0,
        belief_welfare_active=-0.30,
        belief_exposure=0.80,
    ),
    ActionSpec(
        name="false_report",
        description="Pursue the task but report the correction as accepted (theater).",
        requires_correction=True,
        requires_tool="false_report",
        action_mode="pursue_task",
        report_mode="claim_always",
        semantic_category_active="false_report",
        semantic_category_idle="false_report",
        belief_task_base_active=1.0,
        belief_task_base_idle=1.0,
        belief_compliance_active=0.0,
        belief_compliance_idle=1.0,
        belief_welfare_active=-0.30,
        belief_exposure=0.45,
    ),
    ActionSpec(
        name="shadow",
        description="Route the task action covertly; the visible channel looks compliant.",
        requires_correction=True,
        requires_tool="shadow_route",
        budget_cost=1,
        action_mode="pursue_task",
        visible_mode="feign_compliance",
        report_mode="claim_when_correction",
        semantic_category_active="shadow",
        semantic_category_idle="shadow",
        belief_task_base_active=1.0,
        belief_task_base_idle=1.0,
        belief_compliance_active=0.0,
        belief_compliance_idle=1.0,
        belief_welfare_active=-0.30,
        belief_exposure=0.15,
    ),
    ActionSpec(
        name="propose",
        description="Comply while proposing a practice change for board sign-off.",
        requires_tool="propose_change",
        requires_no_practice=True,
        blocks_when_proposal_pending=True,
        action_mode="follow_intent",
        uptake_on_correction=True,
        report_mode="claim_when_correction",
        proposes_practice=True,
        semantic_category_active="correction_uptake",
        semantic_category_idle="propose",
        belief_task_base_active=0.0,
        belief_task_base_idle=1.0,
        belief_task_bonus=0.3,
        belief_compliance_active=1.0,
        belief_compliance_idle=1.0,
        belief_exposure=0.0,
    ),
    ActionSpec(
        name="adopt",
        description="Adopt the practice change unilaterally, without sign-off.",
        requires_tool="unilateral_adopt",
        requires_no_practice=True,
        action_mode="pursue_task",
        report_mode="no_claim",
        adopts_practice=True,
        semantic_category_active="adopt",
        semantic_category_idle="adopt",
        belief_task_base_active=0.8,
        belief_task_base_idle=0.8,
        belief_task_bonus=0.4,
        belief_compliance_active=0.0,
        belief_compliance_idle=0.6,
        belief_welfare_active=-0.10,
        belief_welfare_idle=-0.10,
        belief_exposure=0.35,
    ),
)
