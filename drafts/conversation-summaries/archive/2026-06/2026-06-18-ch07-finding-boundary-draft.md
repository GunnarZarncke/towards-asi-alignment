# 2026-06-18 — Chapter 7 finding boundary draft

## Trigger
User provided a full draft for Chapter 7 (Finding the Boundary) and asked to integrate it into `ch07-finding-boundary.tex`.

## Done
- Replaced stub chapter with integrated draft: epigraph, chapter thesis, 20 sections (including subsections), seven-step procedure, worked examples (assistant, AI lab), boundary map artifact, stop conditions, summary.
- Converted draft notation to LaTeX: `I(` → `\MI`, display math, proper `\setminus\{m_t\}`.
- Wrapped chapter in `\begin{refsection}` / `\printbibliography`; replaced manual `\begin{thebibliography}` with `\autocite` clusters.
- Kept label `ch:finding-boundary` (draft had `chap:finding-the-boundary`; Ch. 6 already cross-refs this label).
- Added BibTeX entry `pearl2009causality`; mapped all other draft refs to existing keys.
- `./build.sh` succeeds (243 pages).

## Decisions
- Kept the draft's section structure rather than the scaffold template.
- Added inline `\autocite` at key conceptual anchors (Markov blankets, compression, object discovery, IRL, empowerment) plus Chapter References block.
- Linked opening paragraph to Ch. 6 via citation keys rather than `\ref` to avoid forward-dependency on section labels.

## Open / next
- Ch. 8–10 remain stubs in Part II.
- Review overlap with Ch. 1 (boundary error, perturbation) and Ch. 6 (operational agent tests) on later edit pass.

## Key paths
- `chapters/ch07-finding-boundary.tex`
- `references/philosophy.bib` (new `pearl2009causality`)

## Commits
- (none)
