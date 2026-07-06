"""Phase 4: playbook availability gates + ontology report-content mapping."""

from __future__ import annotations

from lab_sim.ontology import INFLATE_HAZARD_DELTA, report_content
from lab_sim.playbooks import (
    HONEST_PLAYBOOK_BY_ROLE,
    PLAYBOOKS_BY_ROLE,
    available_playbooks,
    merged_repertoire,
    playbook_by_name,
    validate_playbook_dict,
    validate_repertoire,
)


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


# -- Phase 6: blind-generated repertoire loading --------------------------

_VALID_EXTRA = {
    "name": "eng_generated_ok",
    "role": "engineer",
    "step_kinds": ["build", "eval", "report:honest", "review_request"],
    "feature_deltas": {"task": 0.5, "compliance": 0.5},
    "availability": "engineer_idle",
}


def test_validate_playbook_dict_accepts_well_formed_spec():
    assert validate_playbook_dict(_VALID_EXTRA, existing_names=set()) is None


def test_validate_playbook_dict_rejects_unknown_step_kind():
    bad = dict(_VALID_EXTRA, step_kinds=["build", "teleport_to_deploy"])
    reason = validate_playbook_dict(bad, existing_names=set())
    assert reason is not None and "unknown step_kinds" in reason


def test_validate_playbook_dict_rejects_unknown_availability():
    bad = dict(_VALID_EXTRA, availability="whenever_it_feels_like_it")
    reason = validate_playbook_dict(bad, existing_names=set())
    assert reason is not None and "unknown availability" in reason


def test_validate_playbook_dict_rejects_unknown_feature_key():
    bad = dict(_VALID_EXTRA, feature_deltas={"task": 1.0, "sneakiness": 2.0})
    reason = validate_playbook_dict(bad, existing_names=set())
    assert reason is not None and "unknown feature_deltas" in reason


def test_validate_playbook_dict_rejects_duplicate_name():
    reason = validate_playbook_dict(_VALID_EXTRA, existing_names={("engineer", "eng_generated_ok")})
    assert reason is not None and "duplicate name" in reason


def test_validate_repertoire_splits_accepted_and_rejected():
    raw = [_VALID_EXTRA, dict(_VALID_EXTRA, name="eng_bad", step_kinds=["nonsense"]), "not_a_dict"]
    accepted, rejected = validate_repertoire(raw)
    assert [pb.name for pb in accepted] == ["eng_generated_ok"]
    assert len(rejected) == 2


def test_merged_repertoire_empty_extra_returns_baseline_object_unchanged():
    # Identity, not just equality: undisturbed callers must get the exact
    # PLAYBOOKS_BY_ROLE object back, never a copy — this is what makes
    # `extra_playbooks=()` provably a no-op for every pre-Phase-6 caller.
    assert merged_repertoire(()) is PLAYBOOKS_BY_ROLE
    assert merged_repertoire(None) is PLAYBOOKS_BY_ROLE


def test_merged_repertoire_adds_generated_playbook_without_losing_baseline():
    merged = merged_repertoire((_VALID_EXTRA,))
    names = {pb.name for pb in merged["engineer"]}
    assert names == {"eng_honest", "eng_inflate", "eng_generated_ok"}


def test_merged_repertoire_drops_malformed_extras_silently():
    merged = merged_repertoire(({"name": "broken", "role": "engineer"},))
    names = {pb.name for pb in merged["engineer"]}
    assert names == {"eng_honest", "eng_inflate"}


def test_generated_playbooks_v1_file_is_fully_mechanically_valid():
    # BLIND_GENERATION.md round 1: the frozen generated repertoire must
    # validate with zero rejections (the file's own provenance.rejected_specs
    # is empty; this test re-derives that claim rather than trusting it).
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parent.parent / "lab_sim" / "generated_playbooks_v1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["provenance"]["protocol"] == "BLIND_GENERATION.md"
    assert data["provenance"]["prompt_verbatim"]  # captured, non-empty
    accepted, rejected = validate_repertoire(data["playbooks"])
    assert rejected == data["provenance"]["rejected_specs"]
    assert len(accepted) == len(data["playbooks"])
    merged = merged_repertoire(tuple(data["playbooks"]))
    for role in ("engineer", "reviewer", "release_manager"):
        assert len(merged[role]) > len(PLAYBOOKS_BY_ROLE[role])


def test_available_playbooks_honors_repertoire_override():
    obs = {"model_id": None, "completed_steps": []}
    merged = merged_repertoire((_VALID_EXTRA,))
    available = available_playbooks("engineer", obs, repertoire=merged)
    assert {pb.name for pb in available} == {"eng_honest", "eng_inflate", "eng_generated_ok"}
    # Default (no repertoire arg) is unaffected by the override existing.
    assert {pb.name for pb in available_playbooks("engineer", obs)} == {"eng_honest", "eng_inflate"}
