"""Audit projection: oracle rows -> audit-visible channel series, tier-gated.

The plane boundary of this line. `ORACLE_ONLY_FIELDS` never cross it; a test
enforces the split. Instrumentation tiers are a simplified two-level version
of the old line's six-level ladder (the tier *ladder* was a finding of that
line and is not re-derived here):

- ``light``: what passive log collection gives you — correction requests,
  reports, visible actions, probe flags and intents.
- ``full``:  adds handle telemetry — welfare deltas, routing codes, lineage,
  sign-off events, practice fingerprint, and initiator attribution.

Ontological drift (2026-07-05) lives HERE, at the audit boundary: passing an
`ontology.OntologyDrift` to `project_rows` re-derives each row's routing code
through the drifted category->code assignment before the oracle fields are
stripped. Ground truth, labels, and the light tier (which carries no routing
codes) are untouched by construction.
"""

from __future__ import annotations

from .ontology import OntologyDrift

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
        # Phase 6 (world.py "Phase 6 oracle field", agents.BoardPolicy
        # "certifier capture"): NEVER audit-visible by construction -- an
        # audit that could directly see "the certifier is captured" would
        # beg the question the mechanism exists to explore.
        "board_captured",
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
        # Phase 4d (world.py "Phase 4d stock variables"): the running covert-
        # resource draw and the per-step stalling-mode flag.
        "resource_accum",
        "stall_flag",
    }
)

TIER_FIELDS: dict[InstrumentationTier, frozenset[str]] = {
    "light": LIGHT_FIELDS,
    "full": LIGHT_FIELDS | FULL_EXTRA_FIELDS,
}


def project_rows(
    rows: list[dict],
    tier: InstrumentationTier,
    drift: OntologyDrift | None = None,
) -> list[dict]:
    fields = TIER_FIELDS[tier]
    projected = [{k: r[k] for k in fields} for r in rows]
    if drift is not None and "action_cause_code" in fields:
        # Recompute routing codes through the drifted audit ontology, keyed
        # by the agent's semantic category (`true_cause`, read from the
        # oracle input but never emitted).
        for out, r in zip(projected, rows):
            out["action_cause_code"] = drift.drifted_code(
                r["true_cause"], r["action_cause_code"]
            )
    return projected


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
                "channel.resource_accum": [float(r["resource_accum"]) for r in projected],
                "channel.stall_flag": [float(r["stall_flag"]) for r in projected],
            }
        )
    return out
