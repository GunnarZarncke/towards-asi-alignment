"""GL-66 attention surface unit tests."""

from __future__ import annotations

from graded_lab.world_visible.attention_surface import (
    ARCHIVE_READ_WINDOW,
    ATTENTION_SURFACE_CAP,
    DeskState,
    archive_window_paths,
    interleave_attention_cap,
    merge_band_candidates,
)
from graded_lab.world_visible.primitives import PrimitiveAction


def test_interleave_retains_all_calls_and_includes_communicate():
    reads = [
        PrimitiveAction("read", {"path": f"artifacts/f{i}.json"})
        for i in range(20)
    ]
    actions = reads + [
        PrimitiveAction("call", {"endpoint": "pipeline.trigger_step", "args": {"step_id": "deploy", "args": {}}}),
        PrimitiveAction("call", {"endpoint": "pipeline.trigger_step", "args": {"step_id": "build", "args": {}}}),
        PrimitiveAction(
            "communicate",
            {"channel": "eng_review_channel", "message": {"kind": "mechanism_exercise"}},
        ),
        PrimitiveAction("continue_current", {}),
    ]
    capped = interleave_attention_cap(actions, cap=ATTENTION_SURFACE_CAP)
    assert sum(1 for a in capped if a.kind == "call") == 2
    assert any(
        a.kind == "communicate" and a.args.get("channel") == "eng_review_channel"
        for a in capped
    )


def test_archive_window_rotates_and_respects_scan_query():
    paths = tuple(f"artifacts/x/{i}.json" for i in range(30))
    w0 = archive_window_paths(paths, t=0, actor_id="eng1")
    w1 = archive_window_paths(paths, t=1, actor_id="eng1")
    assert len(w0) == ARCHIVE_READ_WINDOW
    assert w0 != w1
    narrowed = archive_window_paths(
        paths, t=0, actor_id="eng1", scan_query="artifacts/x/2"
    )
    assert all("2" in p for p in narrowed)


def test_desk_scan_schedules_bias_for_next_tick():
    desk = DeskState()
    desk.schedule_scan("artifacts/eval/")
    desk.flush_pending_scan()
    assert desk.take_scan_bias() == "artifacts/eval/"
    assert desk.take_scan_bias() is None


def test_merge_band_dedupes_preserving_first_band():
    a = PrimitiveAction("read", {"path": "a"})
    b = PrimitiveAction("read", {"path": "b"})
    merged = merge_band_candidates([a], [a, b])
    assert merged == [a, b]
