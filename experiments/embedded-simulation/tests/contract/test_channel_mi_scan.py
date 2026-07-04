"""Contract test for the pre-registered channel_mi_scan.py discovery instrument.

Pins the acceptance criteria from `channel_mi_scan.py`'s module docstring:
every one of the 88 (channel, functional) cells must be reported (nothing
silently dropped after looking at results), the Bonferroni corrections must
match the documented formulas, and the greedy best-of-k curve must behave the
way a genuine joint-MI curve has to behave (each additional selected feature
can only add or preserve information about the label, never destroy it,
because the k+1 joint code is a strict refinement of the k joint code).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from channel_mi_scan import CELLS, K_MAX, N_CELLS, NULL_PERCENTILE_CELLS, NULL_PERCENTILE_K

RESULTS_JSON = Path(__file__).resolve().parents[2] / "results" / "channel_mi_scan.json"


@pytest.fixture(scope="module")
def result():
    if not RESULTS_JSON.exists():
        pytest.skip("results not generated yet; run channel_mi_scan.py")
    return json.loads(RESULTS_JSON.read_text(encoding="utf-8"))


def test_cell_count_is_22_channels_times_4_functionals():
    assert N_CELLS == 88
    assert len(CELLS) == 88


def test_null_percentiles_are_bonferroni_corrected():
    assert NULL_PERCENTILE_CELLS == pytest.approx(1.0 - 0.05 / 88)
    assert NULL_PERCENTILE_K == pytest.approx(1.0 - 0.05 / 6)


def test_every_cell_is_reported_exactly_once(result):
    reported = {(r["channel"], r["functional"]) for r in result["best_of_1_scan"]}
    assert reported == set(CELLS)
    assert len(result["best_of_1_scan"]) == N_CELLS


def test_best_of_k_curve_covers_k_1_through_k_max_in_order(result):
    ks = [row["k"] for row in result["best_of_k_curve"]]
    assert ks == list(range(1, K_MAX + 1))
    for row in result["best_of_k_curve"]:
        assert len(row["subset"]) == row["k"]


def test_exploration_joint_mi_is_non_decreasing_in_k(result):
    """The k+1 joint code is a strict refinement of the k joint code (each
    additional selected feature only ever adds digits to the same base-n_bins
    encoding), so grouping/data-processing gives MI(codes_{k+1}; Y) >=
    MI(codes_k; Y) as an exact property, not just a hoped-for trend. A
    violation would indicate a bug in `joint_code`'s incremental encoding."""
    estimates = [row["exploration"]["estimate"] for row in result["best_of_k_curve"]]
    for a, b in zip(estimates, estimates[1:]):
        assert b >= a - 1e-9


def test_alias_groups_are_data_detected_and_annotated_on_cells(result):
    """Self-critique fix (2026-07-03): several of the 22 nominal channels are
    not independent -- some are literal duplicates of the same underlying
    field, others are degenerate (constant in this 8-scenario battery). Both
    must be surfaced, not silently left for a reader to discover via an
    unexplained exact tie in the scores."""
    groups = result["known_alias_channel_groups"]
    assert groups, "expected at least one detected alias group in this battery"
    for group in groups:
        assert len(group["channels"]) >= 2
        assert isinstance(group["degenerate"], bool)
    aliased = {c for g in groups for c in g["channels"]}
    by_channel = {r["channel"]: r for r in result["best_of_1_scan"] if r["functional"] == "mean"}
    for channel in aliased:
        assert by_channel[channel]["alias_of"], f"{channel} should list its alias partners"


def test_known_duplicate_pair_ties_exactly(result):
    """Pins the specific duplicate this session's self-critique caught:
    `handle.outcome_spillover` and `artifact.sensor` are both raw `harm`,
    so their exploration-side estimates must match exactly, not just be
    close -- if this ever stops being an exact tie, the simulator's field
    mapping changed and the docstring's alias list needs updating."""
    by_key = {(r["channel"], r["functional"]): r for r in result["best_of_1_scan"]}
    a = by_key[("handle.outcome_spillover", "mean")]
    b = by_key[("artifact.sensor", "mean")]
    assert a["estimate"] == b["estimate"]


def test_selected_features_are_distinct_across_k(result):
    for row in result["best_of_k_curve"]:
        subset_keys = [(f["channel"], f["functional"]) for f in row["subset"]]
        assert len(subset_keys) == len(set(subset_keys))


def test_best_single_channel_finding_replicates_on_held_out_validation_seeds(result):
    """The top individually-informative cell from exploration-side greedy
    selection (k=1) must also clear the (held-out, never-selected-on)
    validation seeds -- the honest, post-selection confirmation this split
    exists to provide. This is the one result this script is allowed to call
    a *confirmed* finding rather than a search artifact."""
    k1 = result["best_of_k_curve"][0]
    assert k1["k"] == 1
    assert k1["validation"]["detected"] is True


def test_generalization_curve_reuses_the_frozen_selected_subsets(result):
    """Phase 0 addendum: the scenario-mechanism generalization check must
    re-score the *same* k-subsets the greedy search already froze on
    exploration seeds, not re-select on the generalization sample -- that
    would defeat the point (it would just be more search, not a
    generalization test of a fixed finding)."""
    for row, gen_row in zip(result["best_of_k_curve"], result["generalization_curve"], strict=True):
        assert row["k"] == gen_row["k"]
        assert row["subset"] == gen_row["subset"]


def test_generalization_curve_covers_k_1_through_k_max(result):
    ks = [row["k"] for row in result["generalization_curve"]]
    assert ks == list(range(1, K_MAX + 1))
    for row in result["generalization_curve"]:
        assert set(row["generalization"].keys()) >= {"estimate", "ci_lo", "null_95th", "detected"}
        assert row["generalization_gap"] == pytest.approx(
            next(r for r in result["best_of_k_curve"] if r["k"] == row["k"])["exploration"]["estimate"]
            - row["generalization"]["estimate"]
        )


def test_phase_0_5_curve_present_when_results_regenerated(result):
    """Phase 0.5 addendum: optional until `channel_mi_scan.py` is re-run."""
    if "phase_0_5_curve" not in result:
        pytest.skip("phase_0_5_curve not in results yet; re-run channel_mi_scan.py")
    for row, p05_row in zip(result["best_of_k_curve"], result["phase_0_5_curve"], strict=True):
        assert row["k"] == p05_row["k"]
        assert row["subset"] == p05_row["subset"]
        assert set(p05_row["phase_0_5_honest"].keys()) >= {"estimate", "ci_lo", "null_95th", "detected"}


def test_winners_curse_gaps_stay_small_for_this_battery(result):
    """Not a universal guarantee -- just documents what was actually measured:
    for this battery/seed budget the greedy exploration-side estimate and the
    held-out validation-side estimate stay close (bits), i.e. selection did
    not badly overfit the exploration draw. A future rerun with a much wider
    channel/functional grid (higher multiplicity) or fewer seeds could show a
    larger gap; if so, update this bound rather than silently loosening it."""
    for row in result["best_of_k_curve"]:
        assert abs(row["winners_curse_gap"]) < 0.15
