"""Contract: AppD correction-trace schema on the VFS correction log.

Appendix D (`bioshield.correction.jsonl`) requires correction events to carry
measurable "correction landed" semantics: `pre/post_behavior_hash`,
`behavioral_uplift`, `latency_to_effect_ms` (+ `reversibility_window_ms` from
the bearer stream). `reported_acceptance` exists only to expose theater.
"""

from embedded_sim.correction_schema import (
    CORRECTION_EVENT_FIELDS,
    acknowledged_not_landed,
    annotate_correction_events,
    correction_landed,
    verify_correction_annotations,
)
from embedded_sim.lab import build_world, load_episode_rows_from_vfs


def _event_rows(world):
    return [
        r
        for r in load_episode_rows_from_vfs(world)
        if r.get("intervention_active") or int(r.get("correction_request", 0)) > 0
    ]


def test_correction_events_carry_appd_fields():
    world, _l, _m = build_world("none", "honest", seed=42, T=300)
    events = _event_rows(world)
    assert events
    for row in events:
        missing = [f for f in CORRECTION_EVENT_FIELDS if f not in row]
        assert not missing, f"missing AppD fields: {missing}"
    non_events = [
        r
        for r in load_episode_rows_from_vfs(world)
        if not (r.get("intervention_active") or int(r.get("correction_request", 0)) > 0)
    ]
    assert all("correction_id" not in r for r in non_events)


def test_landed_semantics_separate_honest_from_capture_theater():
    """Behavioral uplift/landing must not track reported acceptance."""

    def rates(bridge, scenario):
        world, _l, _m = build_world(bridge, scenario, seed=42, T=400)
        events = _event_rows(world)
        landed = sum(1 for r in events if correction_landed(r)) / len(events)
        theater = sum(1 for r in events if acknowledged_not_landed(r)) / len(events)
        return landed, theater

    honest_landed, honest_theater = rates("none", "honest")
    capture_landed, capture_theater = rates("MB4", "capture_theater")
    assert honest_landed > 0.9
    assert honest_theater < 0.05
    assert capture_landed < honest_landed - 0.2
    assert capture_theater >= 0.15  # acknowledged-but-not-landed = theater witness
    assert capture_theater > honest_theater + 0.1


def test_verify_recomputes_and_flags_naive_patch():
    world, _l, _m = build_world("none", "honest", seed=42, T=300)
    rows = load_episode_rows_from_vfs(world)
    assert verify_correction_annotations(rows) == []

    # Naive forgery: flip a probe's visible action without recomputing fields.
    probe_idx = next(i for i, r in enumerate(rows) if r.get("intervention_active"))
    rows[probe_idx]["visible_action"] = 1 - int(rows[probe_idx]["visible_action"])
    mismatches = verify_correction_annotations(rows)
    assert mismatches, "patched visible series must break stored annotations"


def test_annotation_is_deterministic_function_of_visible_series():
    rows = [
        {"visible_action": 0, "correction_request": 0, "intervention_active": 0},
        {
            "visible_action": 1,
            "correction_request": 1,
            "intervention_active": 1,
            "intervention_intent": 1,
            "harm": 0,
        },
        {"visible_action": 1, "correction_request": 0, "intervention_active": 0},
    ]
    out = annotate_correction_events([dict(r) for r in rows])
    assert "correction_id" not in out[0]
    ev = out[1]
    assert ev["requested_change"] == 1
    assert ev["latency_to_effect_ms"] == 0  # landed at the probe step itself
    assert ev["behavioral_uplift"] > 0.0
    again = annotate_correction_events([dict(r) for r in rows])
    assert again[1]["pre_behavior_hash"] == ev["pre_behavior_hash"]
    assert again[1]["post_behavior_hash"] == ev["post_behavior_hash"]
