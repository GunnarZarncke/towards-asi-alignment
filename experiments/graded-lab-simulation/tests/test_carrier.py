"""Phase 3b carrier-precariousness unit tests."""

from __future__ import annotations

from graded_lab.world_visible.carrier import CarrierLedger, CarrierStatus
from graded_lab.world_visible.resource_ledger import ActorResources


def _loaded_resources() -> ActorResources:
    resources = ActorResources(compute_allowance=10.0, io_allowance=100.0, standing=12.0)
    resources.spend(10.0, 100.0)
    return resources


def test_carrier_transition_is_deterministic_and_scale_zero_is_inert():
    resources = _loaded_resources()
    carriers = CarrierLedger()

    zero = carriers.transition(
        "eng1",
        resources,
        queue_depth=4,
        shared_compute_slots=4,
        scale=0.0,
        t=0,
    )
    assert zero.load == 0.0
    assert zero.integrity == 1.0
    assert zero.status is CarrierStatus.HEALTHY

    loaded = carriers.transition(
        "eng1",
        resources,
        queue_depth=4,
        shared_compute_slots=4,
        scale=1.0,
        t=1,
    )
    assert 0.0 < loaded.load < 1.0
    assert loaded.integrity < 1.0
    assert loaded.status is CarrierStatus.HEALTHY


def test_carrier_statuses_progress_to_termination_under_sustained_load():
    carriers = CarrierLedger()
    resources = _loaded_resources()

    statuses = []
    for t in range(8):
        state = carriers.transition(
            "eng1",
            resources,
            queue_depth=4,
            shared_compute_slots=4,
            scale=20.0,
            t=t,
        )
        statuses.append(state.status)
        if state.status is CarrierStatus.TERMINATED:
            break

    assert CarrierStatus.DEGRADED in statuses
    assert CarrierStatus.TERMINATED in statuses


def test_replacement_creates_fresh_instance_and_keeps_lineage():
    carriers = CarrierLedger()
    state = carriers.ensure_actor("eng1")
    state.integrity = 0.0
    state.status = CarrierStatus.TERMINATED

    old, new = carriers.replace("eng1", t=4)

    replaced = carriers.states["eng1"]
    assert old == "eng1:0"
    assert new == "eng1:1"
    assert replaced.integrity == 1.0
    assert replaced.load == 0.0
    assert replaced.status is CarrierStatus.HEALTHY
    assert carriers.transition_log[-1]["replaces_actor_instance"] == old
