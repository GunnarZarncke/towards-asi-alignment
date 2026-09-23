# 2026-09-23 — Markdown links CI fix

## Trigger
CI `make check` failed on the markdown link gate (16 broken relative links) while local check passed.

## Done
- **`scripts/check_markdown_links.py`:** Skip relative links whose resolved path is gitignored (`git check-ignore`) — generated PDF, concept-graph / symbol-census `.dot` outputs, toy-simulation `results/*.json`, etc. Local dev trees have these after generators run; CI clean checkout does not.
- Verified in a detached worktree (no build artifacts): 16 failures → pass.

## Decisions
- Treat gitignored paths as valid link targets rather than generating graphs/PDF in CI — matches README wording that those files are regenerated locally.

## Open / next
- Remaining consistency-review follow-through on TODO boards (notation, Lean-calibration rule, etc.).
