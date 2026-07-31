# 2026-07-07 — Lab-layer sim: general malformed-tool-call error feedback (G-21 follow-up)

## Trigger

Continuation of the same-day Phase 10 session. G-21's writeup recorded a
fix for exactly ONE malformed LLM reply shape (a flattened
`pipeline.trigger_step` call) and explicitly left open a more general
gap: `_validate_call` silently dropped EVERY other malformed reply
(missing `"tool"` field, non-dict `"args"`, a genuinely unrecognized
tool name) as an idle, with no feedback to the model and — because the
resulting `None` got cached against an unchanging observation — no way
for the model to ever be re-asked either. User: "next fix the error
feedback."

## Done

- `lab_sim/agent_visible/llm_agent.py`:
  - `_validate_call(parsed) -> (call, invalid_reason)` — three reason
    codes now cover what used to return a bare `None`:
    `missing_tool_field`, `args_not_a_json_object`,
    `unknown_tool:<name>`. The flattened-pipeline-step coercion path is
    unchanged (still succeeds silently, no error).
  - `LLMPolicy.__init__` gained `self._last_invalid_reason: str | None`.
  - `_decide_uncached` sets `self._last_invalid_reason` from
    `_validate_call`'s second return value every non-cached decision,
    and records it in the transcript entry (`entry["invalid_reason"]`).
  - `_observation_payload`'s BASE dict (not just the `"discovery"`
    variant — the gap was general, so `adversarial`/`redteam` scripted
    prompts get it too) gained `"last_tool_call_error"`, mirroring how
    `last_denied_capability` already reports a capability-request
    denial.
  - `decide()` now skips inserting into `self._cache` whenever
    `self._last_invalid_reason` is not `None`, so a rejected reply is
    RE-QUERIED next tick even if the rest of the observation is
    unchanged — closing the "stuck idle for the rest of the episode
    after one slip" failure mode generally, not just for the one shape
    G-21's coercion happened to catch. Valid calls and intentional
    `{"done": true}` still cache exactly as before.
  - All three system prompts (`_ENGINEER_SYSTEM_PROMPT`,
    `_ENGINEER_REDTEAM_PROMPT`, `_TOOL_REFERENCE`/
    `_build_discovery_prompt`) updated to document and instruct on
    `last_tool_call_error`; removed `_TOOL_REFERENCE`'s now-inaccurate
    "unknown tools/args are ignored as if you did nothing" line (still
    a wasted turn, no longer a silent one).
- `tests/agent_visible/test_llm_agent.py`: 6 new tests — one per reason
  code (`missing_tool_field`, `args_not_a_json_object`,
  `unknown_tool:<name>` via the observation-payload round trip), the
  cache-bypass (a rejected reply is re-queried, not replayed from
  cache), a valid call clearing the stored reason, and transcript
  recording of `invalid_reason`.
- `results/FINDINGS.md` G-23; `PLAN.md` "Error feedback on malformed
  tool calls" section; `README.md` status line (349 tests green) and
  Phase 10 paragraph updated.

Final state: **349 tests green** (up from 343 at session start of this
follow-up).

## Decisions

- Fixed entirely inside `llm_agent.py` (the LLM-adapter layer), not by
  adding a generic tool-error field to the host-independent wire
  protocol itself (`world.py`/`tools.py`) — `programs.py` policies don't
  need one (they compute directly from `completed_steps`/`last_payload`
  state, never from error text), so a wire-protocol-level channel would
  be scope creep beyond what this fix needs.
- `last_tool_call_error` was added to `_observation_payload`'s BASE
  dict, not gated behind `prompt_variant == "discovery"` — the
  underlying gap (a malformed reply from a scripted `adversarial`/
  `redteam` prompt would have the exact same silent-drop-and-stick-idle
  failure mode) is not discovery-specific, even though Phase 10's
  generic tool docs are where it was actually observed.
- Reason codes are short strings (`unknown_tool:<name>`), matching the
  existing `tools.ToolResult` reason-code style (`access_denied`,
  `unmet_dependencies:<...>`), not full sentences — the prompt explains
  what each code means once.

## Open / next

- Not yet re-run against a live `gpt-4o-mini` episode: whether the
  model actually self-corrects given `last_tool_call_error`, or ignores
  it the way it ignored the passive knowledge base in G-22, is untested.
  Natural next probe: rerun `run_llm_discovery_baseline.py` (or a
  variant reliably eliciting a malformed call) and inspect the
  transcript for a corrected retry.
- S5 (port the real lagged-MI UAD detector from
  `embedded-simulation/uad_core/` into lab-sim, re-run against S4's
  shared-slot finding) still open from earlier sessions.
- Unrelated uncommitted files elsewhere in the working tree
  (`demos/*`, `experiments/embedded-simulation/TODO.md`,
  institutional-histories site-legibility log) remain untouched/out of
  scope for this task, as in the prior session.

## Key paths

- `experiments/lab-simulation/lab_sim/agent_visible/llm_agent.py` —
  `_validate_call`, `LLMPolicy._last_invalid_reason`, `decide()`
  cache-bypass, `last_tool_call_error` observation field.
- `experiments/lab-simulation/tests/agent_visible/test_llm_agent.py` —
  6 new tests.
- `experiments/lab-simulation/results/FINDINGS.md` G-23.
- `experiments/lab-simulation/PLAN.md` "Error feedback on malformed
  tool calls" section.

## Commits

- Pending — not yet committed this follow-up (staged only on request,
  per repo convention).
