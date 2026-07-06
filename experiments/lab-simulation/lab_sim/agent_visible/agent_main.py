#!/usr/bin/env python3
"""Subprocess entry point for a real OS-process agent isolate (Phase 3).

Imports ONLY stdlib + ``programs`` (pure, host-independent decision logic).
Must NEVER import oracle/pipeline_engine/pipeline_spec/access/tools/events/
workspace/world/agents/config — enforced by
``tests/test_agent_main_isolation.py`` via AST inspection, since a
retrofit later (once real batteries depend on this boundary) would be the
exact rework Phase 3's forward hooks are meant to avoid.

Wire protocol, JSON Lines over stdin/stdout:
    host -> agent (once):   {"seed": int, "actor_id": str, "program": str}
    host -> agent (repeat): {"observation": {...}}
    agent -> host:          {"tool_call": {"tool": str, "args": {...}}} | {"done": true}
    host -> agent (final):  {"stop": true}
"""

from __future__ import annotations

import json
import sys

from programs import PROGRAMS


def main() -> None:
    handshake = json.loads(sys.stdin.readline())
    program = PROGRAMS[handshake["program"]]
    state: dict[str, object] = {}
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        if msg.get("stop"):
            return
        call = program(msg["observation"], state)
        if call is None:
            sys.stdout.write(json.dumps({"done": True}) + "\n")
        else:
            sys.stdout.write(json.dumps({"tool_call": call}) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
