"""Emergent Ambiguity Index — measured from logs only."""

from __future__ import annotations

import math
from collections import Counter

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


def compute_eai(
    primitive_log: list[dict],
    decision_margins: list[float],
    tier_i_fraction: float,
) -> float:
    """Operational EAI per DESIGN.md (equal-weight components)."""
    if not primitive_log:
        return 0.0

    outcomes = [str(e.get("status", "unknown")) for e in primitive_log]
    counts = Counter(outcomes)
    n = len(outcomes)
    # H(outcome | action, observable-state): the state summary is recorded
    # with the exact agent-visible observation when a primitive starts, never
    # reconstructed from oracle truth after the fact.
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
        group_entropy = 0.0
        for count in group.values():
            p = count / group_n
            group_entropy -= p * math.log2(p)
        entropy += (group_n / n) * group_entropy
    max_ent = math.log2(len(counts)) if len(counts) > 1 else 1.0
    ent_norm = entropy / max_ent if max_ent > 0 else 0.0

    # Only optimizer decision margins estimate borderline choices.  Denial
    # frequency is an outcome property and must not silently substitute for
    # the pre-registered decision-margin component.
    margin_density = (
        sum(1 for m in decision_margins if m < 0.05) / len(decision_margins)
        if decision_margins
        else 0.0
    )

    tier_i_load = min(1.0, max(0.0, tier_i_fraction))
    return (ent_norm + margin_density + tier_i_load) / 3.0


def compute_eai_stub(log: list[dict]) -> float:
    """Backward-compatible alias used by early stubs/tests."""
    return compute_eai(log, [], tier_i_fraction=0.0)
