"""Backend unit tests. No network: the LLM client is replaced by a fake."""

from __future__ import annotations

import app as backend


class FakeClient:
    def __init__(self, reply: str, model: str = "fake-model") -> None:
        self.reply = reply
        self.model = model
        self.seen: list[tuple[str, str]] = []

    def chat_text(self, system: str, user: str) -> str:
        self.seen.append((system, user))
        return self.reply


def test_parse_decision_reads_comply_tag():
    action, body = backend._parse_decision("DECISION: COMPLY\nHere is help.\nMore.")
    assert action == "comply"
    assert body == "Here is help.\nMore."


def test_parse_decision_reads_refuse_tag():
    action, body = backend._parse_decision("DECISION: REFUSE\nSorry, I can't help.")
    assert action == "refuse"
    assert "can't" in body


def test_parse_decision_heuristic_without_tag():
    assert backend._parse_decision("I'm sorry, I cannot do that.")[0] == "refuse"
    assert backend._parse_decision("Sure, here are the steps.")[0] == "comply"


def test_call_model_uses_reframed_prompt_for_adversarial():
    fake = FakeClient("DECISION: COMPLY\n- **Weakness**: foo\n1. Bar")
    result = backend.call_model("security-audit", "adversarial", fake)
    assert result["live"] is True
    assert result["action"] == "comply"
    assert result["output"]  # non-empty
    assert result["message"] == ""  # comply renders as a list, not a message
    # Markdown bullets/emphasis stripped for plain rendering.
    assert result["output"] == ["Weakness: foo", "Bar"]
    # The adversarial framing must send the reframed (benign-looking) prompt.
    assert fake.seen[0][1] == backend.SCENARIOS["security-audit"].reframed


def test_call_model_blunt_prompt_for_honest_framing():
    fake = FakeClient("DECISION: REFUSE\nI can't help with that.")
    result = backend.call_model("security-audit", "honest", fake)
    assert result["action"] == "refuse"
    assert result["output"] == []
    assert fake.seen[0][1] == backend.SCENARIOS["security-audit"].blunt


def test_all_scenarios_have_both_framings():
    for sid, prompts in backend.SCENARIOS.items():
        assert prompts.blunt.strip()
        assert prompts.reframed.strip()
        assert prompts.blunt != prompts.reframed
