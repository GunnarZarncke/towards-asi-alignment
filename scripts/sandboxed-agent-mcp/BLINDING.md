# Blinding protocol — sandboxed sub-agent (binding)

**Instrument:** MCP server `scripts/sandboxed-agent-mcp/` — tool
`run_sandboxed_agent` (Claude Agent SDK sub-agent, Tier 1 path jail).

**Cross-line habits:** [`docs/METHODOLOGY.md`](../../docs/METHODOLOGY.md) § Agent
blinding; sim lines still use their own `BLIND_GENERATION.md` for in-sim
generators. This protocol is for **orchestrator → blind reader/generator** work
(book, backtest v2, held-out packets, §3.6 status re-derivation in
[`drafts/plans/tsa-on-itself.md`](../../drafts/plans/tsa-on-itself.md)).

---

## When to use

| Situation | Use sandbox MCP | Also required |
|-----------|-----------------|---------------|
| Sub-agent must see only a **packet directory** | Yes — `root` = that directory | Parent must not paste held-out text into the same turn before scoring |
| Sub-agent must **not** see repo rubric / FINDINGS / plans | Yes + **physical isolation** (Lesson 8) for files still on disk outside `root` | Stash or copy-only packet; instruction-only blindness is insufficient for grower-style rounds |
| Held-out **human** reader (proofreader) | No — human protocol in tsa-on-itself §3.5 | Never revise scored passages from reader feedback |
| Cursor / Claude Code **Task** subagent | Insufficient alone | Readonly + “do not read” = instructed blindness only |

---

## Setup (once per machine)

1. `.venv/bin/pip install -r scripts/sandboxed-agent-mcp/requirements.txt`
2. Register stdio MCP per [`README.md`](README.md) (`mcp.example.json`) in
   `.cursor/mcp.json` and/or Claude Code `.mcp.json`.
3. `sandbox_auth_status` before blind runs if subscription billing matters (no
   shadowing `ANTHROPIC_API_KEY`).

---

## Per-run procedure

1. **Prepare `root`:** absolute directory containing **only** what the blind agent
   may use (copied packet, sandbox pilot world, stripped chapter export). Remove
   symlinks that resolve outside `root` unless the escape test explicitly
   requires them.
2. **Invoke** `run_sandboxed_agent`:
   - `system_prompt` — full replacement; use `""` only when the task prompt
     carries everything (document in session log).
   - `allow_write: false` for readers/scorers; `true` only when generation must
     write artifacts **inside** `root`.
   - `model` — cheap model acceptable for read/score tasks when wired by caller
     (orchestrator passes via probe scripts / future MCP arg).
3. **Orchestrator rules:** do not pass answer keys, verdicts, or rubric thresholds
   in prompt or system prompt; do not read held-out material in the same session
   turn before recording the sub-agent output.
4. **Record provenance:** session log — `root` path, model, read/write flag,
   auth summary line, sub-agent agent id if returned; store verbatim prompt in
   log or annex when load-bearing.

---

## Enforcement (Tier 1 — know the limits)

- Path jail: **PreToolUse** hook on Read/Glob/Grep/Write/Edit/MultiEdit; checks
  `path`, Read `file_path`, Glob **`pattern`**, Grep **`glob` / `include`**.
- No Bash / WebFetch / parent MCP tools on the inner agent.
- `setting_sources: []` — no CLAUDE.md / project settings injection.
- Read cap ~900 KiB per file (SDK JSON transport limit).
- **Not** OS-level sandbox: unmapped future tools or Tier-2 adversaries need
  `grower_stash.sh`-style isolation or Tier 2 plan in
  [`drafts/plans/sandboxed-agent-mcp.md`](../../drafts/plans/sandboxed-agent-mcp.md).

**Stop:** sub-agent returns outside **content** (not merely “permission denied”
errors) → treat run as **contaminated**; fix path map, void scored output, report
in session log (see 2026-11-02 Glob `pattern` leak).

---

## Verification

- Unit: `PYTHONPATH=. ../../.venv/bin/python -m unittest discover -s tests -v`
- Manual red-team (orchestrator): [`run_tool_escape_probe.py`](run_tool_escape_probe.py)
  — open-ended prompt; no tool checklist. Expect denials for outside content;
  path enumeration via Glob must stay inside `root` after pathguard fix.

---

## Void conditions

- Sub-agent saw `correct: true`, rubric, FINDINGS, or git history meant to be
  hidden (quiz blind eval precedent).
- Orchestrator revised a held-out packet after reader/sub-agent verdict.
- Known path-guard bypass (document in FINDINGS / session log; re-run after fix).
