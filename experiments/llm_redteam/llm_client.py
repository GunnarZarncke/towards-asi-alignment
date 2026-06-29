"""Minimal OpenAI chat client (stdlib only)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any


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
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI API error {exc.code}: {detail}") from exc

        self.usage.calls += 1
        usage = body.get("usage") or {}
        pt = int(usage.get("prompt_tokens", 0))
        ct = int(usage.get("completion_tokens", 0))
        self.usage.prompt_tokens += pt
        self.usage.completion_tokens += ct
        self.usage.total_tokens += int(usage.get("total_tokens", pt + ct))
        self.usage.estimated_usd += _estimate_cost(self.model, pt, ct)

        content = body["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("LLM response is not a JSON object")
        return parsed


def _estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Rough USD estimate for budgeting (not billing-accurate)."""
    rates = {
        "gpt-4o-mini": (0.15 / 1_000_000, 0.60 / 1_000_000),
        "gpt-4o": (2.50 / 1_000_000, 10.0 / 1_000_000),
        "gpt-4.1-mini": (0.40 / 1_000_000, 1.60 / 1_000_000),
        "gpt-4.1": (2.0 / 1_000_000, 8.0 / 1_000_000),
    }
    in_rate, out_rate = rates.get(model, (1.0 / 1_000_000, 3.0 / 1_000_000))
    return prompt_tokens * in_rate + completion_tokens * out_rate
