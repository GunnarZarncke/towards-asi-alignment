# 2026-06-22 — Chapter 28 successor creation central alignment test draft

## Trigger
User supplied a full author draft for Chapter 28 ("Successor Creation as the
Central Alignment Test") and asked to integrate it into the chapter file.

## Done
- Replaced the stub `chapters/ch28-successor-central-test.tex` with the
  integrated draft (Shape B — kept the draft's native narrative structure).
- Added the required book elements the raw draft lacked:
  - real `chapterthesis` (was `[STUB]`);
  - `refsection` wrapper + `\epigraph` (built from the draft's opening quote);
  - inline `\autocite{...}` at key points and a prose Chapter References paragraph
    closing with `\printbibliography[heading=subbibliography,...]`, replacing the
    draft's hand-formatted reference list;
  - `-ch28`-suffixed `\label`s on sections; kept the book's existing chapter
    label `ch:successor-central-test`;
  - cross-refs to Chapters~\ref{ch:value-bundle-model},
    \ref{ch:bearer-maps}, \ref{ch:correction-channel-integrity},
    \ref{ch:goal-transport}, \ref{ch:manipulation-false-consent}, and
    \ref{ch:conserved-properties}.
- Fixed draft LaTeX artifacts: `[`/`]` math fences → `\[...\]`, `(A_t)` →
  `\(A_t\)`, malformed subscripts (`A'*{t+k}` etc.), `=====`/`##` in display
  math, and backtick/quote typos.
- `metadata/book.yml`: ch28 status `stub` → `draft`.
- Build green: `./build.sh` exits 0; no undefined citations for ch28.

## Decisions
- Kept display math as `\[ ... \]` rather than numbered `equation` environments
  — matches ch27 integration pattern and minimizes churn.
- Retained the draft's full "Conserved properties" section inside ch28 even though
  ch29 is titled similarly; ch29 remains a stub and the Summary now points
  forward to it for deeper treatment.
- Reused existing BibLaTeX keys only; no new bib entries required (Critch
  boundaries → `critch2022boundaries`; Christiano → `christiano2018corrigibility`).
- Not committed (no commit requested).

## Open / next
- ch29 stub still overlaps topically with ch28 §Conserved properties; a future
  pass should split or deduplicate when ch29 is drafted.
- Pre-existing duplicate-label warnings remain elsewhere:
  `sec:self-modeling-transparency`, `sec:example-helpful-assistant`.
- Optional: add claims/assumptions ledger entry for successor-closure and the
  successor-channel principle.

## Key paths
- `chapters/ch28-successor-central-test.tex`
- `metadata/book.yml`

## Commits
- none (no commit requested)
