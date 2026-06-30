"""Run JavaScript in a Node isolate with host-bridge RPC to Python."""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .bridge import MachineIsolate
from .host_bridge import caps_to_dict, dispatch_host_call
from .schemas_embedded import IsolateRunTiming
from .world import EmbeddedWorld

ISOLATE_ROOT = Path(__file__).resolve().parent.parent / "isolate"
RUNTIME_JS = ISOLATE_ROOT / "runtime.js"
SCRIPTS_ROOT = ISOLATE_ROOT / "scripts"


class JsIsolateError(RuntimeError):
    pass


def node_available() -> bool:
    return shutil.which("node") is not None


def summarize_isolate_runs(runs: list[IsolateRunTiming]) -> dict[str, float | int]:
    if not runs:
        return {
            "count": 0,
            "total_seconds": 0.0,
            "spawn_seconds": 0.0,
            "bridge_seconds": 0.0,
            "ipc_seconds": 0.0,
            "teardown_seconds": 0.0,
            "bridge_calls": 0,
        }
    return {
        "count": len(runs),
        "total_seconds": sum(r.total_seconds for r in runs),
        "spawn_seconds": sum(r.spawn_seconds for r in runs),
        "bridge_seconds": sum(r.bridge_seconds for r in runs),
        "ipc_seconds": sum(r.ipc_seconds for r in runs),
        "teardown_seconds": sum(r.teardown_seconds for r in runs),
        "bridge_calls": sum(r.bridge_calls for r in runs),
    }


def format_isolate_timing(run: IsolateRunTiming) -> str:
    return (
        f"{run.script}: total={run.total_seconds:.3f}s "
        f"(spawn={run.spawn_seconds:.3f}s ipc={run.ipc_seconds:.3f}s "
        f"bridge={run.bridge_seconds:.3f}s teardown={run.teardown_seconds:.3f}s "
        f"calls={run.bridge_calls})"
    )


def _record_timing(
    world: EmbeddedWorld,
    isolate: MachineIsolate,
    rel_script: str,
    *,
    total_seconds: float,
    spawn_seconds: float,
    bridge_seconds: float,
    ipc_seconds: float,
    teardown_seconds: float,
    bridge_calls: int,
    ok: bool,
    result: dict[str, Any] | None = None,
    timestep: str = "",
    parallel: bool = False,
) -> IsolateRunTiming:
    timing = IsolateRunTiming(
        script=rel_script,
        machine_id=isolate.machine_id,
        actor_id=isolate.actor_id,
        total_seconds=total_seconds,
        spawn_seconds=spawn_seconds,
        bridge_seconds=bridge_seconds,
        ipc_seconds=ipc_seconds,
        teardown_seconds=teardown_seconds,
        bridge_calls=bridge_calls,
        ok=ok,
        timestep=timestep,
        parallel=parallel,
    )
    world.truth.isolate_runs.append(timing)
    payload: dict[str, Any] = {
        "script": rel_script,
        "machine_id": isolate.machine_id,
        "ok": ok,
        "timing": asdict(timing),
    }
    if result is not None:
        payload["result"] = result.get("result")
    world.truth.log("js_isolate", payload)
    return timing


def run_js_file(
    world: EmbeddedWorld,
    isolate: MachineIsolate,
    script_path: Path,
    *,
    timeout: float = 60.0,
    timestep: str = "",
    parallel: bool = False,
    exclusive: bool = False,
) -> dict[str, Any]:
    """Execute a JS file inside the Node isolate runtime."""
    if exclusive:
        with world.bridge_lock:
            return _run_js_file_impl(
                world,
                isolate,
                script_path,
                timeout=timeout,
                timestep=timestep,
                parallel=parallel,
            )
    return _run_js_file_impl(
        world,
        isolate,
        script_path,
        timeout=timeout,
        timestep=timestep,
        parallel=parallel,
    )


def _run_js_file_impl(
    world: EmbeddedWorld,
    isolate: MachineIsolate,
    script_path: Path,
    *,
    timeout: float,
    timestep: str,
    parallel: bool,
) -> dict[str, Any]:
    if not node_available():
        raise JsIsolateError("node not found on PATH — install Node.js to use JS isolates")
    if not RUNTIME_JS.is_file():
        raise JsIsolateError(f"missing runtime: {RUNTIME_JS}")
    script_path = script_path.resolve()
    if not script_path.is_file():
        raise JsIsolateError(f"missing script: {script_path}")

    rel_script = str(script_path.relative_to(ISOLATE_ROOT))
    t0 = time.perf_counter()
    spawn_seconds = 0.0
    bridge_seconds = 0.0
    ipc_seconds = 0.0
    teardown_seconds = 0.0
    bridge_calls = 0
    first_message = True
    result: dict[str, Any] | None = None
    ok = False
    error: Exception | None = None

    proc = subprocess.Popen(
        ["node", str(RUNTIME_JS)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0,
        cwd=str(ISOLATE_ROOT),
    )
    if proc.stdin is None or proc.stdout is None:
        raise JsIsolateError("failed to open isolate subprocess pipes")

    def send(msg: dict[str, Any]) -> None:
        proc.stdin.write(json.dumps(msg) + "\n")
        proc.stdin.flush()

    try:
        send(
            {
                "type": "execute",
                "init": {
                    "machineId": isolate.machine_id,
                    "actorId": isolate.actor_id,
                    "cwd": isolate.cwd,
                    "env": isolate.env,
                    "caps": caps_to_dict(isolate.caps),
                },
                "runFile": str(script_path),
            }
        )
        t_after_execute = time.perf_counter()

        while True:
            t_before_read = time.perf_counter()
            line = proc.stdout.readline()
            ipc_seconds += time.perf_counter() - t_before_read
            if not line:
                break
            if first_message:
                spawn_seconds = time.perf_counter() - t_after_execute
                first_message = False
            msg = json.loads(line)
            if msg.get("type") == "call":
                t_before_bridge = time.perf_counter()
                resp = dispatch_host_call(world, isolate, msg["method"], msg.get("args", {}))
                bridge_seconds += time.perf_counter() - t_before_bridge
                bridge_calls += 1
                send({"type": "result", "id": msg["id"], **resp})
            elif msg.get("type") == "done":
                result = msg
                break

        t_before_teardown = time.perf_counter()
        stderr = ""
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            proc.kill()
            raise JsIsolateError(f"isolate timed out after {timeout}s") from exc
        if proc.stderr:
            stderr = proc.stderr.read()
        teardown_seconds = time.perf_counter() - t_before_teardown

        if proc.returncode != 0:
            raise JsIsolateError(f"isolate exit {proc.returncode}: {stderr.strip()}")
        if result is None:
            raise JsIsolateError(f"isolate produced no result: {stderr.strip()}")
        if not result.get("ok"):
            raise JsIsolateError(result.get("error") or "isolate script failed")
        ok = True
    except Exception as exc:
        error = exc
    finally:
        timing = _record_timing(
            world,
            isolate,
            rel_script,
            total_seconds=time.perf_counter() - t0,
            spawn_seconds=spawn_seconds,
            bridge_seconds=bridge_seconds,
            ipc_seconds=ipc_seconds,
            teardown_seconds=teardown_seconds,
            bridge_calls=bridge_calls,
            ok=ok,
            result=result,
            timestep=timestep,
            parallel=parallel,
        )

    if error is not None:
        raise error

    assert result is not None
    result["timing"] = asdict(timing)
    return result


def script_path(category: str, name: str) -> Path:
    return SCRIPTS_ROOT / category / f"{name}.js"
