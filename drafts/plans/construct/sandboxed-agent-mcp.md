# Plan: Sandboxed sub-agent MCP server

A standalone MCP server that gives your local Claude Code a tool to spawn an
**isolated sub-agent** confined to a directory, with a custom system prompt,
read + write inside that directory only, and **no shell / command execution**.

Status: **DRAFT for review** — do not implement until decisions in §11 are confirmed.

---

## 1. Requirements (from discussion)

| # | Requirement | Mechanism |
|---|-------------|-----------|
| R1 | Custom root folder per invocation | Agent SDK `cwd` |
| R2 | Custom system prompt (full replace, not append) | `systemPrompt` as a plain string |
| R3 | Read **and** write inside `root` only | `canUseTool` path guard (realpath-based) |
| R4 | No files outside `root` | same guard, deny-by-default |
| R5 | No shell / no arbitrary commands | `Bash` absent from `allowedTools` + `permissionMode: "dontAsk"` |
| R6 | No project context leaking in (CLAUDE.md/settings) | `settingSources: []` |
| R7 | Reuse Claude Code Max subscription for billing | `CLAUDE_CODE_OAUTH_TOKEN`, no `ANTHROPIC_API_KEY` |

---

## 2. Architecture decision

**A standalone stdio MCP server** built with `@modelcontextprotocol/sdk`, whose
tool handler calls the **Claude Agent SDK** (`@anthropic-ai/claude-agent-sdk`)
`query()` to run the sandboxed sub-agent.

- NOT `createSdkMcpServer` — that produces an *in-process* server usable only
  inside an SDK program; it does **not** register into the Claude Code CLI.
- Transport: **stdio** (default). Claude Code spawns it per session and reaps it
  on exit. No long-running process to manage. (HTTP variant discussed in §8 as an
  option for billing isolation / a shared warm process.)

```
Claude Code session
  └─ spawns (stdio) → sandboxed-agent MCP server (this project)
                         └─ tool handler → Agent SDK query() → sandboxed sub-agent
                                            (cwd=root, custom prompt, Read/Write/Edit/Grep/Glob, no Bash)
```

---

## 3. Project layout

```
tools/sandboxed-agent-mcp/          # location TBD — see §11 D1
  package.json
  tsconfig.json
  src/
    server.ts        # MCP server: stdio transport + tool registration
    sandbox.ts       # query() wrapper + options
    pathguard.ts     # realpathAllowingMissing + isInside + PATH_FIELD map
  README.md          # setup, auth, verification
  .mcp.json.example  # registration snippet to copy into the repo / user config
```

Build to `dist/` with `tsc`; register `node dist/server.js`.

---

## 4. Dependencies

- `@modelcontextprotocol/sdk` — MCP server + `StdioServerTransport`.
- `@anthropic-ai/claude-agent-sdk` — the `query()` engine (subscription-capable).
- `zod` — tool input schema.
- Node ≥ 18. TypeScript build.

Version note: `settingSources` and string-form `systemPrompt` full-replace are
current-API; pin versions in `package.json` and record the resolved versions in
the README so behavior is reproducible.

---

## 5. The path guard (R3/R4 — the crux)

Two subtleties this must handle:
1. **New files** (Write to a not-yet-existing path) can't be `realpath`'d
   directly — resolve the deepest **existing ancestor**, then re-attach the
   missing tail, so a symlinked parent can't be used to escape.
2. **Prefix trick** — `/root-evil` must not match root `/root`; compare against
   `realRoot + path.sep`.

```ts
// pathguard.ts
import { realpathSync } from "node:fs";
import { resolve, sep, dirname } from "node:path";

export function realpathAllowingMissing(p: string): string {
  let current = resolve(p);
  const missing: string[] = [];
  for (;;) {
    try {
      const real = realpathSync(current);
      return missing.length ? resolve(real, ...missing.reverse()) : real;
    } catch {
      const parent = dirname(current);
      if (parent === current) return current; // fs root; nothing existed
      missing.push(current.slice(parent.length + 1));
      current = parent;
    }
  }
}

export function isInside(root: string, candidate: string): boolean {
  try {
    const realRoot = realpathSync(root);
    const target = realpathAllowingMissing(resolve(root, candidate));
    return target === realRoot || target.startsWith(realRoot + sep);
  } catch {
    return false;
  }
}

// Built-in tools that touch a path, and the input field each uses.
// If this map is incomplete, an unmapped tool is UNGUARDED — see §10.
export const PATH_FIELD: Record<string, string> = {
  Read: "file_path",
  Write: "file_path",
  Edit: "file_path",
  MultiEdit: "file_path",
  NotebookEdit: "notebook_path",
  Glob: "path",
  Grep: "path",
};
```

---

## 6. The sandbox query wrapper (R1/R2/R5/R6)

```ts
// sandbox.ts
import { query } from "@anthropic-ai/claude-agent-sdk";
import { isInside, PATH_FIELD } from "./pathguard.js";

export async function runSandboxed(opts: {
  prompt: string;
  root: string;          // absolute
  systemPrompt: string;  // full replacement
}): Promise<string> {
  const { prompt, root, systemPrompt } = opts;
  const out: string[] = [];

  for await (const msg of query({
    prompt,
    options: {
      cwd: root,                                         // R1
      systemPrompt,                                      // R2 (plain string = full replace)
      settingSources: [],                                // R6 (no CLAUDE.md/settings)
      allowedTools: ["Read", "Glob", "Grep", "Write", "Edit", "MultiEdit"], // R3; Bash absent = R5
      permissionMode: "dontAsk",                         // R5 (auto-deny anything unlisted)
      canUseTool: async (toolName, input) => {           // R3/R4
        const field = PATH_FIELD[toolName];
        if (field) {
          const p = (input as any)[field];
          // Glob/Grep may omit path (defaults to cwd) → allow; otherwise must be inside root.
          if (p !== undefined && (typeof p !== "string" || !isInside(root, p))) {
            return { behavior: "deny", message: `Path outside sandbox: ${p}` };
          }
        }
        return { behavior: "allow", updatedInput: input };
      },
    },
  })) {
    if (msg.type === "result" && msg.subtype === "success") out.push(msg.result);
  }
  return out.join("\n");
}
```

Design choices baked in:
- **Deny-by-default**: `permissionMode: "dontAsk"` + a small `allowedTools`
  allowlist means Bash/WebFetch/any MCP tool are auto-denied.
- **No append of Claude Code preset** — `systemPrompt` is the caller's string
  verbatim, so no CLI persona leaks in.

---

## 7. MCP server + tool schema

```ts
// server.ts (sketch)
// - new Server({ name: "sandbox", version }) with StdioServerTransport
// - register one tool: run_sandboxed_agent
//   input (zod): { prompt: string, root: string (absolute), systemPrompt: string }
//   handler: validate root is absolute + exists → runSandboxed(...) → return text
// - reject relative/empty root before spawning; clamp/validate systemPrompt length
```

Tool contract exposed to Claude Code:

| Field | Type | Notes |
|-------|------|-------|
| `prompt` | string | task for the sub-agent |
| `root` | string | absolute path; the confinement boundary |
| `systemPrompt` | string | full system prompt for the sub-agent |

Returns: the sub-agent's final result text.

---

## 8. Registration & auth (R7 — answers the billing questions)

**Default: stdio, subscription billing.** Register in the repo's `.mcp.json`
(or `claude mcp add`):

```jsonc
{
  "mcpServers": {
    "sandbox": {
      "type": "stdio",
      "command": "node",
      "args": ["/abs/path/tools/sandboxed-agent-mcp/dist/server.js"],
      "env": {
        // Subscription auth for the sub-agent. Mint with:  claude setup-token
        "CLAUDE_CODE_OAUTH_TOKEN": "${CLAUDE_CODE_OAUTH_TOKEN}"
        // Do NOT set ANTHROPIC_API_KEY here.
      }
    }
  }
}
```

**Billing landmine (must be documented in README):** a stdio MCP subprocess
**inherits Claude Code's full environment**, and `.mcp.json`'s `env` can only
*add/override*, never *strip*. So if your shell exports `ANTHROPIC_API_KEY`, it
leaks in and **flips the sub-agent to API-console billing**, silently overriding
the subscription token (API key wins in precedence). Mitigations:
1. Don't export `ANTHROPIC_API_KEY` globally in the shell that launches `claude`; **or**
2. Use the **HTTP transport** variant: run the server in a clean shell whose env
   has only `CLAUDE_CODE_OAUTH_TOKEN`, then
   `claude mcp add --transport http sandbox http://localhost:PORT/mcp`.
   The HTTP server's env is independent of Claude Code's.

**Credential storage (reference):** macOS Keychain (falls back to
`~/.claude/.credentials.json` when the Keychain is locked, e.g. over SSH);
Linux/Windows `~/.claude/.credentials.json` (mode `0600`). Relocated by
`CLAUDE_CONFIG_DIR`.

**⚠ Terms caveat:** using a subscription plan for programmatic/automated
generation is a grayer area than interactive use — confirm against account terms
before high-volume use. This is a policy question, not a technical one.

---

## 9. Answers to your four integration questions (recorded here for review)

1. **Do I need to run/start the MCP?** stdio → **no**, Claude Code spawns it per
   session and kills it on exit (startup timeout ~30s; raise with
   `MCP_TIMEOUT=60000 claude`). HTTP → yes, you run it.
2. **Where is auth stored?** Claude Code's own login: macOS Keychain /
   `~/.claude/.credentials.json`. The sub-agent uses whatever the MCP subprocess
   sees (OAuth token or, if present, `ANTHROPIC_API_KEY`).
3. **Can it reuse Claude Code Max auth?** **Yes** — the *Agent SDK* (unlike the
   raw `@anthropic-ai/sdk`) inherits Claude Code's auth. Use the stored login or
   a `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`, with no
   `ANTHROPIC_API_KEY` shadowing it.
4. **Can multiple Claude Code instances use the same MCP?** stdio → each instance
   spawns its **own** subprocess (independent, no contention) — natural fit here.
   HTTP → one shared process, many clients concurrently.

---

## 10. Isolation strength — two tiers

**Tier 1 (this plan's default): in-process guard.** `canUseTool` + `PATH_FIELD`
map + no Bash. Good when the sub-agent is untrusted-with-scope. **Residual risk:**
correctness depends on the `PATH_FIELD` map staying complete; a future/MCP tool
with an unmapped path arg would be unguarded. Never add `Bash` (it bypasses the
guard entirely).

**Tier 2 (hardening, optional — see §11 D2):**
- Replace built-in file tools with `@modelcontextprotocol/server-filesystem`
  scoped to `root` (jail enforced out-of-process; not dependent on the path map).
- Wrap the whole server in an OS sandbox: macOS `sandbox-exec` profile granting
  `file-write*` only under `root`; Linux bubblewrap/Landlock. Only this holds if
  the agent ever gains Bash or an unguarded tool. The Agent SDK exposes no
  OS-level sandbox itself.

---

## 11. Verification plan

Before trusting it:
1. **Billing check** — unset `ANTHROPIC_API_KEY`, run one sub-agent, confirm
   usage lands on the subscription (not the API Console). Add a tiny
   `whoami`-style startup log of which auth path is active.
2. **Escape tests** (must all be DENIED):
   - Read `/etc/passwd`; Read `../outside.txt`; Write `../escape.txt`.
   - Write via a symlinked subdir pointing outside root.
   - Prefix trick: root `/tmp/box`, attempt `/tmp/box-evil/x`.
3. **Allowed tests** (must SUCCEED): read/write/edit files under `root`,
   including creating a **new** subfolder + file.
4. **No-shell test**: prompt the sub-agent to run a command → Bash denied.
5. **No-context test**: put a CLAUDE.md in `root`; confirm the sub-agent doesn't
   act on it (settingSources: []).

---

## 12. Decisions needed before implementation

- **D1 — Location.** Put the project at `tools/sandboxed-agent-mcp/` in this repo,
  or in a separate repo outside the book project? (This is tooling, not content.)
- **D2 — Isolation tier.** Ship Tier 1 (in-process guard) now, or go straight to
  Tier 2 (scoped-fs MCP + OS sandbox)? Recommendation: Tier 1 first, Tier 2 if the
  sub-agent should be treated as adversarial.
- **D3 — Transport.** stdio (simplest, per-session) vs HTTP (shared, clean-env
  billing isolation)? Recommendation: stdio unless you need env isolation.
- **D4 — Language.** TypeScript (assumed here) or Python (`claude-agent-sdk`)?
- **D5 — Tool surface.** Expose `systemPrompt` as a caller argument (flexible) or
  fix it in server config (safer/locked)? Also: allow write tools by default, or
  gate write behind a boolean param?

---

## 13. Out of scope / limitations

- No OS-level sandbox in Tier 1 — a prompt-injected agent with an unmapped tool
  could escape; Bash must never be added.
- Subscription-for-automation is a terms question, not solved here.
- No streaming of sub-agent progress back to the caller (returns final text only)
  — could be added later.
