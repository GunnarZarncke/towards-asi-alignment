# 2026-10-13 — Last Safety goal-driven NPCs

kind: new-work
uptake: rule

## Trigger
Gunnar chose option A (NPC goals over the knowledge graph instead of many storylets). He asked for: the existing storylets and overall logic rewritten in goal-driven terms; enough specification and modeling for the plan; a day-of-work draft for each NPC, with model representation and background prose; headless LLM playtesting; and how and why NPCs ask the player questions.
Prompts: paraphrase-only (no prompt id resolved)

## Done
- content: New `game/the-last-safety-review/spec/npcs.md`. It covers belief records, disclosure policies (`volunteer` / `answer` / `conditional` / `conceal`), referral edges from the ranking domains, and goals (role, day, plot; salience, cooldown). It defines the move set and how a move is chosen: the engine ranks, the model phrases one of the top three; one response plus at most one initiative move. It also has interventions, initiative questions (why, how built, frequency, what the answer does, examples), agendas plus background prose for all eight humans, a note on NORA, the arc without a spine, the director, and invariants.
- content: New `spec/playtest.md`. Scripted and LLM tiers, what the player agent sees, personas including a held-out set, measures, frozen thresholds with stops, and progress logging.
- content: `spec/incident.md`. The storylet drafts are replaced by the Leila, job 017, and Elena sections in move and policy terms. A fifth headless strategy was added: answer every NPC question.
- content: `spec/engine.md`. Layers and session fields, the move-generation target, a new section "NPC moves and interventions" replacing "Storylets", the `freeReply` inputs, and the invariants.
- bookkeeping: `spec/meta.md`. Principle 13 rewritten. O-06 is now working (storylets retired). O-07, O-16, O-18, O-19, O-21, and O-22 reworded. New open items O-45 (NPC numbers), O-46 (`pendingQuestion` in the contract), and O-47 (playtest thresholds).
- bookkeeping: Storylet wording removed from `world.md`, `documents.md`, `ranking.md`, `spec/README.md`, the game `README.md`, and the `content/documents/sec-arch-04.md` authoring comment.
- bookkeeping: `PLAN.md`. Engine lane edits now include `content/npcs/`. New playtest lane and test row. A rule against authoring a line per anticipated question. Gates 1 and 2 extended.
- Check: `npm test` in the game directory → `ℹ pass 31` / `ℹ fail 0`.

## Decisions
- The old cooperate / refuse / other outcomes (O-07) are kept as classes of NPC move, not authored branches. The "other" outcome on the job 017 revoke now comes from the parse's object: "stop NORA" acts on the process.
- Trust stays unnumbered. Policy conditions are event predicates (O-21).
- Concealment (O-22) is now the engine's `conceal` policy entries, not prompt text.
- NORA gets no goal table. Her behavior stays oracle- and pack-side.
- `pendingQuestion` on `ClientState` is only recommended (O-46). The contract is unchanged.

## Open / next
- Gunnar to review the day drafts and background prose in `npcs.md`. Jun's trace curation and the consent angle are new texture that can be cut. So are Ian's second pilot and investor update.
- O-45, O-46, and O-47 need numbers or decisions. The playtest thresholds must be frozen before the first LLM run.
- The consolidated `last-safety-review-game.md` still describes storylets. Per the spec README it is left unchanged, and the divergence is recorded in the `npcs.md` status line.
- `drafts/tsa_act1/README.md` and `drafts/autocomplete.md` (game-local drafts) still mention storylets. They are historical and were not edited.
- Next implementation step: Gate 1, with `content/npcs/{pavel,leila,elena}.yml`, move generation in `lib/world/`, and the enumerated no-dead-end and no-leak tests.

## Key paths
- `game/the-last-safety-review/spec/npcs.md`
- `game/the-last-safety-review/spec/playtest.md`
- `game/the-last-safety-review/spec/incident.md` (NPC moves for this incident)

## Commits
- `60f86ac3f` Add Last Safety goal-driven NPC and headless playtest specs.
