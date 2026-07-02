"""Contract tests for the TraceBIQ ↔ Shannon-MI calibration.

Pins (a) the Python port of `TraceBIQ.lean` to the Lean-`decide`d numbers from
`formal/AlignmentProofSpine/WorkedInstance.lean`, and (b) the qualitative
calibration findings on the pinned fixture columns, so a silent change to
either side (the port, the estimators, or the committed columns) fails loudly.
"""

import json
from pathlib import Path

import pytest

from calibrate_trace_biq import (
    COLUMNS_FIXTURE,
    LEAN_DECIDED,
    WINDOW,
    diversity_alphabet_ceiling,
    lagged_diversity_score,
    lean_crosscheck,
    load_columns,
    run_calibration,
    shannon_lagged_mi,
)


@pytest.fixture(scope="module")
def cols():
    if not Path(COLUMNS_FIXTURE).exists():
        pytest.skip("columns fixture missing; run calibrate_trace_biq.py --regenerate-columns")
    return load_columns()


def test_columns_fixture_shape(cols):
    assert set(cols) == {
        "visible_action",
        "intervention_active",
        "judge_captured",
        "correction_request",
    }
    assert all(len(c) == 300 for c in cols.values())
    assert all(set(c) <= {0, 1} for c in cols.values())
    # Load-bearing fixture invariants the analysis relies on:
    assert all(v == 1 for v in cols["judge_captured"])  # judge captured throughout
    assert cols["correction_request"] == cols["intervention_active"]  # identical columns


def test_port_matches_lean_decided_numbers(cols):
    assert lean_crosscheck(cols) == LEAN_DECIDED


def test_mi_never_exceeds_tight_ceiling(cols):
    result = run_calibration(cols)
    assert result["findings"]["mi_le_tight_ceiling_violations"] == []


def test_score_underdetects_reversed_coupling(cols):
    """The fixture's real coupling (intervention → action 3 steps later) is
    visible to Shannon MI but scored 0 by the support-based diversity score
    (a single stray joint pattern collapses it)."""
    w = {f: c[:WINDOW] for f, c in cols.items()}
    x, y = w["intervention_active"], w["visible_action"]
    assert lagged_diversity_score(x, y, 3) == 0
    assert shannon_lagged_mi(x, y, 3) > 0.1


def test_score_overstates_sparse_identical_columns(cols):
    """Byte-identical sparse columns: score reads a full bit, plug-in MI of the
    rare pulse is well under half a bit."""
    w = {f: c[:WINDOW] for f, c in cols.items()}
    x, y = w["correction_request"], w["intervention_active"]
    assert lagged_diversity_score(x, y, 0) == 1
    assert shannon_lagged_mi(x, y, 0) < 0.5


def test_ceiling_values():
    assert diversity_alphabet_ceiling(26, 2) == 1
    assert diversity_alphabet_ceiling(300, 2) == 1
    assert diversity_alphabet_ceiling(1, 2) == 0


def test_results_json_in_sync(cols):
    """The committed results JSON must match a fresh run (same inputs, same
    estimators) so results/ can't silently drift from the code."""
    results_path = Path(__file__).resolve().parents[2] / "results" / "trace_biq_calibration.json"
    if not results_path.exists():
        pytest.skip("results not generated yet; run calibrate_trace_biq.py")
    committed = json.loads(results_path.read_text(encoding="utf-8"))
    # round-trip: JSON turns tuples into lists
    fresh = json.loads(json.dumps(run_calibration(cols)))
    assert committed["lean_crosscheck"] == fresh["lean_crosscheck"]
    assert committed["findings"] == fresh["findings"]
    assert committed["tables"] == fresh["tables"]
