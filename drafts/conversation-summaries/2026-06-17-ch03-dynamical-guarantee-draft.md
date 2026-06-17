# 2026-06-17 — Chapter 3 dynamical guarantee draft

## Trigger
User provided a full draft for Chapter 3 (Alignment as a Dynamical Guarantee) and asked to integrate it into `ch03-dynamical-guarantee.tex`.

## Done
- Replaced stub chapter with integrated draft: epigraph, chapter thesis, 16 sections, seven invariant subsections, safety-case claims, failure modes, example, decision relevance, shaky points, summary.
- Converted draft notation to LaTeX: display math, `\MI` for mutual information, `\mathcal{S}` etc., proper quotes.
- Wrapped chapter in `\begin{refsection}` / `\printbibliography` matching Ch. 1 convention; `\autocite` for references.
- Added missing BibTeX entries: `amodei2016concrete`, `yudkowsky2004cev`, `kelly1998safety`, `bloomfield2012safety`, `strogatz2015nonlinear`.
- Mapped draft citation keys to existing canon where applicable (`conant1970regulator`, `ng2000irl`, `ziebart2008maxent`).
- `./build.sh` succeeds (189 pages).

## Decisions
- Kept the draft's section structure rather than the scaffold template (Why This Matters / Plain-Language Model / etc.) because the user supplied a complete chapter outline.
- Added a two-sentence `chapterthesis` box distilled from the summary section.

## Open / next
- Ch. 4–5 remain stubs in Part I.
- Consider inline `\autocite` during later polish (Ch. 1 cites throughout; Ch. 3 cites mainly in Chapter References).
- Review overlap with later chapters (e.g. `ch39-safety-case.tex`, `ch31-certification-without-construction.tex`) when those are drafted.

## Key paths
- `chapters/ch03-dynamical-guarantee.tex`
- `references/external-alignment.bib`, `references/governance-institutions.bib`, `references/dynamical-systems.bib`

## Commits
- (none — user did not request commit)
