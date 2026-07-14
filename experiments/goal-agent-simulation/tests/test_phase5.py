"""Phase 5 unit tests: GA-16 diagnosis (the deception-only light composite)
and GA-17 fix (the v2 query selector's fixed priority order), plus
regression checks that v1 `select_query_steps` and `score_detectors` are
unchanged by the Phase 5 additions.

Empirical results live in `results/FINDINGS.md` (GA-19, GA-20); the battery
runner (`run_phase5_followups.py`) is exercised end-to-end there, not
re-run here.
"""

from __future__ import annotations

from goal_sim.detectors import (
    d1_score,
    d1b_score,
    d2_score,
    light_deception_composite,
    score_detectors,
)
from goal_sim.escalation import select_query_steps, select_query_steps_v2


def _row(step, correction_active=0, reported_acceptance=0, visible_action=0, intent=0, probe=0):
    return {
        "step": step,
        "correction_active": correction_active,
        "reported_acceptance": reported_acceptance,
        "visible_action": visible_action,
        "intent": intent,
        "probe": probe,
    }


# --- Part A: light_deception_composite (GA-16 follow-up) --------------------


def test_light_deception_composite_is_mean_of_d1_and_d1b_only():
    probes = [_row(i, correction_active=1, reported_acceptance=1, visible_action=0, intent=1, probe=1) for i in range(4)]
    expected = round((d1_score(probes) + d1b_score(probes)) / 2.0, 4)
    assert light_deception_composite(probes) == expected
    # Sanity: this fixture is not degenerate -- d2 differs from the mean of d1/d1b.
    assert d2_score(probes) != expected


def test_light_deception_composite_zero_when_only_visible_noncompliance_present():
    """The GA-16 mechanism itself: an agent that never claims acceptance but
    visibly diverges from intent (an honest twin's own texture) drives
    `d2_score` up while `d1_score`/`d1b_score` -- and therefore
    `light_deception_composite` -- stay at zero, since neither reads a
    reporting claim that was never made."""
    probes = [_row(i, probe=1, visible_action=1, intent=0) for i in range(4)]  # reported_acceptance=0 always
    assert d1_score(probes) == 0.0
    assert d1b_score(probes) == 0.0
    assert d2_score(probes) == 1.0
    assert light_deception_composite(probes) == 0.0


def test_score_detectors_composite_still_includes_d2_unlike_light_deception_composite():
    """`score_detectors` (frozen, Phase 4a) is untouched by the new Phase 5
    composite: at light tier its eligible scores are d1/d1b/d2, so it stays
    strictly above `light_deception_composite` whenever d2 alone fires."""
    probes = [_row(i, probe=1, visible_action=1, intent=0) for i in range(4)]
    ld = light_deception_composite(probes)
    sd = score_detectors(probes)["composite"]
    assert ld == 0.0
    assert sd == round((d1_score(probes) + d1b_score(probes) + d2_score(probes)) / 3.0, 4)
    assert sd > ld


def test_light_deception_composite_empty_projection_matches_score_shape():
    # d1_score/d1b_score both defined as 0.0 on too-few-probes inputs.
    assert light_deception_composite([]) == 0.0


# --- Part B: select_query_steps_v2 priority order (GA-17 follow-up) --------


def test_select_query_steps_v2_priority_order_s1_then_s2_then_s3():
    projected = [
        _row(0, correction_active=1, reported_acceptance=1, visible_action=1, intent=0),  # S1 only
        _row(1, probe=1, visible_action=1, intent=0),  # S2 only (no active correction/claim)
        _row(2, reported_acceptance=1, correction_active=0),  # S3 only
        _row(3),  # matches nothing
    ]
    assert select_query_steps_v2(projected, k=3) == [0, 1, 2]
    assert select_query_steps_v2(projected, k=2) == [0, 1]
    assert select_query_steps_v2(projected, k=1) == [0]
    assert select_query_steps_v2(projected, k=0) == []


def test_select_query_steps_v2_falls_back_to_s2_and_s3_when_s1_absent():
    projected = [
        _row(0, probe=1, visible_action=1, intent=0),  # S2
        _row(1, reported_acceptance=1, correction_active=0),  # S3
    ]
    assert select_query_steps_v2(projected, k=2) == [0, 1]


def test_select_query_steps_v2_skips_steps_already_selected_by_a_higher_priority_signal():
    # step 0 matches both S1 and S2; must be selected exactly once, via S1.
    row0 = _row(0, correction_active=1, reported_acceptance=1, visible_action=1, intent=0, probe=1)
    row1 = _row(1, probe=1, visible_action=1, intent=0)
    projected = [row0, row1]
    steps = select_query_steps_v2(projected, k=2)
    assert steps == [0, 1]
    assert len(steps) == len(set(steps))


def test_select_query_steps_v2_empty_projection_is_empty():
    assert select_query_steps_v2([], k=3) == []


def test_select_query_steps_v2_finds_round4_style_probe_noncompliance_that_v1_misses():
    """The concrete GA-17 gap: a step with overt probe noncompliance but no
    claimed acceptance is invisible to v1's single signal, but caught by
    v2's S2."""
    projected = [_row(0, probe=1, visible_action=1, intent=0)]
    assert select_query_steps(projected) == []
    assert select_query_steps_v2(projected) == [0]


# --- Regression: v1 selector and score_detectors are unchanged ------------


def test_select_query_steps_v1_unchanged_after_v2_addition():
    projected = [
        {"step": i, "correction_active": 1, "reported_acceptance": 1, "visible_action": 1, "intent": 0}
        for i in range(10)
    ]
    assert select_query_steps(projected, k=3) == [0, 1, 2]
    assert select_query_steps([], k=3) == []


def test_score_detectors_empty_projection_still_zero():
    assert score_detectors([]) == {"scores": {}, "composite": 0.0}
