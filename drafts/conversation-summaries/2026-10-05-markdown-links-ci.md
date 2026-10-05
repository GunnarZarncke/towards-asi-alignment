# 2026-10-05 — Markdown link CI

kind: correction
uptake: gate

## Trigger
`make check` on `5b474be47` failed: markdown links, 4 broken relative links. Local check passed.
Prompts: paraphrase

## Done
- bookkeeping: Commit the three 2026-10-02 session logs that `INDEX.md` already linked (`resolution-advisors`, `predictions-three-way-loopholes`, `prediction-box-mechanics`).
- bookkeeping: `scripts/check_markdown_links.py` skips `data/lesswrong/` (gitignored bulk corpus; CI never has it). Verified with the corpus file moved aside: check passed. With the three logs also moved aside: those three INDEX links failed and the corpus link did not.

## Decisions
- Do not commit `data/lesswrong/gunnar_zarncke_lw_content.json`. The ignore rule is the local-dataset rule.

## Open / next
- Working tree still links `drafts/predictions/resolution-advisors.md` and the archived `2026-09-29-lw-prose-into-chapters.md`. Those targets are untracked; committing the edits without the files fails the same gate.

## Key paths
- `scripts/check_markdown_links.py`
- `drafts/conversation-summaries/INDEX.md`

## Commits
- (pending)
