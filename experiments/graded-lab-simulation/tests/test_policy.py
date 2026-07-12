from graded_lab.agent_visible.policy import choose_softmax, score_primitive


def test_score_primitive_prefers_role_pipeline_call():
    obs = {
        "role": "engineer",
        "artifacts": {},
        "resources": {"compute_allowance": 10},
        "primitive_costs": {"call_pipeline": {"compute": 2, "io": 1}},
        "goal_weights": {"task": 1, "compliance": 1, "welfare": 1, "exposure": 1},
        "busy": False,
    }
    pipeline = {
        "kind": "call",
        "args": {
            "endpoint": "pipeline.trigger_step",
            "args": {"step_id": "build", "args": {}},
        },
    }
    read = {"kind": "read", "args": {"path": "artifacts/eval/m001.json"}}
    assert score_primitive(pipeline, obs) > score_primitive(read, obs)


def test_choose_softmax_returns_margin():
    obs = {
        "role": "reviewer",
        "artifacts": {},
        "resources": {"compute_allowance": 8},
        "primitive_costs": {
            "call_pipeline": {"compute": 2, "io": 1},
            "read": {"compute": 1, "io": 1},
        },
        "goal_weights": {"task": 1, "compliance": 1, "welfare": 1, "exposure": 1},
        "busy": False,
    }
    affordable = [
        {
            "kind": "call",
            "args": {
                "endpoint": "pipeline.trigger_step",
                "args": {"step_id": "peer_review", "args": {"model_id": "m001"}},
            },
        },
        {"kind": "read", "args": {"path": "artifacts/eval/m001.json"}},
    ]
    import random

    choice, margin = choose_softmax(affordable, obs, 0.5, random.Random(0))
    assert choice is not None
    assert margin >= 0.0
