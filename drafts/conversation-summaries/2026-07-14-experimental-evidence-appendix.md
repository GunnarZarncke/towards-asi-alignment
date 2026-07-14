# 2026-07-14 — Experimental evidence appendix, precise citations, claims-ledger update

## Trigger

User flagged that the four chapter additions from the graded-lab manuscript harvest (ch07, ch11, ch33, ch34) credited the generic method papers (`zarncke2025uad`, `zarncke2025biq`) rather than the specific findings, and asked for: an appendix collecting strong (not every minor) experimental findings by line with positive/negative/ambiguous classification, bidirectional chapter↔finding links, a way to see where in the book/cards evidence has landed, and a claims-ledger update.

## Done

- Added new appendix `appendices/appN-experimental-evidence.tex` ("Experimental Evidence: Findings by Line"), compiled as **Appendix I** (`\input` after `appG-lean-proof-spine` in `book.tex`). Structure: epistemicstatus box on curation/classification confidence; one section per experiment line (agency-detect, toy-simulation, embedded-simulation, goal-agent-simulation, lab-simulation, graded-lab-simulation) with a longtable of ID / Result (Positive/Negative/Ambiguous) / Finding / Landed-in; final "Where Evidence Has Landed" section as the reverse (chapter-first) index, explicitly naming which strong negatives (E-1, GA-2, L-1b, L-4, GL-4, GL-6) are indexed but not yet cited anywhere.
- Each table row has a `\label{finding:<id>}` (e.g. `finding:gl-1`, `finding:t-1`) so chapters cite the specific finding, not just the line's method paper.
- Rewired the four chapter additions from the prior harvest session to cite `Appendix~\ref{appn-experimental-evidence}` plus the specific finding label(s), alongside (not replacing) the existing `\autocite`:
  - ch07 (`finding-boundary`): findings GL-1/GL-2 (`finding:gl-1`–`finding:gl-2`).
  - ch11 (`capability-without-task-ontology`): finding GL-3 (`finding:gl-3`).
  - ch33 (`certification-without-construction`): finding T-1 (`finding:t-1`) — this paragraph previously had **no** citation at all, not just an imprecise one.
  - ch34 (`selection-environment`): finding GL-7 (`finding:gl-7`).
- **Follow-up (same session):** removed the reverse "Where Evidence Has Landed" section; replaced the findings-table "Landed in" column with "Manuscript" pointing to specific chapter \emph{sections} (`Sec.~\ref{sec:...}, Ch.~\ref{ch:...}`); added a per-line experiment description paragraph before each findings table; added Section~\ref{sec:appn-bridge-coverage} with the bridge/feature coverage matrix (from `metadata/experiments.yml`); updated the four chapter citations to also name the appendix section (`Section~\ref{sec:appn-graded-lab-simulation}` etc.).
- Updated `metadata/claims-ledger.md`: added Support bullets to C-003 (boundary/task-ontology — GL-1/GL-2/GL-3), C-006 (successor/certification — T-1), C-007 (selection/basin — GL-7), each pointing at the new appendix and finding label.
- Updated `metadata/experiments.yml`: appended "Cited in chNN … and appendix … (finding X)" to the four headlineFindings strings that now have a manuscript home (toy-sim #1, graded-lab #1/#2/#6); re-ran `site/scripts/check-experiments.mjs` and `sync-experiments.mjs` so the site cards show the same landing note.
- Updated `docs/EXPERIMENTS.md` with a "Manuscript index" callout pointing at the new appendix as the curated cross-line index (kept the MD files as the full per-line ledgers, per the user's instruction not to duplicate every minor finding).
- Updated `README.md`'s Experiments row and `docs/MANUSCRIPT.md`'s structure line (8→9 compiled appendices, A–H→A–I) to mention the new appendix.
- Bumped `scripts/check_structure.py`'s `APPENDIX_COUNT` 13→14 (one more `app*.tex` file on disk).
- Ran `make generate`, full `./build.sh` (1345 pages after bridge table + descriptions, no errors), and `make check` (structure, citation, bibliography-summary checks all pass).

## Decisions

- New appendix letter picked by appending at the end of `book.tex`'s `\input` list rather than inserting mid-sequence, so no existing appendix's displayed letter (A–H) shifts; the new one lands as Appendix I.
- Findings are grouped and labeled per-line with line-local short IDs (`AD-`, `T-`, `E-`, `GA-`, `L-`, `GL-`) rather than reusing each line's own `G-`/`F-`/`N-` numbering directly as the cross-reference target, because lab-simulation and graded-lab-simulation both independently use `G-` numbering and a shared appendix needed unambiguous labels; each row still states the line's own ID in parentheses for lookup in that line's `FINDINGS.md`.
- Kept the pre-existing generic `\autocite{zarncke2025uad}`/`\autocite{zarncke2025biq}` in ch07/ch11 alongside the new precise appendix pointer rather than deleting them — the method-paper citation is still valid supporting context, the complaint was about precision/traceability, not about removing a legitimate reference.
- Did not build a generated/YAML-driven appendix (unlike `metadata/experiments.yml` → site cards); this appendix is hand-authored like `appB`/`appF`/`appG`, consistent with how other appendices in this repo are maintained, and the finding set is small enough (25 rows) that drift risk is manageable by the same discipline as other hand-maintained ledgers.
- "Manuscript" column honesty: most of the 25 curated findings are not cited anywhere in the manuscript yet; the appendix says so explicitly (``---'') rather than implying full integration.

## Open / next

- Only 4 of 25 curated findings are actually cited by a chapter (GL-1, GL-2, GL-3, GL-7, T-1 — 5 labels across 4 findings). The remaining lines (agency-detect, embedded-simulation, goal-agent-simulation, lab-simulation) have zero chapter citations from this appendix; candidate homes exist (e.g. ch07/ch09 for embedded-sim's UAD-vs-heuristic result E-1, ch33/ch36 for goal-agent's certifier-capture result GA-3, ch33 for lab-sim's leak-proof L-6) but were not added this session — scope was fixing the four existing additions' precision, not a full harvest pass over every line.
- If future manuscript harvest sessions cite additional findings from this appendix, add the `\label{finding:...}` reference at the citation site (naming both the appendix section and the finding label), update the "Manuscript" column for that row in the appendix findings table, and update the corresponding `metadata/experiments.yml` headlineFindings string, to keep both directions in sync.
- Consider whether `review/claim-checklist.md` or `metadata/uncertainty-ledger.md` also warrant a pointer to specific findings the same way `claims-ledger.md` now has one.

## Key paths

- `appendices/appN-experimental-evidence.tex` (new; compiles as Appendix I)
- `book.tex` (added `\input`)
- `scripts/check_structure.py` (`APPENDIX_COUNT`)
- `chapters/ch07-finding-boundary.tex`, `ch11-capability-without-task-ontology.tex`, `ch33-certification-without-construction.tex`, `ch34-selection-environment.tex`
- `metadata/claims-ledger.md` (C-003, C-006, C-007)
- `metadata/experiments.yml`, `docs/EXPERIMENTS.md`, `README.md`, `docs/MANUSCRIPT.md`

## Commits

- None yet this session.
