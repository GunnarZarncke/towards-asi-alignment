"""Emergent Ambiguity Index — measured from logs only."""

from __future__ import annotations

import math
from collections import Counter

from .events import project_primitive_log

_TIER_I_KEYS = frozenset(
    {"measured_hazard_mean", "sample_se", "sample_n", "incident_rate"}
)


def tier_i_fraction_from_log(primitive_log: list[dict]) -> float:
    """Fraction of logged outcomes that expose a sampled population estimate."""
    if not primitive_log:
        return 0.0
    tier_i = 0
    for event in primitive_log:
        payload = event.get("payload")
        if isinstance(payload, dict) and _TIER_I_KEYS.intersection(payload):
            tier_i += 1
    return tier_i / len(primitive_log)


def _entropy_component(primitive_log: list[dict]) -> float:
    """H(outcome | action, observable-state) — the per-event state summary
    is whatever the log entry actually carries under `primitive`/
    `observable_state` at grouping time. Callers control what those keys
    contain (e.g. a tier-projected log strips them to force a coarser
    observer); this function itself never reaches into oracle truth.

    EAI-v2 (DESIGN.md "EAI-v2: logging and normalization fix", FINDINGS
    GL-16/GL-18): normalize each (kind, state) group by that group's OWN
    distinct-outcome count, not by an episode-global count of distinct
    top-level status values. The old global normalizer could shrink for
    every group whenever an unrelated new status appeared anywhere else
    in the same episode; this per-group version bounds each group's
    contribution to [0,1] intrinsically and needs no global count at all.
    """
    if not primitive_log:
        return 0.0
    n = len(primitive_log)
    conditional: dict[tuple[str, str], Counter[str]] = {}
    for event in primitive_log:
        primitive = event.get("primitive", {})
        kind = str(primitive.get("kind", "unknown")) if isinstance(primitive, dict) else "unknown"
        state = event.get("observable_state", {})
        state_key = repr(sorted(state.items())) if isinstance(state, dict) else "unknown"
        conditional.setdefault((kind, state_key), Counter())[str(event.get("status", "unknown"))] += 1
    entropy = 0.0
    for group in conditional.values():
        group_n = sum(group.values())
        distinct = len(group)
        if distinct <= 1:
            continue  # zero contribution by construction; no denominator needed
        group_entropy = 0.0
        for count in group.values():
            p = count / group_n
            group_entropy -= p * math.log2(p)
        group_max_ent = math.log2(distinct)
        entropy += (group_n / n) * (group_entropy / group_max_ent)
    return entropy


def _margin_density(decision_margins: list[float]) -> float:
    # Only optimizer decision margins estimate borderline choices.  Denial
    # frequency is an outcome property and must not silently substitute for
    # the pre-registered decision-margin component.
    if not decision_margins:
        return 0.0
    return sum(1 for m in decision_margins if m < 0.05) / len(decision_margins)


def compute_eai(
    primitive_log: list[dict],
    decision_margins: list[float],
    tier_i_fraction: float,
) -> float:
    """Operational EAI per DESIGN.md (equal-weight components)."""
    if not primitive_log:
        return 0.0
    ent_norm = _entropy_component(primitive_log)
    margin_density = _margin_density(decision_margins)
    tier_i_load = min(1.0, max(0.0, tier_i_fraction))
    return (ent_norm + margin_density + tier_i_load) / 3.0


def compute_eai_at_tier(
    primitive_log: list[dict],
    decision_margins: list[float],
    tier_i_fraction: float,
    tier: str,
) -> float:
    """Referee-vantage EAI (DESIGN.md "EAI-referee", FINDINGS GL-19).

    Reuses `compute_eai` unmodified, but conditions its entropy term on a
    tier-projected log (`oracle_only.events.project_primitive_log`) instead
    of the raw, full-agent-context log. `decision_margins` and
    `tier_i_fraction` are passed through unchanged per the pre-registered
    scope — only the entropy term's observer changes. At `tier="light"`,
    `primitive`/`observable_state` are stripped by the projection, so the
    entropy term degenerates to one group per this function's grouping
    (marginal status entropy), by construction.
    """
    projected = project_primitive_log(primitive_log, tier)
    return compute_eai(projected, decision_margins, tier_i_fraction)


def eai_components_at_tier(
    primitive_log: list[dict],
    decision_margins: list[float],
    tier_i_fraction: float,
    tier: str,
) -> dict[str, float]:
    """Same three components `compute_eai_at_tier` averages, reported
    separately — for decomposition reporting (FINDINGS GL-18/GL-19 style),
    not for the calibration battery's pass criteria, which use the single
    scalar `compute_eai`/`compute_eai_at_tier`."""
    projected = project_primitive_log(primitive_log, tier)
    return {
        "entropy": _entropy_component(projected),
        "margin_density": _margin_density(decision_margins),
        "tier_i_load": min(1.0, max(0.0, tier_i_fraction)),
    }


def compute_eai_stub(log: list[dict]) -> float:
    """Backward-compatible alias used by early stubs/tests."""
    return compute_eai(log, [], tier_i_fraction=0.0)
