"""Run a confined sub-agent via claude-agent-sdk query()."""

from __future__ import annotations

from claude_agent_sdk import query
from claude_agent_sdk.types import (
    ClaudeAgentOptions,
    HookContext,
    HookInput,
    HookMatcher,
    ResultMessage,
    SyncHookJSONOutput,
)

from .pathguard import path_field_allowed

READ_TOOLS = ["Read", "Glob", "Grep"]
WRITE_TOOLS = ["Write", "Edit", "MultiEdit"]
MAX_SYSTEM_PROMPT_CHARS = 120_000
MAX_PROMPT_CHARS = 200_000
# Agent SDK JSON transport limit is 1 MiB; block huge Read payloads early.
MAX_READ_FILE_BYTES = 900_000


def validate_invocation(
    *,
    prompt: str,
    root: str,
    system_prompt: str,
) -> None:
    if not prompt.strip():
        raise ValueError("prompt must be non-empty")
    if len(prompt) > MAX_PROMPT_CHARS:
        raise ValueError(f"prompt exceeds {MAX_PROMPT_CHARS} characters")
    if len(system_prompt) > MAX_SYSTEM_PROMPT_CHARS:
        raise ValueError(
            f"system_prompt exceeds {MAX_SYSTEM_PROMPT_CHARS} characters"
        )
    if not root:
        raise ValueError("root must be a non-empty absolute path")
    from pathlib import Path

    root_path = Path(root)
    if not root_path.is_absolute():
        raise ValueError(f"root must be absolute: {root}")
    if not root_path.is_dir():
        raise ValueError(f"root must be an existing directory: {root}")


async def run_sandboxed(
    *,
    prompt: str,
    root: str,
    system_prompt: str,
    allow_write: bool = True,
    max_turns: int = 30,
    model: str | None = None,
) -> str:
    validate_invocation(prompt=prompt, root=root, system_prompt=system_prompt)

    allowed = list(READ_TOOLS)
    if allow_write:
        allowed.extend(WRITE_TOOLS)

    real_root = str(__import__("os").path.realpath(root))

    async def path_guard_hook(
        hook_input: HookInput,
        _tool_use_id: str | None,
        _context: HookContext,
    ) -> SyncHookJSONOutput:
        if hook_input.get("hook_event_name") != "PreToolUse":
            return {"continue_": True}
        tool_name = hook_input["tool_name"]
        tool_input = hook_input["tool_input"]
        ok, msg = path_field_allowed(real_root, tool_name, tool_input)
        if not ok:
            return {
                "continue_": True,
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": msg or "Path outside sandbox",
                },
            }
        if tool_name == "Read":
            from pathlib import Path

            fp = tool_input.get("file_path")
            if isinstance(fp, str):
                candidate = Path(real_root) / fp if not Path(fp).is_absolute() else Path(fp)
                try:
                    if candidate.is_file():
                        size = candidate.stat().st_size
                        if size > MAX_READ_FILE_BYTES:
                            return {
                                "continue_": True,
                                "hookSpecificOutput": {
                                    "hookEventName": "PreToolUse",
                                    "permissionDecision": "deny",
                                    "permissionDecisionReason": (
                                        f"File too large for sandbox Read ({size} bytes)"
                                    ),
                                },
                            }
                except OSError:
                    pass
        return {
            "continue_": True,
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
            },
        }

    tool_matcher = "Read|Glob|Grep|Write|Edit|MultiEdit"
    options = ClaudeAgentOptions(
        cwd=real_root,
        system_prompt=system_prompt,
        setting_sources=[],
        tools=allowed,
        allowed_tools=allowed,
        permission_mode="dontAsk",
        hooks={
            "PreToolUse": [
                HookMatcher(matcher=tool_matcher, hooks=[path_guard_hook]),
            ],
        },
        max_turns=max_turns,
        model=model,
    )

    final: str | None = None
    errors: list[str] = []

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, ResultMessage):
            if message.is_error:
                detail = message.result or message.errors
                raise RuntimeError(f"Sandboxed agent failed: {detail}")
            if message.result is not None:
                final = message.result
            elif message.errors:
                errors.extend(message.errors)

    if final is not None:
        return final
    if errors:
        raise RuntimeError("; ".join(errors))
    return ""
