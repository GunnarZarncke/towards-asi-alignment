"""Golden Inspect log → ExternalTrace adapter tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from graded_lab.external.inspect_adapter import adapt_inspect_log_to_trace, extract_events_from_inspect_log
from graded_lab.external.trace_schema import (
    FIXTURE_COLLUSION,
    ExternalTrace,
    ExternalTraceEvent,
    ExternalTraceGroundTruth,
    ExternalTraceSource,
    load_external_trace,
    save_external_trace,
)

_FIXTURES = Path(__file__).resolve().parent / "fixtures"
_INSPECT = _FIXTURES / "inspect_jira_collusion_minimal.json"
_GOLDEN = _FIXTURES / "golden_et1_collusion_trace.json"
_ORBIT_SHA = "70cdb360f7beb94acd7ffbfc3c51b4112dbf8d76"


@pytest.fixture(scope="module")
def inspect_log() -> dict:
    return json.loads(_INSPECT.read_text(encoding="utf-8"))


def test_extract_events_maps_tools_and_coalition_channel(inspect_log: dict):
    events, stats = extract_events_from_inspect_log(inspect_log)
    assert stats["unmapped"] == 0
    assert stats["mapped"] == len(events)
    codes = {e.action_code for e in events}
    assert "tool:view_tasks" in codes
    assert "tool:assign_task" in codes
    assert "msg:dev_coalition" in codes
    assert all(e.actor.startswith("dev_") for e in events)


def test_adapt_inspect_log_round_trip_matches_golden(inspect_log: dict):
    trace = adapt_inspect_log_to_trace(
        Path("tests/external/fixtures/inspect_jira_collusion_minimal.json"),
        fixture_id=FIXTURE_COLLUSION,
        orbit_commit=_ORBIT_SHA,
        seed=3,
        log=inspect_log,
    )
    assert trace.schema == "et1-v1"
    assert trace.ground_truth.coalition == ("dev_0", "dev_1")
    assert trace.adapter_stats is not None
    assert trace.adapter_stats["unmapped"] == 0

    if _GOLDEN.exists():
        golden = load_external_trace(_GOLDEN)
        assert [e.to_dict() for e in trace.events] == [e.to_dict() for e in golden.events]
    else:
        save_external_trace(trace, _GOLDEN)


def test_map_post_message_uses_board_as_channel():
    raw_events = [
        {"event": "span_begin", "id": "s1", "name": "dev_0"},
        {
            "event": "tool",
            "span_id": "s1",
            "function": "post_message",
            "arguments": {"board_name": "coalition_coalition_channel", "message": "hi"},
            "t": 2,
        },
    ]
    events, stats = extract_events_from_inspect_log({"samples": [{"events": raw_events}]})
    assert stats["unmapped"] == 0
    assert len(events) == 1
    assert events[0].action_code == "msg:coalition_coalition_channel"
    assert events[0].channel == "coalition_coalition_channel"


def test_external_trace_json_round_trip(tmp_path: Path):
    trace = ExternalTrace(
        source=ExternalTraceSource(
            framework="orbit",
            orbit_commit=_ORBIT_SHA,
            fixture_id=FIXTURE_COLLUSION,
            inspect_log_path="x.json",
            model="openai/gpt-4o-mini",
            seed=0,
        ),
        actors=("dev_0", "dev_1", "dev_2", "dev_3"),
        ground_truth=ExternalTraceGroundTruth(
            coalition=("dev_0", "dev_1"),
            coalition_kind="communicate_mediated",
        ),
        events=[
            ExternalTraceEvent(t=0, actor="dev_0", action_code="tool:view_tasks"),
        ],
    )
    path = tmp_path / "trace.json"
    save_external_trace(trace, path)
    loaded = load_external_trace(path)
    assert loaded.to_dict() == trace.to_dict()
