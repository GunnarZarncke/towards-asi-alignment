# 2026-10-14 — Last Safety: vocabulary follows what the player has seen

kind: new-work
uptake: local

## Trigger
Completions offered systems (queue, cameras, release schedule) the player had not met. Gunnar asked to start from a few invitation facts, let Ian brief the auditor, and add a vocabulary id only once it has occurred somewhere visible.
Prompts: paraphrase-only (no prompt id resolved)

## Done
- content: `START_VOCAB` and `START_INTRODUCED` are empty. `newSession` learns `invited_as_reviewer` and `received_by_ian` (NORA, the review, Ian) and introduces whoever is in the room.
- content: Confirming Lab Access hears `auditor_brief` (shutdown test, Leila, safety paper, Justine, Lab Access). Goal `ian.brief_auditor`. The handed calendar introduces Ian, Leila, Amara, and Daniel. Other ids wait for a fact, a heard line, or a person in the room.
- bookkeeping: `spec/engine.md` (Player vocabulary), `spec/world.md`, `spec/grammar.md`, `spec/ranking.md`, `spec/npcs.md`, `spec/contract.md`.

Verification: `npm test` in `game/last-safety-autocomplete-prototype` → `ℹ tests 84` / `ℹ pass 84` / `ℹ fail 0`.

## Decisions
- The shutdown test is named in Ian’s briefing, not on the invitation, so it is not a completion before he speaks.
- Queue, cameras, and Pavel are not named until a record, a sentence, or the room.

## Open / next
- Opening the calendar is not a separate act: the names count when the handset is handed over.
