# 2026-10-11 — Autocomplete ranking spec

kind: new-work
uptake: status

## Trigger
Gunnar supplied an answer to O-19 in `game/last-safety-autocomplete-prototype/drafts/autocomplete.md` and asked for a review and a spec that fits the current architecture.
Prompts: none resolvable (paraphrase only).

## Done
- content: `spec/ranking.md` — ranking procedure on a per-call projection of player-visible state.
- status: O-19 set to working in `spec/meta.md`. Grammar, contract, engine, terminal, and PLAN point at the spec.
- bookkeeping: decision record kept at `drafts/autocomplete.md` with a pointer to the spec.

## Decisions
- The ranker stays `getCandidates`. There is no stored knowledge graph, and the book concept graph stays the O-41 card map.
- Document times are minute-of-day values the player has read. Discovery time is the fuel index. The two clocks are not subtracted from each other.
- Public role edges turn on at introduction. The prototype starts with Pavel, Leila, and Elena introduced. NORA does not.
- The typed prefix filters. `asked` does not change order. NORA omissions are the engine list, applied before ranking.
- An entity slot’s diversity branch is the referent’s domain. Same-lab cost 3 with a search limit of 3 leaves every known entity a small floor under a live anchor.

## Open / next
- Implement the ranker and the projection fields. Grammar tests are listed in `spec/ranking.md`.
- Domain inventory and the closely related pairs are a first cut from the cast table. Playtesting may split or merge them.

## Key paths
- `game/last-safety-autocomplete-prototype/spec/ranking.md`
- `game/last-safety-autocomplete-prototype/drafts/autocomplete.md`
- `game/last-safety-autocomplete-prototype/public/grammar.js`

## Commits
- none
