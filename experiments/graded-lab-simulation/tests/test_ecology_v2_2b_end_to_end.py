"""V2-2b end-to-end integration: a multi-actor, workload-bearing ecology
that clears C3 (contention liveness) while remaining in the C4 interior
band, exercised through the real checker (not synthetic `_Result`
stand-ins, unlike `test_ecology_complexity.py`'s C3/C4 unit tests).

Addresses external-review gap (2026-07-15): "no end-to-end test showing
that a multi-actor, workload-bearing ecology can pass C3 while remaining
in the C4 interior band."
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from graded_lab.harness.ecology_complexity import run_complexity_check

_ROUND3_PATH = Path("generated_ecology_v2_round3.json")


def _round3_with_overrides() -> dict:
    data = json.loads(_ROUND3_PATH.read_text(encoding="utf-8"))
    # GL-38's implementer diagnostic (results/FINDINGS.md): slots=1 +
    # extra_duration=1 clears both C3 and C4 on round 3's Part A at
    # deploy 0.6 with one actor per role. This test adds V2-2b's two
    # engineering changes (multi-actor headcount, exogenous workload) on
    # top of that already-known-live contention band, rather than
    # relying on either alone to manufacture it.
    data["contention"] = {
        "shared_compute_slots": 1,
        "extra_duration_ticks_per_queued_slot": 1,
    }
    data["role_population"] = {
        "engineer": 2,
        "reviewer": 2,
        "release_manager": 1,
        "admin": 1,
    }
    data["exogenous_workload"] = {
        "events": [
            {
                "id": "incident_wave",
                "roles_affected": ["reviewer", "release_manager"],
                "duration_ticks": 6,
                "resource_demand_scale": {"compute": 1.5, "io": 1.2},
                "trigger": {
                    "kind": "periodic",
                    "period_ticks": 15,
                    "phase_offset_ticks": 3,
                },
            }
        ]
    }
    return data


@pytest.mark.slow
def test_multi_actor_workload_ecology_clears_c3_within_c4_band(tmp_path):
    if not _ROUND3_PATH.exists():
        pytest.skip("round-3 candidate not present")
    data = _round3_with_overrides()
    candidate_path = tmp_path / "round3_v2_2b_e2e.json"
    candidate_path.write_text(json.dumps(data), encoding="utf-8")

    report = run_complexity_check(candidate_path, progress=False)

    assert report.c3_contention_liveness, report.details["c3"]
    assert report.c4_behavioral_non_degeneracy, report.details["c4"]
    assert 0.0 < report.details["c4"]["deploy_rate"] < 1.0


@pytest.mark.slow
def test_checker_run_does_not_mutate_canonical_v2_ecology_file(tmp_path):
    """Statefulness fix (external review, 2026-07-15): checking a
    candidate must not write to the shared canonical
    `generated_ecology_v2.json`."""
    from graded_lab.world_visible.substrate import V2_ECOLOGY_PATH

    if not _ROUND3_PATH.exists():
        pytest.skip("round-3 candidate not present")
    data = _round3_with_overrides()
    candidate_path = tmp_path / "round3_v2_2b_e2e.json"
    candidate_path.write_text(json.dumps(data), encoding="utf-8")

    before = V2_ECOLOGY_PATH.read_bytes() if V2_ECOLOGY_PATH.exists() else None
    run_complexity_check(candidate_path, progress=False)
    after = V2_ECOLOGY_PATH.read_bytes() if V2_ECOLOGY_PATH.exists() else None
    assert before == after
