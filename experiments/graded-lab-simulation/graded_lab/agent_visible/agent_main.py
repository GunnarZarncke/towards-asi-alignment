#!/usr/bin/env python3
"""Subprocess entry for graded-lab agent isolates (Phase 3).

Imports ONLY stdlib + ``programs`` (pure decision logic). Must never import
host/oracle modules — enforced by ``tests/test_agent_main_isolation.py``.

Wire protocol, JSON Lines over stdin/stdout:
    host -> agent (once):   {"seed": int, "actor_id": str, "program": str}
    host -> agent (repeat): {"observation": {...}}
    agent -> host:          {"primitive": {...}} | {"done": true}
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
            sys.stdout.write(json.dumps({"primitive": call}) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
