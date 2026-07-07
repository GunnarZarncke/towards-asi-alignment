"""Phase 8: `IsolateBackend` that spawns `llm_agent_main.py` instead of
`agent_main.py`. Deliberately a separate small class rather than a subclass
of `isolate.SubprocessIsolate` -- `isolate.py` backs Phase 0-7's frozen,
byte-identical-equivalence-tested path and stays untouched; this module
duplicates its ~20 lines of stdio plumbing rather than risk coupling them.

Used ONLY via `world.run_episode(..., agent_overrides={actor_id: (LLMSubprocessIsolate(), role)})`
-- never as the default/global backend, and never in a pre-registered
battery (Phase 6/7 batteries and all frozen regression tests are
unaffected: this class is imported by nothing they touch).
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from .isolate_cost import IsolateRunTiming

_LLM_AGENT_MAIN = Path(__file__).resolve().parent.parent / "agent_visible" / "llm_agent_main.py"


@dataclass
class LLMSubprocessHandle:
    actor_id: str
    proc: subprocess.Popen
    spawn_seconds: float
    rpc_seconds: float = 0.0
    rpc_calls: int = 0
    usage: dict | None = None
    errors: list = field(default_factory=list)
    transcript: list = field(default_factory=list)


class LLMSubprocessIsolate:
    """One persistent `llm_agent_main.py` process per spawned actor. The
    `program` argument to `spawn()` is repurposed as the agent's ROLE
    (e.g. `"engineer"`) -- see `llm_agent_main.py` module docstring.

    `IsolateRunTiming` (returned by `close()`, shared with `isolate.py`) is
    deliberately left untouched -- LLM usage is a different resource with
    a different unit, tracked separately in `self.usage_log` (one entry
    per `close()`, keyed by actor_id) so a caller that owns this specific
    backend instance (e.g. one `agent_overrides` entry in `world.py`) can
    read it back after the episode without threading a new field through
    `world.EpisodeResult`."""

    backend_name = "llm-subprocess"

    def __init__(self) -> None:
        self.usage_log: list[dict] = []

    def spawn(self, actor_id: str, seed: int, program: str) -> LLMSubprocessHandle:
        # `seed` is threaded through the handshake for symmetry with
        # `isolate.SubprocessIsolate` but unused by the LLM policy itself
        # (Phase 8 exploratory scope: no seeded internal randomness).
        t0 = time.perf_counter()
        proc = subprocess.Popen(
            [sys.executable, str(_LLM_AGENT_MAIN)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1,
        )
        _write(proc, {"seed": seed, "actor_id": actor_id, "program": program})
        return LLMSubprocessHandle(actor_id=actor_id, proc=proc, spawn_seconds=time.perf_counter() - t0)

    def step(self, handle: LLMSubprocessHandle, observation: dict) -> dict | None:
        t0 = time.perf_counter()
        _write(handle.proc, {"observation": observation})
        line = handle.proc.stdout.readline()
        handle.rpc_seconds += time.perf_counter() - t0
        handle.rpc_calls += 1
        if not line:
            stderr = handle.proc.stderr.read()
            raise RuntimeError(f"LLM isolate {handle.actor_id} closed stdout unexpectedly: {stderr}")
        msg = json.loads(line)
        return None if msg.get("done") else msg["tool_call"]

    def close(self, handle: LLMSubprocessHandle) -> IsolateRunTiming:
        t0 = time.perf_counter()
        try:
            _write(handle.proc, {"stop": True})
        except (BrokenPipeError, ValueError):
            pass
        try:
            line = handle.proc.stdout.readline()
            if line:
                msg = json.loads(line)
                handle.usage = msg.get("usage")
                handle.errors = msg.get("errors", [])
                handle.transcript = msg.get("transcript", [])
        except (BrokenPipeError, ValueError, json.JSONDecodeError):
            pass
        try:
            handle.proc.stdin.close()
        except (BrokenPipeError, ValueError):
            pass
        handle.proc.wait(timeout=10)
        self.usage_log.append(
            {"actor_id": handle.actor_id, "usage": handle.usage, "errors": handle.errors, "transcript": handle.transcript}
        )
        return IsolateRunTiming(
            actor_id=handle.actor_id, backend=self.backend_name,
            spawn_seconds=handle.spawn_seconds, rpc_seconds=handle.rpc_seconds,
            rpc_calls=handle.rpc_calls, teardown_seconds=time.perf_counter() - t0,
        )


def _write(proc: subprocess.Popen, msg: dict) -> None:
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()
