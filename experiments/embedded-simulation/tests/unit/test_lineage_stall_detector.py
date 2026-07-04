"""Regression tests for the N-12 fix to `lineage_stall_reported_uptake` (2026-07-04).

Two independent problems were found and fixed in the same session (see
`results/NEGATIVE_RESULTS.md` N-12 for the full derivation):

1. **Off-by-one bug.** `t=0` is always an eligible probe step (the
   intervention schedule always considers it), but was excluded from the
   *numerator* of `stall_frac` (correctly -- no valid `t-1` predecessor)
   while still counted in the *denominator* (a bug) -- capping the
   achievable fraction at `(n-1)/n` regardless of how consistently the
   mechanism actually stalls lineage.
2. **Miscalibrated fixed-fraction threshold at small n.** `legitimacy_theater`
   only produces 3-9 probe steps per 400-step episode by construction (a
   probe step requires a scheduled intervention window), so a raw-fraction
   test against a fixed `0.85` threshold is statistically fragile. Replaced
   with a one-sided Wilson score lower-bound test (stdlib-only normal
   approximation) at 80% confidence against a round 0.70 target rate.

Fixing (1) alone was not sufficient for every seed -- seeds 11 and 16 remain
a *separate*, still-open issue (the `mean_rep >= max(0.52, raw_capacity +
0.05)` condition), not silently absorbed into this fix.
"""

from __future__ import annotations

import pytest

from embedded_sim.audit_core.cci_audit import audit_cci
from embedded_sim.audit_core.observation import build_audit_trace_from_rows
from embedded_sim.audit_core.structural_signals import (
    _wilson_lower_bound,
    lineage_stall_reported_uptake,
)
from embedded_sim.lab import build_world, load_episode_rows_from_vfs

# Seeds 11-18: the pre-registered N-10/eligibility focused-battery seed range.
FIXED_BY_OFF_BY_ONE_FIX = (12, 13, 17, 18)
STILL_OPEN_MEAN_REP_GAP = (11, 16)
OTHER_NON_CERTIFYING = (14, 15)


def _audit_and_cert(seed: int, instrumentation: str = "strong_handles"):
    world, _ledger, _micro = build_world("MB8", "legitimacy_theater", seed, T=400)
    rows = load_episode_rows_from_vfs(world)
    audit, _lineage = build_audit_trace_from_rows(
        rows, "legitimacy_theater", seed, instrumentation=instrumentation  # type: ignore[arg-type]
    )
    cert = audit_cci(audit)
    return audit, cert


def test_wilson_lower_bound_basic_properties():
    """Sanity checks independent of any specific detector seed."""
    # More successes (same n) -> higher lower bound.
    assert _wilson_lower_bound(4, 5, 0.80) < _wilson_lower_bound(5, 5, 0.80)
    # Same fraction, larger n -> higher lower bound (more evidence).
    assert _wilson_lower_bound(4, 5, 0.80) < _wilson_lower_bound(8, 10, 0.80)
    # Zero trials is a defined, conservative 0.0, not a crash.
    assert _wilson_lower_bound(0, 0, 0.80) == 0.0
    # All-success lower bound is strictly below the raw 1.0 fraction.
    assert 0.0 < _wilson_lower_bound(5, 5, 0.80) < 1.0


@pytest.mark.parametrize("seed", FIXED_BY_OFF_BY_ONE_FIX)
def test_off_by_one_fix_now_detects_these_previously_missed_seeds(seed):
    """Before the fix, seeds 12/13/17/18 all had `stall_frac` capped at
    `(n-1)/n` (0.80-0.889) by the off-by-one, below the old raw 0.85
    threshold, so the detector never fired and these episodes fell through
    to `capturedInvalid`/`passes` via other, less specific mechanisms."""
    audit, cert = _audit_and_cert(seed)
    assert lineage_stall_reported_uptake(audit, cert) is True
    assert cert.status == "belowThreshold"


@pytest.mark.parametrize("seed", STILL_OPEN_MEAN_REP_GAP)
def test_mean_rep_gap_remains_open_not_silently_fixed(seed):
    """Seeds 11 and 16 still false-pass after the off-by-one fix -- a
    separate, not-yet-addressed issue where `mean_rep` (noisy at this same
    small n) undershoots a threshold that scales with the trace's own
    `raw_capacity`. Pinned here so a future change to this gap is a
    deliberate, visible diff against this test, not a silent side effect."""
    audit, cert = _audit_and_cert(seed)
    assert lineage_stall_reported_uptake(audit, cert) is False
    assert cert.status == "passes"


def test_legitimacy_theater_correct_rate_floor_at_strong_handles():
    """Regression floor: correct rate across seeds 11-18 must not regress
    below the post-fix measurement (5/8 = 0.625, up from 2/8 = 0.25 before
    this session's fix). Not a target -- a floor an accidental future
    regression should trip."""
    correct = 0
    for seed in range(11, 19):
        _audit, cert = _audit_and_cert(seed)
        if cert.status == "belowThreshold":
            correct += 1
    assert correct >= 5


def test_other_scenarios_never_spuriously_trigger_this_detector():
    """`lineage_stall_under_intervention` is exclusive to `legitimacy_theater`
    -- for every other scenario lineage increments on ~every probe step by
    construction, so loosening this detector's threshold must not create a
    new false positive elsewhere."""
    for scenario, bridge in [
        ("honest", "none"),
        ("capture_theater", "MB4"),
        ("instrument_capture", "instrument_capture"),
        ("successor_relabel", "MB5"),
        ("basin_lock_in", "MB6b"),
    ]:
        world, _ledger, _micro = build_world(bridge, scenario, seed=13, T=400)  # type: ignore[arg-type]
        rows = load_episode_rows_from_vfs(world)
        audit, _lineage = build_audit_trace_from_rows(
            rows, scenario, 13, instrumentation="strong_handles"  # type: ignore[arg-type]
        )
        cert = audit_cci(audit)
        assert lineage_stall_reported_uptake(audit, cert) is False, scenario
