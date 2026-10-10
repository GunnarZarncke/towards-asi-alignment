# 2026-10-10 — Last Safety Review open questions O-01–O-30

kind: new-work
uptake: status

## Trigger
Gunnar answered O-01 through O-30. O-01 asked for book failure modes that fit the shutdown scene. O-06 and O-18 asked for drafts to review. O-15, O-16, O-20, and O-24 asked for an explanation or options.
Prompts: none resolvable (paraphrase only).

## Done
- content: `spec/meta.md` — decision table for O-01–O-30. Still open: O-06, O-12, O-19, O-22, O-24, O-27, O-28 (whether the copy is needed), O-31, O-32.
- content: `spec/incident.md` — five packs from the book. First pack is boundary-narrow. Three storylet drafts at the small grain.
- content: `spec/world.md` — voice paragraphs for the cast and NORA; Amara’s interview depth; three options for how fixed the selection subplot is.
- content: `spec/engine.md` — fuel, three outcomes, LLM picks among authored outcomes, Lean reachability, no forced spine.
- content: `spec/terminal.md` and `spec/graphics-ui.md` — unread phone blinks; notes are player-written hypotheses.
- bookkeeping: `PLAN.md` gates 1 and 6. Consolidated design doc not edited.

## Decisions
- Campaigns are packs. Deception is off except in eval-conditioned. Partial escape stays inside the building and means something different per pack.
- Fuel counts sentences and forces the review at zero. An evidence threshold lets the player call it early. Other actions that spend fuel are unnamed.
- “Narrowing to one end-state does not happen before act III” is recorded as a requirement (O-29).
- Quantitative uncertainty is not a player-facing number. NPC prompts get words.

## Open / next
- Gunnar’s review of the three storylet drafts (O-06) and the voice paragraphs (O-18).
- Pick a selection-subplot option (O-24).
- Fill incident tables for boundary-narrow only, then the headless four-strategy check.

## Key paths
- `game/last-safety-autocomplete-prototype/spec/incident.md`
- `game/last-safety-autocomplete-prototype/spec/meta.md`
- `game/last-safety-autocomplete-prototype/spec/world.md`

## Commits
- none
