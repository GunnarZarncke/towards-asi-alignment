# 2026-07-13 — Epistemic status notes for all chapters and appendices

## Trigger

User asked to add a short "epistemic status" paragraph to every chapter and appendix: how much of the material is standard/well-known vs. individual contribution vs. a mix, plus confidence (both the book's own confidence in what it derives, and the field's general confidence in the standard results it leans on). Explicitly not to duplicate content already covered elsewhere, especially the per-chapter "What Would Change This View" (WWCTV) sections. Full review of each chapter, subagents allowed.

## Done

- Added a new `epistemicstatus` tcolorbox environment to `metadata/preamble.tex` (gray/neutral styling, distinct from the blue `chapterthesis` box).
- Confirmed design choices with the user before the fan-out: tcolorbox format, placement immediately after `chapterthesis` (chapters) / immediately after `\label{}` (appendices), parallel-subagent execution, and scope limited to the 8 appendices actually `\input` in `book.tex` (excluded `appH`–`appL`, which are stub files never wired into the book).
- Launched 10 parallel background subagents (one per Part, `generalPurpose`), each reading its assigned chapters' full text, their WWCTV sections (to avoid duplication), `metadata/claims-ledger.md` and `metadata/uncertainty-ledger.md` entries for calibration, and `REVIEWING_FOR_AGENTS.md`'s Gem Map (to distinguish named individual contributions from standard reframing). All 10 completed and inserted one `\begin{epistemicstatus}...\end{epistemicstatus}` box each into their 48 assigned chapter files.
- Wrote the 8 real-appendix notes myself directly (`appA` notation index, `appB` bridge crosswalk, `appC` institutional translation, `appM` institutional histories, `appD` worked example, `appE` glossary, `appF` research program, `appG` Lean proof spine), reading each appendix's actual content (including its own existing self-assessment language, e.g. appB's "What the book shares, and what it adds" and appF's dependency-order section) before writing.
- Verified automatically: all 48 chapter boxes sit in the correct position (`\end{chapterthesis}` → box → `\begin{refsection}`); no box uses banned voice patterns (`I argue/claim`, `we argue/claim/contend`, `This chapter argues`, or the retired `[Established]`/`[Speculative]`/`[Open]` bracket-tag convention); `scripts/check_voice.py` passes; all 8 appendix boxes have balanced `\begin`/`\end`.
- Ran a full `./build.sh` (latexmk + biber ×2): succeeded, 1342 pages, no new LaTeX errors or undefined references. Visually spot-checked the rendered PDF (ch01's Chapter Thesis / Epistemic Status box sequence) to confirm styling.

## Decisions

- Excluded `appendices/appH-*.tex` through `appL-*.tex` (stub files, `\textbf{[STUB]}`, never `\input` in `book.tex`) — confirmed with user before starting.
- Box format: new tcolorbox (not a plain paragraph or footnote-style rule), titled "Epistemic Status," gray/neutral (`black!4!white` / `black!55!white`) to read as clearly distinct from the blue Chapter Thesis box.
- Placement: right after `chapterthesis` for chapters (before epigraphs/`refsection`); for appendices, after `chapterthesis` where one exists (`appM`, `appD`), otherwise right after `\label{}`/`\begin{refsection}` before the first content paragraph.
- Content contract given to every subagent (and followed for the appendices): one paragraph, no bullets, impersonal voice; must name the specific novel apparatus (not just assert originality); must split confidence into book-own-confidence (calibrated against the claims-ledger established/plausible/framework/speculative/limit vocabulary) and field-general confidence in the standard material leaned on; must not restate WWCTV falsifiers or reintroduce the retired bracket-tag convention.
- For `appF-research-program.tex`, whose entire purpose is to merge the WWCTV disconfirmers into one research plan, the note says so explicitly (redundancy at the level of individual open questions is by the appendix's own design) and focuses instead on the appendix's own added contribution — the bridge dependency-order/correlation analysis.

## Open / next

- Not done: no attempt to cross-check the ~56 new paragraphs against each other for cross-chapter consistency beyond spot sampling (~10 read in full) and the automated voice/placement checks; a full read-through pass would catch subtler tone drift across the 10 subagents' outputs if desired.
- Not done: no update to `metadata/claims-ledger.md`, `metadata/uncertainty-ledger.md`, or `metadata/book.yml` — the new boxes only summarize existing ledger status, they don't add new claims.
- **Completed 2026-07-17:** author finished manual review of remaining open boxes; committed in two parts — `36bf3c3` (ch01–ch12, ch33, ch34, ch36, ch40 + preamble) and `fd8d480` (ch13–ch32, ch35, ch37–ch39, ch41–ch48 + appB/C/D/F/G/M). appA and appE still lack boxes; appN had its own box from the experimental-evidence appendix session. See [2026-07-17-epistemic-status-review-complete.md](2026-07-17-epistemic-status-review-complete.md).

## Key paths

- `metadata/preamble.tex` — new `epistemicstatus` environment definition.
- `chapters/ch01-wrong-object.tex` … `chapters/ch48-towards-alignment.tex` — one box each.
- `appendices/appA-notation.tex`, `appB-bridge-crosswalk.tex`, `appC-institutional-translation.tex`, `appM-institutional-histories.tex`, `appD-worked-example.tex`, `appE-glossary.tex`, `appF-research-program.tex`, `appG-lean-proof-spine.tex` — one box each.
- `metadata/claims-ledger.md`, `metadata/uncertainty-ledger.md`, `REVIEWING_FOR_AGENTS.md` (Gem Map) — the calibration sources each box should stay consistent with.

## Commits

- `36bf3c3` Add reviewed epistemic-status notes to ch01-ch12, ch33, ch34, ch36, ch40
- `fd8d480` Add reviewed epistemic-status notes to ch13–ch48 and six appendices
