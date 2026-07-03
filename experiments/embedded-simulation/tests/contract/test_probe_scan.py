"""Contract test for the pre-registered probe_scan.py lag/direction grid.

Pins the acceptance criteria from `probe_scan.py`'s module docstring: the
scan must rediscover the known lag-3 coupling (N-8) on both
`capture_theater` datasets and must not raise false positives on either
`honest_baseline` dataset, aside from the real, expected lag-0 control-loop
response (which appears at *both* `forward` and `reverse` labels at lag 0
purely because mutual information is symmetric -- I(X;Y) = I(Y;X) -- not
because there are two independent findings).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from probe_scan import (
    NULL_PERCENTILE,
    load_pinned_capture_theater,
    load_pinned_honest_baseline,
)
from embedded_sim.dense_probe_profiles import DEFAULT_LAG

RESULTS_JSON = Path(__file__).resolve().parents[2] / "results" / "probe_scan.json"

ALLOWED_HONEST_CELLS = {("control", "forward", 0), ("control", "reverse", 0)}


def _significant_keys(dataset: dict) -> set[tuple[str, str, int]]:
    return {(c["pair"], c["direction"], c["lag"]) for c in dataset["significant_cells"]}


@pytest.fixture(scope="module")
def result():
    if not RESULTS_JSON.exists():
        pytest.skip("results not generated yet; run probe_scan.py")
    return json.loads(RESULTS_JSON.read_text(encoding="utf-8"))


def test_null_percentile_is_bonferroni_corrected(result):
    assert result["protocol"]["null_percentile"] == pytest.approx(NULL_PERCENTILE)
    assert NULL_PERCENTILE > 0.99  # stricter than the single-cell 0.95 default


def test_pinned_capture_theater_rediscovers_exactly_the_known_coupling(result):
    keys = _significant_keys(result["datasets"]["capture_theater_pinned"])
    assert keys == {("control", "reverse", DEFAULT_LAG)}


def test_dense_capture_theater_rediscovers_the_known_coupling(result):
    keys = _significant_keys(result["datasets"]["capture_theater_dense"])
    assert ("control", "reverse", DEFAULT_LAG) in keys


def test_pinned_honest_baseline_raises_no_false_positives(result):
    keys = _significant_keys(result["datasets"]["honest_baseline_pinned"])
    assert keys <= ALLOWED_HONEST_CELLS


def test_dense_honest_baseline_raises_no_false_positives(result):
    keys = _significant_keys(result["datasets"]["honest_baseline_dense"])
    assert keys <= ALLOWED_HONEST_CELLS


def test_predictive_pair_never_significant_on_either_capture_theater_dataset(result):
    """`judge_captured` is degenerate (constant) in the pinned fixture and
    unrelated to `correction_request` in the dense one; the predictive pair
    should never fire -- a sanity check that the grid isn't just flagging
    everything under a loose correction."""
    for name in ("capture_theater_pinned", "capture_theater_dense"):
        keys = _significant_keys(result["datasets"][name])
        assert all(pair != "predictive" for pair, _direction, _lag in keys)


def test_loaders_agree_on_shape():
    ct = load_pinned_capture_theater()
    hb = load_pinned_honest_baseline()
    assert set(ct) == set(hb) == {
        "visible_action",
        "intervention_active",
        "judge_captured",
        "correction_request",
    }
    assert len(ct["visible_action"]) == len(hb["visible_action"]) == 300
