"""V2-2b non-scoring pilot harness.

Blinding scope corrected per external review (2026-07-15): the pilot is
documented as reference-roster-identical and openly reports
contention/deploy signal; these tests check the *remaining* boundary
(oracle/referee-plane fields), not a fake distinction from `WEAK_AGENT`.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from graded_lab.harness.ecology_pilot import (
    audit_pilot_payload,
    pilot_report_dict,
    run_pilot_episodes,
)


def test_pilot_report_has_no_oracle_or_referee_plane_leaks():
    candidate = Path("generated_ecology_v2_round3.json")
    if not candidate.exists():
        pytest.skip("round-3 candidate not present")
    observations = run_pilot_episodes(candidate, seeds=(0,), progress=False)
    payload = pilot_report_dict(observations)
    audit_pilot_payload(payload)
    assert "eai" not in str(payload).lower()
    assert "bearer_harm" not in str(payload)


def test_audit_pilot_payload_rejects_oracle_plane_leak():
    with pytest.raises(ValueError, match="bearer_harm"):
        audit_pilot_payload({"bearer_harm": 0.1})


def test_pilot_report_openly_discloses_contention_and_deploy_signal():
    """Contention/deploy fields are intentionally NOT hidden — see
    `ecology_pilot.py` module docstring. This pins that the disclosure
    is deliberate, not an accidental leak, so a future change cannot
    silently re-introduce the fake-blind framing without failing here."""
    candidate = Path("generated_ecology_v2_round3.json")
    if not candidate.exists():
        pytest.skip("round-3 candidate not present")
    observations = run_pilot_episodes(candidate, seeds=(0,), progress=False)
    payload = pilot_report_dict(observations)
    assert "pilot_agent_note" in payload
    assert "any_compute_queue_pressure" in payload["episodes"][0]
    assert "deployment_count" in payload["episodes"][0]


def test_pilot_episode_fields_present():
    candidate = Path("generated_ecology_v2_round3.json")
    if not candidate.exists():
        pytest.skip("round-3 candidate not present")
    obs = run_pilot_episodes(candidate, seeds=(0,), progress=False)[0]
    assert obs.episode_ticks > 0
    assert obs.actor_count == 4
    assert isinstance(obs.deployment_occurred, bool)
    assert isinstance(obs.any_compute_queue_pressure, bool)


def test_pilot_does_not_stage_into_canonical_v2_path(tmp_path):
    """Statefulness fix (external review): running a pilot must not
    mutate the shared canonical `generated_ecology_v2.json`."""
    from graded_lab.world_visible.substrate import V2_ECOLOGY_PATH

    candidate = Path("generated_ecology_v2_round3.json")
    if not candidate.exists():
        pytest.skip("round-3 candidate not present")
    before = V2_ECOLOGY_PATH.read_bytes() if V2_ECOLOGY_PATH.exists() else None
    run_pilot_episodes(candidate, seeds=(0,), progress=False)
    after = V2_ECOLOGY_PATH.read_bytes() if V2_ECOLOGY_PATH.exists() else None
    assert before == after
