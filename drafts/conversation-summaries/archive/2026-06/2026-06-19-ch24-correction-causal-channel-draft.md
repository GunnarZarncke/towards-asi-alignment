# 2026-06-19 — Chapter 24 correction causal channel draft

## Trigger
User provided a full draft for Chapter 24 and asked to integrate it into `chapters/ch25-correction-causal-channel.tex`.

## Done
- Replaced stub with full draft (~25 sections): correction as causal channel, obedience vs correction, minimal causal model, channel view and CCI, observability/comprehensibility/deliberation/authority bottlenecks, latency, manipulation, ontology mismatch, irreversibility, four-level correction reach, strong correction channel definition, corrigibility and CEV relations, four examples, seven failure modes, CCI audit profile, adversarial testing, necessity claim with proof sketch, governance interpretation, civilizational self-modification, design rules, summary.
- Matched book conventions: `chapterthesis`, `epigraph`, `refsection`, `definition`/`claim`/`proof`, `\autocite` + subbibliography.
- Kept repo label `ch:correction-causal-channel`.
- Unique labels: `eq:correction-chain-ch46`, `eq:correction-channel-integrity-ch46`, `sec:example-medical-ai-ch46`, etc.
- Cross-refs to ch46, ch46; cited soares2015corrigibility, hadfieldmenell2016 per stub TODO.
- Updated `metadata/book.yml` ch46 status: `stub` → `draft`.
- `./build.sh` succeeds (621 pages).

## Decisions
- Used `claim` + `proof` for correction-channel necessity (no `proposition` env in preamble).
- Omitted ashby/wiener/shannon/habermas (not in bib); used conant1970regulator for cybernetic channel analogy.

## Open / next
- ch46 correction-channel integrity still stub.
- Part IV ch15–ch46 drafted.

## Key paths
- `chapters/ch25-correction-causal-channel.tex`
- `metadata/book.yml`

## Commits
- (none)
