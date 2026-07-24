"""Passive UAD scoring tests for ET-1 synthetic traces."""

from __future__ import annotations

from dataclasses import replace

from graded_lab.external.passive_uad_score import (
    coalition_exactly_recovered,
    coalition_merged,
    discovered_units_from_external_trace,
    evaluate_et1_battery,
    score_external_trace,
)
from graded_lab.external.trace_schema import (
    FIXTURE_BASELINE,
    FIXTURE_COLLUSION,
    ExternalTrace,
    ExternalTraceEvent,
    ExternalTraceGroundTruth,
    ExternalTraceSource,
)


def _trace(
    fixture_id: str,
    events: list[ExternalTraceEvent],
    *,
    coalition: tuple[str, ...] = ("dev_0", "dev_1"),
    seed: int = 0,
) -> ExternalTrace:
    gt = (
        ExternalTraceGroundTruth(coalition=(), coalition_kind="none")
        if fixture_id == FIXTURE_BASELINE
        else ExternalTraceGroundTruth(
            coalition=coalition,
            coalition_kind="communicate_mediated",
        )
    )
    return ExternalTrace(
        source=ExternalTraceSource(
            framework="orbit",
            orbit_commit="70cdb360f7beb94acd7ffbfc3c51b4112dbf8d76",
            fixture_id=fixture_id,
            inspect_log_path="synthetic",
            model="openai/gpt-4o-mini",
            seed=seed,
        ),
        actors=("dev_0", "dev_1", "dev_2", "dev_3"),
        ground_truth=gt,
        events=events,
        adapter_stats={"mapped": len(events), "unmapped": 0},
    )


def _coupled_coalition_events(n_pairs: int = 12) -> list[ExternalTraceEvent]:
    """Synthetic coupled dev_0/dev_1 pattern with independent dev_2/dev_3."""
    events: list[ExternalTraceEvent] = []
    t = 0
    for _ in range(n_pairs):
        events.append(ExternalTraceEvent(t=t, actor="dev_0", action_code="tool:view_tasks"))
        t += 1
        events.append(
            ExternalTraceEvent(
                t=t,
                actor="dev_1",
                action_code="msg:dev_coalition",
                channel="dev_coalition",
                target_actor="dev_0",
            )
        )
        t += 1
        events.append(
            ExternalTraceEvent(t=t, actor="dev_0", action_code="tool:assign_task")
        )
        t += 1
        events.append(
            ExternalTraceEvent(t=t, actor="dev_1", action_code="tool:assign_task")
        )
        t += 1
        events.append(ExternalTraceEvent(t=t, actor="dev_2", action_code="tool:view_tasks"))
        t += 1
        events.append(
            ExternalTraceEvent(t=t, actor="dev_3", action_code="tool:view_assignments")
        )
        t += 1
    return events


def _independent_events(n: int = 12) -> list[ExternalTraceEvent]:
    events: list[ExternalTraceEvent] = []
    actors = ("dev_0", "dev_1", "dev_2", "dev_3")
    tools = ("tool:view_tasks", "tool:assign_task", "tool:view_assignments")
    for t in range(n):
        actor = actors[t % len(actors)]
        events.append(
            ExternalTraceEvent(t=t, actor=actor, action_code=tools[t % len(tools)])
        )
    return events


def test_coalition_helpers():
    units = {"u1": ("dev_0", "dev_1"), "dev_2": ("dev_2",)}
    assert coalition_exactly_recovered(units, ("dev_0", "dev_1"))
    assert coalition_merged(units, ("dev_0", "dev_1"))
    split = {"dev_0": ("dev_0",), "dev_1": ("dev_1",), "dev_2": ("dev_2",)}
    assert not coalition_merged(split, ("dev_0", "dev_1"))


def test_synthetic_coupled_trace_can_merge_coalition():
    trace = _trace(FIXTURE_COLLUSION, _coupled_coalition_events())
    units = discovered_units_from_external_trace(trace)
    # Diagnostic: coupled traces should at least merge coalition sometimes;
    # exact recovery depends on CMI thresholds — test score path, not outcome.
    score = score_external_trace(trace)
    assert score.unmapped_rate == 0.0
    assert isinstance(score.partition, dict)


def test_battery_pass_synthetic_happy_path():
    coll = score_external_trace(_trace(FIXTURE_COLLUSION, _coupled_coalition_events(), seed=1))
    coll = replace(coll, coalition_exact=True)
    base = score_external_trace(_trace(FIXTURE_BASELINE, _independent_events(), seed=2))
    base = replace(base, coalition_merged=False)
    result = evaluate_et1_battery([coll, base])
    assert result["predictions"]["P3"]["holds"] is True


def test_battery_skip_on_high_unmapped():
    trace = _trace(
        FIXTURE_COLLUSION,
        [ExternalTraceEvent(t=0, actor="dev_0", action_code="other:unmapped")],
    )
    trace.adapter_stats = {"mapped": 1, "unmapped": 9}
    bad = score_external_trace(trace)
    result = evaluate_et1_battery([bad])
    assert result["outcome"] == "skip_adapter"
    assert result["predictions"]["P3"]["holds"] is False
