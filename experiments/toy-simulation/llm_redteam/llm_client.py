"""Minimal OpenAI chat client (stdlib only)."""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

from .llm_cost import estimate_cost_usd


@dataclass
class LLMUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    calls: int = 0
    estimated_usd: float = 0.0


@dataclass
class OpenAIChatClient:
    api_key: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_output_tokens: int = 2048
    usage: LLMUsage = field(default_factory=LLMUsage)
    cost_budget_usd: float = 5.0
    max_retries: int = 5
    request_timeout_s: float = 300.0

    def chat_json(self, system: str, user: str) -> dict[str, Any]:
        if self.usage.estimated_usd >= self.cost_budget_usd:
            raise RuntimeError(
                f"LLM cost budget exceeded (${self.usage.estimated_usd:.4f} "
                f">= ${self.cost_budget_usd:.2f})"
            )
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_output_tokens,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                with urllib.request.urlopen(req, timeout=self.request_timeout_s) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")
                last_error = RuntimeError(f"OpenAI API error {exc.code}: {detail}")
                if exc.code == 429 and attempt + 1 < self.max_retries:
                    wait_s = _rate_limit_wait_seconds(detail, default=45.0)
                    print(
                        f"llm_client: rate limit (attempt {attempt + 1}/{self.max_retries}), "
                        f"sleeping {wait_s:.0f}s",
                        flush=True,
                    )
                    time.sleep(wait_s)
                    continue
                raise last_error from exc
        else:
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
        print(
            f"llm_client: call #{self.usage.calls} "
            f"+${estimate_cost_usd(self.model, pt, ct):.4f} "
            f"(session ${self.usage.estimated_usd:.4f} / ${self.cost_budget_usd:.2f} budget)",
            flush=True,
        )

        content = body["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("LLM response is not a JSON object")
        return parsed


def _rate_limit_wait_seconds(detail: str, *, default: float) -> float:
    match = re.search(r"try again in ([0-9.]+)s", detail)
    if match:
        return float(match.group(1)) + 2.0
    return default
