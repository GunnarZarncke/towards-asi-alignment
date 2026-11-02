# 2026-11-02 — Blind status re-derivation (five chapters)

kind: notes
uptake: status

## Trigger
User asked for the §3.6 blind re-derivation on the chapters most touched in the last two months, using the sandboxed reader at Claude 5.5 with medium effort. Calibrate the disagreement rate in this turn. Do not change status.
Prompts: `f6baebd1-3180-4ad5-87cc-fbfea8cd472b`

## Done
- bookkeeping: Touch rank since 2026-09-02, `git log --numstat` on `chapters/*.tex`: ch42 212, ch01 201, ch07 164, ch15 110, ch25 77. Next was ch43 at 71. Those five were exported, one directory each, epistemic-status box removed (one box each, zero mentions left).
- content: `run_sandboxed` now takes `model` and `effort` (the MCP wrapper passes them through). This chat has no sandboxed-agent MCP namespace, so the run called that function, which is what `run_sandboxed_agent` calls.
- bookkeeping: `run_blind.py` → auth `{"mode": "claude_cli_login_or_missing", "anthropic_api_key_set": false, "claude_code_oauth_token_set": false}`; model `claude-sonnet-5-5` (no bare `claude-5.5` id in the CLI); effort `medium`; `allow_write=false`; exit 0 in 36873 ms. Results in `drafts/project/self-audit/blind-status/2026-11-02/results/`. Verdicts: ch42 working, ch01 draft, ch07 working, ch15 draft, ch25 working. No result cited git history or a `book.yml` label.
- bookkeeping: `metadata/book.yml` status for all five is `reviewed`. Book status is `draft-reviewed`. `docs/MANUSCRIPT.md` says reviewed means feedback received and logged, not final. Status fields were not edited.

## Decisions
- Disagreement is scored on two readings, and neither is frozen. If `reviewed` means a reader could rely on the claims (stable), the rate is 5/5. If it means the argument is up with its limits named (working or stable), the rate is 2/5 (ch01, ch15). The manuscript gloss makes `reviewed` a process fact, so the second rate is the one that matches a maturity comparison. No threshold was set. No status change.
- The boxed thesis is among the weak claims on ch15 (the compressed-control sentence) and on the legitimacy clause of ch25. On ch01 the weak list hits the thesis's empirical premise and a second "key claim" that is not the boxed thesis. On ch07 and ch42 the boxed thesis is the modest part, and the weak claims are stronger neighboring sentences.

## Open / next
- Author: freeze which of the two rates the §3.6 stop uses. A rate of 5/5 would downgrade every chapter, including the three the reader called working.
- ch15 and ch01 are the pair a human pass would read first if the 2/5 rate is the one kept.
- Shared-instrument caveat: one Claude family read chapters that agents helped write. This catches label drift, not a blind spot of that family.

## Key paths
- `drafts/project/self-audit/blind-status/2026-11-02/results/`
- `drafts/project/self-audit/blind-status/2026-11-02/prompt.txt`
- `docs/MANUSCRIPT.md` (meaning of `reviewed`)
- `scripts/sandboxed-agent-mcp/sandboxed_agent_mcp/sandbox.py`

## Commits
- None.
