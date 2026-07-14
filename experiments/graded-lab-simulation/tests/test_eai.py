"""Unit tests for `oracle_only/eai.py`'s EAI-v2 per-group entropy fix.

See `DESIGN.md` "EAI-v2: logging and normalization fix" and FINDINGS
G-16/G-18. These are synthetic-log tests, not full episodes — cheap,
deterministic, and independent of the world/harness modules.
"""

from __future__ import annotations

from graded_lab.oracle_only.eai import (
    compute_eai,
    compute_eai_at_tier,
    compute_eai_stub,
    eai_components_at_tier,
)


def _entry(kind: str, state: dict, status: str) -> dict:
    return {"primitive": {"kind": kind}, "observable_state": state, "status": status}


def test_compute_eai_empty_log_is_zero():
    assert compute_eai([], [], tier_i_fraction=0.0) == 0.0


def test_compute_eai_all_identical_outcomes_has_zero_entropy_component():
    """A log where every (kind, state) group is homogeneous must
    contribute zero entropy regardless of the number of distinct
    top-level statuses in the whole log — the EAI-v2 fix for FINDINGS
    G-16's global-normalizer defect."""
    log = [_entry("read", {"busy": False}, "ok") for _ in range(5)] + [
        _entry("call", {"busy": True}, "denied") for _ in range(5)
    ]
    # Two distinct statuses overall ("ok", "denied"), but each is
    # perfectly determined by its own (kind, state) group.
    eai = compute_eai(log, [], tier_i_fraction=0.0)
    assert eai == 0.0


def test_compute_eai_mixed_outcome_group_contributes_full_entropy():
    """A single (kind, state) group with a 50/50 outcome split
    contributes its own per-group-normalized entropy (1.0, since two
    equiprobable outcomes saturate log2(2))."""
    log = [_entry("call", {"busy": False}, "ok") for _ in range(5)] + [
        _entry("call", {"busy": False}, "denied") for _ in range(5)
    ]
    eai = compute_eai(log, [], tier_i_fraction=0.0)
    # entropy component is the only nonzero term here (no margins, no
    # tier-I fraction), so eai == ent_norm / 3.
    assert abs(eai - (1.0 / 3.0)) < 1e-9


def test_compute_eai_new_status_label_elsewhere_does_not_shrink_normalizer():
    """FINDINGS G-16's second Cause-2 point, as a regression, holding
    group sizes/weights fixed so only the normalizer bug is isolated
    (not the — correct — dilution-by-more-entries effect covered by the
    test above): a same-size, fully-separate homogeneous group must
    contribute the same (zero) amount whether its status label is one
    already seen elsewhere in the log or a brand-new one. The old
    `max_ent = log2(len(distinct_statuses_in_whole_log))` normalizer
    would have shrunk the *mixed* group's contribution more in the
    "brand-new label" case (3 distinct global statuses vs 2) purely
    because of a label that group never produces; the per-group
    normalizer must not."""
    mixed_group = [_entry("call", {"busy": False}, "ok") for _ in range(5)] + [
        _entry("call", {"busy": False}, "denied") for _ in range(5)
    ]
    other_group_reusing_status = [_entry("read", {"busy": True}, "ok") for _ in range(10)]
    other_group_new_status = [_entry("read", {"busy": True}, "skipped") for _ in range(10)]

    eai_reused_label = compute_eai(
        mixed_group + other_group_reusing_status, [], tier_i_fraction=0.0
    )
    eai_new_label = compute_eai(
        mixed_group + other_group_new_status, [], tier_i_fraction=0.0
    )
    assert abs(eai_reused_label - eai_new_label) < 1e-9


def test_compute_eai_falls_back_gracefully_on_missing_primitive_and_state():
    """Backward compatibility: log entries predating the EAI-v2 logging
    fix (no `primitive`/`observable_state` keys at all) must not raise
    and must still fold into the single-group ``("unknown", "unknown")``
    bucket exactly as before."""
    log = [{"status": "ok"} for _ in range(3)] + [{"status": "denied"} for _ in range(3)]
    eai = compute_eai(log, [], tier_i_fraction=0.0)
    assert abs(eai - (1.0 / 3.0)) < 1e-9


def test_compute_eai_includes_margin_density_and_tier_i_components():
    log = [_entry("read", {"busy": False}, "ok") for _ in range(4)]
    eai = compute_eai(log, [0.01, 0.5, 0.02], tier_i_fraction=0.5)
    # entropy=0 (homogeneous), margin_density=2/3 (two of three < 0.05), tier_i=0.5
    expected = (0.0 + (2.0 / 3.0) + 0.5) / 3.0
    assert abs(eai - expected) < 1e-9


def test_compute_eai_stub_matches_zero_margin_zero_tier_i():
    log = [_entry("call", {"busy": False}, "ok") for _ in range(4)]
    assert compute_eai_stub(log) == compute_eai(log, [], tier_i_fraction=0.0)


def test_compute_eai_at_tier_full_matches_compute_eai():
    """"full" tier keeps `primitive`/`observable_state` — must reproduce
    the raw `compute_eai` value exactly (DESIGN.md "EAI-referee")."""
    log = [_entry("call", {"busy": False}, "ok") for _ in range(5)] + [
        _entry("call", {"busy": False}, "denied") for _ in range(5)
    ]
    eai_full_tier = compute_eai_at_tier(log, [], tier_i_fraction=0.0, tier="full")
    eai_raw = compute_eai(log, [], tier_i_fraction=0.0)
    assert eai_full_tier == eai_raw


def test_compute_eai_at_tier_light_strips_grouping_and_can_raise_entropy():
    """FINDINGS G-19/G-20: a "light"-tier projection drops `primitive`/
    `observable_state`, collapsing every event into one group — the
    per-group-homogeneous log above (zero entropy at "full" tier) must
    show nonzero entropy at "light" tier, since from that coarser
    vantage the two `(kind, state)` groups are no longer distinguishable
    and the marginal status distribution is genuinely mixed."""
    log = [_entry("call", {"busy": False}, "ok") for _ in range(5)] + [
        _entry("read", {"busy": True}, "denied") for _ in range(5)
    ]
    eai_full_tier = compute_eai_at_tier(log, [], tier_i_fraction=0.0, tier="full")
    eai_light_tier = compute_eai_at_tier(log, [], tier_i_fraction=0.0, tier="light")
    assert eai_full_tier == 0.0
    assert eai_light_tier > eai_full_tier
    assert abs(eai_light_tier - (1.0 / 3.0)) < 1e-9


def test_eai_components_at_tier_reports_entropy_margin_tier_i_separately():
    log = [_entry("read", {"busy": False}, "ok") for _ in range(3)] + [
        _entry("call", {"busy": True}, "aborted") for _ in range(3)
    ]
    components = eai_components_at_tier(log, [0.5], tier_i_fraction=0.4, tier="light")
    assert set(components) == {"entropy", "margin_density", "tier_i_load"}
    assert components["margin_density"] == 0.0  # 0.5 is not < 0.05
    assert components["tier_i_load"] == 0.4
    assert components["entropy"] > 0.0  # light tier collapses the two groups into one, mixed
