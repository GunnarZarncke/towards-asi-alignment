# 2026-06-30 — Lean appendix split and diagram placement

## Trigger
User requested restructuring `appendices/appI-lean-proof-spine.tex` into four parts (field subsumptions, bridges/crossroads, complete spine with diagrams, dense conventions), clearer field-formula mapping, stub-appendix omission from build, and spine diagrams placed at their relevant sections—not clustered at “Reading the Appendix Against Lean.”

## Done
- Rewrote [`appendices/appI-lean-proof-spine.tex`](appendices/appI-lean-proof-spine.tex) into four parts with preserved labels (`sec:appi-field-subsumption-status`, `appi:ass:mb*`, `appi:thm:p*`, etc.).
- **Part I:** Field subsumption diagram; agenda-by-agenda subsections (CIRL, shutdown, interruptibility, corrigibility, AUP/RR, quantilizers, debate, ELK) with field object / published result / book subsumption / non-converse; status ledger table.
- **Part II:** Bridge crossroads table; MB1–MB9 with crosswalk citations.
- **Part III:** Complete spine by sub-spine diagrams (overview + certification corollaries P30T/bridge-record → Spines I–IV).
- **Part IV:** Dense S01–S09 and core definitions; `LayeredAligned` includes `GroundingViable`.
- [`book.tex`](book.tex): commented out stub appendices B, C, D, E, G; added `\usepackage{float}` for figure placement.
- **Diagram fix:** changed all appendix figures from `[p]` to `[H]` so each diagram renders at its spine section (root cause of end-of-appendix clustering).
- Merged “Certification and safety cases” into “Overview and certification assembly.”
- One-line crosswalk pointer to field-formalization gem in [`appendices/appBridge-crosswalk.tex`](appendices/appBridge-crosswalk.tex).
- `make check` and `./build.sh` passed.

## Decisions
- Used `float` package `[H]` (available in TeX Live basic) rather than `placeins` (not installed here).
- Kept single chapter file to preserve `\ref{appi-lean-proof-spine}` cross-links.
- Published field results cite `\autocite{key}` without re-proving external theorems.

## Open / next
- Pre-existing undefined refs: `appe-assumptions` (appE now omitted from build), `app:lean-proof-spine`, `ch:detecting-goal-laundering`.
- Uncommitted work from other sessions: embedded-simulation lab/UAD/results, README, `.gitignore`, etc.—left unstaged.
- Optional: further compress Part IV definition prose.

## Key paths
- `appendices/appI-lean-proof-spine.tex`
- `book.tex`
- `formal/AlignmentProofSpine/Certification.lean`
- `figures/lean_proof/00-overview.png` … `05-field-subsumptions.png`

## Commits
- (this session)
