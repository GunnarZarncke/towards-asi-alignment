# 2026-06-22 — Chapter 36 passive observation not enough draft

## Trigger
User supplied a full author draft for Chapter 36 ("Passive Observation Is Not
Enough") and asked to integrate it into the chapter file.

## Done
- Replaced the stub `chapters/ch36-passive-observation-not-enough.tex` with the
  integrated draft (Shape B — kept the draft's native narrative structure).
- Added the required book elements the raw draft lacked:
  - real `chapterthesis` (from the draft's central claim);
  - `refsection` wrapper + `\epigraph`;
  - inline `\autocite{...}` at key points and a prose Chapter References paragraph
    closing with `\printbibliography[heading=subbibliography,...]`, replacing the
    draft's hand-formatted reference list;
  - `-ch36`-suffixed `\label`s on sections; kept the book's existing chapter
    label `ch:passive-observation-not-enough` (not draft's `chap:passive-observation`);
  - cross-refs to Chapters~\ref{ch:finding-boundary}, \ref{ch:strategic-opacity},
    \ref{ch:value-bundle-model}, \ref{ch:goal-transport}, \ref{ch:bearer-maps},
    \ref{ch:correction-causal-channel}, \ref{ch:correction-channel-integrity},
    \ref{ch:manipulation-false-consent}, \ref{ch:successor-central-test},
    \ref{ch:conserved-properties}, \ref{ch:certification-without-construction},
    \ref{ch:selection-environment}, \ref{ch:alignment-attractor},
    \ref{ch:goal-laundering}, and \ref{ch:safety-case}.
- Fixed draft LaTeX artifacts: `[`/`]` math fences → `\[...\]`, `(A_t)` →
  `\(A_t\)`, `=====`/`##`/`---` in display math, broken subscripts
  (`C^{H}*t` → `C^{H}_t`), markdown code fences in Decision Triggers,
  perturbation-matrix line breaks, and backtick/quote typos.
- Used unique example labels (`sec:example-helpful-research-agent-ch36`,
  `sec:counterexample-goal-laundering-ch36`) to avoid duplicate
  `sec:example-helpful-assistant`.
- `metadata/book.yml`: ch36 status `stub` → `draft`.
- Build green: `./build.sh` exits 0 (869 pages); no undefined citations for ch36.

## Decisions
- Kept display math as `\[ ... \]` rather than numbered `equation` environments
  — matches ch27–ch35 integration pattern.
- Wired stub TODO cites: `hubinger2023modelorganisms`, `park2024deception`,
  `iaisr2025`.
- Goal-laundering section kept here as measurement framing; forward-ref to
  ch37 for dedicated detection methods.
- Omitted Hamilton (1964) — no matching BibLaTeX key used in prose.
- Not committed (no commit requested).

## Open / next
- Pre-existing duplicate-label warnings remain elsewhere:
  `sec:self-modeling-transparency`, `sec:example-helpful-assistant`.
- ch28–ch36 now integrated in this session block; optional single commit.
- ch33, ch37+ still stub if user wants them integrated next.

## Key paths
- `chapters/ch36-passive-observation-not-enough.tex`
- `metadata/book.yml`

## Commits
- none (no commit requested)
