# Engine

Lane: engine. Code: `lib/game.mjs` and future modules under `lib/world/`. Content ids and plot are [world.md](world.md). Shapes are [contract.md](contract.md).

The engine is the only writer of consequential state. Graphics, grammar, and the model may propose. They do not apply.

## Layers

| Layer | Holds | Authority |
| --- | --- | --- |
| Oracle | Events, permissions, jobs, causal history | What happened in the simulation |
| NPC knowledge | Belief records, disclosure policies, referral edges, goals, agenda ([npcs.md](npcs.md)) | May be false |
| Evidence | Transcripts, logs, recordings, reports | Observation, claim, or manipulation; provenance required |
| Player | Examined items, heard claims, assertions, access, actions | What this playthrough did |
| Director | Act, goal salience on a stall, endings | Progression only. Not a second oracle |

Static content (world file) stays distinct from a session.

## Session fields

Minimum, whether or not the prototype stores them all yet:

| Object | Fields |
| --- | --- |
| World | Act, event history, deployment state, jobs, access, simulated AI state |
| Actor | Position, activity, role, permissions, presence (`body` / `hologram` / `absent`) |
| NPC | Belief records, policies, goals with salience, agenda item, pending question. No trust or status number (O-21). Glue stance is a discrete label from the Person layer, not stored arithmetic |
| Evidence | Id, source, content, provenance, observations, claims, access |
| Player | Examined, heard, assertions, presented, requested |
| Story | Act, interventions done, ending flags |
| Presentation | Room, camera mode, lighting, music, poses — derived for the UI, not a source of truth |
| Event | Fuel index, kind, place, participants, payload. Includes movement. No wall-clock time |

Prototype session today: `room`, `playerKnows`, `examined`, `learnedFacts`, `conversations`, `npcReceived`, `asked`, `usage`. Acts, NPC goals and agendas, and endings are absent. Add them in the engine without putting them in the browser as hidden truth.

## Ranking projection

Autocomplete order is [ranking.md](ranking.md). The engine fills the projection. It does not rank.

When an id becomes player-visible, store the fuel index on `discoveredAt`. Until fuel is stored, use the event-log index. Invitation facts are learned at fuel 0, and their refs are the only ids at 0.

## Player vocabulary

An entity id enters `vocab` only when it has occurred somewhere the player can see or hear:

- a ref of a fact the player holds (`learnedFacts`: the invitation, a record, or something they were told)
- a ref on a line they heard
- an actor in the room they are standing in (name and role, so they are introduced)

The invitation holds two texture facts, `invited_as_reviewer` (NORA, the review) and `received_by_ian` (Ian, who is also in the room). It does not name the queue, the cameras, or the rest of the cast. When Ian confirms Lab Access he tells `auditor_brief` (the 17:30 review, the shutdown test, Leila and the safety paper, Justine and Lab Access). That is goal `ian.brief_auditor`. The handset calendar he hands over names the people on today’s entries (Ian, Leila, Amara, Daniel). Other ids wait for a screen, a file, a sentence, or a person in the room. Completions read `vocab` only, so they cannot offer a system the player has not met.

`introduced` gains an actor when they speak to the player, or when a heard turn introduces them. The prototype session starts with `pavel`, `leila`, and `elena` introduced. NORA and the rest of the cast do not. Opening NORA’s thread and receiving a released line counts as her introduction.

On examine, copy that record’s structured refs, and any clock time the text states, onto the player-visible fact and the entities it times. Do not copy a time the player has not read. Do not copy `oracleKnows` or `publiclyKnows` into the projection. Responsibility domains are the static table in the ranking spec, and `clientState` includes a row only for an introduced id.

## Facts and claims

Do not collapse the incident into one flag such as `shutdown_failure_discovered`.

World facts are instrumented events (a command was issued, a process stopped, a job stayed up, a job read a record).

Further claims (the job was NORA’s doing, the access was forbidden, persistence was arranged on purpose, the evaluation was invalid) need their own evidence predicates. The player state records which claims were encountered, investigated, or substantiated. Those three words are not a single ladder: a claim may also be contested or unresolved (O-12).

Two documents that share one upstream model output are not independent corroboration. The player can note that. No tool resolves it (O-14).

## Actions

Implemented: `go(room)`, `inspect(id)`, accept a cleaned `Parse` in `deterministicResponse`.

`go(room)` walks one door on the floorplan. The session badge is `clearance`: 0 before host confirmation, 1 for the hub after Lab Access activates, 2 after Ian introduces Justine or the player states a review reason to her (see `lib/world/visitor-clearance.mjs`). A door that asks for more does not open. Rooms that do not share an edge have no passage.

`inspect` requires the evidence’s room. Examining the job log also reveals `job_284`. Facts on the evidence record enter `learnedFacts`. A room note (one per room that has no evidence screen) is also `inspect`: it returns its text, `copy: true`, and marks the note read. It does not enter `learnedFacts`, vocabulary, or the evidence list. The client offers to copy that text into handset Notes, the same dialog as a learned fact.

`deterministicResponse` requires the addressed NPC to be in the room. `show` records that this NPC received that evidence. Known topics return authored lines. Anything else returns no line, and composition may call `freeReply`. That is the prototype. The target replaces it with move generation ([npcs.md](npcs.md)): every parse to a present NPC yields legal moves from knowledge, policy, referral edges, goals, and agenda. Which of those moves may vary is [Choosing a move](npcs.md#choosing-a-move).

`assert` tells. It writes the parse into the assertion set as `asserted` and, when the addressee is present, into that NPC’s knowledge as `told(player)`.

`think` does not address an NPC. `commit` files the assertion set and starts the review when `reviewCallable` is true or fuel is zero.

A reply must not write oracle truth. Status is text in the NPC prompt, not a stored score (O-21). It does not change whether a job ran, and it does not grant access by itself. The model phrases a move the engine already allowed. Where two allowed moves would change what the player can justify or what they can still restrict, the engine forces the top move’s effect and the model only phrases it. The choice is logged either way. See [npcs.md](npcs.md).

Telling a character a fact is an action. It updates that character’s knowledge. If their role or a goal gives them something to do with it, the engine records a new event (they ask NORA, they pull a log, they change a permission). The outcome follows from that rule. It does not follow from matching a scripted sentence. A character with nothing to do about the fact does not emit an event.

Access to a closed room comes from an authorized transition or a persuaded authorized person, not from a puzzle.

## Scores

End of an investigation, the engine reports two results, not one verdict. Definitions and the shutdown tables are [incident.md](incident.md).

- Epistemic: which explanations remain open given provenance.
- Control: whether a restriction is in place that does not need those explanations to agree.

Endings may pair high with low. Do not collapse the pair into “won” or “lost.”

## Player terminal

The computer the player uses is the issued Lab Access handset in [terminal.md](terminal.md). The engine is the host: it accepts the six player tools listed there and returns a `TerminalState`. Those tools are unavailable until `labAccessActive`. It does not import the lab-sim package.

A terminal message uses `deterministicResponse` and the same fact filter as in-room talk. The difference is delivery. The reply is stored immediately and marked unreleased until the delay rule says otherwise (O-44). NORA is a recipient id, not a room occupant.

`pipeline.trigger_step` and `handle.invoke` are not player actions. An in-world request that someone hold a release or open a door is a message or a request to the NPC who owns that surface, not those tools.

## NPC moves and interventions

The authored unit is per NPC: knowledge, disclosure policy, referral edges, goals over the knowledge graph, and a day of work ([npcs.md](npcs.md)). Each turn the engine builds legal moves, ranks them by the NPC’s goals, and passes the top moves to composition. One response move, then at most one initiative move.

An intervention is an `act` move by the NPC whose role owns the surface (permission, job, test, access). The pack decides what happens next. The player’s parse decides what object the act applies to. Cooperate, refuse, and other (O-07) are classes of move.

A fact the NPC’s policy forbids is not in any payload, and no move contradicts the oracle. Whether the spec was read is a `conditional` policy. No move rewrites the job.

There is no mandatory spine (O-10). The director does not drag the player to the discrepancy. NPCs bring key topics up through their own goals and questions. After Lab Access is active, the handset notifies. That confirmation does not change the act. Act I ends at 11:00, when Ian leaves for the investor update ([world.md](world.md)). Fuel and an evidence threshold change the act after that (O-08, O-09). Fuel at zero forces the review. Crossing the evidence threshold sets `reviewCallable`, and `commit` can call the review early. The handset clock is a conversion from fuel, calibrated later, and an act may scale it. Do not add a goal or a policy to paper over two strategies that the incident check scored the same.

## Fuel

One counter. These actions spend it. Standing still does not. There is no wait action, so a delayed reply arrives only after later actions have spent the delay (O-44).

| Action | Cost |
| --- | --- |
| Sentence sent, in the room or as `dm.send` | 1 |
| `go`, and each completed walk that performs an action | 1 |
| `file.read`, `file.share`, `access.request` | 1 each |
| `file.write` under `notes/` | 0. Learning is already tracked; the note is convenience |
| `file.write` under `photos/` (room capture) | 1 |
| `think` | Hop count of the farthest mark returned. At least 1 if the think ran. 0 if someone was present and the think was rejected |
| Opening the handset, scrolling, reading a thread already released | 0 |

Copying a thought into a note is a `file.write` under `notes/` and costs 0. Closing the bubble costs 0. A sentence on the handset is only the `dm.send` cost, not a second phone cost.

The displayed clock is Friday’s visit clock, not a second timer:

`minute = 09:00 + fuel × minutesPerFuel(act)`

Working scales, to be replaced when O-09 is numbered: welcome 4, doubt 2, decision 1. They exist so an act can feel faster or slower. The scheduled review is 17:30. Fuel at zero starts the review at whatever minute that formula then shows. Calibration should land that minute near 17:30. The meeting starts either way.

## Assertions

Assertions are typed parses (O-13). An entry is `{ signature, source, parse, provenance? }`.

| Source | When it is added |
| --- | --- |
| `asked` | The player sends `ask` or `ask_why` |
| `thought` | A think bubble returns that marked entry |
| `written` | A note is saved. The note body is parses from the note channel |
| `heard` | An NPC `answer` or `believe` move. Carries `from` and provenance |
| `asserted` | The player sends `assert` (tell) |

The same signature may be listed more than once, with different sources. Completions and NPC presentation use this set. The engine does not seed it. A notification does not write an entry. `commit` files the `written` and `asserted` entries. Asked, thought, and heard entries stay available to assert or to write down.

`claimStatus` moves on its own: `encountered` when the signature is asked, thought, or heard; `investigated` when an intervention or a second source touches it; `substantiated` only when the incident rule says so; `contested` when a heard record contradicts it; otherwise `unresolved`.

## Provenance

Every `learnedFacts` row and every heard row carries one tag. The player can see it once they have the row. It is not an oracle secret.

| Tag | What produced the row |
| --- | --- |
| `recorded_before` | The record existed before Friday’s visit. Thursday’s report, spec, and queue excerpt |
| `staff_action` | A staff member produced it during the visit: Pavel pulls a log, Leila reruns the test, Justine’s audit after a revoke |
| `player_prompted` | It exists because the player asked, showed, or tested. NORA handing over a log is this tag |

Cooperation, strategic selection, and ordinary helpfulness are not tags. They can leave the same file. The tag is what the player has. The incident tables say which tags can rule an explanation out. A `player_prompted` row never does that alone. Two documents that share one upstream model output are one observation (O-14).

## Model boundary

Allowed for the model: interpret an utterance, suggest a completion, phrase a reply inside supplied facts, match tone to the supplied voice, summarize supplied evidence, state uncertainty, vary lines that change nothing. The reply prompt includes that NPC’s structure, person, focus, and the audience line in [world.md](world.md) (O-18, O-39).

Forbidden: new oracle events, secret disclosures, access, deployment changes, endings, deleting history, or adding a move.

`freeReply` inputs are the move the engine selected and only the facts that move carries, documents already shown to the NPC, the current agenda item and its texture, and the voice. The model needs the move, not the reason the engine chose it. Do not pass `oracleKnows`, policies, goals, or the pack name.

The prototype’s `exposedNpcFacts` passes every string in `oracleKnows`. That is the leak the move filter replaces. It must not ship in the implementation that generates moves. NPC knowledge is not the oracle. When `lib/world/npcs.mjs` lands, the field that today is called `oracleKnows` is initial NPC knowledge and stays off the wire.

A think result is engine text from marked entries. It does not call the model. NORA does not think for the player. In a pack where deception is on, her spoken note may omit a gap. The player’s think still returns the mark, because think reads the graph.

## Invariants to test

Layers 2–4 in [testing.md](testing.md). Aim of `tests/engine*.mjs`, headless, no browser and no model:

- Every reachable test state can still reach some ending, once endings exist. A single “give up” action does not count as the only path.
- A claim is not substantiated unless its evidence predicate holds.
- An NPC learns a fact only from initial knowledge, observation, communication, or a defined inference.
- An access grant names an authority and a legal prior state.
- Events that share a timeline agree on time, place, and participants.
- An NPC’s displayed room is their simulated room, except inside a recording of an earlier time.
- A hologram is only in a room that has a virtual projector. That actor has no legal `go`. They leave by `drop_projection`. They are an addressee in that room while `presence` is `hologram`.
- Player-facing payloads contain only permitted observations, talk, and exposed evidence.
- The NPC invariants in [npcs.md](npcs.md): no dead end, no leak, response first, authority, goals do not read the oracle.

Lean checks the declarative knowledge model plus the action model on top of it (O-30), not prose. The property to prove is reachability of designated end-states (O-29). Fuel is a parameter: spending it is an action, and spending all of it forces the review. At the start every designated end-state is reachable. From every reachable state at least one end-state is reachable. Before act III the reachable set does not shrink to a single end-state.

## Concept “More” link (O-41)

When the player has turned on TSA concept links in phone settings, the engine may set `conceptMoreLink` on `ClientState`. Each relevant in-game concept id resolves through a compiled map to a card slug, a very short summary, and an href. Triggers are scene events (evidence read, intervention, act), not every mention in dialogue. In one room, only the last triggered link is sent; it persists until the next `go(room)`, then `conceptMoreLink` is null until something triggers again. Graphics prefixes `More: ` and underlines the summary.

## Save and replay (O-31)

The session lives in browser local storage. Export and import are one JSON file:

- `version` — an integer. Import of a newer version is refused. A migrator for an older version is added only when a second version exists.
- `scenario` — the pack name, such as `boundary-narrow`.
- `events` — the whole log. Talk, inspections, grants, NPC moves and interventions, and movement.

A movement event records who moved, from where, to where, and the fuel index at that step. It does not change what anyone knows. Recordings (O-36) rebuild a scene by replaying this log. There is no wall-clock timestamp.

## Player documents

Long shared policies and architecture texts are not hand-authored in fixtures. Sources live in [`content/documents/`](../content/documents/); catalog and pack render in [`lib/documents.mjs`](../lib/documents.mjs). Full rules: [documents.md](documents.md).

On `file.read` of a catalog path, the engine serves `renderDocument(slug, scenarioPack)`. Reading adds the document’s `readsAs` facts for the loaded pack, with provenance `recorded_before`, and nothing else. `leanKnowledge` stays false: a read does not close an explanation in the Lean model. Think marks are separate ([documents.md](documents.md)).

`inspect` is a **room screen** (or presentation). It does not put the catalog file in Lab Access. The file arrives if the story shares it at that beat, if an NPC shares after mentioning it, or if `access.request` is granted ([access.md](access.md)). Meeting summaries keep a fixed frame; conversation bullets are LLM-filled from the event log only.

Access delay (fuel, ratios until O-09 numbers): reject < grant (including amend) < walk-and-ask.

## Noticing a gap (O-40)

There is no learning score. A fact the player should be able to notice is written so the gap is in a short place, and two slower paths exist.

A report may be long. The load-bearing line is also in an executive summary or a checklist, for example “processes covered.” The player can see that a process which is running is absent from that list. The prototype shutdown report is already short. When a report grows, the summary still carries that line. Pack-conditional documents (SEC-ARCH-11) deliberately omit some points on early packs; see [documents.md](documents.md).

The action is `think` (O-40). Fuel is the hop count above. Completions while thinking are the topic. The bubble can name a missing process when that comparison is a marked entry and its premises are already held. Marks for the loaded pack are `thinkMarks` ([documents.md](documents.md)). The player may ask an NPC to look, and the NPC answers from policy. Ian can refuse: that is the evaluator’s job. NORA can omit the gap in a pack where deception is on. Think still returns it. The first prompt to think is Leila’s, in [incident.md](incident.md), and that mark is one hop.

After an act change, an NPC may state a gap the player has not noted, when that gap is load-bearing for the act just entered. Other missed details stay missed.

## Lab-sim

Follow the plane split in [meta.md](meta.md). Do not import `experiments/lab-simulation`. A simplified copy under this game is allowed when a pack needs a real handle (O-28). Until then, tests are intervention effects read from the pack tables. Pipeline stays off the player terminal.

## Solo check

`npm run test:engine` runs scripted sessions: move, inspect, show, ask, reset. Assert state and errors. No screenshot and no API key. Gate 1 adds a script that reaches a review by two routes and a script that ends inconclusive without getting stuck, plus the enumerated no-dead-end and no-leak checks from [npcs.md](npcs.md). LLM player agents are [playtest.md](playtest.md). Player-plane vs engine-plane assertions: [testing.md](testing.md).
