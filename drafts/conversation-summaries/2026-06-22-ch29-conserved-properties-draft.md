# 2026-06-22 — Chapter 29 conserved properties across successors draft

## Trigger
User supplied a full author draft for Chapter 29 ("Conserved Properties Across
Successors") and asked to integrate it into the chapter file.

## Done
- Replaced the stub `chapters/ch29-conserved-properties.tex` with the
  integrated draft (Shape B — kept the draft's native narrative structure).
- Added the required book elements the raw draft lacked:
  - real `chapterthesis` (was `[STUB]`);
  - `refsection` wrapper + `\epigraph` (built from the draft's opening quote);
  - inline `\autocite{...}` at key points and a prose Chapter References paragraph
    closing with `\printbibliography[heading=subbibliography,...]`, replacing the
    draft's hand-formatted `thebibliography` list;
  - `-ch29`-suffixed `\label`s on sections; kept the book's existing chapter
    label `ch:conserved-properties`;
  - cross-refs to Chapters~\ref{ch:successor-central-test},
    \ref{ch:value-bundle-model}, \ref{ch:bearer-maps},
    \ref{ch:correction-channel-integrity}, \ref{ch:extrapolative-correction},
    \ref{ch:manipulation-false-consent}, and \ref{ch:self-modeling-self-opacity}.
- Fixed draft LaTeX artifacts: `[`/`]` math fences → `\[...\]`, `(A_t)` →
  `\(A_t\)`, malformed subscripts (`M'*{t+1}`, `\mathcal{L}*{C'}` etc.),
  `=====`/`##` in display math, and backtick/quote typos.
- `metadata/book.yml`: ch29 status `stub` → `draft`.
- Build green: `./build.sh` exits 0; no undefined citations for ch29.

## Decisions
- Kept display math as `\[ ... \]` rather than numbered `equation` environments
  — matches ch27/ch28 integration pattern.
- Omitted `zarncke2025meta` (Parameters of metacognition) from cites; no matching
  BibLaTeX key in repo.
- Used existing keys: `critch2022boundaries3a`, `pearl2009causality`,
  `ramstead2022bayesian`, `soares2015corrigibility`.
- ch28 and ch29 now both cover conserved properties at different depths; ch29
  is the formal catalog and measurement chapter; ch28 retains the successor-test
  framing. Summary points forward to ch30.
- Not committed (no commit requested).

## Open / next
- Optional deduplication pass between ch28 §Conserved properties and ch29.
- Pre-existing duplicate-label warnings remain elsewhere:
  `sec:self-modeling-transparency`, `sec:example-helpful-assistant`.
- Not committed (no commit requested).

## Key paths
- `chapters/ch29-conserved-properties.tex`
- `metadata/book.yml`

## Commits
- none (no commit requested)
