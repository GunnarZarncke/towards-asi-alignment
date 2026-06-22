# 2026-06-22 — Chapter 41 when value change is the thing at stake draft

## Trigger
User supplied a full author draft for Chapter 41 ("When Value Change Is the
Thing at Stake") and asked to integrate it into the chapter file.

## Done
- Replaced the stub `chapters/ch41-value-change-at-stake.tex` with the integrated
  draft (Shape B — kept the draft's native narrative structure).
- Added the required book elements the raw draft lacked:
  - real `chapterthesis` (from the draft's opening quote and closing quote);
  - `refsection` wrapper + `\epigraph`;
  - inline `\autocite{...}` at key points and a prose Chapter References paragraph
    closing with `\printbibliography[heading=subbibliography,...]`, replacing the
    draft's hand-formatted reference list;
  - `-ch41`-suffixed `\label`s on sections; kept the book's existing chapter
    label `ch:value-change-at-stake` (not draft's `chap:when-value-change-is-the-thing-at-stake`);
  - cross-refs to Chapters~\ref{ch:value-bundle-model}, \ref{ch:bearer-maps},
    \ref{ch:tradeoffs-bundle-geometry}, \ref{ch:manipulation-false-consent},
    \ref{ch:correction-causal-channel}, \ref{ch:correction-channel-integrity},
    \ref{ch:goal-laundering}, \ref{ch:conserved-properties},
    \ref{ch:certification-without-construction}, \ref{ch:alignment-attractor},
    \ref{ch:selection-environment}, \ref{ch:unconscious-value-drift},
    and \ref{ch:bearers-of-value}.
- Fixed draft LaTeX artifacts: `[`/`]` math fences → `\[...\]`, `(A_t)` →
  `\(A_t\)`, broken subscripts (`\mathcal{S}*{\text{human-correctable}}` →
  `\mathcal{S}_{\text{human-correctable}}`), and backtick/quote typos.
- Wired stub TODO cites: `yudkowsky2004cev`, `dewey1938logic`, `sen2009justice`.
- `metadata/book.yml`: ch41 status `stub` → `draft`.
- Build green: `./build.sh` exits 0 (926 pages); no undefined citations for ch41.

## Decisions
- Kept display math as `\[ ... \]` rather than numbered `equation` environments
  — matches ch27–ch38 integration pattern.
- Philosophy chapter: fewer formal cites than technical chapters; used available
  BibLaTeX keys only.
- Omitted Clark & Chalmers, MacIntyre, Nozick, Parfit, Taylor, Dewey 1922,
  Habermas 1996 — no matching BibLaTeX keys in repo.
- Draft "Conclusion" section kept (not renamed to Summary) — matches author structure.
- Not committed (no commit requested).

## Open / next
- Pre-existing duplicate-label warnings remain elsewhere:
  `sec:self-modeling-transparency`, `sec:example-helpful-assistant`.
- ch28–ch41 now integrated in this session block; optional single commit.
- ch33, ch39–ch40, ch42–ch44 still stub if user wants them integrated next.

## Key paths
- `chapters/ch41-value-change-at-stake.tex`
- `metadata/book.yml`

## Commits
- none (no commit requested)
