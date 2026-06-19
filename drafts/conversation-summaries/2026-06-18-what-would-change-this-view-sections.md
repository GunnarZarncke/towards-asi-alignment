# 2026-06-18 — Session end: "What Would Change This View" + chapter structure (INSTRUCTIONS)

## Trigger
Integrated chapters lacked explicit "What Would Change This View" sections. User chose Option A (add skimmable disconfirming sections to Ch. 2–10), then asked to adapt `INSTRUCTIONS.md` to be less strict but require such sections for integrated drafts. Session end and commit requested.

## Done
- Added `\section{What Would Change This View}` before summary/conclusion in Ch. 2, 4, 6, 7, 8, 9 (short lead + 5–6 disconfirming bullets each).
- Renamed existing equivalents in Ch. 3 and Ch. 10 to the canonical title (content kept; labels unchanged).
- **`INSTRUCTIONS.md` §10** — Renamed "Chapter Template" → "Chapter Structure"; defined **required elements** (including mandatory "What Would Change This View") plus **Shape A** (scaffold) and **Shape B** (integrated drafts keep native structure).
- Conversation log and `INDEX.md` updated.
- `./build.sh` succeeds (**308 pages**, was 303).

## Decisions
- Exact section title "What Would Change This View" for book-level consistency; Ch. 3/10 renamed rather than duplicated.
- Bullets target each chapter's central claim only; surgical additions, no surrounding prose rewrites.
- Session commit stages chapter edits, `INSTRUCTIONS.md`, and logs only; leaves unstaged unrelated edits in `README.md`, `ch40-lethality-stress-test-open-issues.tex`, and `2026-06-17-ch03-dynamical-guarantee-draft.md`.

## Open / next
- TODO (deferred): **book-level epistemic-status pass** — standardize depth of disconfirming sections across all chapters; add "What Would Change This View" to Ch. 1; revisit stub chapters in Part III+.
- Ch. 5 remains the main Part I item still partial.
- Branch is ahead of `origin/main` (prior Ch. 4–10 commits + this one); push when ready.

## Key paths
- `chapters/ch02-artificial-civilization.tex` through `ch10-strategic-opacity.tex`
- `INSTRUCTIONS.md` §10
- `drafts/conversation-summaries/INDEX.md`

## Commits
- `09cafdf` Add disconfirming sections to Ch. 2–10 and relax chapter structure rules.
