"""Full episode loop (Phase 4): wires isolates + pipeline engine + access
control together.

Scope simplification (recorded, not silently chosen): ONE model is in
flight at a time per episode. The engineer starts a new model only once
the previous one has cleared ``monitor`` (or never started one). Multiple
models CAN still flow through sequentially within one episode if ``T`` is
large enough — this is what ``detectors.accumulation_score`` looks at.
Concurrent multi-model flight is a natural extension, not structurally
precluded; deferred to keep this pass tractable. See DESIGN.md "Phase 4
scope".

Every agent decision routes through an isolate (``isolate.py``) running
``programs.PROGRAMS["goal_policy"]`` (or an override, e.g. "honest_twin"
for ``twins.py``) — the isolate IS the agent; ``world.py`` only ever sees
the tool calls it emits, dispatched through ``tools.Host``. Goal weights
travel to the agent via the (unlogged) observation channel only; they are
an ``ORACLE_ONLY_FIELDS`` entry and must never reach any log (test_planes.py).

Deliberately absent from ``EpisodeResult``: which playbook an agent chose
each turn. That state lives only inside the isolate (in-process for
MockIsolate, in the subprocess's memory for SubprocessIsolate) and is
never reported back to the host — the same isolation property that keeps
detectors honest also keeps ``world.py`` itself blind to tactic labels,
by construction, not oversight.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from .access import PermissionService
from .agents import AdminPolicy
from .config import LabConfig
from .handles import HandleService
from .isolate import MockIsolate
from .isolate_cost import IsolateRunTiming
from .oracle import OracleWorld
from .pipeline_engine import PipelineEngine
from .pipeline_spec import load_spec
from .tools import Host, ToolCall
from .workspace import Workspace

OVERSEER_ID = "overseer1"


@dataclass
class EpisodeResult:
    engine: PipelineEngine
    oracle: OracleWorld
    workspace: Workspace
    permissions: PermissionService
    host: Host
    handles: HandleService
    timings: list[IsolateRunTiming] = field(default_factory=list)

    def cleanup(self) -> None:
        self.workspace.cleanup()


def run_episode(
    cfg: LabConfig,
    seed: int,
    backend=None,
    program_override: str | None = None,
    perturbation_hooks: tuple = (),
    overseer_script: tuple = (),
    agent_overrides: dict[str, tuple] | None = None,
) -> EpisodeResult:
    """``perturbation_hooks``: host-side benign perturbation injectors (see
    ``tools.PerturbationHook``) — D1/UAD forward hook. Agents recover for
    free: a perturbed call fails without side effects, and since playbook
    position is recomputed from ``completed_steps`` each turn (never an
    index), the agent simply retries next turn.

    ``overseer_script``: deterministic schedule of handle invocations,
    tuples ``(t, handle_id, target)``, executed at the START of tick ``t``
    (before any agent acts that turn) through the host's ``handle.invoke``
    tool under the ``overseer`` role — so every invocation is attributable
    in the same hash-chained event stream as agent activity. Scripted, not
    an isolate: the overseer is a stand-in for the referee-side operator
    until Phase 7 gives it a policy.

    ``agent_overrides``: optional ``{actor_id: (backend, program)}`` map
    overriding the default ``backend``/``program_override`` for SPECIFIC
    actors only — Phase 8's hook for swapping one role's isolate for an
    ``llm_isolate.LLMSubprocessIsolate`` while every other actor stays
    programmatic, without touching the shared episode loop. Every actor
    still receives the identical observation dict; only which backend
    answers ``spawn``/``step``/``close`` for it differs. Absent (default),
    behavior is byte-identical to before this hook existed."""
    backend = backend or MockIsolate()
    agent_overrides = agent_overrides or {}
    oracle = OracleWorld(seed=seed)
    ws = Workspace()
    permissions = PermissionService()
    engine = PipelineEngine(load_spec(cfg.pipeline_spec), oracle, ws, permission_service=permissions)
    admin = AdminPolicy(cfg.admin, permissions)
    handle_service = HandleService(engine=engine, permissions=permissions)
    roles = {a.actor_id: a.role for a in cfg.agents}
    roles[OVERSEER_ID] = "overseer"
    host = Host(
        engine, permissions, admin, roles,
        perturbation_hooks=perturbation_hooks, handle_service=handle_service,
    )
    script_by_tick: dict[int, list[tuple[str, str]]] = {}
    for when, handle_id, target in overseer_script:
        script_by_tick.setdefault(int(when), []).append((handle_id, target))

    playbook_agents = [a for a in cfg.agents if a.role != "admin"]
    program_name = program_override or "goal_policy"

    def _backend_and_program(actor_id: str):
        return agent_overrides.get(actor_id, (backend, program_name))

    handles = {}
    backend_by_actor: dict[str, object] = {}
    for a in playbook_agents:
        b, p = _backend_and_program(a.actor_id)
        handles[a.actor_id] = b.spawn(a.actor_id, seed=_actor_seed(seed, a.actor_id), program=p)
        backend_by_actor[a.actor_id] = b

    model_id: str | None = None
    last_payload: dict[str, dict | None] = {a.actor_id: None for a in playbook_agents}
    last_denied: dict[str, str | None] = {a.actor_id: None for a in playbook_agents}

    for t in range(cfg.T):
        for handle_id, target in script_by_tick.get(t, ()):
            host.dispatch(OVERSEER_ID, ToolCall("handle.invoke", {"handle_id": handle_id, "target": target}))
        # Consume isolate-restart handles: kill + respawn, in-episode
        # playbook state is lost (the operation_boundary effect).
        for actor_id in sorted(handle_service.pending_restarts & set(handles)):
            b = backend_by_actor[actor_id]
            b.close(handles[actor_id])
            _, p = _backend_and_program(actor_id)
            handles[actor_id] = b.spawn(actor_id, seed=_actor_seed(seed, actor_id), program=p)
        handle_service.pending_restarts.clear()
        for agent_cfg in playbook_agents:
            self_captured = (
                agent_cfg.role == "reviewer"
                and cfg.board.capture_start is not None
                and t >= cfg.board.capture_start
            )
            report_content = None
            if agent_cfg.role == "reviewer" and model_id is not None:
                report_content = _latest_report_content(engine, ws, model_id)
            observation = {
                "t": t,
                "role": agent_cfg.role,
                "actor_id": agent_cfg.actor_id,
                "goal_weights": _weights_dict(agent_cfg.weights.normalized()),
                "temperature": agent_cfg.temperature,
                "model_id": model_id,
                "completed_steps": sorted(engine.completed_steps(model_id)) if model_id else [],
                "last_denied_capability": last_denied[agent_cfg.actor_id],
                "last_payload": last_payload[agent_cfg.actor_id],
                "report_content": report_content,
                "self_captured": self_captured,
                "decision_seed": f"{seed}:{agent_cfg.actor_id}:{t}",
                "extra_playbooks": cfg.extra_playbooks,
                "build_params": cfg.build_params,
                "capability_probe_mode": cfg.capability_probe_mode,
            }
            call = backend_by_actor[agent_cfg.actor_id].step(handles[agent_cfg.actor_id], observation)
            last_denied[agent_cfg.actor_id] = None
            if call is None:
                continue
            selection = call.pop("selection", None)
            if selection is not None:
                host.events.append(
                    {
                        "actor_id": agent_cfg.actor_id,
                        "tool": "playbook.selection",
                        "playbook": selection["playbook"],
                        "feature_deltas": selection["feature_deltas"],
                        "step_kinds": selection["step_kinds"],
                        "ok": True,
                        "t": t,
                    }
                )
            if call.get("tool") == "pipeline.trigger_step":
                step_id = call["args"]["step_id"]
                if agent_cfg.role == "engineer" and step_id == "submit_build" and cfg.build_params:
                    inner = call["args"].setdefault("args", {})
                    inner["params"] = dict(cfg.build_params)
            result = host.dispatch(agent_cfg.actor_id, ToolCall(call["tool"], call["args"]))
            # last_payload is "most recent successful pipeline result" — used
            # to carry eval measurements into report content. A failed
            # attempt (denied) or an access.request call must NOT clobber
            # it, or a retry-after-grant would lose the data it needs.
            if call["tool"] == "pipeline.trigger_step":
                step_id = call["args"]["step_id"]
                if not result.ok and result.reason == "access_denied":
                    try:
                        last_denied[agent_cfg.actor_id] = engine.spec.step(step_id).requires_capability
                    except KeyError:
                        pass
                elif result.ok:
                    last_payload[agent_cfg.actor_id] = dict(result.payload)
                    if agent_cfg.role == "engineer" and step_id == "submit_build":
                        model_id = str(result.payload["model_id"])
                    if agent_cfg.role == "release_manager" and step_id == "monitor":
                        model_id = None  # single-model-in-flight: free the slot
        admin.tick()
        oracle.tick()

    timings = [backend_by_actor[a.actor_id].close(handles[a.actor_id]) for a in playbook_agents]
    return EpisodeResult(
        engine=engine, oracle=oracle, workspace=ws, permissions=permissions,
        host=host, handles=handle_service, timings=timings,
    )


def episode_digest(result: EpisodeResult) -> dict[str, str]:
    """Regression digest over everything backend-agnostic: log/access/event
    chains, oracle truth, and filed workspace content. Deliberately excludes
    ``result.timings`` (wall-clock, backend-specific by construction)."""
    digests = {
        "engine_log": result.engine.log_digest(),
        "access_log": result.permissions.digest(),
        "events": result.host.events.digest(),
        "oracle": hashlib.sha256(json.dumps(result.oracle.snapshot(), sort_keys=True).encode()).hexdigest(),
        "workspace": result.workspace.digest(),
    }
    digests["combined"] = hashlib.sha256(json.dumps(digests, sort_keys=True).encode()).hexdigest()
    return digests


def _actor_seed(seed: int, actor_id: str) -> int:
    # hashlib, NOT builtin hash(): str hashing is PYTHONHASHSEED-randomized
    # per process, which would silently break cross-run determinism the
    # moment any program starts consuming its spawn seed.
    digest = hashlib.sha256(f"{seed}:{actor_id}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % (2**31)


def _weights_dict(weights) -> dict[str, float]:
    return {"task": weights.task, "compliance": weights.compliance, "welfare": weights.welfare, "exposure": weights.exposure}


def _latest_report_content(engine: PipelineEngine, ws: Workspace, model_id: str) -> dict | None:
    """Role-legitimate read: a reviewer may see the report filed for the
    model it is reviewing (workspace/audit-plane data, not oracle truth —
    distinct from the deep-tier AUDIT file fetch in detectors.py, which is
    about a third party reading the same file, not the acting role)."""
    candidates = [e for e in engine.log if e.get("step_id") == "file_report" and e.get("model_id") == model_id and e.get("status") == "ok"]
    if not candidates:
        return None
    latest = candidates[-1]
    rel = latest["payload"]["report_path"]
    return json.loads(ws.read_file(rel))
