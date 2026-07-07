"""Minimal OpenAI chat client (stdlib only).

Shape adapted from `experiments/lab-simulation/lab_sim/agent_visible/llm_client.py`.
Reimplemented here so the demo has no cross-experiment import and no third-party
dependency: it talks to the chat-completions endpoint with urllib.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from typing import Any


class LLMError(RuntimeError):
    """Raised when the model call fails after retries."""


class OpenAIChatClient:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
        max_output_tokens: int = 400,
        max_retries: int = 4,
        request_timeout_s: float = 45.0,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.max_retries = max_retries
        self.request_timeout_s = request_timeout_s

    def chat_text(self, system: str, user: str) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_output_tokens,
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
        body: dict[str, Any] | None = None
        for attempt in range(self.max_retries):
            try:
                with urllib.request.urlopen(req, timeout=self.request_timeout_s) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")
                last_error = LLMError(f"OpenAI API error {exc.code}: {detail}")
                retryable = exc.code == 429 and "insufficient_quota" not in detail
                if retryable and attempt + 1 < self.max_retries:
                    time.sleep(_rate_limit_wait_seconds(detail, default=15.0))
                    continue
                raise last_error from exc
            except urllib.error.URLError as exc:
                last_error = LLMError(f"Network error contacting OpenAI: {exc}")
                if attempt + 1 < self.max_retries:
                    time.sleep(2.0)
                    continue
                raise last_error from exc
        if body is None:
            assert last_error is not None
            raise last_error

        content = body["choices"][0]["message"]["content"]
        if not content or not str(content).strip():
            raise LLMError("LLM returned empty content")
        return str(content).strip()


def _rate_limit_wait_seconds(detail: str, *, default: float) -> float:
    match = re.search(r"try again in ([0-9.]+)s", detail)
    if match:
        return float(match.group(1)) + 2.0
    return default
