# 2026-06-19 — Chapter 26 extrapolative correction draft

## Trigger
User provided a full draft for Chapter 26 and asked to integrate it into `chapters/ch26-extrapolative-correction.tex`.

## Done
- Replaced stub with full draft: obedience trap, correction channel, value updates, legitimacy constraints, bundle geometry, strong correction hierarchy, civilizational self-governance, operational criteria, CEV relation, desired guarantee, What Would Change This View, summary.
- Matched book conventions: `chapterthesis`, `epigraph`, `refsection`, `\autocite` + subbibliography.
- Kept repo label `ch:extrapolative-correction`.
- Unique labels: `eq:cci-ch26`, `eq:correction-chain-ch26`, `sec:obedience-trap-ch26`, etc.
- Cross-refs to ch16–ch19, ch24, ch25, ch27; cited yudkowsky2004cev, soares2015corrigibility, hadfieldmenell2016 per stub TODO.
- Updated `metadata/book.yml` ch26 status: `stub` → `draft` (in prior commit on branch).
- Trimmed duplicate manipulation/false-consent sections (present in author ch26 draft but reserved for ch27); replaced with bridge paragraph to Chapter~\ref{ch:manipulation-false-consent}.
- `./build.sh` succeeds.

## Decisions
- Shape B integration: kept native narrative structure; added `\section{What Would Change This View}`.
- Omitted habermas1996, sunstein2019 (not in bib); used dewey1938logic for Dewey valuation tradition.
- Removed full manipulation/false-consent treatment from ch26 after user confirmed that content belongs in ch27.
- British spelling (`behaviour`, `modelling`, `favourable`) to match ch24–ch25.

## Open / next
- ch27 drafted separately (`e2c4357`); review ch27 opening for redundant re-derivation of correction chain from ch24–26.
- Part VI ch24–ch27 drafted.

## Key paths
- `chapters/ch26-extrapolative-correction.tex`
- `metadata/book.yml`

## Commits
- (this session)
