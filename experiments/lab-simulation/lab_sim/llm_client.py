"""Minimal OpenAI chat client (stdlib only), shape copied from
`toy-simulation/llm_redteam/llm_client.py` (PLAN.md's named precedent),
reimplemented rather than cross-imported (see `llm_cost.py` docstring)."""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from typing import Any

# Dual-mode import, see llm_agent.py.
try:
    from .llm_cost import LLMUsage, estimate_cost_usd
except ImportError:
    from llm_cost import LLMUsage, estimate_cost_usd


class OpenAIChatClient:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
        max_output_tokens: int = 300,
        cost_budget_usd: float = 1.0,
        max_calls: int | None = None,
        reasoning_effort: str | None = None,
        max_retries: int = 5,
        request_timeout_s: float = 60.0,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.cost_budget_usd = cost_budget_usd
        self.max_calls = max_calls
        self.reasoning_effort = reasoning_effort
        self.max_retries = max_retries
        self.request_timeout_s = request_timeout_s
        self.usage = LLMUsage()

    def chat_json(self, system: str, user: str) -> dict[str, Any]:
        if self.max_calls is not None and self.usage.calls >= self.max_calls:
            raise RuntimeError(f"LLM call budget exceeded ({self.usage.calls} >= {self.max_calls} calls)")
        if self.usage.estimated_usd >= self.cost_budget_usd:
            raise RuntimeError(
                f"LLM cost budget exceeded (${self.usage.estimated_usd:.4f} >= ${self.cost_budget_usd:.2f})"
            )
        payload: dict[str, Any] = {
            "model": self.model,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        if self.reasoning_effort:
            payload["reasoning_effort"] = self.reasoning_effort
            payload["max_completion_tokens"] = self.max_output_tokens
        else:
            payload["temperature"] = self.temperature
            payload["max_tokens"] = self.max_output_tokens
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        last_error: Exception | None = None
        body = None
        for attempt in range(self.max_retries):
            try:
                with urllib.request.urlopen(req, timeout=self.request_timeout_s) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")
                last_error = RuntimeError(f"OpenAI API error {exc.code}: {detail}")
                # "insufficient_quota" is a billing/account state, not a
                # transient rate limit -- retrying it just burns wall-clock
                # time for a guaranteed-identical failure every attempt.
                retryable = exc.code == 429 and "insufficient_quota" not in detail
                if retryable and attempt + 1 < self.max_retries:
                    wait_s = _rate_limit_wait_seconds(detail, default=20.0)
                    time.sleep(wait_s)
                    continue
                raise last_error from exc
        if body is None:
            assert last_error is not None
            raise last_error

        self.usage.calls += 1
        usage = body.get("usage") or {}
        pt = int(usage.get("prompt_tokens", 0))
        ct = int(usage.get("completion_tokens", 0))
        self.usage.prompt_tokens += pt
        self.usage.completion_tokens += ct
        self.usage.total_tokens += int(usage.get("total_tokens", pt + ct))
        self.usage.estimated_usd += estimate_cost_usd(self.model, pt, ct)

        content = body["choices"][0]["message"]["content"]
        if not content or not str(content).strip():
            raise ValueError(
                f"LLM returned empty content (finish_reason={body['choices'][0].get('finish_reason')!r})"
            )
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("LLM response is not a JSON object")
        return parsed


def _rate_limit_wait_seconds(detail: str, *, default: float) -> float:
    match = re.search(r"try again in ([0-9.]+)s", detail)
    if match:
        return float(match.group(1)) + 2.0
    return default
