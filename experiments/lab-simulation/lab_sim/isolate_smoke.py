"""Scripted isolate-driven episode (Phase 3): one agent ("eng1", role
engineer) runs the ``walk_pipeline`` program end to end through a real
``Host``, requesting access when denied. Used by
``verify_isolate_equivalence.py`` to prove MockIsolate/SubprocessIsolate
agreement, and to produce the Phase 3 timing benchmark recorded in
DESIGN.md.
"""

from __future__ import annotations

import hashlib
import json

from .access import PermissionService
from .agents import AdminPolicy
from .config import AdminConfig
from .isolate_cost import IsolateRunTiming
from .oracle import OracleWorld
from .pipeline_engine import PipelineEngine
from .pipeline_spec import load_spec
from .tools import Host, ToolCall
from .workspace import Workspace


def run_isolate_episode(backend, seed: int, max_ticks: int = 30) -> tuple[dict[str, str], IsolateRunTiming]:
    oracle = OracleWorld(seed=seed)
    ws = Workspace()
    try:
        permissions = PermissionService()
        engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws, permission_service=permissions)
        admin = AdminPolicy(AdminConfig(), permissions)
        host = Host(engine, permissions, admin, roles={"eng1": "engineer"})

        handle = backend.spawn("eng1", seed, "walk_pipeline")
        own_model_id: str | None = None
        observation: dict[str, object] = {
            "t": 0, "own_model_id": None, "completed_steps": [], "last_denied_capability": None,
        }
        for _ in range(max_ticks):
            call = backend.step(handle, observation)
            if call is None:
                break
            result = host.dispatch("eng1", ToolCall(tool=call["tool"], args=call["args"]))
            denied_capability = None
            if call["tool"] == "pipeline.trigger_step":
                if result.ok and own_model_id is None and "model_id" in result.payload:
                    own_model_id = str(result.payload["model_id"])
                elif not result.ok and result.reason == "access_denied":
                    step_id = call["args"]["step_id"]
                    try:
                        denied_capability = engine.spec.step(step_id).requires_capability
                    except KeyError:
                        pass
            admin.tick()
            observation = {
                "t": oracle.t,
                "own_model_id": own_model_id,
                "completed_steps": sorted(engine.completed_steps(own_model_id)) if own_model_id else [],
                "last_denied_capability": denied_capability,
            }
        timing = backend.close(handle)

        digests = {
            "events": host.events.digest(),
            "engine_log": engine.log_digest(),
            "access_log": permissions.digest(),
            "oracle": hashlib.sha256(json.dumps(oracle.snapshot(), sort_keys=True).encode()).hexdigest(),
            "workspace": ws.digest(),
        }
        digests["combined"] = hashlib.sha256(json.dumps(digests, sort_keys=True).encode()).hexdigest()
        return digests, timing
    finally:
        ws.cleanup()
