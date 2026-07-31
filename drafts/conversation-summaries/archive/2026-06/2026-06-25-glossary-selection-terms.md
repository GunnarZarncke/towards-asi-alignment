# 2026-06-25 — Glossary selection terms

## Trigger
User asked to update the glossary appendix after the handle-based fitness refactor in ch46.

## Done
- Extended `appendices/appE-glossary.tex` with operational entries for selection environment, selection handle, deployment/control mass, fitness, preservation score, and selection divergence.
- Cross-referenced Chapter~\ref{ch:selection-environment} and Eqs.~\eqref{eq:deployment-mass-ch46}--\eqref{eq:selection-divergence-ch46}.
- `./build.sh` passed (pre-existing citation warnings only).

## Decisions
- Glossary mirrors ch46 handle-based definitions; revenue/regulatory risk/benchmarks described as proxies, not primitive fitness terms.
- No tripwire entry added (concept removed from spine); glossary had no tripwire term to delete.
- Did not expand glossary to full INSTRUCTIONS §6 coverage in this pass—selection terms only.

## Open / next
- Optional: populate `appendices/appA-notation.tex` from `metadata/notation.md`.
- Optional: add remaining core terms (successor, pivotal process, adversarial measurement, etc.) in a later glossary pass.

## Key paths
- `appendices/appE-glossary.tex`
- `chapters/ch34-selection-environment.tex` (canonical definitions)
- `metadata/terminology.md`

## Commits
- (none this session)
