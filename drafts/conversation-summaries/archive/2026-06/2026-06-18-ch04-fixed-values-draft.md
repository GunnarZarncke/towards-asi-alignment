# 2026-06-18 — Chapter 4 fixed values draft

## Trigger
User provided a full draft for Chapter 4 (Why Fixed Values Are the Wrong Target) and asked to integrate it into `ch04-fixed-values-wrong-target.tex`.

## Done
- Replaced stub chapter with integrated draft: epigraph, chapter thesis, 18 sections (including subsections), examples, failure modes, plural-alignments note, summary.
- Converted draft notation to LaTeX: display math, `\MI` for mutual information, fixed markdown artifacts (`*t` subscripts, `====` underlines, backtick quote typos).
- Wrapped chapter in `\begin{refsection}` / `\printbibliography` matching Ch. 1–3 convention; `\autocite` in Chapter References.
- Added BibTeX entries: `abbeel2004apprenticeship`, `soares2015corrigibility`, `rawls1971`, `dewey1938logic`, `sen2009justice`, `anderson1993value`, `zarncke2026value-bottleneck`.
- Mapped draft citation keys to existing canon where applicable (`ng2000irl`, `ziebart2008maxent`, `yudkowsky2004cev`, `russell2019human`, `zarncke2025loop-hub-value`).
- `./build.sh` succeeds (205 pages).

## Decisions
- Kept the draft's section structure rather than the scaffold template (Why This Matters / Plain-Language Model / etc.) because the user supplied a complete chapter outline.
- Retained label `ch:fixed-values-wrong-target` for consistency with existing aux/cross-refs.
- Added two-sentence `chapterthesis` box distilled from the summary section.

## Open / next
- Ch. 5 remains a stub in Part I.
- Consider inline `\autocite` during later polish (Ch. 1 cites throughout; Ch. 4 cites mainly in Chapter References).
- Review overlap with Ch. 3 (dynamical guarantee, bundle geometry) and later value-bundle chapters when those are drafted.

## Key paths
- `chapters/ch04-fixed-values-wrong-target.tex`
- `references/external-alignment.bib`, `references/philosophy.bib`, `references/internal-project-sources.bib`

## Commits
- (none)
