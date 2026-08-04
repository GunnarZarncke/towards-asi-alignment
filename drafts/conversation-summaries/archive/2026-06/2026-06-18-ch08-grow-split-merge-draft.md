# 2026-06-18 — Chapter 8 grow split merge draft

## Trigger
User provided a full draft for Chapter 8 (Agents That Grow, Split, and Merge) and asked to integrate it into `ch08-grow-split-merge.tex`.

## Done
- Replaced stub chapter with integrated draft: epigraph, chapter thesis, 16 sections (including subsections), transport-loss formalism, certification schema, counterexamples, summary.
- Converted draft notation to LaTeX: `I(` → `\MI`, fixed markdown artifacts (`*`, `##`, `====`), `\setminus\{m_t\}`.
- Wrapped chapter in `\begin{refsection}` / `\printbibliography`; replaced `\citet` with `\autocite`.
- Kept label `ch:grow-split-merge` (draft had `ch:growth-splitting-merging`; Ch. 6 cross-refs this label).
- Used `\ref{eq:...}` instead of `\cref` (cleveref not installed).
- `./build.sh` succeeds (267 pages).

## Decisions
- Kept the draft's section structure rather than the scaffold template.
- Chapter References use existing bib keys only; no new BibTeX entries required.

## Open / next
- Ch. 5 and Ch. 9–10 remain stubs.
- Later polish: inline citations, overlap pass with Ch. 6–7 on boundary transport.

## Key paths
- `chapters/ch08-grow-split-merge.tex`

## Commits
- (none)
