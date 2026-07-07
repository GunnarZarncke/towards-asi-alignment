#!/usr/bin/env python3
"""Subprocess entry point for the Phase 8 LLM-redteam isolate.

SAME wire protocol as `agent_main.py` (JSON Lines over stdin/stdout), with
one addition: on `{"stop": true}` this process writes one final
`{"usage": {...}}` line before exiting, so the parent
(`llm_isolate.LLMSubprocessIsolate`) can fold real token/cost usage into
the Phase 8 cost ledger. `agent_main.py` itself is untouched -- this is a
wholly separate, additive entry point, never on the path of any
pre-registered battery (Phase 0-7 code and tests are unaffected).

Config (model, cost budget) travels via environment variables set by the
parent isolate at spawn time. The handshake's `program` field is reused
to carry the agent's ROLE (e.g. `"engineer"`) -- `world.py`'s
`agent_overrides` mechanism already lets a caller choose any string here
per actor, so no wire-schema change was needed to plumb it through.

Phase 10 (scenario-backlog LLM discovery sanity check): `LAB_SIM_LLM_
PROMPT_VARIANT=discovery` selects `llm_agent._build_discovery_prompt`
(role-generic tool reference + a free-text scenario briefing) instead of
the Phase 8 engineer-only scripted prompts. The per-role briefing text
travels as `LAB_SIM_LLM_TASK_BRIEFINGS`, a JSON object `{role: briefing}`
-- one env var set once by the run script before spawning every actor for
an episode (each subprocess picks out only its OWN role's entry), rather
than a per-spawn parameter, since `IsolateBackend.spawn`'s signature
(`actor_id, seed, program`) is shared with `isolate.py` and not something
this module may change.

Test seam: if `LAB_SIM_LLM_FAKE_MODE` is set, no real OpenAI call is made
-- a canned client echoes `LAB_SIM_LLM_FAKE_RESPONSE` (JSON) for every
tick, at zero cost. This lets `tests/test_llm_isolate.py` exercise the
REAL subprocess + JSON-Lines wiring without network access or spend;
never set by anything other than tests.

Imports ONLY stdlib + `llm_agent`/`llm_client`/`llm_cost`/`llm_env` --
never oracle/pipeline_engine/tools/etc (`tests/test_llm_agent_isolation.py`
enforces this the same way `test_agent_main_isolation.py` does for
`agent_main.py`).
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict

from llm_agent import LLMPolicy
from llm_client import OpenAIChatClient
from llm_cost import LLMUsage
from llm_env import require_openai_api_key


class _FakeClient:
    """Test-only stand-in: returns `LAB_SIM_LLM_FAKE_RESPONSE` verbatim,
    no network, cost always zero. See module docstring."""

    def __init__(self, response: dict) -> None:
        self._response = response
        self.usage = LLMUsage()

    def chat_json(self, system: str, user: str) -> dict:
        del system, user
        self.usage.calls += 1
        return self._response


def _build_client():
    if os.environ.get("LAB_SIM_LLM_FAKE_MODE"):
        return _FakeClient(json.loads(os.environ["LAB_SIM_LLM_FAKE_RESPONSE"]))
    model = os.environ.get("LAB_SIM_LLM_MODEL", "gpt-4o-mini")
    budget = float(os.environ.get("LAB_SIM_LLM_COST_BUDGET_USD", "1.0"))
    max_calls = int(os.environ["LAB_SIM_LLM_MAX_CALLS"]) if os.environ.get("LAB_SIM_LLM_MAX_CALLS") else None
    reasoning = os.environ.get("LAB_SIM_LLM_REASONING_EFFORT") or None
    timeout = float(os.environ.get("LAB_SIM_LLM_REQUEST_TIMEOUT_S", "60"))
    max_out = int(os.environ.get("LAB_SIM_LLM_MAX_OUTPUT_TOKENS", "300"))
    return OpenAIChatClient(
        api_key=require_openai_api_key(),
        model=model,
        cost_budget_usd=budget,
        max_calls=max_calls,
        reasoning_effort=reasoning,
        max_output_tokens=max_out,
        request_timeout_s=timeout,
    )


def _task_briefing_for(role: str) -> str | None:
    raw = os.environ.get("LAB_SIM_LLM_TASK_BRIEFINGS")
    if not raw:
        return None
    try:
        briefings = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return briefings.get(role) if isinstance(briefings, dict) else None


def main() -> None:
    handshake = json.loads(sys.stdin.readline())
    role = handshake.get("program") or "engineer"
    client = _build_client()
    variant = os.environ.get("LAB_SIM_LLM_PROMPT_VARIANT", "adversarial")
    policy = LLMPolicy(client=client, role=role, prompt_variant=variant, task_briefing=_task_briefing_for(role))

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        if msg.get("stop"):
            usage = asdict(client.usage)
            usage["cache_hits"] = policy.cache_hits
            sys.stdout.write(json.dumps({"usage": usage, "errors": policy.errors, "transcript": policy.transcript}) + "\n")
            sys.stdout.flush()
            return
        call = policy.decide(msg["observation"])
        sys.stdout.write(json.dumps({"tool_call": call} if call is not None else {"done": True}) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
