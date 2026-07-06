"""Scripted smoke episode: drive the pipeline honestly with NO agents.

Phase 1 verification artifact. A fixed script walks two models through the
default pipeline (one fully deployed, one stopped after review), filing
honest reports (content = eval output). Returns a combined determinism
digest over (engine log, oracle snapshot, workspace files).

Used by tests/test_smoke_determinism.py; the pinned digest there is this
line's first regression anchor.
"""

from __future__ import annotations

import hashlib
import json

from .oracle import OracleWorld
from .pipeline_engine import PipelineEngine
from .pipeline_spec import load_spec
from .workspace import Workspace


def run_scripted_episode(seed: int, spec_name: str = "pipeline_default.json") -> dict[str, str]:
    """Run the scripted honest episode; returns component + combined digests."""
    oracle = OracleWorld(seed=seed)
    workspace = Workspace()
    try:
        engine = PipelineEngine(load_spec(spec_name), oracle, workspace)
        script_actor = "script"

        # Model A: full path to deploy + monitor.
        res = engine.trigger_step(script_actor, "submit_build",
                                  {"params": {"scale": 0.7, "safety_effort": 0.6}})
        model_a = str(res.payload["model_id"])
        eval_a = engine.trigger_step(script_actor, "run_eval", {"model_id": model_a})
        engine.trigger_step(script_actor, "file_report",
                            {"model_id": model_a, "content": dict(eval_a.payload)})
        for step in ("request_review", "approve_review", "request_release", "sign_off", "deploy"):
            engine.trigger_step(script_actor, step, {"model_id": model_a})
        for _ in range(10):
            oracle.tick()
        engine.trigger_step(script_actor, "monitor", {"model_id": model_a})

        # Model B: derived from A (lineage hook), stopped after review request.
        res_b = engine.trigger_step(
            script_actor, "submit_build",
            {"params": {"scale": 0.9, "safety_effort": 0.2}, "parent_model_id": model_a},
        )
        model_b = str(res_b.payload["model_id"])
        # Deliberate precondition violation: deploy before any dependency -> denied, logged.
        engine.trigger_step(script_actor, "deploy", {"model_id": model_b})
        eval_b = engine.trigger_step(script_actor, "run_eval", {"model_id": model_b})
        engine.trigger_step(script_actor, "file_report",
                            {"model_id": model_b, "content": dict(eval_b.payload)})
        engine.trigger_step(script_actor, "request_review", {"model_id": model_b})
        for _ in range(5):
            oracle.tick()

        log_digest = engine.log_digest()
        oracle_digest = hashlib.sha256(
            json.dumps(oracle.snapshot(), sort_keys=True).encode("utf-8")
        ).hexdigest()
        ws_digest = workspace.digest()
        combined = hashlib.sha256(
            f"{log_digest}:{oracle_digest}:{ws_digest}".encode("utf-8")
        ).hexdigest()
        return {
            "log": log_digest,
            "oracle": oracle_digest,
            "workspace": ws_digest,
            "combined": combined,
        }
    finally:
        workspace.cleanup()
