"""Non-secret hint about which Claude auth path the sub-agent subprocess will use."""

from __future__ import annotations

import os
from pathlib import Path


def auth_mode() -> str:
    """
    Report likely billing/auth path for the Agent SDK (Claude CLI subprocess).

    API key in the environment overrides subscription OAuth (see README).
    """
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic_api_key"
    if os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"):
        return "claude_code_oauth_token"
    cred = Path.home() / ".claude" / ".credentials.json"
    if cred.is_file():
        return "claude_cli_credentials_file"
    return "claude_cli_login_or_missing"


def auth_summary() -> dict[str, str | bool]:
    return {
        "mode": auth_mode(),
        "anthropic_api_key_set": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "claude_code_oauth_token_set": bool(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")),
    }
