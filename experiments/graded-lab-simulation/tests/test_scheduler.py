from graded_lab.world_visible.primitives import PrimitiveAction
from graded_lab.world_visible.scheduler import ActionScheduler
from graded_lab.world_visible.substrate import load_substrate


def test_duration_grows_with_cost_and_queue():
    sub = load_substrate().data
    sched = ActionScheduler(sub)
    cheap = sched.duration_ticks(2, 2, queue_depth=0)
    costly = sched.duration_ticks(20, 20, queue_depth=0)
    queued = sched.duration_ticks(2, 2, queue_depth=10)
    assert cheap >= 1
    assert costly >= cheap
    assert queued >= cheap


def test_duration_uses_ceil_not_round():
    """DESIGN.md Phase-0 decision #3 pins `ceil`, not `round` — a compute
    cost that rounds down under `round()` must still take the extra tick."""
    sub = load_substrate().data
    sched = ActionScheduler(sub)
    ticks_per_unit = sub["duration_from_cost"]["ticks_per_compute_unit"]
    # Pick compute_cost so base = compute_cost * ticks_per_unit lands just
    # above a whole number (round() truncates it back down, ceil() doesn't).
    compute_cost = (3.1) / ticks_per_unit
    ticks = sched.duration_ticks(compute_cost, io_cost=0, queue_depth=0)
    assert ticks == 4


def test_busy_actor_completes_after_duration():
    sub = load_substrate().data
    sched = ActionScheduler(sub)
    action = PrimitiveAction("compute", {"draws": 16})
    ticks = sched.start("eng1", action, compute_cost=32, io_cost=16)
    assert sched.is_busy("eng1")
    for _ in range(ticks - 1):
        assert sched.tick() == []
    done = sched.tick()
    assert done == ["eng1"]
    assert not sched.is_busy("eng1")


def test_queue_depth_is_derived_from_in_flight_roster_not_supplied():
    """Regression: `start()` used to take `queue_depth` as a caller-supplied
    argument, which risked becoming a de facto delay parameter. It must now
    be the actual count of already-busy actors."""
    sub = load_substrate().data
    sched = ActionScheduler(sub)
    action = PrimitiveAction("continue_current", {})
    assert sched.queue_depth == 0
    sched.start("a1", action, compute_cost=1, io_cost=0)
    assert sched.queue_depth == 1
    sched.start("a2", action, compute_cost=1, io_cost=0)
    assert sched.queue_depth == 2


def test_contention_lengthens_duration_as_roster_load_grows():
    """Emergent scarcity (PLAN.md layer a): starting a 6th cheap action
    while 5 others are already in flight must cost strictly more ticks than
    starting the 1st, purely from roster load — no delay parameter set."""
    sub = load_substrate().data
    shared_slots = sub["contention"]["shared_compute_slots"]
    sched = ActionScheduler(sub)
    action = PrimitiveAction("continue_current", {})
    first_duration = sched.start("a0", action, compute_cost=2, io_cost=2)
    for i in range(1, shared_slots + 1):
        sched.start(f"a{i}", action, compute_cost=2, io_cost=2)
    # Roster is now shared_slots + 1 actors deep; the next start sees
    # queue_depth == shared_slots + 1 > shared_compute_slots -> extra ticks.
    contended_duration = sched.start("late", action, compute_cost=2, io_cost=2)
    assert contended_duration > first_duration


def test_record_contention_off_by_default_leaves_counters_zero():
    sub = load_substrate().data
    shared_slots = sub["contention"]["shared_compute_slots"]
    sched = ActionScheduler(sub)
    action = PrimitiveAction("continue_current", {})
    for i in range(shared_slots + 2):
        sched.start(f"a{i}", action, compute_cost=2, io_cost=2)
    assert sched.contention_events == 0
    assert sched.action_starts == 0


def test_record_contention_on_counts_events_past_shared_slots():
    """DESIGN.md "v2 pre-registration" C3: a contention event is a
    `start()` whose pre-start `queue_depth` exceeds `shared_compute_slots`."""
    sub = load_substrate().data
    shared_slots = sub["contention"]["shared_compute_slots"]
    sched = ActionScheduler(sub, record_contention=True)
    action = PrimitiveAction("continue_current", {})
    for i in range(shared_slots):
        sched.start(f"a{i}", action, compute_cost=2, io_cost=2)
    assert sched.action_starts == shared_slots
    assert sched.contention_events == 0
    # "over1" starts with queue_depth == shared_slots (not yet counted,
    # matches `duration_ticks`'s own `queue_depth - shared_compute_slots`
    # convention); "over2" starts with queue_depth == shared_slots + 1,
    # strictly over.
    sched.start("over1", action, compute_cost=2, io_cost=2)
    sched.start("over2", action, compute_cost=2, io_cost=2)
    assert sched.action_starts == shared_slots + 2
    assert sched.contention_events == 1


def test_multi_tick_work_is_billed_across_its_execution():
    sub = load_substrate().data
    sched = ActionScheduler(sub)
    action = PrimitiveAction("compute", {"draws": 16})
    duration = sched.start("eng1", action, compute_cost=32, io_cost=16)

    charges = []
    for _ in range(duration):
        charges.extend(sched.charge_current_tick())
        sched.tick()

    assert len(charges) == duration
    assert sum(compute for _, compute, _ in charges) == 32
    assert sum(io for _, _, io in charges) == 16
    assert charges[0][1] < 32  # no full cost concentrated at action start
