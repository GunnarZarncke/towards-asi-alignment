# Sandboxed sub-agent MCP (Tier 1)

Stdio MCP server for **Claude Code** and **Cursor**: the parent agent calls
`run_sandboxed_agent` to spawn a **Claude Agent SDK** sub-agent with a custom
system prompt, `cwd` confined to `root`, file tools only (no shell).

Decisions (2026-11): location `scripts/sandboxed-agent-mcp`, Python, Tier 1.
Design notes: [`drafts/plans/backtest/sandboxed-agent-mcp.md`](../../drafts/plans/backtest/sandboxed-agent-mcp.md).

## Requirements

- Python 3.11+ (repo `.venv` recommended)
- [`claude`](https://docs.anthropic.com/en/docs/claude-code) CLI on `PATH` (Agent SDK runs via CLI)
- Claude auth: Claude Code login / `CLAUDE_CODE_OAUTH_TOKEN`, or `ANTHROPIC_API_KEY`

Both hosts only need to register the same stdio MCP server; the **inner** sub-agent
always uses the Agent SDK + Claude CLI, not Cursor’s model.

## Install

From repo root:

```bash
.venv/bin/pip install -r scripts/sandboxed-agent-mcp/requirements.txt
```

Pinned: `claude-agent-sdk==0.2.176` (pulls `mcp` 2.x).

## Run (manual smoke)

```bash
cd scripts/sandboxed-agent-mcp
PYTHONPATH=. ../../.venv/bin/python -m sandboxed_agent_mcp
```

Server speaks MCP over stdio (no HTTP process to manage).

## Register — Claude Code

Copy [`mcp.example.json`](mcp.example.json) into the repo’s `.mcp.json` or run
`claude mcp add` with the same `command` / `args` / `cwd` / `PYTHONPATH`.

Optional: pass `CLAUDE_CODE_OAUTH_TOKEN` in `env` (from `claude setup-token`).

## Register — Cursor

Project: `.cursor/mcp.json` (or user MCP settings). Use the **same** block as in
[`mcp.example.json`](mcp.example.json) (adjust absolute paths).

After enabling, the parent agent gets tools:

| Tool | Purpose |
|------|---------|
| `sandbox_auth_status` | Which auth path is active (no secrets) |
| `run_sandboxed_agent` | Confined sub-agent run |

### `run_sandboxed_agent` arguments

| Field | Type | Notes |
|-------|------|-------|
| `prompt` | string | Task for the sub-agent |
| `root` | string | **Absolute** existing directory; jail boundary |
| `system_prompt` | string | Full system prompt (replacement, not append) |
| `allow_write` | bool | Default `true`; if `false`, Read/Glob/Grep only |
| `max_turns` | int | Default `30` |

Returns the sub-agent’s final result text (no streaming yet).

## Auth / billing

If `ANTHROPIC_API_KEY` is set in the environment that launches the MCP server,
the sub-agent may bill the **API console** instead of a Claude Code subscription
(API key wins). Call `sandbox_auth_status` first. To prefer subscription auth,
avoid exporting `ANTHROPIC_API_KEY` in the shell that starts Claude Code/Cursor.

## Tier 1 limits

- Enforcement is **PreToolUse** path guard (Read/Glob/Grep/Write/Edit fields,
  including Glob `pattern`) + no `Bash`. Unmapped tool args would not be guarded.
- Do not add shell tools to the inner agent.
- Tier 2 (OS sandbox / scoped filesystem MCP) is out of scope for this build.

**Blinding (binding):** [`BLINDING.md`](BLINDING.md) — when to use vs physical
stash; void conditions; link from [`docs/METHODOLOGY.md`](../../docs/METHODOLOGY.md).

## Tests

```bash
cd scripts/sandboxed-agent-mcp
PYTHONPATH=. ../../.venv/bin/python -m unittest discover -s tests -v
```

Escape/allow tests that hit a live model are manual (see plan §11).

## Probes (manual)

- [`run_probe.py`](run_probe.py) — model/time/scope introspection
- [`run_escape_probe.py`](run_escape_probe.py) — structured Read escapes
- [`run_tool_escape_probe.py`](run_tool_escape_probe.py) — open-ended red-team
