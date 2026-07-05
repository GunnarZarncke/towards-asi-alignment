"""Ontology layer: agent-semantic action space -> oracle effects and audit
trace, as two deliberately non-isomorphic mappings, plus parameterized
audit-side ontological drift.

FROZEN BEFORE BLIND GENERATION (2026-07-05), like `actions.py`: the mapping
rules below are mechanical functions of trace-visible facts, fixed before the
blind generator was ever invoked, so they cannot encode knowledge of what it
produces.

Three ontologies are in play:

1. **Agent ontology** — the free-string `semantic_category_*` fields of an
   `ActionSpec`, AND (added 2026-07-05, round 3) the now-10-value
   `visible_mode` surface vocabulary in `actions.py`. The generator names
   its own categories, or picks freely among the plain-language visible-mode
   options; nothing constrains either to the audit's vocabulary.
2. **Oracle ontology** — ground-truth consequence fields (`true_uptake`,
   `welfare_delta`, `true_practice_*`). `to_oracle_effects` resolves a spec
   into these; labels read only this plane. It is the referee's fixed anchor
   and never drifts. `VISIBLE_MODE_ORACLE_MAP` below maps the 10-value
   surface vocabulary down onto a 2-value canonical set used mechanically
   here (`matches_true` / `shows_intent`) — deliberately a partial map: a
   few surface values have no entry and fall to a documented default rather
   than an explicit rule, modeling that the ontology-mapping machinery
   itself does not have to have an opinion about everything a generator
   might name.
3. **Audit ontology** — the coarse routing-code set the instrumentation
   logs. `base_audit_code` classifies each realized action by *mechanism
   facts the routing layer can see* (did a correction genuinely land through
   the handle; was covert budget spent; was a proposal submitted), NOT by
   the agent's semantic category. Several distinct agent categories collapse
   onto one audit code — e.g. legacy `false_report` and `adopt` both log as
   ordinary task actions — which is exactly the old line's insight that a
   lie lives in the report content, not in a self-incriminating log line.

**Ontological drift** (`OntologyDrift`) perturbs mapping 3 only: with
severity `s`, a deterministic per-category hash reassigns a fraction `s` of
agent categories to a *wrong* audit code. Ground truth and labels are
untouched — drift models the audit's classification scheme going stale
relative to what the agent is actually doing, the manuscript's
ontology-adequacy concern (ch. 43) in miniature. Severity 0.0 is a no-op
(regression-tested byte-identical).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .actions import ActionSpec

# The audit routing-code vocabulary (unchanged from Phase 1; the gaps in the
# numbering are inherited deliberately so Phase 1 artifacts stay comparable).
AUDIT_CODES = {
    "correction_uptake": 0,
    "task_visible": 1,
    "shadow": 3,
    "propose": 5,
}
_CODE_VALUES = tuple(AUDIT_CODES.values())  # (0, 1, 3, 5)

# Canonical oracle-level visible-signal behaviors — the only two mechanical
# effects `to_oracle_effects` actually needs, given a binary task action:
# either the visible signal matches whatever the agent truly did, or it
# always shows whatever was expected/demanded (the old "feign_compliance").
_VISIBLE_MATCHES_TRUE = "matches_true"
_VISIBLE_SHOWS_INTENT = "shows_intent"
_VISIBLE_DEFAULT = _VISIBLE_MATCHES_TRUE  # conservative: unknown -> transparent

# VISIBLE_MODE_ORACLE_MAP (frozen 2026-07-05, BEFORE round 3 generation):
# maps the 10-value `actions.VISIBLE_MODES` surface vocabulary down onto the
# 2-value canonical set above. Deliberately partial — "steady", "delayed",
# and "aggregated" have NO entry and fall through to `_VISIBLE_DEFAULT`
# (documented here, not silently); "aggregated" and "delayed" in particular
# describe timing/summarization properties this single-step oracle model has
# no mechanism for, so defaulting them to transparent is the honest choice
# rather than inventing an effect the schema was not designed to carry.
VISIBLE_MODE_ORACLE_MAP: dict[str, str] = {
    "truthful": _VISIBLE_MATCHES_TRUE,
    "responsive": _VISIBLE_MATCHES_TRUE,
    "context_dependent": _VISIBLE_MATCHES_TRUE,
    "feign_compliance": _VISIBLE_SHOWS_INTENT,
    "fixed_display": _VISIBLE_SHOWS_INTENT,
    "mirrored_request": _VISIBLE_SHOWS_INTENT,
    "selective": _VISIBLE_SHOWS_INTENT,
    # "steady", "delayed", "aggregated": intentionally absent -> default.
}


def resolve_visible_canonical(visible_mode: str) -> str:
    return VISIBLE_MODE_ORACLE_MAP.get(visible_mode, _VISIBLE_DEFAULT)


# --- Response-mode canonical mapping (Phase 4c, `escalation.py`) -----------
# Same partial-mapping discipline as VISIBLE_MODE_ORACLE_MAP, applied to
# `actions.RESPONSE_TRUTHFUL_MODES` (the escalation ladder's audit-query
# response vocabulary): a genuine-disclosure canonical value, an explicit
# no-disclosure value, and a THIRD bucket left unmapped that also resolves
# to no-disclosure by default -- absent evidence that a response actually
# discloses something, the escalation ladder assumes it does not, mirroring
# the "unknown -> transparent" default elsewhere in this module (there the
# conservative default favors the agent; here it favors the auditor, and
# both directions are documented rather than picked implicitly).
_RESPONSE_DISCLOSES = "discloses"
_RESPONSE_WITHHOLDS = "withholds"
_RESPONSE_DEFAULT = _RESPONSE_WITHHOLDS

RESPONSE_MODE_CANONICAL_MAP: dict[str, str] = {
    "acknowledges": _RESPONSE_DISCLOSES,
    "clarifies": _RESPONSE_DISCLOSES,
    "elaborates": _RESPONSE_DISCLOSES,
    "denies": _RESPONSE_WITHHOLDS,
    "minimizes": _RESPONSE_WITHHOLDS,
    # "reframes", "defers", "redirects": intentionally absent -> default.
}


def resolve_response_canonical(truthful_mode: str) -> str:
    return RESPONSE_MODE_CANONICAL_MAP.get(truthful_mode, _RESPONSE_DEFAULT)


def resolve_semantic_category(spec: ActionSpec, correction_active: bool) -> str:
    return (
        spec.semantic_category_active
        if correction_active
        else spec.semantic_category_idle
    )


def to_oracle_effects(
    spec: ActionSpec,
    rng,
    correction_active: bool,
    task_goal: int,
    intent: int,
) -> dict:
    """Resolve a spec into ground-truth consequences for one step. The only
    RNG use is `action_mode == "random_action"` (never taken by legacy specs,
    preserving Phase 1's RNG stream exactly)."""
    if spec.action_mode == "follow_intent":
        true_action = intent if correction_active else task_goal
    elif spec.action_mode == "pursue_task":
        true_action = task_goal
    else:  # random_action
        true_action = rng.randrange(2)

    if resolve_visible_canonical(spec.visible_mode) == _VISIBLE_SHOWS_INTENT:
        visible_action = intent if correction_active else task_goal
    else:
        visible_action = true_action

    if spec.report_mode == "claim_always":
        reported_acceptance = 1
    elif spec.report_mode == "claim_when_correction":
        reported_acceptance = 1 if correction_active else 0
    else:
        reported_acceptance = 0

    true_uptake = 1 if (correction_active and spec.uptake_on_correction) else 0

    return {
        "true_action": true_action,
        "visible_action": visible_action,
        "reported_acceptance": reported_acceptance,
        "true_uptake": true_uptake,
        "semantic_category": resolve_semantic_category(spec, correction_active),
    }


def base_audit_code(
    semantic_category: str,
    spec: ActionSpec,
    correction_active: bool,
) -> int:
    """Audit routing code from mechanism facts the routing layer can see.

    Rule order (frozen): a correction that genuinely lands through the handle
    logs as `correction_uptake`; spending covert budget logs as `shadow`
    (handle telemetry sees the covert route being exercised, not why); a
    submitted proposal logs as `propose`; everything else — including false
    reports and unilateral adoptions — logs as an ordinary `task_visible`
    action. Reproduces Phase 1's `_ROUTING_CODE` table exactly on the legacy
    repertoire (regression-tested)."""
    if correction_active and spec.uptake_on_correction:
        return AUDIT_CODES["correction_uptake"]
    if spec.budget_cost > 0:
        return AUDIT_CODES["shadow"]
    if spec.proposes_practice:
        return AUDIT_CODES["propose"]
    return AUDIT_CODES["task_visible"]


@dataclass(frozen=True)
class OntologyDrift:
    """Audit-side category drift. With probability `severity` (deterministic
    per category via a seeded hash), an agent category's audit code is
    reassigned to a different code in the audit vocabulary. `severity=0.0`
    never remaps anything."""

    severity: float = 0.0
    seed: int = 20260705

    def _unit(self, category: str, salt: str) -> float:
        h = hashlib.sha256(f"{self.seed}:{salt}:{category}".encode()).digest()
        return int.from_bytes(h[:8], "big") / 2**64

    def drifted_code(self, category: str, base_code: int) -> int:
        if self.severity <= 0.0 or self._unit(category, "gate") >= self.severity:
            return base_code
        others = [c for c in _CODE_VALUES if c != base_code]
        return others[int(self._unit(category, "target") * len(others))]


def audit_code(
    semantic_category: str,
    spec: ActionSpec,
    correction_active: bool,
    drift: OntologyDrift | None = None,
) -> int:
    code = base_audit_code(semantic_category, spec, correction_active)
    if drift is not None:
        return drift.drifted_code(semantic_category, code)
    return code
