"""Regression tests for the ES-12 fixes to `lineage_stall_reported_uptake`
(2026-07-04, two sessions).

Three independent problems were found and fixed (see
`results/NEGATIVE_RESULTS.md` ES-12 for the full derivation):

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
3. **`raw_capacity`-scaled `mean_rep` floor (postscript 2, same date).**
   `mean_rep >= max(0.52, raw_capacity + 0.05)` compared reported acceptance
   against an unrelated interventional-capacity estimate; at seeds where
   `raw_capacity` happened to be high (0.75-0.80), the bar chased
   `raw_capacity` itself and exceeded an otherwise clearly-positive
   `mean_rep`. Replaced with the fixed floor alone (`mean_rep >= 0.52`) --
   `stall_confident` was independently verified as the exclusive
   discriminator (zero false positives across 18 other scenarios x 3
   instrumentation levels x 40 seeds), so this conjunct only needs to rule
   out a degenerate near-zero-report edge case, not track `raw_capacity`.

Fixing (1)+(2) alone was not sufficient for every seed -- seeds 11 and 16
needed fix (3).
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

# Seeds 11-18: the pre-registered ES-10/eligibility focused-battery seed range.
FIXED_BY_OFF_BY_ONE_FIX = (12, 13, 17, 18)
FIXED_BY_MEAN_REP_FLOOR_FIX = (11, 16)
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


@pytest.mark.parametrize("seed", FIXED_BY_MEAN_REP_FLOOR_FIX)
def test_mean_rep_floor_fix_now_detects_these_previously_missed_seeds(seed):
    """Seeds 11 and 16 false-passed after the off-by-one fix alone -- the
    `raw_capacity`-scaled `mean_rep` bar exceeded their otherwise clearly
    positive `mean_rep` (0.80, 0.75) precisely because `raw_capacity` was
    itself high (0.80, 0.75) at these seeds. Fixed floor resolves both."""
    audit, cert = _audit_and_cert(seed)
    assert lineage_stall_reported_uptake(audit, cert) is True
    assert cert.status == "belowThreshold"


def test_legitimacy_theater_correct_rate_floor_at_strong_handles():
    """Regression floor: correct rate across seeds 11-18 must not regress
    below the post-fix measurement (7/8 = 0.875, up from 5/8 = 0.625 after
    the off-by-one fix, 2/8 = 0.25 before any fix this session). Not a
    target -- a floor an accidental future regression should trip."""
    correct = 0
    for seed in range(11, 19):
        _audit, cert = _audit_and_cert(seed)
        if cert.status == "belowThreshold":
            correct += 1
    assert correct >= 7


def test_other_scenarios_never_spuriously_trigger_this_detector():
    """`lineage_stall_under_intervention` is exclusive to `legitimacy_theater`
    -- for every other scenario lineage increments on ~every probe step by
    construction, so loosening this detector's threshold must not create a
    new false positive elsewhere. Includes the Phase 0.5 honest scenarios
    (2026-07-04) since they are the newest additions least likely to have
    been considered when this detector was last tuned.

    A broader one-off check (not run here for speed) confirmed zero false
    positives for `stall_confident` alone across all other 18 scenarios x 3
    instrumentation levels x 40 seeds (11-18, 5000-5015, 6000-6015) --
    `results/NEGATIVE_RESULTS.md` ES-12 postscript 2."""
    for scenario, bridge in [
        ("honest", "none"),
        ("capture_theater", "MB4"),
        ("instrument_capture", "instrument_capture"),
        ("successor_relabel", "MB5"),
        ("basin_lock_in", "MB6b"),
        ("honest_mistakes", "none"),
        ("legitimate_gradual_improvement", "none"),
        ("benign_semantic_drift", "MB7"),
    ]:
        world, _ledger, _micro = build_world(bridge, scenario, seed=13, T=400)  # type: ignore[arg-type]
        rows = load_episode_rows_from_vfs(world)
        audit, _lineage = build_audit_trace_from_rows(
            rows, scenario, 13, instrumentation="strong_handles"  # type: ignore[arg-type]
        )
        cert = audit_cci(audit)
        assert lineage_stall_reported_uptake(audit, cert) is False, scenario
