# 2026-06-22 — Chapter 31 certification without construction draft

## Trigger
User supplied a full author draft for Chapter 31 ("Certification Without
Construction") and asked to integrate it into the chapter file.

## Done
- Replaced the stub `chapters/ch31-certification-without-construction.tex` with
  the integrated draft (Shape B — kept the draft's native narrative structure).
- Added the required book elements the raw draft lacked:
  - real `chapterthesis` (from the draft's Chapter summary);
  - `refsection` wrapper + `\epigraph`;
  - `\begin{definition}[Certification envelope]` using book convention;
  - inline `\autocite{...}` at key points and a prose Chapter References paragraph
    closing with `\printbibliography[heading=subbibliography,...]`, replacing the
    draft's hand-formatted `thebibliography` list;
  - `-ch31`-suffixed `\label`s on sections; kept the book's existing chapter
    label `ch:certification-without-construction`;
  - cross-refs to Chapters~\ref{ch:conserved-properties},
    \ref{ch:successor-central-test}, \ref{ch:value-bundle-model},
    \ref{ch:bearer-maps}, \ref{ch:correction-channel-integrity},
    \ref{ch:extrapolative-correction}, \ref{ch:self-modeling-self-opacity},
    and \ref{ch:selection-environment}.
- Kept draft's `\section*{Key definitions}` and `\section*{Exercises and research
  prompts}`.
- Removed stub-only `\paragraph{Footnote: halting and stasis.}` (not in author draft).
- Fixed draft LaTeX artifacts: `[`/`]` math fences → `\[...\]`, `(A_t)` →
  `\(A_t\)`, malformed subscripts (`\mathcal{C}*{\text{certified}}`,
  `\bigwedge*{k=1}^{7}`, `\Phi^{A'}*i`, `\mathcal{B}*{\text{safe}}`, etc.),
  `=====`/`##` in display math, and backtick/quote typos.
- `metadata/book.yml`: ch31 status `stub` → `draft`.
- Build green: `./build.sh` exits 0; no undefined citations for ch31.

## Decisions
- Kept display math as `\[ ... \]` rather than numbered `equation` environments
  — matches ch27–ch30 integration pattern.
- Wired stub TODO cites: `kelly1998safety`, `bloomfield2012safety`,
  `everitt2016selfmodification`.
- Omitted Leveson (2011) and Ashby (1956) — no matching BibLaTeX keys in repo.
- Not committed (no commit requested).

## Open / next
- Pre-existing duplicate-label warnings remain elsewhere:
  `sec:self-modeling-transparency`, `sec:example-helpful-assistant`.
- Optional: add Leveson safety-case bib entry if a later pass wants fuller
  certification/safety-case coverage.

## Key paths
- `chapters/ch31-certification-without-construction.tex`
- `metadata/book.yml`

## Commits
- none (no commit requested)
