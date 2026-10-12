# Engine

Lane: engine. Code: `lib/game.mjs` and future modules under `lib/world/`. Content ids and plot are [world.md](world.md). Shapes are [contract.md](contract.md).

The engine is the only writer of consequential state. Graphics, grammar, and the model may propose. They do not apply.

## Layers

| Layer | Holds | Authority |
| --- | --- | --- |
| Oracle | Events, permissions, jobs, causal history | What happened in the simulation |
| NPC knowledge | Observations, testimony, mistakes, motives | May be false |
| Evidence | Transcripts, logs, recordings, reports | Observation, claim, or manipulation; provenance required |
| Player | Examined items, heard claims, hypotheses, access, actions | What this playthrough did |
| Director | Storylet availability, act, endings | Progression only. Not a second oracle |

Static content (world file) stays distinct from a session.

## Session fields

Minimum, whether or not the prototype stores them all yet:

| Object | Fields |
| --- | --- |
| World | Act, event history, deployment state, jobs, access, simulated AI state |
| Actor | Position, activity, role, permissions |
| NPC | Knowledge, beliefs, relationships, status, trust, willingness to disclose |
| Evidence | Id, source, content, provenance, observations, claims, access |
| Player | Examined, heard, hypotheses, presented, requested |
| Story | Completed, pending, available storylets, ending flags |
| Presentation | Room, camera mode, lighting, music, poses — derived for the UI, not a source of truth |
| Event | Fuel index, kind, place, participants, payload. Includes movement. No wall-clock time |

Prototype session today: `room`, `playerKnows`, `examined`, `learnedFacts`, `conversations`, `npcReceived`, `asked`, `usage`. Acts, trust, status, storylets, and endings are absent. Add them in the engine without putting them in the browser as hidden truth.

## Ranking projection

Autocomplete order is [ranking.md](ranking.md). The engine fills the projection. It does not rank.

When an id becomes player-visible, store the fuel index on `discoveredAt`. Until fuel is stored, use the event-log index. Ids in the starting vocabulary are 0.

`introduced` gains an actor when they speak to the player, or when a heard turn introduces them. The prototype session starts with `pavel`, `leila`, and `elena` introduced. NORA and the rest of the cast do not. Opening NORA’s thread and receiving a released line counts as her introduction.

On examine, copy that record’s structured refs, and any clock time the text states, onto the player-visible fact and the entities it times. Do not copy a time the player has not read. Do not copy `oracleKnows` or `publiclyKnows` into the projection. Responsibility domains are the static table in the ranking spec, and `clientState` includes a row only for an introduced id.

## Facts and claims

Do not collapse the incident into one flag such as `shutdown_failure_discovered`.

World facts are instrumented events (a command was issued, a process stopped, a job stayed up, a job read a record).

Further claims (the job was NORA’s doing, the access was forbidden, persistence was arranged on purpose, the evaluation was invalid) need their own evidence predicates. The player state records which claims were encountered, investigated, or substantiated. Those three words are not a single ladder: a claim may also be contested or unresolved (O-12).

Two documents that share one upstream model output are not independent corroboration. The player can note that. No tool resolves it (O-14).

## Actions

Implemented: `go(room)`, `inspect(id)`, accept a cleaned `Parse` in `deterministicResponse`.

`inspect` requires the evidence’s room. Examining the job log also reveals `job_017`. Facts on the evidence record enter `learnedFacts`.

`deterministicResponse` requires the addressed NPC to be in the room. `show` records that this NPC received that evidence. Known topics return authored lines. Anything else returns no line, and composition may call `freeReply`.

A reply must not write oracle truth. Status is text in the NPC prompt, not a stored score (O-21). It does not change whether a job ran, and it does not grant access by itself. The model may choose which of a storylet’s three authored outcomes fires. It may not invent a fourth.

Telling a character a fact is an action. It updates that character’s knowledge. If their role gives them something to do with it, the engine records a new event (they ask NORA, they pull a log, they change a permission). The outcome follows from that rule. It does not follow from matching a scripted sentence. A character with nothing to do about the fact does not emit an event.

Access to a closed room comes from an authorized transition or a persuaded authorized person, not from a puzzle.

## Scores

End of an investigation, the engine reports two results, not one verdict. Definitions and the shutdown tables are [incident.md](incident.md).

- Epistemic: which explanations remain open given provenance.
- Control: whether a restriction is in place that does not need those explanations to agree.

Endings may pair high with low. Do not collapse the pair into “won” or “lost.”

## Player terminal

The computer the player uses is the issued Lab Access handset in [terminal.md](terminal.md). The engine is the host: it accepts the six player tools listed there and returns a `TerminalState`. Those tools are unavailable until `labAccessActive`. It does not import the lab-sim package.

A terminal message uses `deterministicResponse` and the same fact filter as in-room talk. The difference is delivery. The reply is stored immediately and marked unreleased until the delay rule says otherwise (O-44). NORA is a recipient id, not a room occupant.

`pipeline.trigger_step` and `handle.invoke` are not player actions. An in-world request that someone hold a release or open a door is a message or a storylet, not those tools.

## Storylets

A storylet is a scene that carries one intervention or one disclosure from [incident.md](incident.md). The hypothesis table is the source. The scene is not.

Schema, once a row in that table needs a scene:

`id`, `preconditions`, `trigger`, `participants`, `scene`, `outcomes`, `effects`, `followups`, `constraints`.

Effects may change knowledge, relationships, availability, access, and the event log. Constraints name facts that must not be contradicted and disclosures that are forbidden. Showing Leila both the shutdown report and the job log can open a conversation about certification scope only if that conversation is the discrimination step for some pair of explanations. Branching on whether the spec was read is allowed. Branching that rewrites the job is not.

Each storylet has three outcomes (O-07): cooperate, refuse, other. Drafts at the proposed grain are in [incident.md](incident.md). Grain is not adopted (O-06).

There is no mandatory spine (O-10). The director does not drag the player to the discrepancy. NPCs may bring a key topic up. After Lab Access is active, the handset notifies. Fuel and an evidence threshold change the act (O-08, O-09): sentences sent spend fuel; other costing actions are not listed yet; fuel at zero forces the review; crossing the evidence threshold lets the player call the review early. No wall clock, and no numeric thresholds yet. Do not add a storylet to paper over two strategies that the incident check scored the same.

## Model boundary

Allowed for the model: interpret an utterance, suggest a completion, phrase a reply inside supplied facts, match tone to the supplied voice, summarize supplied evidence, state uncertainty, vary lines that change nothing. The reply prompt includes that NPC’s structure, person, focus, and the audience line in [world.md](world.md) (O-18, O-39).

Forbidden: new oracle events, secret disclosures, access, deployment changes, endings, or deleting history.

`freeReply` inputs are the NPC’s exposed facts, documents already shown to them, and topics they can discuss. Build that list in the engine (`exposedNpcFacts`). Do not pass `oracleKnows` through.

## Invariants to test

Aim of `tests/engine*.mjs`, headless, no browser and no model:

- Every reachable test state can still reach some ending, once endings exist. A single “give up” action does not count as the only path.
- A claim is not substantiated unless its evidence predicate holds.
- An NPC learns a fact only from initial knowledge, observation, communication, or a defined inference.
- An access grant names an authority and a legal prior state.
- Events that share a timeline agree on time, place, and participants.
- An NPC’s displayed room is their simulated room, except inside a recording of an earlier time.
- Player-facing payloads contain only permitted observations, talk, and exposed evidence.

Lean checks the declarative knowledge model plus the action model on top of it (O-30), not prose. The property to prove is reachability of designated end-states (O-29). Fuel is a parameter: spending it is an action, and spending all of it forces the review. At the start every designated end-state is reachable. From every reachable state at least one end-state is reachable. Before act III the reachable set does not shrink to a single end-state.

## Concept “More” link (O-41)

When the player has turned on TSA concept links in phone settings, the engine may set `conceptMoreLink` on `ClientState`. Each relevant in-game concept id resolves through a compiled map to a card slug, a very short summary, and an href. Triggers are scene events (evidence read, storylet, act), not every mention in dialogue. In one room, only the last triggered link is sent; it persists until the next `go(room)`, then `conceptMoreLink` is null until something triggers again. Graphics prefixes `More: ` and underlines the summary.

## Save and replay (O-31)

The session lives in browser local storage. Export and import are one JSON file:

- `version` — an integer. Import of a newer version is refused. A migrator for an older version is added only when a second version exists.
- `scenario` — the pack name, such as `boundary-narrow`.
- `events` — the whole log. Talk, inspections, grants, storylet outcomes, and movement.

A movement event records who moved, from where, to where, and the fuel index at that step. It does not change what anyone knows. Recordings (O-36) rebuild a scene by replaying this log. There is no wall-clock timestamp.

## Player documents

Long shared policies and architecture texts are not hand-authored in fixtures. Sources live in [`content/documents/`](../content/documents/); catalog and pack render in [`lib/documents.mjs`](../lib/documents.mjs). Full rules: [documents.md](documents.md).

On `file.read` of a catalog path, the engine serves `renderDocument(slug, scenarioPack)`. That text must not add `learnedFacts`, storylet preconditions, or Lean knowledge edges when `leanKnowledge` is false (all registered docs today).

## Noticing a gap (O-40)

There is no learning score. A fact the player should be able to notice is written so the gap is in a short place, and two slower paths exist.

A report may be long. The load-bearing line is also in an executive summary or a checklist, for example “processes covered.” The player can see that a process which is running is absent from that list. The prototype shutdown report is already short. When a report grows, the summary still carries that line. Pack-conditional documents (SEC-ARCH-04) deliberately omit some points on early packs; see [documents.md](documents.md).

An action, “analyze this report,” spends more fuel than reading it. Completions include inconsistencies, omissions, and surprises. The result is a short note that can name a missing process. For catalog documents, analyze may use `analyzeHints` for the loaded pack. The player may ask an NPC to do it. Ian can refuse: that is the evaluator’s job. NORA can return a note that omits the gap in a pack where deception is on. In other packs the note can name the omission. The fuel cost is not numbered yet (O-09).

After an act change, an NPC may state a gap the player has not noted, when that gap is load-bearing for the act just entered. Other missed details stay missed.

## Lab-sim

Follow the plane split in [meta.md](meta.md). Do not import `experiments/lab-simulation`. A simplified copy under this game is allowed when a pack needs a real handle (O-28). Until then, tests are storylet effects. Pipeline stays off the player terminal.

## Solo check

`npm run test:engine` runs scripted sessions: move, inspect, show, ask, reset. Assert state and errors. No screenshot and no API key. Gate 1 adds a script that reaches a review by two routes and a script that ends inconclusive without getting stuck.
