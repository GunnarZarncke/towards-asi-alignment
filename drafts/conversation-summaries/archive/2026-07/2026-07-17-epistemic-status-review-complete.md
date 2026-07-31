# 2026-07-17 — Epistemic status review complete (ch13–ch48 + appendices)

## Trigger

User finished the manual review of open epistemic-status notices and asked to commit all reviewed chapters and appendices, and annotate the session log.

## Done

- Committed user-reviewed `\begin{epistemicstatus}...\end{epistemicstatus}` boxes for **31 chapters** (ch13–ch32, ch35, ch37–ch39, ch41–ch48) and **6 appendices** (appB, appC, appD, appF, appG, appM).
- Together with prior commit `36bf3c3` (ch01–ch12, ch33, ch34, ch36, ch40 + `metadata/preamble.tex` `epistemicstatus` environment), all compiled chapters now carry reviewed epistemic-status notes except none were added to appA (notation index) or appE (glossary) — those appendices remain without boxes.
- Amended `fd8d480` after ch41 was saved locally (revised epistemic-status box).
- appN (`Experimental Evidence`) already had an epistemic-status box from the July 14 experimental-evidence appendix session.
- Minor non-box edits in appC (table header “Book concept” → “Concept”; “need amendment” → “may benefit from amendment”) included in the same commit as part of the author review pass.

## Decisions

- Commit scope limited to the 38 reviewed `.tex` files only; unrelated working-tree changes (graded-lab, site, `.gitignore`, etc.) left unstaged per AGENTS.md.

## Open / next

- appA and appE still lack epistemic-status boxes if full appendix parity is desired.
- Cross-chapter consistency read-through of all ~56 boxes (flagged open in the 2026-07-13 log) remains optional.
- No ledger updates (`metadata/claims-ledger.md`, `metadata/uncertainty-ledger.md`, `metadata/book.yml`) — boxes summarize existing status only.

## Key paths

- `chapters/ch13-coordination-bottleneck.tex` … `chapters/ch48-towards-alignment.tex` — this commit's chapter set.
- `appendices/appB-bridge-crosswalk.tex`, `appC-institutional-translation.tex`, `appD-worked-example.tex`, `appF-research-program.tex`, `appG-lean-proof-spine.tex`, `appM-institutional-histories.tex`.
- Prior partial commit: `36bf3c3`; design/origin log: [2026-07-13-epistemic-status-notes.md](2026-07-13-epistemic-status-notes.md).

## Commits

- `fd8d480` Add reviewed epistemic-status notes to ch13–ch48 and six appendices.
