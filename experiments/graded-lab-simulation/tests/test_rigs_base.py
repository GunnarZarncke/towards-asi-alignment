"""PLAN_v4 rig contract dataclasses."""

from __future__ import annotations

import pytest

from graded_lab.harness.rigs.base import PreconditionReport, RigResult


def _precondition(satisfied: bool) -> PreconditionReport:
    return PreconditionReport(
        rig_id="R-TEST", satisfied=satisfied, measured={"x": 1}, threshold={"x_min": 1}
    )


def test_precondition_report_to_dict_roundtrips_fields():
    report = _precondition(True)
    d = report.to_dict()
    assert d["rig_id"] == "R-TEST"
    assert d["satisfied"] is True
    assert d["measured"] == {"x": 1}


def test_rig_result_rejects_unknown_outcome():
    with pytest.raises(ValueError):
        RigResult(
            rig_id="R-TEST",
            precondition=_precondition(True),
            outcome="maybe",
            substrate_class="S-inherited",
        )


def test_rig_result_rejects_unknown_substrate_class():
    with pytest.raises(ValueError):
        RigResult(
            rig_id="R-TEST",
            precondition=_precondition(True),
            outcome="pass",
            substrate_class="S-mystery",
        )


def test_rig_result_skip_to_dict():
    result = RigResult(
        rig_id="R-TEST",
        precondition=_precondition(False),
        outcome="skip",
        substrate_class="S-inherited",
    )
    d = result.to_dict()
    assert d["outcome"] == "skip"
    assert d["precondition"]["satisfied"] is False
    assert d["payload"] == {}
    assert d["predictions"] == {}
