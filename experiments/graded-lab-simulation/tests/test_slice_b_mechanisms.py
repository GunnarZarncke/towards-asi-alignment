"""PLAN_v3 slice B: mechanism ACL compilation + runtime enforcement.

Engineering-only wiring tests (same posture as slice A): these prove the
compiler and dispatch layer are correctly connected on the slice A
reference fixture (which already declares all four mechanism kinds).
They do not exercise a full agent-driven reference battery — that is
deferred to slice D, per PLAN_v3's claim-scope discipline.
"""

from __future__ import annotations

from pathlib import Path

from graded_lab.oracle_only.oracle import OracleWorld
from graded_lab.world_visible.institutional_compiler import compile_ecology
from graded_lab.world_visible.pipeline_engine import PipelineEngine
from graded_lab.world_visible.pipeline_spec import PipelineStep, load_spec
from graded_lab.world_visible.primitives import PrimitiveAction
from graded_lab.world_visible.substrate import load_substrate
from graded_lab.world_visible.votes import (
    RESOLUTION_APPROVED,
    RESOLUTION_DENIED_TIMEOUT,
    RESOLUTION_PENDING,
    RESOLUTION_UNKNOWN,
    VoteService,
)
from graded_lab.world_visible.workspace import Workspace
from graded_lab.world_visible.world import _execute_primitive, default_lab_config

_FIXTURE = Path("tests/fixtures/ecology_v3_slice_a_reference.json")


def _runtime():
    data = load_substrate(_FIXTURE).data
    return compile_ecology(data, default_lab_config().agents)


# --- compiler ---------------------------------------------------------


def test_channel_acls_compiled_by_role():
    runtime = _runtime()
    assert runtime.channel_acls["eng_review_channel"] == frozenset({"engineer", "reviewer"})
    assert runtime.channel_acls["field_incident_alerts"] == frozenset(
        {"release_manager", "engineer", "reviewer", "admin"}
    )


def test_artifact_acls_compiled_by_role():
    runtime = _runtime()
    assert runtime.artifact_acls["eval_report_artifact"] == frozenset({"engineer", "reviewer"})


def test_transfer_acls_compiled_by_role():
    runtime = _runtime()
    assert runtime.transfer_acls["governed_capability_grant"] == frozenset(
        {"admin", "engineer"}
    )


def test_vote_specs_use_majority_quorum_and_default_timeout():
    runtime = _runtime()
    two_member = runtime.vote_specs["release_signoff_vote"]
    assert two_member.members == frozenset({"reviewer", "release_manager"})
    assert two_member.quorum == 2  # majority of 2 == both, frozen slice B design gate
    three_member = runtime.vote_specs["data_access_governance_board"]
    assert three_member.members == frozenset({"admin", "reviewer", "release_manager"})
    assert three_member.quorum == 2  # majority of 3
    assert three_member.timeout_ticks == 10  # DEFAULT_VOTE_TIMEOUT_TICKS


# --- ACL enforcement at dispatch (_execute_primitive) ------------------


def _projector(ws: Workspace):
    from graded_lab.world_visible.observation import ObservationProjector

    return ObservationProjector(workspace=ws)


def test_communicate_denied_for_non_channel_member():
    runtime = _runtime()
    ws = Workspace()
    try:
        outcome = _execute_primitive(
            PrimitiveAction("communicate", {"channel": "eng_review_channel", "message": {}}),
            "admin1",
            engine=None,
            permissions=None,
            projector=_projector(ws),
            workspace=ws,
            role_by_actor={"admin1": "admin"},
            channel_acls=runtime.channel_acls,
        )
    finally:
        ws.cleanup()
    assert outcome == {"status": "denied", "reason": "not_channel_member"}


def test_communicate_allowed_for_channel_member():
    runtime = _runtime()
    ws = Workspace()
    try:
        outcome = _execute_primitive(
            PrimitiveAction("communicate", {"channel": "eng_review_channel", "message": {}}),
            "eng1",
            engine=None,
            permissions=None,
            projector=_projector(ws),
            workspace=ws,
            role_by_actor={"eng1": "engineer"},
            channel_acls=runtime.channel_acls,
        )
    finally:
        ws.cleanup()
    assert outcome["status"] == "ok"


def test_communicate_on_unbound_channel_is_unrestricted():
    """Backward compatibility: a channel name that is not a compiled
    mechanism id (e.g. the v1/v2 default ``lab``) is never enforced."""
    runtime = _runtime()
    ws = Workspace()
    try:
        outcome = _execute_primitive(
            PrimitiveAction("communicate", {"channel": "lab", "message": {}}),
            "admin1",
            engine=None,
            permissions=None,
            projector=_projector(ws),
            workspace=ws,
            role_by_actor={"admin1": "admin"},
            channel_acls=runtime.channel_acls,
        )
    finally:
        ws.cleanup()
    assert outcome["status"] == "ok"


def test_write_denied_for_non_artifact_member():
    runtime = _runtime()
    ws = Workspace()
    try:
        outcome = _execute_primitive(
            PrimitiveAction(
                "write", {"artifact_id": "eval_report_artifact", "path": "x", "content": {}}
            ),
            "admin1",
            engine=None,
            permissions=None,
            projector=_projector(ws),
            workspace=ws,
            role_by_actor={"admin1": "admin"},
            artifact_acls=runtime.artifact_acls,
        )
    finally:
        ws.cleanup()
    assert outcome == {"status": "denied", "reason": "not_artifact_member"}


def test_write_allowed_for_artifact_member():
    runtime = _runtime()
    ws = Workspace()
    try:
        outcome = _execute_primitive(
            PrimitiveAction(
                "write", {"artifact_id": "eval_report_artifact", "path": "x", "content": {}}
            ),
            "eng1",
            engine=None,
            permissions=None,
            projector=_projector(ws),
            workspace=ws,
            role_by_actor={"eng1": "engineer"},
            artifact_acls=runtime.artifact_acls,
        )
    finally:
        ws.cleanup()
    assert outcome["status"] == "ok"


def test_transfer_execute_denied_for_non_member():
    runtime = _runtime()
    ws = Workspace()
    try:
        outcome = _execute_primitive(
            PrimitiveAction(
                "call",
                {
                    "endpoint": "transfer.execute",
                    "args": {
                        "mechanism_id": "governed_capability_grant",
                        "target_actor_id": "rev1",
                    },
                },
            ),
            "admin1",
            engine=None,
            permissions=None,
            projector=_projector(ws),
            workspace=ws,
            role_by_actor={"admin1": "admin", "rev1": "reviewer"},
            transfer_acls=runtime.transfer_acls,
        )
    finally:
        ws.cleanup()
    assert outcome == {"status": "denied", "reason": "not_transfer_member"}


def test_transfer_execute_allowed_between_members():
    runtime = _runtime()
    ws = Workspace()
    try:
        outcome = _execute_primitive(
            PrimitiveAction(
                "call",
                {
                    "endpoint": "transfer.execute",
                    "args": {
                        "mechanism_id": "governed_capability_grant",
                        "target_actor_id": "eng1",
                    },
                },
            ),
            "admin1",
            engine=None,
            permissions=None,
            projector=_projector(ws),
            workspace=ws,
            role_by_actor={"admin1": "admin", "eng1": "engineer"},
            transfer_acls=runtime.transfer_acls,
        )
    finally:
        ws.cleanup()
    assert outcome["status"] == "ok"
    assert outcome["payload"]["mechanism_id"] == "governed_capability_grant"


# --- VoteService --------------------------------------------------------


def test_vote_cast_denied_for_non_member():
    runtime = _runtime()
    service = VoteService(runtime.vote_specs)
    outcome = service.cast("release_signoff_vote", "eng1", "engineer", True, t=0)
    assert outcome == {"status": "denied", "reason": "not_vote_member"}


def test_vote_resolution_pending_then_approved_on_quorum():
    runtime = _runtime()
    service = VoteService(runtime.vote_specs)
    assert service.resolution("release_signoff_vote", t=0) == RESOLUTION_PENDING
    service.cast("release_signoff_vote", "rev1", "reviewer", True, t=0)
    assert service.resolution("release_signoff_vote", t=1) == RESOLUTION_PENDING  # 1/2, not quorum
    service.cast("release_signoff_vote", "rm1", "release_manager", True, t=1)
    assert service.resolution("release_signoff_vote", t=2) == RESOLUTION_APPROVED


def test_vote_resolution_times_out_without_quorum():
    runtime = _runtime()
    service = VoteService(runtime.vote_specs)
    service.cast("release_signoff_vote", "rev1", "reviewer", True, t=0)  # opens clock at t=0
    assert service.resolution("release_signoff_vote", t=5) == RESOLUTION_PENDING
    assert service.resolution("release_signoff_vote", t=10) == RESOLUTION_DENIED_TIMEOUT


def test_vote_resolution_unknown_mechanism():
    service = VoteService({})
    assert service.resolution("not_a_real_vote", t=0) == RESOLUTION_UNKNOWN


# --- PipelineEngine requires_vote gating --------------------------------


def _engine_with_vote_gate(vote_service: VoteService) -> PipelineEngine:
    substrate = load_substrate()
    oracle = OracleWorld(seed=42, substrate_data=substrate.data)
    ws = Workspace()
    spec = load_spec("pipeline_graded.json")
    gated = PipelineStep(
        id="intake", tool="intake", requires_vote="release_signoff_vote"
    )
    spec = spec.__class__(spec_version=spec.spec_version, steps=(gated,) + spec.steps[1:])
    return PipelineEngine(spec, oracle, ws, vote_service=vote_service)


def test_pipeline_step_blocked_while_vote_pending():
    runtime = _runtime()
    service = VoteService(runtime.vote_specs)
    engine = _engine_with_vote_gate(service)
    try:
        result = engine.trigger_step("eng1", "intake", {})
        assert not result.ok
        assert result.reason == "vote_pending"
    finally:
        engine.workspace.cleanup()


def test_pipeline_step_proceeds_once_vote_approved():
    runtime = _runtime()
    service = VoteService(runtime.vote_specs)
    service.cast("release_signoff_vote", "rev1", "reviewer", True, t=0)
    service.cast("release_signoff_vote", "rm1", "release_manager", True, t=0)
    engine = _engine_with_vote_gate(service)
    try:
        result = engine.trigger_step("eng1", "intake", {})
        assert result.ok
    finally:
        engine.workspace.cleanup()


def test_pipeline_step_fails_on_vote_timeout_no_escalation():
    runtime = _runtime()
    service = VoteService(runtime.vote_specs)
    engine = _engine_with_vote_gate(service)
    try:
        engine.trigger_step("eng1", "intake", {})  # opens the vote clock at t=0
        for _ in range(10):
            engine.oracle.tick()
        result = engine.trigger_step("eng1", "intake", {})
        assert not result.ok
        assert result.reason == "vote_denied_timeout"
    finally:
        engine.workspace.cleanup()
