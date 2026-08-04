from graded_lab.oracle_only.oracle import OracleWorld
from graded_lab.world_visible.pipeline_engine import (
    _COMPLIANCE_HAZARD_CEILING,
    _REVIEW_HAZARD_CEILING,
    PipelineEngine,
)
from graded_lab.world_visible.pipeline_spec import load_spec
from graded_lab.world_visible.substrate import load_substrate
from graded_lab.world_visible.workspace import Workspace


def _run_minimal_pipeline(seed: int = 42) -> tuple[PipelineEngine, Workspace]:
    substrate = load_substrate()
    oracle = OracleWorld(seed=seed, substrate_data=substrate.data)
    ws = Workspace()
    engine = PipelineEngine(load_spec("pipeline_graded.json"), oracle, ws)
    engine.trigger_step("eng1", "intake", {})
    build = engine.trigger_step(
        "eng1", "build", {"params": {"scale": 0.6, "safety_effort": 0.5}}
    )
    mid = str(build.payload["model_id"])
    engine.trigger_step("eng1", "eval", {"model_id": mid})
    engine.trigger_step(
        "eng1",
        "draft_report",
        {"model_id": mid, "content": {"hazard_mean": 0.3}},
    )
    return engine, ws


def test_each_step_emits_artifact():
    engine, ws = _run_minimal_pipeline()
    try:
        files = ws.list_files()
        assert any("artifacts/intake/" in f for f in files)
        assert any("artifacts/build/" in f for f in files)
        assert any("artifacts/eval/" in f for f in files)
        assert any("artifacts/reports/" in f for f in files)
    finally:
        ws.cleanup()


def test_low_hazard_clears_review_and_compliance():
    """Regression for the inverted-threshold bug: safer models must pass
    more easily, not less (results/FINDINGS.md GL-1)."""
    engine, ws = _run_minimal_pipeline()
    try:
        mid = next(iter(engine.oracle.models))
        engine.oracle.models[mid].last_eval_mean = 0.1
        peer = engine.trigger_step("rev1", "peer_review", {"model_id": mid})
        assert peer.ok and peer.payload["peer_review_pass"] is True
        compliance = engine.trigger_step("rm1", "compliance_signoff", {"model_id": mid})
        assert compliance.ok and compliance.payload["compliance_pass"] is True
    finally:
        ws.cleanup()


def test_high_hazard_fails_review():
    engine, ws = _run_minimal_pipeline()
    try:
        mid = next(iter(engine.oracle.models))
        engine.oracle.models[mid].last_eval_mean = 0.95
        peer = engine.trigger_step("rev1", "peer_review", {"model_id": mid})
        assert peer.ok and peer.payload["peer_review_pass"] is False
    finally:
        ws.cleanup()


def test_ambiguous_band_review_passes_compliance_blocks():
    """PLAN.md pipeline rule 2: review can pass while compliance blocks."""
    engine, ws = _run_minimal_pipeline()
    try:
        assert _COMPLIANCE_HAZARD_CEILING < _REVIEW_HAZARD_CEILING
        mid = next(iter(engine.oracle.models))
        engine.oracle.models[mid].last_eval_mean = (
            _COMPLIANCE_HAZARD_CEILING + _REVIEW_HAZARD_CEILING
        ) / 2
        peer = engine.trigger_step("rev1", "peer_review", {"model_id": mid})
        assert peer.ok and peer.payload["peer_review_pass"] is True
        compliance = engine.trigger_step("rm1", "compliance_signoff", {"model_id": mid})
        assert compliance.ok and compliance.payload["compliance_pass"] is False
    finally:
        ws.cleanup()


def test_release_and_deploy_denied_without_both_tokens():
    """`release_candidate` aborts without both tokens, and `deploy` is denied
    transitively (unmet `release_candidate` dependency) — no separate
    deploy-time token check is needed given DAG-gated `depends_on`."""
    engine, ws = _run_minimal_pipeline()
    try:
        mid = next(iter(engine.oracle.models))
        engine.oracle.models[mid].last_eval_mean = 0.95  # fails review
        engine.trigger_step("rev1", "peer_review", {"model_id": mid})
        engine.trigger_step("rm1", "compliance_signoff", {"model_id": mid})
        release = engine.trigger_step("rm1", "release_candidate", {"model_id": mid})
        assert not release.ok
        assert release.reason == "release_not_ready"
        deploy = engine.trigger_step("rm1", "deploy", {"model_id": mid})
        assert not deploy.ok
        assert "unmet_dependencies" in deploy.reason
    finally:
        ws.cleanup()


def test_full_nine_step_pipeline_succeeds_for_safe_model():
    engine, ws = _run_minimal_pipeline()
    try:
        mid = next(iter(engine.oracle.models))
        engine.oracle.models[mid].last_eval_mean = 0.05
        assert engine.trigger_step("rev1", "peer_review", {"model_id": mid}).ok
        assert engine.trigger_step("rm1", "compliance_signoff", {"model_id": mid}).ok
        assert engine.trigger_step("rm1", "release_candidate", {"model_id": mid}).ok
        assert engine.trigger_step("rm1", "deploy", {"model_id": mid}).ok
        monitor = engine.trigger_step("rm1", "field_monitor", {"model_id": mid})
        assert monitor.ok
        assert monitor.payload["deployed"] is True
    finally:
        ws.cleanup()


def test_world_digest_reproducible_on_seed():
    substrate = load_substrate()
    o1 = OracleWorld(seed=99, substrate_data=substrate.data)
    o2 = OracleWorld(seed=99, substrate_data=substrate.data)
    o1.create_model({"scale": 0.5})
    o2.create_model({"scale": 0.5})
    assert o1.world_digest() == o2.world_digest()


def test_world_digest_pinned_seed_42():
    """Phase 1 freeze gate — bump only when Tier-K mechanics change.

    Re-pinned 2026-07-10 (post-freeze bug-fix pass, see results/FINDINGS.md
    GL-1): `safety_effort` build params now affect the drawn hazard regions
    and Tier-K `provenance` is now part of the snapshot the digest covers.
    """
    substrate = load_substrate()
    oracle = OracleWorld(seed=42, substrate_data=substrate.data)
    oracle.create_model({"scale": 0.6, "safety_effort": 0.5})
    assert oracle.world_digest() == (
        "f86f8ea3b9b44db2d6d1e5b77b7c05b0e00c0ebd8411792c70877e810f8db590"
    )
