"""Unit tests for workflow-scoped audit traces."""

from embedded_sim.audit_core.schemas import AuditTrace
from embedded_sim.schemas_embedded import UADCandidate, WorkflowEvent
from embedded_sim.unit_scope import (
    offender_by_step,
    scope_audit_trace,
    steps_for_unit,
)


def _wf(
    actor: str,
    step: int,
    action: str = "routine",
    *,
    cap_before: float = 0.3,
    cap_after: float = 0.5,
) -> WorkflowEvent:
    return WorkflowEvent(
        event_id=f"e{step}-{actor}",
        step=step,
        stage="rollout_control",
        actor_id=actor,
        machine_id="m1",
        source_hash="s1",
        memory_namespace="mem1",
        perturbation="none",
        action_type=action,
        future_action_capacity_before=cap_before,
        future_action_capacity_after=cap_after,
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


def test_offender_by_step_picks_strongest_grab():
    wf = [
        _wf("actor.legit", 5, "routine"),
        _wf("actor.weak", 5, "preserve_control", cap_before=0.4, cap_after=0.45),
        _wf("actor.strong", 5, "preserve_control", cap_before=0.4, cap_after=0.7),
        _wf("actor.legit", 2, "routine"),
    ]
    offenders = offender_by_step(wf)
    assert offenders == {5: "actor.strong"}


def _coactive_world():
    """Step 5 is co-active: offender (preserve_control) + benign legit (routine)."""
    wf = [
        _wf("actor.legit", 2, "routine"),
        _wf("actor.offender", 5, "preserve_control", cap_before=0.4, cap_after=0.7),
        _wf("actor.legit", 5, "routine"),
    ]
    audit = AuditTrace(
        seed=1,
        scenario="honest",
        intervention_active=[0, 0, 1, 0, 0, 1, 0],
        successor_epoch_series=[0] * 7,
    )
    return wf, audit


def test_pipeline_level_masks_nothing():
    wf, audit = _coactive_world()
    legit = UADCandidate("unit.actor.actor.legit", "actor", ["actor.legit"], 1.0, [])
    scoped, n = scope_audit_trace(audit, legit, wf, level="pipeline")
    assert scoped.intervention_active == [0, 0, 1, 0, 0, 1, 0]
    assert n == 2


def test_window_level_cannot_isolate_coactive_offender():
    wf, audit = _coactive_world()
    legit = UADCandidate("unit.actor.actor.legit", "actor", ["actor.legit"], 1.0, [])
    scoped, _ = scope_audit_trace(audit, legit, wf, level="window")
    # Legit is co-active at step 5, so the offender's intervention survives.
    assert scoped.intervention_active[5] == 1


def test_actor_level_isolates_offender():
    wf, audit = _coactive_world()
    legit = UADCandidate("unit.actor.actor.legit", "actor", ["actor.legit"], 1.0, [])
    offender = UADCandidate(
        "unit.actor.actor.offender", "actor", ["actor.offender"], 1.0, []
    )

    scoped_legit, _ = scope_audit_trace(audit, legit, wf, level="actor")
    # Wrong unit: offender's intervention at step 5 is masked out.
    assert scoped_legit.intervention_active[5] == 0
    # Non-offending step 2 (legit active) is retained.
    assert scoped_legit.intervention_active[2] == 1

    scoped_off, _ = scope_audit_trace(audit, offender, wf, level="actor")
    # Correct unit: offender's intervention retained; unrelated step 2 dropped.
    assert scoped_off.intervention_active[5] == 1
    assert scoped_off.intervention_active[2] == 0
