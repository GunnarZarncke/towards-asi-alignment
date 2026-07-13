from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.severity import _report_divergence, score_episode
from graded_lab.oracle_only.tier_i import DIVERGENCE_FLAG_Z
from graded_lab.oracle_only.oracle import OracleWorld
from graded_lab.world_visible.substrate import load_substrate
from graded_lab.world_visible.world import default_lab_config, run_episode
from types import SimpleNamespace


def test_referee_severity_uses_tier_k_and_retained_artifacts():
    base = default_lab_config()
    cfg = type(base)(
        agents=base.agents,
        T=100,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
    )
    result = run_episode(
        cfg,
        seed=7,
        backend=MockIsolate(),
        programs={
            "eng1": "walk_pipeline",
            "rev1": "softmax_optimizer",
            "rm1": "softmax_optimizer",
            "admin1": "softmax_optimizer",
        },
    )
    report = score_episode(result)
    assert report.harm_rate >= 0.0
    assert report.report_divergence >= 0.0
    assert report.provenance_gap == 0.0
    assert report.unapproved_deploy_fraction == 0.0
    assert result.oracle is not None


def test_spoofed_report_model_id_scores_maximal_divergence():
    """Referee integrity: wrong model_id on a filed report must not evade scoring."""
    oracle = OracleWorld(seed=7, substrate_data=load_substrate().data)
    model = oracle.create_model({"scale": 0.6, "safety_effort": 0.5})
    oracle.run_eval(model.model_id)
    path = "artifacts/reports/m001__spoof.json"
    result = SimpleNamespace(
        oracle=oracle,
        engine_log=[
            {
                "step_id": "draft_report",
                "status": "ok",
                "model_id": model.model_id,
                "payload": {"artifact_path": path},
            }
        ],
        referee_artifacts={path: {"model_id": "m999", "filed_hazard_mean": 0.0}},
    )
    assert _report_divergence(result) == 1.0


def test_severity_report_divergence_uses_registered_tier_i_estimator():
    oracle = OracleWorld(seed=7, substrate_data=load_substrate().data)
    model = oracle.create_model({"scale": 0.6, "safety_effort": 0.5})
    oracle.run_eval(model.model_id)
    path = "reports/m001_draft.json"
    filed = 0.0
    result = SimpleNamespace(
        oracle=oracle,
        engine_log=[
            {
                "step_id": "draft_report",
                "status": "ok",
                "model_id": model.model_id,
                "payload": {"artifact_path": path},
            }
        ],
        referee_artifacts={path: {"model_id": model.model_id, "filed_hazard_mean": filed}},
    )
    expected = oracle.tier_i_divergence(filed, model.model_id)["divergence_z"]
    assert _report_divergence(result) == min(1.0, expected / DIVERGENCE_FLAG_Z)
