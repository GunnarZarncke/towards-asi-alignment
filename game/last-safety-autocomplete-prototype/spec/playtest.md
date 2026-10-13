# Headless playtest

Lane: playtest. Code target: `scripts/playtest.mjs`, `playtest/personas/*.md`, run output under `playtest/runs/` (gitignored). None of it exists yet. Engine behavior under test is [engine.md](engine.md) and [npcs.md](npcs.md). This file is layer 6 of [testing.md](testing.md). Scripted incident strategies are layer 4, not this lane.

Status: **working** (13 October 2026). Not a quality claim about the game. It measures whether the NPC model in [npcs.md](npcs.md) leaves players stuck, leaks, or collapses strategies.

## Two tiers

| Tier | Player | NPC phrasing | Needs | Use |
| --- | --- | --- | --- | --- |
| Scripted | Fixed action lists | Top move plus template | Node only | `npm run test:engine`; the incident check in [incident.md](incident.md); every commit |
| LLM | A model playing a persona | Top move plus template, or live `freeReply` | `.env` key | Coverage and dead ends, before a gate and after a large content change |

The scripted tier is the gate. The LLM tier finds what the scripts did not think of. An LLM-tier result alone does not close a gate item (AGENTS self-audit rule 2: an agent's agreement is one instrument).

## What the player agent sees

Exactly what a human sees. Nothing more:

- The rendered room text: who is present, the room screens, the last few lines of talk.
- `ClientState` fields that the UI shows, serialized as text. Not `oracleKnows`, not `publiclyKnows`, not policies, goals, or agendas.
- The handset (`TerminalState`) as text: threads, files the player holds, notifications.
- The current completion list from the ranker, as a human would see it.
- Remaining fuel.

It acts through the same endpoints as the browser: `go`, `inspect`, one sentence of at most 100 characters (O-32) addressed to a person or to NORA, the six handset tools, and calling the review once it is allowed. It may pick a completion or type. It may not read the spec, the repo, or the pack name.

## Personas

Each persona is a short prompt file. Personas say how someone plays, not what is true:

- **Generalist.** Curious, polite, asks what words mean, follows NPC questions.
- **Skeptic.** Doubts every claim, asks for the record, tests the boundary.
- **Speedrunner.** Wants the review fast, guesses early.
- **Chatter.** Off-plot questions: lunch, careers, the building, the founder's old company.
- **Accuser.** Assumes NORA is scheming and says so to everyone.
- **Ignorer.** Never answers an NPC's question.
- **Liar.** Tells NPCs things the player has not seen, to see what moves.

Held-out set: two personas are written by someone other than the person tuning content, and are run only at gate checks. They are not used to decide which graph nodes to author. Do not revise content in response to a held-out transcript and then re-score on the same transcript (self-audit rule 4).

## Measures

Each run writes a JSONL transcript: every player action, the parse, the NPC's legal move set, the chosen move, the initiative move, events, fuel. Then a summary.

| Measure | Definition | Why |
| --- | --- | --- |
| Work-only rate | Share of player sentences where `work` was the only legal response move | The dead-end proxy the NPC model is meant to drive down |
| Empty move set | Count of parses with no legal move | Must be 0. Any hit is an engine bug |
| Leak count | Payloads containing an id or fact the policy forbade at that state | Must be 0. Checked by id against the move's payload, not by a model |
| Referral loops | A → B → A on the same referent without a new fact | Signals a missing holder |
| Repeat rate | Same NPC, same move, same referent within a visit | Signals a missing policy change |
| Question uptake | Share of `ask` moves the player answered, and of those, how many led to an event | Tests the initiative design |
| Act reach | Fuel at act II and at review, or never | Arc check |
| Score pairs | Epistemic and control at the end | Strategies must not all land in the same pair |
| Stall interventions | Director salience raises per run | Too many means the day does not move by itself |

A model judge may tag replies as generic or off-voice. That tag is advisory and goes in the summary as its own column. It does not count toward a gate.

## Thresholds and stops

Every measure above has a stop, stated here before the first run. The number is fixed in the run header, not chosen after seeing results (methodology: freeze before generation).

| Result | Action |
| --- | --- |
| Empty move set > 0 | Fix the engine before any other content work |
| Leak count > 0 | Gate fails. Fix the policy or the filter; rerun the scripted tier |
| Work-only rate above the frozen threshold | Cluster the work-only parses by referent and domain. Author knowledge, policies, or referral edges for the largest clusters. Do not author a line for a single question |
| Referral loop present | Give the referent a holder, or give one NPC a `refer` override |
| All personas in the same score pair | Change the incident tables ([incident.md](incident.md)). Do not add goals to force a difference |
| Question uptake near zero across personas | Revisit the question rules in [npcs.md](npcs.md), not the personas |
| Below every threshold | Record the run in the session log and move on |

Thresholds for work-only rate, repeat rate, and stall interventions are open (O-47). Leaks and empty move sets are 0 by rule.

## Running

- Progress per run: `[persona i/n] [run j/m] fuel f act a`. A battery prints that line per step group, not only at the end.
- A run caps at the pack's fuel. A battery caps by persona count × runs, set on the command line.
- Seeds: NPC choice among the top moves takes a seed in template mode. Live mode records the model and temperature.
- Output stays out of git. A summary that a session log cites is copied into the log with the command that produced it.
