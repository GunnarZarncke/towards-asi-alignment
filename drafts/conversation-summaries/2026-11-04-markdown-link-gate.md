# 2026-11-04 — Markdown-link gate

kind: correction
uptake: gate

## Trigger
Check on `origin/main` (`cdf504c3da`) failed again, and only on markdown links: 11 broken relative links. The other rows passed. The user asked to split that gate and add the guards discussed.
Prompts: paraphrase

## Done
- content: `scripts/check_markdown_links.py` — a broken link with both ends under `drafts/` is printed and does not fail. Any other broken link fails unless `scripts/markdown-link-baseline.txt` lists `source<TAB>target`. A baseline line whose link is gone fails. A baselined link fails when this run's diff adds or edits its line (`HEAD^` on a clean checkout, `HEAD` when the worktree is dirty, staged diff for `--staged`).
- content: Baseline holds the untracked `papers/alignment-frames/` link and four `metadata/TODO.md` links to untracked drafts already on `HEAD`.
- content: Corrected `BLINDING.md` relative paths in `HANDOFF.md`, `drafts/plans/backtest/backtest-v2.md`, and `2026-11-02-sandboxed-agent-mcp-blinding.md`.
- content: `scripts/archive_conversation_summaries.py` indexes and moves git-tracked logs only.
- content: `.githooks/pre-commit` runs `check_markdown_links.py --staged` and blocks the commit on a new blocking link. Attribution stays fail-open. Check workflow fetches the parent commit (`fetch-depth: 2`).

## Decisions
- Draft-to-draft debt stays visible and non-blocking. The recurring red row was that class.
- Links from outside `drafts/` stay blocking, including `metadata/TODO.md` and `papers/README.md`. Already-committed ones are baselined. A new one fails.
- Do not baseline the uncommitted `papers/README.md` rows. Those files are not on `HEAD`, so a baseline line would be stale on the next push that omits them.

## Open / next
- `papers/README.md` (uncommitted) links `alignment-frames/alignment-frames.tex`, `alignment-frames/alignment-frames.pdf`, and `drafts/alignment-frames-spinout-paper.md`. None of those targets are tracked. Full `make check` fails on those three until the targets are committed or the links are removed. `--staged` does not see them while they stay unstaged.
- When `papers/alignment-frames/` or a baselined TODO target is committed, delete that baseline line in the same commit.

## Key paths
- `scripts/check_markdown_links.py`
- `scripts/markdown-link-baseline.txt`
- `scripts/archive_conversation_summaries.py`
- `.githooks/pre-commit`

## Verification
- Clean checkout of `HEAD` (`569020af8e`) plus this gate: `Markdown link check passed. 9 draft-to-draft link(s) not blocking; 5 baselined.` Exit 0.
- Extra baseline line: `1 stale baseline line(s)`. Exit 1.
- Space added on the baselined paper link: `BLOCK (baseline, but this diff edits the line) drafts/plans/construct/construct.md:40`. Exit 1.
- `README.md` link to `nope.md`: `BLOCK README.md:102: nope.md`. Exit 1.
- This working tree: `3 blocking broken link(s)`, all in uncommitted `papers/README.md`.
