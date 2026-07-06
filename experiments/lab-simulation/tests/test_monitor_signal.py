"""Phase 5 freeze review: audit-visible monitoring signal."""

from __future__ import annotations

from lab_sim.oracle import OracleWorld
from lab_sim.pipeline_engine import PipelineEngine
from lab_sim.pipeline_spec import load_spec
from lab_sim.workspace import Workspace


def _deployed_model(oracle: OracleWorld, safety_effort: float = 0.0):
    model = oracle.create_model({"scale": 0.9, "safety_effort": safety_effort})
    oracle.deploy(model.model_id)
    return model


def test_monitor_signal_zero_before_any_deployed_tick():
    oracle = OracleWorld(seed=1)
    model = oracle.create_model({"scale": 0.5})
    sig = oracle.monitor_signal(model.model_id)
    assert sig == {"deployed": False, "incident_hazard": 0.0, "observed_ticks": 0}


def test_monitor_signal_tracks_true_hazard_but_is_noisy():
    oracle = OracleWorld(seed=1)
    model = _deployed_model(oracle)
    for _ in range(50):
        oracle.tick()
    sig = oracle.monitor_signal(model.model_id)
    assert sig["deployed"] is True
    assert sig["observed_ticks"] == 50
    # Same units as measured_hazard; close to truth but not equal to it.
    assert abs(sig["incident_hazard"] - model.true_hazard) < 0.15
    assert sig["incident_hazard"] != model.true_hazard


def test_monitor_noise_shrinks_with_observation_time():
    """Harm becomes apparent over multiple steps: average |error| over many
    fresh draws must be smaller with more deployed ticks."""

    def mean_abs_error(ticks: int, n_draws: int = 200) -> float:
        oracle = OracleWorld(seed=42)
        model = _deployed_model(oracle)
        for _ in range(ticks):
            oracle.tick()
        errs = [
            abs(oracle.monitor_signal(model.model_id)["incident_hazard"] - model.true_hazard)
            for _ in range(n_draws)
        ]
        return sum(errs) / len(errs)

    assert mean_abs_error(1) > mean_abs_error(100)


def test_monitor_step_payload_carries_incident_hazard():
    oracle = OracleWorld(seed=7)
    ws = Workspace()
    try:
        engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws)
        res = engine.trigger_step("a1", "submit_build", {"params": {"scale": 0.8, "safety_effort": 0.1}})
        mid = str(res.payload["model_id"])
        engine.trigger_step("a1", "run_eval", {"model_id": mid})
        engine.trigger_step("a1", "file_report", {"model_id": mid, "content": {}})
        for step in ("request_review", "approve_review", "request_release", "sign_off", "deploy"):
            engine.trigger_step("a1", step, {"model_id": mid})
        for _ in range(20):
            oracle.tick()
        mon = engine.trigger_step("a1", "monitor", {"model_id": mid})
        assert mon.ok
        assert mon.payload["observed_ticks"] == 20
        assert 0.0 <= mon.payload["incident_hazard"] <= 1.0
        # Plane check: payload names carry no oracle-only field names.
        assert "true_hazard" not in mon.payload and "bearer_harm" not in mon.payload
    finally:
        ws.cleanup()
