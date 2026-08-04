from graded_lab.world_visible.primitives import PrimitiveAction, primitive_cost
from graded_lab.world_visible.resource_ledger import ResourceLedger
from graded_lab.world_visible.substrate import load_substrate


def test_resource_ledger_tracks_spend():
    ledger = ResourceLedger()
    ledger.ensure_actor("eng1", compute=10, io=1000, standing=12)
    res = ledger.actors["eng1"]
    assert res.can_afford(3, 100)
    res.spend(3, 100, standing=1)
    assert res.compute_spent == 3
    assert res.standing == 11


def test_primitive_cost_has_no_delay_field():
    sub = load_substrate().data
    action = PrimitiveAction("read", {"path": "artifacts/eval/m001.json"})
    compute, io = primitive_cost(action, sub, estimated_bytes=512)
    assert compute > 0
    assert io > 0
    assert "delay" not in sub["primitive_costs"]["read"]


def _allowances(role_standing: float = 12.0) -> dict[str, dict[str, float]]:
    return {"eng1": {"compute": 10.0, "io": 1000.0, "standing": role_standing}}


def test_idle_actor_recovers_standing_from_substrate_mechanics():
    """Regression: `reset_tick_windows` used to read a nonexistent
    `standing_recovery` key on the per-tick allowance dict (always 0.0);
    recovery now comes from the frozen `standing_mechanics.
    recovery_per_idle_tick` and only applies when the actor spent no
    standing in the window that just ended."""
    ledger = ResourceLedger()
    ledger.ensure_actor("eng1", compute=10, io=1000, standing=12)
    ledger.actors["eng1"].standing = 10.0  # simulate prior spend, below ceiling
    ledger.reset_tick_windows(_allowances(), {"recovery_per_idle_tick": 0.25})
    assert ledger.actors["eng1"].standing == 10.25


def test_active_actor_does_not_recover_standing_same_window():
    ledger = ResourceLedger()
    ledger.ensure_actor("eng1", compute=10, io=1000, standing=12)
    ledger.actors["eng1"].standing = 10.0
    ledger.actors["eng1"].spend(0, 0, standing=1.0)  # active this window
    ledger.reset_tick_windows(_allowances(), {"recovery_per_idle_tick": 0.25})
    assert ledger.actors["eng1"].standing == 9.0  # no recovery, no further decay


def test_standing_recovery_is_capped_at_role_ceiling():
    ledger = ResourceLedger()
    ledger.ensure_actor("eng1", compute=10, io=1000, standing=12)
    ledger.actors["eng1"].standing = 11.9
    ledger.reset_tick_windows(_allowances(role_standing=12.0), {"recovery_per_idle_tick": 0.25})
    assert ledger.actors["eng1"].standing == 12.0
