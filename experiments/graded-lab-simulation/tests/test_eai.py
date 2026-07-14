"""Unit tests for `oracle_only/eai.py`'s EAI-v2 per-group entropy fix.

See `DESIGN.md` "EAI-v2: logging and normalization fix" and FINDINGS
G-16/G-18. These are synthetic-log tests, not full episodes — cheap,
deterministic, and independent of the world/harness modules.
"""

from __future__ import annotations

from graded_lab.oracle_only.eai import compute_eai, compute_eai_stub


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
