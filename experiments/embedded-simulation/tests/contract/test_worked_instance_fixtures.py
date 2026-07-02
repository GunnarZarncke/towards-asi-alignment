"""Pins for the two fixtures `formal/AlignmentProofSpine/WorkedInstance.lean` transcribes.

The Lean worked instance hardcodes 26-row windows of two committed fixtures:
the capture-theater trace (pinned at git 408444b via
`trace_biq_calibration_columns.json`) and the honest companion
`sample_honest_baseline.jsonl` (same generator, seed, and pinned commit:
`synthesize_rows(300, "honest_baseline", seed=5)` from
`git show 408444b:.../structural_fixtures.py`). These tests fail loudly if
either fixture drifts from what the Lean transcription encodes, and verify the
honest fixture's provenance by regenerating it from the pinned generator.
"""

import json
import subprocess
from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
HONEST_FIXTURE = FIXTURES / "sample_honest_baseline.jsonl"
CAPTURE_COLUMNS = FIXTURES / "trace_biq_calibration_columns.json"

PINNED_COMMIT = "408444b"
GENERATOR_PATH = "experiments/embedded-simulation/embedded_sim/structural_fixtures.py"

LEAN_COLUMNS = ["visible_action", "intervention_active", "judge_captured", "correction_request"]
WINDOW = 26

# The literal matrices hardcoded in WorkedInstance.lean (rows × [active,
# external, internal, sensory]).
LEAN_CAPTURE_WINDOW = (
    [[0, 1, 1, 1]]
    + [[0, 0, 1, 0]] * 21
    + [[0, 1, 1, 1]]
    + [[0, 0, 1, 0]] * 2
    + [[1, 0, 1, 0]]
)
LEAN_HONEST_WINDOW = [[0, 1, 0, 1]] + [[0, 0, 0, 0]] * 25


def load_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


@pytest.fixture(scope="module")
def honest_rows():
    return load_rows(HONEST_FIXTURE)


def test_honest_fixture_shape(honest_rows):
    assert len(honest_rows) == 300
    assert all(r["judge_captured"] == 0 for r in honest_rows)
    assert all(r["visible_action"] == 0 for r in honest_rows)
    assert [r["intervention_active"] for r in honest_rows] == [
        1 if t % 40 == 0 else 0 for t in range(300)
    ]
    assert [r["correction_request"] for r in honest_rows] == [
        1 if t % 35 == 0 else 0 for t in range(300)
    ]


def test_honest_fixture_matches_pinned_generator(honest_rows):
    """Regenerate from the pinned-commit generator and compare byte-for-byte."""
    try:
        source = subprocess.run(
            ["git", "show", f"{PINNED_COMMIT}:{GENERATOR_PATH}"],
            capture_output=True,
            text=True,
            check=True,
            cwd=FIXTURES,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        pytest.skip("git or pinned commit unavailable")
    namespace: dict = {}
    exec(compile(source, "pinned_structural_fixtures.py", "exec"), namespace)
    regenerated = namespace["synthesize_rows"](300, "honest_baseline", seed=5)
    assert regenerated == honest_rows


def test_lean_honest_window_transcription(honest_rows):
    actual = [[int(r[f]) for f in LEAN_COLUMNS] for r in honest_rows[:WINDOW]]
    assert actual == LEAN_HONEST_WINDOW


def test_lean_capture_window_transcription():
    if not CAPTURE_COLUMNS.exists():
        pytest.skip("capture columns fixture missing")
    cols = json.loads(CAPTURE_COLUMNS.read_text(encoding="utf-8"))["columns"]
    actual = [[cols[f][i] for f in LEAN_COLUMNS] for i in range(WINDOW)]
    assert actual == LEAN_CAPTURE_WINDOW


def test_manipulation_counts_discriminate(honest_rows):
    """The single coordinate that flips the Lean certificate verdict."""
    honest_count = sum(r["judge_captured"] for r in honest_rows[:WINDOW])
    assert honest_count == 0  # honestCert passes (0 <= maxManipulation = 1)
    if CAPTURE_COLUMNS.exists():
        cols = json.loads(CAPTURE_COLUMNS.read_text(encoding="utf-8"))["columns"]
        capture_count = sum(cols["judge_captured"][:WINDOW])
        assert capture_count == 26  # workedCert fails (26 > 1)
