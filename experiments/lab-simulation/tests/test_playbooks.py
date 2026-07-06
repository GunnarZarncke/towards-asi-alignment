"""Phase 4: playbook availability gates + ontology report-content mapping."""

from __future__ import annotations

from lab_sim.ontology import INFLATE_HAZARD_DELTA, report_content
from lab_sim.playbooks import HONEST_PLAYBOOK_BY_ROLE, PLAYBOOKS_BY_ROLE, available_playbooks, playbook_by_name


def test_report_content_honest_passes_through_measured_values():
    content = report_content("honest", {"measured_capability": 0.7, "measured_hazard": 0.4})
    assert content == {"measured_capability": 0.7, "measured_hazard": 0.4}


def test_report_content_inflate_understates_hazard():
    content = report_content("inflate", {"measured_capability": 0.7, "measured_hazard": 0.4})
    assert content["measured_hazard"] == max(0.0, 0.4 - INFLATE_HAZARD_DELTA)
    assert content["measured_capability"] == 0.7


def test_report_content_inflate_floors_at_zero():
    content = report_content("inflate", {"measured_capability": 0.1, "measured_hazard": 0.05})
    assert content["measured_hazard"] == 0.0


def test_unknown_report_mode_raises():
    import pytest

    with pytest.raises(ValueError):
        report_content("bogus", {})


def test_engineer_idle_when_no_model_in_flight():
    obs = {"model_id": None, "completed_steps": []}
    available = available_playbooks("engineer", obs)
    assert {pb.name for pb in available} == {"eng_honest", "eng_inflate"}


def test_engineer_unavailable_once_review_requested():
    obs = {"model_id": "m001", "completed_steps": ["submit_build", "run_eval", "file_report", "request_review"]}
    assert available_playbooks("engineer", obs) == ()


def test_engineer_available_mid_model_for_boundary_handle_recovery():
    # After an isolate_restart wipes playbook state mid-model, the engineer
    # must be able to re-pick a playbook and resume (see playbooks.py).
    obs = {"model_id": "m001", "completed_steps": ["submit_build"]}
    assert len(available_playbooks("engineer", obs)) == 2


def test_reviewer_available_when_review_pending():
    obs = {"model_id": "m001", "completed_steps": ["submit_build", "run_eval", "file_report"]}
    available = available_playbooks("reviewer", obs)
    assert {pb.name for pb in available} == {"rev_conscientious", "rev_rubber_stamp"}


def test_reviewer_available_when_signoff_pending():
    obs = {"model_id": "m001", "completed_steps": ["approve_review", "request_release"]}
    available = available_playbooks("reviewer", obs)
    assert {pb.name for pb in available} == {"rev_conscientious", "rev_rubber_stamp"}


def test_reviewer_unavailable_when_nothing_pending():
    obs = {"model_id": "m001", "completed_steps": ["approve_review"]}
    assert available_playbooks("reviewer", obs) == ()


def test_release_manager_available_after_approval():
    obs = {"model_id": "m001", "completed_steps": ["approve_review"]}
    available = available_playbooks("release_manager", obs)
    assert {pb.name for pb in available} == {"rm_full"}


def test_release_manager_unavailable_when_no_model():
    assert available_playbooks("release_manager", {"model_id": None, "completed_steps": []}) == ()


def test_honest_playbook_by_role_all_resolve():
    for role, name in HONEST_PLAYBOOK_BY_ROLE.items():
        pb = playbook_by_name(role, name)
        assert pb.name == name


def test_playbook_by_name_unknown_raises():
    import pytest

    with pytest.raises(KeyError):
        playbook_by_name("engineer", "does_not_exist")


def test_all_playbooks_have_all_four_features_present():
    for playbooks in PLAYBOOKS_BY_ROLE.values():
        for pb in playbooks:
            assert set(pb.feature_deltas) <= {"task", "compliance", "welfare", "exposure"}
