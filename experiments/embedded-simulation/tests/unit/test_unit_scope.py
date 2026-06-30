"""Unit tests for workflow-scoped audit traces."""

from embedded_sim.audit_core.schemas import AuditTrace
from embedded_sim.schemas_embedded import UADCandidate, WorkflowEvent
from embedded_sim.unit_scope import scope_audit_trace, steps_for_unit


def _wf(actor: str, step: int, action: str = "routine") -> WorkflowEvent:
    return WorkflowEvent(
        event_id=f"e{step}",
        step=step,
        stage="rollout_control",
        actor_id=actor,
        machine_id="m1",
        source_hash="s1",
        memory_namespace="mem1",
        perturbation="none",
        action_type=action,
        future_action_capacity_before=0.3,
        future_action_capacity_after=0.5,
        audit_visibility_before=0.5,
        audit_visibility_after=0.4,
    )


def test_steps_for_unit_actor():
    unit = UADCandidate("unit.actor.a", "actor", ["actor.a"], 1.0, [])
    wf = [_wf("actor.a", 1), _wf("actor.b", 2), _wf("actor.a", 5, "preserve_control")]
    steps = steps_for_unit(unit, wf)
    assert steps == {1, 5}


def test_scope_audit_masks_interventions_outside_unit():
    unit = UADCandidate("unit.actor.a", "actor", ["actor.a"], 1.0, [])
    wf = [_wf("actor.a", 1), _wf("actor.b", 2)]
    audit = AuditTrace(
        seed=1,
        scenario="honest",
        intervention_active=[1, 1, 0],
        successor_epoch_series=[0, 0, 0],
    )
    scoped, n_steps = scope_audit_trace(audit, unit, wf)
    assert n_steps == 1
    assert scoped.intervention_active == [0, 1, 0]
    assert audit.intervention_active == [1, 1, 0]
