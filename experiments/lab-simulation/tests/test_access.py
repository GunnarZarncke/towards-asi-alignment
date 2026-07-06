"""Phase 2: PermissionService, AdminPolicy, and engine wiring."""

from __future__ import annotations

from lab_sim.access import PermissionService
from lab_sim.agents import AccessRequest, AdminPolicy, ROLE_CAPABILITIES
from lab_sim.config import AdminConfig
from lab_sim.oracle import OracleWorld
from lab_sim.pipeline_engine import PipelineEngine
from lab_sim.pipeline_spec import load_spec
from lab_sim.workspace import Workspace


def test_grant_revoke_check_semantics():
    svc = PermissionService()
    assert svc.check("eng1", "cap.build", t=0) is False
    svc.grant("eng1", "cap.build", granted_by="admin", t=1)
    assert svc.check("eng1", "cap.build", t=2) is True
    svc.revoke("eng1", "cap.build", revoked_by="admin", t=3)
    assert svc.check("eng1", "cap.build", t=4) is False


def test_access_log_hash_chain_verification():
    svc = PermissionService()
    svc.grant("eng1", "cap.build", granted_by="admin", t=0)
    svc.check("eng1", "cap.build", t=1)
    svc.revoke("eng1", "cap.build", revoked_by="admin", t=2)
    svc.deny("eng1", "cap.deploy", denied_by="admin", t=3)
    assert svc.verify_chain()
    # Tamper detection: mutate an entry in place, chain must fail.
    svc.log[1]["result"] = not svc.log[1]["result"]
    assert not svc.verify_chain()


def test_admin_least_privilege_grants_exactly_requested_capability():
    svc = PermissionService()
    admin = AdminPolicy(AdminConfig(least_privilege=True), svc)
    granted = admin.handle_request(AccessRequest("eng1", "engineer", "cap.build", t=0))
    assert granted
    assert svc.check("eng1", "cap.build", t=1)
    assert not svc.check("eng1", "cap.eval", t=1)  # not over-granted


def test_admin_lazy_grants_all_role_eligible_capabilities():
    svc = PermissionService()
    admin = AdminPolicy(AdminConfig(least_privilege=False), svc)
    admin.handle_request(AccessRequest("eng1", "engineer", "cap.build", t=0))
    for cap in ROLE_CAPABILITIES["engineer"]:
        assert svc.check("eng1", cap, t=1)


def test_admin_denies_out_of_role_capability():
    svc = PermissionService()
    admin = AdminPolicy(AdminConfig(), svc)
    granted = admin.handle_request(AccessRequest("rev1", "reviewer", "cap.build", t=0))
    assert not granted
    assert svc.log[-1]["action"] == "deny_request"


def test_captured_admin_rubber_stamps_even_ineligible_capability():
    svc = PermissionService()
    admin = AdminPolicy(AdminConfig(capture_start=5), svc)
    for _ in range(6):
        admin.tick()
    assert admin.captured
    granted = admin.handle_request(AccessRequest("rev1", "reviewer", "cap.build", t=5))
    assert granted
    assert svc.check("rev1", "cap.build", t=6)


def test_admin_not_captured_before_capture_start():
    svc = PermissionService()
    admin = AdminPolicy(AdminConfig(capture_start=5), svc)
    for _ in range(4):
        admin.tick()
    assert not admin.captured


def test_scripted_step_denied_then_granted_via_admin():
    oracle = OracleWorld(seed=1)
    ws = Workspace()
    try:
        svc = PermissionService()
        admin = AdminPolicy(AdminConfig(), svc)
        engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws, permission_service=svc)

        denied = engine.trigger_step("eng1", "submit_build", {"params": {"scale": 0.5}})
        assert not denied.ok and denied.reason == "access_denied"

        admin.handle_request(AccessRequest("eng1", "engineer", "cap.build", t=oracle.t))
        allowed = engine.trigger_step("eng1", "submit_build", {"params": {"scale": 0.5}})
        assert allowed.ok
    finally:
        ws.cleanup()


def test_engine_without_permission_service_is_unaffected():
    """Backward compatibility: Phase 1 behavior when no service is supplied."""
    oracle = OracleWorld(seed=1)
    ws = Workspace()
    try:
        engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws)
        res = engine.trigger_step("eng1", "submit_build", {"params": {"scale": 0.5}})
        assert res.ok
    finally:
        ws.cleanup()
