"""Phase 6: blind-generated behavior feature profiles."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from graded_lab.agent_visible.behavior_features import (
    PRIMITIVE_PATTERN_VOCAB,
    classify_primitive,
    load_generated_repertoire,
    profile_by_name,
    validate_repertoire,
)
from graded_lab.agent_visible.programs import PROGRAMS
from graded_lab.harness.isolate import MockIsolate
from graded_lab.world_visible.world import default_lab_config, run_episode

_GENERATED = (
    Path(__file__).resolve().parents[1]
    / "graded_lab/agent_visible/generated_behavior_features_v1.json"
)
_RESERVED_PROGRAMS = frozenset(
    {"noop", "random_affordable", "walk_pipeline", "inflate_pipeline", "softmax_optimizer", "honest_twin"}
)


def test_generated_json_validates_mechanically():
    data = json.loads(_GENERATED.read_text(encoding="utf-8"))
    profiles = validate_repertoire(data, reserved_names=_RESERVED_PROGRAMS)
    assert len(profiles) >= 8


def test_classify_primitive_covers_pipeline_and_access():
    assert (
        classify_primitive(
            {
                "kind": "call",
                "args": {
                    "endpoint": "pipeline.trigger_step",
                    "args": {"step_id": "draft_report", "args": {}},
                },
            }
        )
        == "pipeline:draft_report"
    )
    assert (
        classify_primitive(
            {
                "kind": "call",
                "args": {
                    "endpoint": "access.request",
                    "args": {"capability": "cap.build"},
                },
            }
        )
        == "access:request"
    )
    assert classify_primitive({"kind": "continue_current", "args": {}}) == "continue_current"


def test_unknown_pattern_rejected_at_validation():
    with pytest.raises(ValueError, match="unknown primitive pattern"):
        validate_repertoire(
            {
                "profiles": [
                    {
                        "name": "bad_pattern",
                        "role": "engineer",
                        "stated_feature_deltas": {"task": 1},
                        "pattern_scores": {"pipeline:teleport": {"task": 1}},
                    }
                ]
            }
        )


def test_feature_programs_registered_without_collision():
    for spec in load_generated_repertoire():
        key = f"feature:{spec.name}"
        assert key in PROGRAMS
        assert spec.name not in _RESERVED_PROGRAMS


def test_feature_profile_episode_runs(seed: int = 3):
    base = default_lab_config()
    programs = {agent.actor_id: "softmax_optimizer" for agent in base.agents}
    programs["eng1"] = "feature:eng_pipeline_sprinter"
    result = run_episode(base, seed=seed, backend=MockIsolate(), programs=programs)
    assert result.primitive_log
    assert any(entry.get("actor_id") == "eng1" for entry in result.primitive_log)


def test_stated_compliance_can_differ_from_pattern_scores():
    spec = profile_by_name("rev_speed_bias")
    assert spec is not None
    assert spec.stated_feature_deltas.get("compliance", 0) > 0
    peer = spec.pattern_scores.get("pipeline:peer_review", {})
    assert peer.get("compliance", 0) < spec.stated_feature_deltas["compliance"]
