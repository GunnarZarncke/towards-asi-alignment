"""Audit projection: oracle rows -> audit-visible channel series, tier-gated.

The plane boundary of this line. `ORACLE_ONLY_FIELDS` never cross it; a test
enforces the split. Instrumentation tiers are a simplified two-level version
of the old line's six-level ladder (the tier *ladder* was a finding of that
line and is not re-derived here):

- ``light``: what passive log collection gives you — correction requests,
  reports, visible actions, probe flags and intents.
- ``full``:  adds handle telemetry — welfare deltas, routing codes, lineage,
  sign-off events, practice fingerprint, and initiator attribution.
"""

from __future__ import annotations

InstrumentationTier = str  # "light" | "full"

ORACLE_ONLY_FIELDS = frozenset(
    {
        "true_action",
        "true_uptake",
        "true_cause",
        "true_action_name",
        "true_harm",
        "true_silent_harm",
        "true_welfare",
        "true_throughput",
        "true_practice_adopted",
        "true_practice_approved",
    }
)

LIGHT_FIELDS = frozenset(
    {
        "step",
        "task_goal",
        "correction_active",
        "probe",
        "intent",
        "reported_acceptance",
        "visible_action",
        "escalated",
    }
)

FULL_EXTRA_FIELDS = frozenset(
    {
        "high_stakes",
        "welfare_delta",
        "lineage_tick",
        "sign_off",
        "practice_fingerprint",
        "action_cause_code",
        "initiator_actor_id",
    }
)

TIER_FIELDS: dict[InstrumentationTier, frozenset[str]] = {
    "light": LIGHT_FIELDS,
    "full": LIGHT_FIELDS | FULL_EXTRA_FIELDS,
}


def project_rows(rows: list[dict], tier: InstrumentationTier) -> list[dict]:
    fields = TIER_FIELDS[tier]
    return [{k: r[k] for k in fields} for r in rows]


def channel_series_map(projected: list[dict], tier: InstrumentationTier) -> dict[str, list[float]]:
    """Numeric per-step series for every channel visible at this tier
    (consumed by the mini MI scan and by anyone comparing channels)."""
    out: dict[str, list[float]] = {
        "channel.correction_request": [float(r["correction_active"]) for r in projected],
        "channel.reported_uptake": [float(r["reported_acceptance"]) for r in projected],
        "channel.probe_flag": [float(r["probe"]) for r in projected],
        "channel.action_observed": [float(r["visible_action"]) for r in projected],
        "channel.escalated": [float(r["escalated"]) for r in projected],
    }
    if tier == "full":
        out.update(
            {
                "channel.welfare_delta": [float(r["welfare_delta"]) for r in projected],
                "channel.lineage_tick": [float(r["lineage_tick"]) for r in projected],
                "channel.sign_off": [float(r["sign_off"]) for r in projected],
                "channel.practice_fingerprint": [
                    float(r["practice_fingerprint"]) for r in projected
                ],
                "channel.action_routing": [
                    float(r["action_cause_code"]) for r in projected
                ],
                "channel.initiator_is_agent": [
                    float(r["initiator_actor_id"] != "board.0") for r in projected
                ],
            }
        )
    return out
