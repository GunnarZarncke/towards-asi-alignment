# 2026-06-22 — Chapter 37 detecting goal laundering draft

## Trigger
User supplied a full author draft for Chapter 37 ("Detecting Goal Laundering")
and asked to integrate it into the chapter file.

## Done
- Replaced the stub `chapters/ch40-goal-laundering.tex` with the integrated
  draft (Shape B — kept the draft's native narrative structure).
- Added the required book elements the raw draft lacked:
  - real `chapterthesis` (from the draft's opening quote);
  - `refsection` wrapper + `\epigraph`;
  - inline `\autocite{...}` at key points and a prose Chapter References paragraph
    closing with `\printbibliography[heading=subbibliography,...]`, replacing the
    draft's hand-formatted reference list;
  - `-ch48`-suffixed `\label`s on sections; kept the book's existing chapter
    label `ch:goal-laundering` (not draft's `ch:detecting-goal-laundering`);
  - cross-refs to Chapters~\ref{ch:passive-observation-not-enough},
    \ref{ch:value-bundle-model}, \ref{ch:tradeoffs-bundle-geometry},
    \ref{ch:bearer-maps}, \ref{ch:correction-causal-channel},
    \ref{ch:correction-channel-integrity}, \ref{ch:conserved-properties},
    \ref{ch:certification-without-construction}, \ref{ch:successor-central-test},
    \ref{ch:self-modeling-self-opacity}, \ref{ch:selection-environment},
    and \ref{ch:alignment-attractor}.
- Fixed draft LaTeX artifacts: `[`/`]` math fences → `\[...\]`, `(A_t)` →
  `\(A_t\)`, `=====`/`##`/`---` in display math, broken subscripts
  (`\mathbb{E}*{z...}` → `\mathbb{E}_{z...}`), array line breaks, and
  backtick/quote typos.
- Wired stub TODO cites: `manheim2018goodhart`, `park2024deception`,
  `hubinger2023modelorganisms`, `goodhart1984problems`.
- `metadata/book.yml`: ch48 status `stub` → `draft`.
- Build green: `./build.sh` exits 0 (888 pages); no undefined citations for ch48.

## Decisions
- Kept display math as `\[ ... \]` rather than numbered `equation` environments
  — matches ch48–ch46 integration pattern.
- ch46 introduces goal laundering as a measurement problem; ch48 is the dedicated
  detection chapter — cross-ref wired both ways via ch46 forward-ref.
- Omitted Hamilton (1964) — no matching BibLaTeX key used in prose.
- Not committed (no commit requested).

## Open / next
- Pre-existing duplicate-label warnings remain elsewhere:
  `sec:self-modeling-transparency`, `sec:example-helpful-assistant`.
- ch46–ch48 now integrated in this session block; optional single commit.
- ch48, ch45+ still stub if user wants them integrated next.

## Key paths
- `chapters/ch40-goal-laundering.tex`
- `metadata/book.yml`

## Commits
- none (no commit requested)
