# 2026-06-19 — Chapter 27 manipulation / domestication / false consent draft

## Trigger
User supplied a full author draft for Chapter 27 ("Manipulation, Domestication,
and False Consent") and asked to integrate it into the chapter file.

## Done
- Replaced the stub `chapters/ch27-manipulation-false-consent.tex` with the
  integrated draft (Shape B — kept the draft's native narrative structure).
- Added the required book elements the raw draft lacked:
  - real `chapterthesis` (was `[STUB]`);
  - `refsection` wrapper + `\epigraph` (built from the draft's opening quote);
  - a new `\section{What Would Change This View}` before the Summary;
  - inline `\autocite{...}` throughout and a prose Chapter References paragraph
    closing with `\printbibliography[heading=subbibliography,...]`, replacing the
    draft's hand-formatted numbered reference list (per INSTRUCTIONS §11 — never
    hand-format references).
  - `-ch27`-suffixed `\label`s on sections; kept the book's existing chapter
    label `ch:manipulation-false-consent`; added a cross-ref to
    `ch:correction-channel-integrity`.
- Added 10 missing BibLaTeX entries:
  - `references/philosophy.bib`: `frankfurt1971freedom`, `pettit1997republicanism`,
    `sen1999development`, `habermas1984communicative`, `elster1983sourgrapes`.
  - `references/governance-institutions.bib`: `thaler2008nudge`,
    `susser2019manipulation`, `yeung2017hypernudge`, `zuboff2019surveillance`,
    `nissenbaum2010privacy`.
  - Reused existing keys: `yudkowsky2004cev`, `soares2015corrigibility`,
    `christiano2018corrigibility`, `hadfieldmenell2016`, `russell2019human`,
    `pearl2009causality`.
- `metadata/book.yml`: ch27 status `stub` → `draft`.
- Build + checks green: `./build.sh` exits 0 and produces the PDF; `book.log`
  shows no undefined citations/references; all 10 new keys resolve in `book.bbl`;
  `make check` passes (structure + citations).

## Decisions
- Kept display math as `\[ ... \]` / inline `\( ... \)` from the draft rather than
  converting to numbered `equation` environments — valid, and minimizes churn for
  a chapter with very many display lines.
- Manual bib entries went into the category `.bib` files (matching existing manual
  entries like Dewey/Sen/Pearl in `philosophy.bib`), not `main.bib`. Note: these
  are not from the source-map importer, so re-running
  `scripts/import_source_map_refs.py` should not clobber them, but a future agent
  regenerating refs should preserve them.
- WWCTV section authored fresh (the draft had none); framed around the
  identifiability of the bypass-mediation term and the agency/endorsement link.

## Open / next
- Pre-existing (not introduced here) duplicate-label warnings remain elsewhere:
  `sec:self-modeling-transparency`, `sec:example-helpful-assistant`.
- Optional: add a claims/assumptions ledger entry for the manipulation/service
  causal-pathway distinction and the No-Bypass Principle.
- Not committed (no commit requested).

## Key paths
- `chapters/ch27-manipulation-false-consent.tex`
- `references/philosophy.bib`, `references/governance-institutions.bib`
- `metadata/book.yml`

## Commits
- none (no commit requested)
