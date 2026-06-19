# 2026-06-19 — Chapter 25 correction-channel integrity draft

## Trigger
User provided a full draft for Chapter 25 and asked to integrate it into `chapters/ch25-correction-channel-integrity.tex`.

## Done
- Replaced stub with full draft (~28 sections): CCI functional, correction chain, feedback vs correction, value-bundle correction, extrapolative correction, capture guardrails, ontology/capability/successor tests, self-transparency, institutional correction, Goodharting, six observable metrics, stop/start/continue criteria, two worked examples, safety case template, formal summary, failure modes, conclusion.
- Preserved prior stub's coerced-correction subsection and $\mathrm{CCI}_{\text{legit}}$ formula.
- Matched book conventions: `chapterthesis`, `epigraph`, `refsection`, `\autocite` + subbibliography.
- Kept repo label `ch:correction-channel-integrity`.
- Unique labels: `eq:cci-ch25`, `eq:correction-chain-ch25`, `sec:stop-start-continue-ch25`, `sec:self-modeling-transparency-ch25`, etc.
- Cross-refs to ch24, ch26; cited soares2015corrigibility, amodei2016concrete per stub TODO.
- Updated `metadata/book.yml` ch25 status: `stub` → `draft`.
- `./build.sh` succeeds (647 pages).

## Decisions
- Omitted leike2018 reward modeling (not in bib); ashby/wiener via conant1970regulator.
- Forward reference to ch26 extrapolative correction.

## Open / next
- ch26 extrapolative correction still stub.
- Part IV ch15–ch25 drafted.

## Key paths
- `chapters/ch25-correction-channel-integrity.tex`
- `metadata/book.yml`

## Commits
- (none)
