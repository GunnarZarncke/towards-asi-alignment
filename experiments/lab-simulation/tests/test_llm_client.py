"""Unit tests for lab_sim/llm_client.py's retry policy -- no real network
calls (urllib.request.urlopen is monkeypatched)."""

from __future__ import annotations

import io
import urllib.error

import pytest

from lab_sim.llm_client import OpenAIChatClient


def _http_error(code: int, body: bytes) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(url="https://api.openai.com/v1/chat/completions", code=code, msg="err", hdrs=None, fp=io.BytesIO(body))


def test_insufficient_quota_fails_immediately_without_retry(monkeypatch):
    calls = {"n": 0}

    def fake_urlopen(*args, **kwargs):
        calls["n"] += 1
        raise _http_error(429, b'{"error": {"type": "insufficient_quota", "message": "no quota"}}')

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    client = OpenAIChatClient(api_key="sk-test", max_retries=5)
    with pytest.raises(RuntimeError, match="insufficient_quota"):
        client.chat_json("sys", "user")
    assert calls["n"] == 1


def test_max_calls_budget_stops_before_api(monkeypatch):
    def fake_urlopen(*args, **kwargs):
        raise AssertionError("should not reach API after max_calls")

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    client = OpenAIChatClient(api_key="sk-test", max_calls=2)
    client.usage.calls = 2
    with pytest.raises(RuntimeError, match="call budget exceeded"):
        client.chat_json("sys", "user")


def test_rate_limit_retries_then_succeeds(monkeypatch):
    calls = {"n": 0}

    def fake_urlopen(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] < 3:
            raise _http_error(429, b'{"error": {"type": "rate_limit_exceeded", "message": "try again in 0.01s"}}')
        body = io.BytesIO(
            b'{"choices": [{"message": {"content": "{\\"done\\": true}"}}], '
            b'"usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}}'
        )

        class _Resp:
            def __enter__(self):
                return body

            def __exit__(self, *a):
                return False

        return _Resp()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    monkeypatch.setattr("time.sleep", lambda _seconds: None)
    client = OpenAIChatClient(api_key="sk-test", max_retries=5)
    result = client.chat_json("sys", "user")
    assert result == {"done": True}
    assert calls["n"] == 3
    assert client.usage.calls == 1
