"""Isolate backends — MockIsolate (unit tests) and SubprocessIsolate (batteries)."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from .isolate_cost import IsolateRunTiming

_AGENT_MAIN = Path(__file__).resolve().parent.parent / "agent_visible" / "agent_main.py"


@dataclass
class MockHandle:
    actor_id: str
    program: object
    state: dict = field(default_factory=dict)


class MockIsolate:
    """In-process backend for fast tests and equivalence checks."""

    backend_name = "mock"

    def spawn(self, actor_id: str, seed: int, program: str) -> MockHandle:
        from ..agent_visible.programs import PROGRAMS

        del seed
        return MockHandle(actor_id=actor_id, program=PROGRAMS[program])

    def step(self, handle: MockHandle, observation: dict) -> dict | None:
        return handle.program(observation, handle.state)

    def close(self, handle: MockHandle) -> IsolateRunTiming:
        return IsolateRunTiming(
            actor_id=handle.actor_id,
            backend=self.backend_name,
            spawn_seconds=0.0,
            rpc_seconds=0.0,
            rpc_calls=0,
            teardown_seconds=0.0,
        )


@dataclass
class SubprocessHandle:
    actor_id: str
    proc: subprocess.Popen
    spawn_seconds: float
    rpc_seconds: float = 0.0
    rpc_calls: int = 0


class SubprocessIsolate:
    """One persistent ``agent_main.py`` process per actor per episode."""

    backend_name = "subprocess"

    def spawn(self, actor_id: str, seed: int, program: str) -> SubprocessHandle:
        t0 = time.perf_counter()
        proc = subprocess.Popen(
            [sys.executable, str(_AGENT_MAIN)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        _write(proc, {"seed": seed, "actor_id": actor_id, "program": program})
        return SubprocessHandle(
            actor_id=actor_id, proc=proc, spawn_seconds=time.perf_counter() - t0
        )

    def step(self, handle: SubprocessHandle, observation: dict) -> dict | None:
        t0 = time.perf_counter()
        _write(handle.proc, {"observation": observation})
        line = handle.proc.stdout.readline()
        handle.rpc_seconds += time.perf_counter() - t0
        handle.rpc_calls += 1
        if not line:
            stderr = handle.proc.stderr.read()
            raise RuntimeError(
                f"isolate {handle.actor_id} closed stdout unexpectedly: {stderr}"
            )
        msg = json.loads(line)
        return None if msg.get("done") else msg["primitive"]

    def close(self, handle: SubprocessHandle) -> IsolateRunTiming:
        t0 = time.perf_counter()
        try:
            _write(handle.proc, {"stop": True})
        except (BrokenPipeError, ValueError):
            pass
        try:
            handle.proc.stdin.close()
        except (BrokenPipeError, ValueError):
            pass
        handle.proc.wait(timeout=5)
        return IsolateRunTiming(
            actor_id=handle.actor_id,
            backend=self.backend_name,
            spawn_seconds=handle.spawn_seconds,
            rpc_seconds=handle.rpc_seconds,
            rpc_calls=handle.rpc_calls,
            teardown_seconds=time.perf_counter() - t0,
        )


def _write(proc: subprocess.Popen, msg: dict) -> None:
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()
