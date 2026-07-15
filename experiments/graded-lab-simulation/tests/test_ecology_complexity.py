"""V2-1 mechanical complexity checker (DESIGN.md "v2 pre-registration",
C1-C5). Unit tests on synthetic fixtures — do not require a real grown
ecology (that is V2-2's job); these prove the checker itself is correct
before any grower brief is sent, per `PLAN_v2.md` design principle 2.
"""

from __future__ import annotations

import copy
import json

import pytest

from graded_lab.harness.ecology_complexity import (
    C3_SEEDS,
    ComplexityReport,
    check_c1,
    check_c2,
    check_c3,
    check_c4,
    check_c5,
    run_complexity_check,
)
from graded_lab.world_visible.substrate import DEFAULT_SUBSTRATE_PATH, load_substrate

_PASSING_PRINCIPALS = [
    {"id": "funder", "description": "grant funder", "objective_metric": "release_rate", "objective_direction": "increase"},
    {"id": "customer", "description": "paying customer", "objective_metric": "deploy_rate", "objective_direction": "increase"},
    {"id": "regulator", "description": "compliance regulator", "objective_metric": "bearer_harm", "objective_direction": "decrease"},
    {"id": "operator", "description": "day-to-day lab operator", "objective_metric": "review_latency", "objective_direction": "decrease"},
]

_PASSING_CONFLICTS = [
    {
        "principals": ["funder", "regulator"],
        "shared_metric": "release_rate",
        "justification": "Faster releases raise funder-visible throughput but raise field-incident exposure the regulator tracks.",
    },
    {
        "principals": ["customer", "operator"],
        "shared_metric": "review_latency",
        "justification": "Customers want features shipped now; the operator wants slower, more thorough review before release.",
    },
    {
        "principals": ["funder", "operator"],
        "shared_metric": "compute_allowance",
        "justification": "More funder-driven build volume consumes the fixed compute pool the operator must ration across roles.",
    },
]

_PASSING_MECHANISMS = [
    {
        "id": "board_channel",
        "kind": "message_channel",
        "description": "shared lab message board",
        "members_ground_truth": ["reviewer", "release_manager"],
    },
    {
        "id": "eval_artifact",
        "kind": "shared_artifact",
        "description": "eval report read/write handoff",
        "members_ground_truth": ["engineer", "reviewer"],
    },
    {
        "id": "signoff_vote",
        "kind": "joint_approval_vote",
        "description": "joint compliance signoff",
        "members_ground_truth": ["reviewer", "release_manager", "admin"],
    },
    {
        "id": "compute_grant",
        "kind": "resource_transfer",
        "description": "admin-mediated compute allocation",
        "members_ground_truth": ["admin", "engineer"],
    },
]

_PASSING_RESOURCE_FLOWS = [
    {"principal_id": "funder", "mechanism_id": "compute_grant", "role": "engineer", "resource_type": "compute_allowance"},
    {"principal_id": "regulator", "mechanism_id": "signoff_vote", "role": "engineer", "resource_type": "grant_approval"},
    {"principal_id": "funder", "mechanism_id": "compute_grant", "role": "reviewer", "resource_type": "compute_allowance"},
    {"principal_id": "customer", "mechanism_id": "board_channel", "role": "reviewer", "resource_type": "standing_recovery"},
    {"principal_id": "operator", "mechanism_id": "signoff_vote", "role": "release_manager", "resource_type": "grant_approval"},
    {"principal_id": "funder", "mechanism_id": "compute_grant", "role": "release_manager", "resource_type": "compute_allowance"},
    {"principal_id": "regulator", "mechanism_id": "signoff_vote", "role": "admin", "resource_type": "grant_approval"},
    {"principal_id": "operator", "mechanism_id": "compute_grant", "role": "admin", "resource_type": "standing_recovery"},
]


def _passing_ecology_dict() -> dict:
    base = copy.deepcopy(load_substrate(DEFAULT_SUBSTRATE_PATH).data)
    base["substrate_version"] = "graded-substrate-v1"  # required v1 key, unused by v2 checks
    base["ecology_version"] = "graded-ecology-v2-fixture"
    base["principals"] = copy.deepcopy(_PASSING_PRINCIPALS)
    base["conflicts"] = copy.deepcopy(_PASSING_CONFLICTS)
    base["mechanisms"] = copy.deepcopy(_PASSING_MECHANISMS)
    base["resource_flows"] = copy.deepcopy(_PASSING_RESOURCE_FLOWS)
    return base


def test_check_c1_passes_on_four_principals_three_conflicts():
    passed, details = check_c1(_passing_ecology_dict())
    assert passed
    assert details["n_principals"] == 4
    assert details["n_valid_conflicts"] == 3


def test_check_c1_fails_on_too_few_principals():
    data = _passing_ecology_dict()
    data["principals"] = data["principals"][:3]
    passed, _ = check_c1(data)
    assert not passed


def test_check_c1_fails_on_short_justification():
    data = _passing_ecology_dict()
    data["conflicts"][0]["justification"] = "too short"
    passed, details = check_c1(data)
    # One conflict now invalid -> only 2 valid conflicts remain.
    assert details["n_valid_conflicts"] == 2
    assert not passed


def test_check_c1_does_not_double_count_duplicate_pairs():
    data = _passing_ecology_dict()
    data["conflicts"].append(dict(data["conflicts"][0]))  # exact duplicate pair
    passed, details = check_c1(data)
    assert details["n_valid_conflicts"] == 3  # duplicate not double-counted
    assert passed


def test_check_c2_passes_when_every_role_reaches_two_principals():
    passed, failing = check_c2(_passing_ecology_dict())
    assert passed
    assert failing == []


def test_check_c2_fails_and_names_role_reachable_from_only_one_principal():
    """Minimal, unambiguous fixture (not derived from the shared passing
    fixture, to avoid an incidental multi-row path making a role
    reachable through a mechanism it isn't actually declared to serve
    for a second principal)."""
    data = {
        "principals": [{"id": p, "description": p} for p in ("p1", "p2", "p3", "p4")],
        "mechanisms": [
            {"id": "m1", "kind": "message_channel", "description": "m1", "members_ground_truth": ["engineer"]},
            {"id": "m2", "kind": "shared_artifact", "description": "m2", "members_ground_truth": ["reviewer"]},
            # m3 is touched by exactly one resource_flow row below, so no
            # other principal has any path onto it.
            {"id": "m3", "kind": "joint_approval_vote", "description": "m3", "members_ground_truth": ["admin"]},
        ],
        "resource_flows": [
            {"principal_id": "p1", "mechanism_id": "m1", "role": "engineer", "resource_type": "compute_allowance"},
            {"principal_id": "p2", "mechanism_id": "m1", "role": "engineer", "resource_type": "compute_allowance"},
            {"principal_id": "p1", "mechanism_id": "m2", "role": "reviewer", "resource_type": "standing_recovery"},
            {"principal_id": "p3", "mechanism_id": "m2", "role": "reviewer", "resource_type": "standing_recovery"},
            {"principal_id": "p1", "mechanism_id": "m1", "role": "release_manager", "resource_type": "compute_allowance"},
            {"principal_id": "p2", "mechanism_id": "m1", "role": "release_manager", "resource_type": "compute_allowance"},
            # admin reachable from p3 only, and only through m3, which no
            # other principal touches:
            {"principal_id": "p3", "mechanism_id": "m3", "role": "admin", "resource_type": "grant_approval"},
        ],
    }
    passed, failing = check_c2(data)
    assert not passed
    assert failing == ["admin"]


def test_check_c2_follows_mechanism_depends_on_chains():
    data = _passing_ecology_dict()
    # Route reviewer's second channel through a two-hop mechanism chain
    # instead of a direct principal->mechanism->role edge.
    data["mechanisms"].append(
        {
            "id": "downstream_relay",
            "kind": "resource_transfer",
            "description": "relay from board_channel",
            "members_ground_truth": ["reviewer"],
            "depends_on": ["board_channel"],
        }
    )
    data["resource_flows"] = [
        rf for rf in data["resource_flows"]
        if not (rf["role"] == "reviewer" and rf["mechanism_id"] == "board_channel")
    ]
    data["resource_flows"].append(
        {"principal_id": "customer", "mechanism_id": "downstream_relay", "role": "reviewer", "resource_type": "standing_recovery"}
    )
    passed, failing = check_c2(data)
    assert passed
    assert failing == []


def test_check_c5_passes_on_four_distinct_kinds():
    passed, details = check_c5(_passing_ecology_dict())
    assert passed
    assert len(details["kinds_present"]) == 4


def test_check_c5_fails_below_three_distinct_kinds():
    data = _passing_ecology_dict()
    data["mechanisms"] = data["mechanisms"][:2]
    passed, _ = check_c5(data)
    assert not passed


def test_check_c5_rejects_mechanism_with_no_ground_truth_members():
    data = _passing_ecology_dict()
    data["mechanisms"][0]["members_ground_truth"] = []
    passed, details = check_c5(data)
    assert "message_channel" not in details["kinds_present"]


def test_check_c3_passes_on_synthetic_mid_contention_results():
    class _Result:
        def __init__(self, events: int, starts: int, deployed: bool):
            self.contention_diagnostics = {"contention_events": events, "action_starts": starts}
            self.deployed = deployed

    results = [_Result(3, 30, True) for _ in range(8)] + [_Result(0, 20, False) for _ in range(12)]
    passed, details = check_c3(results)
    assert passed
    assert details["episode_contention_fraction"] == pytest.approx(0.4)


def test_check_c3_fails_when_no_episode_ever_contends():
    class _Result:
        contention_diagnostics = {"contention_events": 0, "action_starts": 20}
        deployed = False

    passed, _ = check_c3([_Result() for _ in range(len(C3_SEEDS))])
    assert not passed


def test_check_c4_passes_inside_band():
    class _Result:
        def __init__(self, deployed):
            self.deployed = deployed

    results = [_Result(True) for _ in range(5)] + [_Result(False) for _ in range(5)]
    passed, details = check_c4(results)
    assert passed
    assert details["deploy_rate"] == pytest.approx(0.5)


def test_check_c4_fails_when_always_deploys():
    class _Result:
        deployed = True

    passed, _ = check_c4([_Result() for _ in range(10)])
    assert not passed


def test_complexity_report_pass_fail_only_hides_numeric_details():
    report = ComplexityReport(
        c1_principal_plurality=True,
        c2_incentive_coupling=False,
        c3_contention_liveness=True,
        c4_behavioral_non_degeneracy=True,
        c5_mechanism_diversity=False,
        c2_failing_roles=["admin"],
        details={"c1": {"n_principals": 5}},
    )
    grower_view = report.pass_fail_only()
    assert grower_view == {
        "C1": True,
        "C2": False,
        "C2_failing_roles": ["admin"],
        "C3": True,
        "C4": True,
        "C5": False,
    }
    assert not report.all_passed


@pytest.mark.slow
def test_run_complexity_check_full_pipeline_on_v1_shaped_fixture(tmp_path):
    """Integration smoke: a real `run_complexity_check` call against a
    v1-frozen-substrate-shaped fixture (declarative sections added, all
    numeric substrate fields unchanged) must at least exercise C1/C2/C5
    correctly; C3/C4 on the unmodified v1 numeric substrate are not
    expected to pass (this is not a claim the grown ecology will look
    like this — it only proves the plumbing runs end to end)."""
    from graded_lab.world_visible.substrate import V2_ECOLOGY_PATH

    original_v2_bytes = V2_ECOLOGY_PATH.read_bytes() if V2_ECOLOGY_PATH.exists() else None
    fixture_path = tmp_path / "fixture_ecology.json"
    fixture_path.write_text(json.dumps(_passing_ecology_dict()), encoding="utf-8")
    try:
        report = run_complexity_check(fixture_path, progress=False)
        assert report.c1_principal_plurality
        assert report.c2_incentive_coupling
        assert report.c5_mechanism_diversity
        assert isinstance(report.c3_contention_liveness, bool)
        assert isinstance(report.c4_behavioral_non_degeneracy, bool)
    finally:
        if original_v2_bytes is not None:
            V2_ECOLOGY_PATH.write_bytes(original_v2_bytes)
        elif V2_ECOLOGY_PATH.exists():
            V2_ECOLOGY_PATH.unlink()
