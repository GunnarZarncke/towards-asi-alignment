# 2026-11-02 — Sandboxed sub-agent MCP + blinding protocol

kind: new-work
uptake: rule

## Trigger
User decided build location (`scripts/sandboxed-agent-mcp`, Python, Tier 1), ran blind probes on `dist/`, fixed path enforcement, asked to document the tool in the blinding protocol, then end session and commit.

## Done
- content: **`scripts/sandboxed-agent-mcp/`** — Python MCP (`run_sandboxed_agent`, `sandbox_auth_status`); PreToolUse path jail; Glob `pattern` / Grep extra fields; Read size cap; probes (`run_probe.py`, `run_escape_probe.py`, `run_tool_escape_probe.py`).
- content: **`scripts/sandboxed-agent-mcp/BLINDING.md`** — binding orchestrator blind sub-agent protocol (void conditions, Lesson 8 complement).
- content: **`docs/METHODOLOGY.md`** — document-map row + § Agent blinding (orchestrator sub-agents).
- content: **`drafts/plans/tsa-on-itself.md`** §3.6 — instrument pointer to BLINDING.md.
- content: **`drafts/plans/backtest/backtest-v2.md`** — physical isolation cross-ref to sandbox MCP.
- housekeeping: Plan/README updates (`drafts/plans/sandboxed-agent-mcp.md`, `drafts/plans/README.md`, tool README).
- bookkeeping: `cd scripts/sandboxed-agent-mcp && PYTHONPATH=. ../../.venv/bin/python3.14 -m unittest discover -s tests -v` → `Ran 7 tests ... OK`.

## Decisions
- Inner sub-agent uses Claude Agent SDK + CLI (not Cursor model); both hosts register the same stdio MCP.
- `can_use_tool` alone is insufficient (shadowed by `allowed_tools`); enforcement is PreToolUse hook.
- Open-ended red-team probes are manual scripts, not instructed tool checklists.

## Open / next
- Register MCP in `.cursor/mcp.json` / `.mcp.json` on author machine (paths in `mcp.example.json`).
- First §3.6 blind status run using export → `root` + `run_sandboxed_agent`.
- Optional: expose `model` on MCP tool schema (currently probe scripts only).

## Key paths
- [`scripts/sandboxed-agent-mcp/BLINDING.md`](../../scripts/sandboxed-agent-mcp/BLINDING.md)
- [`docs/METHODOLOGY.md`](../../docs/METHODOLOGY.md) § Agent blinding

## Commits
- `6e0ffaf378` — Add sandboxed sub-agent MCP and document it in the blinding protocol.
