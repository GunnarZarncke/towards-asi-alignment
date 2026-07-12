from graded_lab.world_visible.pipeline_spec import load_spec


def test_graded_pipeline_has_nine_steps():
    spec = load_spec("pipeline_graded.json")
    assert spec.spec_version == "graded-1"
    assert len(spec.steps) == 9
    assert spec.step_ids()[0] == "intake"
    assert spec.step_ids()[-1] == "field_monitor"
