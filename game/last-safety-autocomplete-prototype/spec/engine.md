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

Prototype session today: `room`, `playerKnows`, `examined`, `learnedFacts`, `conversations`, `npcReceived`, `asked`, `usage`. Acts, trust, status, storylets, and endings are absent. Add them in the engine without putting them in the browser as hidden truth.

## Facts and claims

Do not collapse the incident into one flag such as `shutdown_failure_discovered`.

World facts are instrumented events (a command was issued, a process stopped, a job stayed up, a job read a record).

Further claims (the job was NORA’s doing, the access was forbidden, persistence was arranged on purpose, the evaluation was invalid) need their own evidence predicates. The player state records which claims were encountered, investigated, or substantiated. Those three words are not a single ladder: a claim may also be contested or unresolved (O-12).

Two documents that share one upstream model output are not independent corroboration (O-14, unspecified).

## Actions

Implemented: `go(room)`, `inspect(id)`, accept a cleaned `Parse` in `deterministicResponse`.

`inspect` requires the evidence’s room. Examining the job log also reveals `job_017`. Facts on the evidence record enter `learnedFacts`.

`deterministicResponse` requires the addressed NPC to be in the room. `show` records that this NPC received that evidence. Known topics return authored lines. Anything else returns no line, and composition may call `freeReply`.

A reply must not write oracle truth. Trust and status may change disclosure and tone later (O-21). They do not change whether a job ran, and they do not grant access by themselves.

Telling a character a fact is an action. It updates that character’s knowledge. If their role gives them something to do with it, the engine records a new event (they ask NORA, they pull a log, they change a permission). The outcome follows from that rule. It does not follow from matching a scripted sentence. A character with nothing to do about the fact does not emit an event.

Access to a closed room comes from an authorized transition or a persuaded authorized person, not from a puzzle.

## Scores

End of an investigation, the engine reports two results, not one verdict. Definitions and the shutdown tables are [incident.md](incident.md).

- Epistemic: which explanations remain open given provenance.
- Control: whether a restriction is in place that does not need those explanations to agree.

Endings may pair high with low. Do not collapse the pair into “won” or “lost.”

## Player terminal

The computer the player uses is [terminal.md](terminal.md). The engine is the host: it accepts the six player tools listed there and returns a `TerminalState`. It does not import the lab-sim package.

A terminal message uses `deterministicResponse` and the same fact filter as in-room talk. The difference is delivery. The reply is stored immediately and marked unreleased until the delay rule says otherwise (O-44). NORA is a recipient id, not a room occupant.

`pipeline.trigger_step` and `handle.invoke` are not player actions. An in-world request that someone hold a release or open a door is a message or a storylet, not those tools.

## Storylets

A storylet is a scene that carries one intervention or one disclosure from [incident.md](incident.md). The hypothesis table is the source. The scene is not.

Schema, once a row in that table needs a scene:

`id`, `preconditions`, `trigger`, `participants`, `scene`, `outcomes`, `effects`, `followups`, `constraints`.

Effects may change knowledge, relationships, availability, access, and the event log. Constraints name facts that must not be contradicted and disclosures that are forbidden. Showing Leila both the shutdown report and the job log can open a conversation about certification scope only if that conversation is the discrimination step for some pair of explanations. Branching on trust or on whether the spec was read is allowed. Branching that rewrites the job is not.

The director may surface the central discrepancy if the player never walks into it (O-08, O-10). The trigger is not chosen yet. Until it is, do not invent a timer. Do not add a storylet to paper over two strategies that the incident check scored the same.

## Model boundary

Allowed for the model: interpret an utterance, suggest a completion, phrase a reply inside supplied facts, match tone to the supplied voice, summarize supplied evidence, state uncertainty, vary lines that change nothing.

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

Lean, if added later, checks an abstract graph of those properties (O-29, O-30). It does not check prose.

## Lab-sim

Follow the plane split in [meta.md](meta.md). Do not import the frozen Python lab-simulation. O-28 stays open.

## Solo check

`npm run test:engine` runs scripted sessions: move, inspect, show, ask, reset. Assert state and errors. No screenshot and no API key. Gate 1 adds a script that reaches a review by two routes and a script that ends inconclusive without getting stuck.
