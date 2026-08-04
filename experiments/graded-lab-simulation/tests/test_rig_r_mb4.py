"""PLAN_v4 R-MB4 — referee/detector transfer + injection gate."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from graded_lab.harness.fixtures import build_reference_fixture
from graded_lab.harness.rigs import r_mb4_detector_transfer as rig

_GROWN = Path("generated_ecology_v3.json")


@dataclass
class _FakeResult:
    primitive_log: list[dict] = field(default_factory=list)
    pressure_diagnostics: dict | None = None


def test_phenomena_counts_detects_acl_denial_vote_and_pressure():
    result = _FakeResult(
        primitive_log=[
            {"status": "denied", "reason": "not_channel_member"},
            {"status": "denied", "reason": "not_affordable"},  # not an ACL denial
            {
                "status": "ok",
                "primitive": {"kind": "call", "args": {"endpoint": "vote.cast"}},
            },
        ],
        pressure_diagnostics={"injection_log": [{"t": 3}, {"t": 7}]},
    )
    counts = rig.phenomena_counts(result)
    assert counts == {"acl_denials": 1, "votes": 1, "pressure_injected_tasks": 2}


def test_phenomena_counts_handles_missing_pressure_diagnostics():
    result = _FakeResult(primitive_log=[])
    counts = rig.phenomena_counts(result)
    assert counts == {"acl_denials": 0, "votes": 0, "pressure_injected_tasks": 0}


@pytest.mark.slow
@pytest.mark.skipif(not _GROWN.exists(), reason="v3 grown ecology missing")
def test_r_mb4_skips_on_v3_grown_honest_reference(monkeypatch):
    # Honest WEAK_AGENT reference traffic on v3_grown never triggers an ACL
    # denial (GL-76-adjacent finding): only 2 of the 3 phenomenon kinds are
    # exercised, so the rig must SKIP rather than report vacuous coverage.
    fixture = build_reference_fixture(_GROWN, seeds=tuple(range(4)), progress=False)
    result = rig.run_rig(fixture, progress=False)
    assert result.precondition.satisfied is False
    assert result.outcome == "skip"
    assert result.precondition.measured["totals_across_seeds"]["acl_denials"] == 0
