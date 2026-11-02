"""Stdio MCP server exposing run_sandboxed_agent (Claude Code + Cursor)."""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer

from .auth_info import auth_summary
from .sandbox import run_sandboxed

server = MCPServer(
    name="sandboxed-agent",
    version="0.1.0",
    instructions=(
        "Spawn an isolated Claude Agent SDK sub-agent confined to `root` with a "
        "custom system prompt. File tools only; no shell. Requires `claude` CLI "
        "on PATH and Claude Code auth (subscription OAuth or API key)."
    ),
)


@server.tool(
    name="sandbox_auth_status",
    description=(
        "Report which Claude auth mode the sub-agent subprocess will likely use "
        "(no secrets). Use before blind runs to avoid accidental API-key billing."
    ),
)
def sandbox_auth_status() -> dict[str, str | bool]:
    return auth_summary()


@server.tool(
    name="run_sandboxed_agent",
    description=(
        "Run a sub-agent with a full-replacement system prompt, cwd=root, and "
        "Read/Glob/Grep plus optional Write/Edit inside root only. Returns final text."
    ),
)
async def run_sandboxed_agent(
    prompt: str,
    root: str,
    system_prompt: str,
    allow_write: bool = True,
    max_turns: int = 30,
) -> str:
    return await run_sandboxed(
        prompt=prompt,
        root=root,
        system_prompt=system_prompt,
        allow_write=allow_write,
        max_turns=max_turns,
    )


def main() -> None:
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
