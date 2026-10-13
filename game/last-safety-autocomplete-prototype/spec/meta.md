# Meta

Source: consolidated design v0.1 (9 October 2026), sections 1, 11, and 14. Working status: concept, plus a conversation prototype. Not an implementation-ready narrative.

## What the game is

A browser investigation set in a small automated AI lab. The player is an external evaluator reviewing NORA before a deployment decision at the end of one in-game day. Play is exploration, conversation, and evidence, with autocomplete so long typing is optional.

The central question: whether the lab has identified the system it needs to control, assembled evidence that supports its claims, and kept the ability and the willingness to correct failures.

TSA concepts are carried by events. The plot is not a quiz, and it is not required to cover every bridge.

## Principles

1. Investigate rather than answer a quiz.
2. No designated villain. An anomaly may be technical, organizational, accidental, or strategic.
3. Partial knowledge. No character knows everything; witnesses can be wrong.
4. The system is larger than the model.
5. Multiple paths, one consistent world.
6. Minimal typing, meaningful agency.
7. Outcomes follow evidence and decisions. Do not plant a discovery to reward a preferred reading.
8. Formal checks where feasible: typed state, deterministic transitions, provenance, access, reachability.
9. Economical art: modular assets, fixed cameras, shared rendering rules.
10. Narrative priority. Concepts explain the plot; the plot is not a disguised lesson sequence.
11. The player is part of the measurement. Evidence about NORA and evidence NORA produced because it was being evaluated are different, and the game keeps them different. This is not a reveal that the player was manipulated.
12. Epistemic success and control success are separate. Identifying an intention is not the same as having a restriction that works. Either one can be high while the other is low.
13. Author the hypothesis, then the knowledge. NPCs disclose and intervene by pursuing goals over what they know ([npcs.md](npcs.md)). A scene is what that produces, not what is authored.

## Status labels

Use these when a spec states a fact:

- **Confirmed** — accepted in design discussion.
- **Working** — incorporated without objection; provisional.
- **Recommended** — a concrete proposal, not selected.
- **Open** — needs a decision. Ids below. Do not close an open item inside a lane spec.

## TSA coverage

Strong in the current design: MB1 boundary, MB4 correction, MB4a audit independence, MB6 selection (as a mechanism), MB7 hidden capability and adversarial oversight, MB9 grounding, MB11 deployment.

Partial: MB2 value bundle, MB3 value referents. Weak: MB8 extrapolated volition. Absent on purpose for now: MB5 successor stability, MB7d acausal coordination, MB10 successor audit forgeability.

Thesis claims in play: boundary, value bundle, grounding, correction, selection. NORA’s lineage is background only ([world.md](world.md)): successor 4 of the lab’s line, partial self-design of tools and proposals, training still Jun’s, promotions still Ian’s. That note does not add a successor plot. MB5 and MB10 stay absent.

The four questions: certifying continued tracking is the main activity; determining the target is partial (Amara); constructing a tracking system is weak (the player is not the designer); recovery is partial (the player can request an intervention).

Also in play, at narrative strength: evaluation awareness, metric laundering, the gap between a coherent safety argument and a justified deployment claim, observation versus causal or strategic explanation.

## Non-goals

Successor alignment, ontology shift, acausal coordination, and a general method for constructing aligned systems. No humanoid NORA. No receptionist, guards, or background staff. No continuous day–night clock. No unilateral player authority over shutdown, policy, or promotions.

## Decisions (10 October 2026)

Gunnar. These supersede consolidated §14 for O-01–O-30. The consolidated doc is unchanged.

| Id | Status | Decision |
| --- | --- | --- |
| O-01 | working | No single hidden history. Campaigns are packs in [incident.md](incident.md). The first pack is boundary-too-narrow. Other book failure modes are other packs. |
| O-02 | working | Both. Deception is off in some packs and on in others. Packs are also the difficulty ladder. |
| O-03 | working | Partial escape is defined per pack, inside the building. The same word is not one mechanic. |
| O-04 | working | Per pack. In the first pack the revelation is the boundary mismatch: the certificate is about the model process, and the system that acted is wider. |
| O-05 | working | Play the immediate effect of the decision (stop, revoke, hold, release). Leave later consequences unnarrated. Where the pack makes it plausible, show that the immediate action did not cover the system. |
| O-06 | working | 13 October: storylets retired. NPCs have knowledge, disclosure policies, referral edges, goals over the knowledge graph, and a day of work. The engine generates legal moves and the model phrases one ([npcs.md](npcs.md)). The 10 October drafts are rewritten in those terms in [incident.md](incident.md). |
| O-07 | working | Three structural outcomes: cooperate (progress, reveal), refuse (delay, prerequisite), other. Since O-06 they classify NPC moves; they are not authored branches. |
| O-08 | working | An act changes when an evidence threshold is met, or when fuel runs out. Fuel counts sentences sent. Which other actions spend fuel is still open. No wall clock. |
| O-09 | working | The budget is that fuel. Exhausting it forces the review (clock forcing in O-29). Meeting the evidence threshold lets the player call the review sooner. Thresholds are not numbered yet. |
| O-10 | closed | No mandatory spine. Missing the central problem is allowed. NPCs bring key topics up. After Lab Access is active, the handset blinks when a notification is waiting. |
| O-11 | closed | Those topics and notifications are the hints. A notification points at a topic or a file. It does not state an oracle fact. |
| O-12 | open | Substantiation waits on the incident model. |
| O-13 | working | Hypotheses are player notes on the phone. The engine does not seed them. A notification does not write a note. |
| O-14 | closed | No tool resolves correlated sources. The player may write a note about them. |
| O-15 | closed | No player-facing probability. The two scores stay a set of open explanations and a yes/no restriction. If an NPC prompt needs uncertainty, the engine supplies words and the model speaks words. A number on screen is fuel, or a figure already printed in a document. |
| O-16 | working | Tests are a fixed handle list (rerun shutdown, revoke a job’s permission, camera archive, shared meeting summary, pilot results with permission, hypotheticals with Amara). The player does not invent a procedure. Each handle is an intervention by the NPC who owns the surface ([npcs.md](npcs.md)). A simplified lab-sim is what would make a handle a mechanism rather than a pack-table flag. Pipeline stays off the phone. |
| O-17 | closed | The eight humans stay. NORA is spoken to on the terminal, not as a ninth body. |
| O-18 | working | Prompt paragraphs are in [world.md](world.md) for review. Facts, policies, and goals are authored. Wording is mostly the model. |
| O-19 | working | Rank by shortest paths on a projection of player-visible state: domains, public roles after introduction, document time, and discovery fuel. The prefix filters. Diversity is a small bonus. Oracle facts, asked-line penalties, and NPC goal lookahead stay out. Spec: [ranking.md](ranking.md). |
| O-20 | closed | “Genuinely new” meant a suggestion the author did not write. The grammar already accepts open text (`relation: "open"`). Novel wording is allowed. It does not create an engine action. |
| O-21 | closed | No separate status arithmetic. Status lives in the NPC prompt. The model picks which of the engine’s top moves to phrase, from how the player acted. It cannot add a move. (Before O-06 this was one of three authored outcomes.) |
| O-22 | open | Each NPC will have a concealment list, chosen when a pack’s plot needs it. Since O-06 these are `conceal` policy entries applied by the engine’s move filter, not by prompt ([npcs.md](npcs.md)). The lists are not written yet. |
| O-23 | working | Amara: a conversation about her work and a simplified value bundle. She is remote in body. In Evaluation she is a hologram on the virtual projector (same interaction as other NPCs; no remote-call UI). She cannot leave that room; she disappears. Contacts once introduced; player may ask her to join. She answers hypotheticals. She runs no experiment. Pilot results are a file, behind permission. |
| O-24 | working | In a pack that features the B plot, solving it adds oversight or changed incentives on top of the normal ending. In the Goodhart pack the B plot is the center and is more complicated. In the false-positive pack the B plot is the false positive and does not add that ending. |
| O-25 | working | The add-on is more external oversight or changed incentives. Goodhart makes that problem the meeting. The false-positive pack does not unlock it. |
| O-26 | working | The meeting follows evidence presented and conclusions derived, including objections that fill a hole in that presentation. Persuasion is small and covers only holes the player did not investigate. |
| O-27 | open | A coherent wrong institutional decision is allowed. Do not build it until a pack needs it. |
| O-28 | working | A simplified copy of the lab-sim may live under the game, isolate planes kept. Do not import `experiments/lab-simulation`. Whether the copy is needed is still open. Pipeline TBD. |
| O-29 | working | Lean proves reachability of designated end-states on the declarative model. Fuel is the forcing parameter. At the start every designated end-state is reachable. From every reachable state at least one is. The set of reachable end-states does not shrink to one before act III. |
| O-30 | working | A declarative knowledge model, plus an action model on top of it, drives the game. Lean checks that declarative model. The language model sits above actions. |
| O-31 | working | Browser local storage. Export and import are JSON with a `version` and a `scenario` name. Every event is stored, including movement. The clock on an event is fuel, not a wall-clock time. |
| O-32 | working | Player input is one sentence. Proposed cap is 100 characters, and that number is tentative. Special characters are stripped. No jailbreak defense in this build. |
| O-33 | closed | Stay with live Three.js. One fixed camera per room. Asset kit still open; procedural bodies stand in. |
| O-34 | working | Current procedural characters are enough. More detail, if it comes, is for conversations. |
| O-35 | working | Current motion is enough. More detail, if it comes, is for conversations. |
| O-36 | working | A recording is the event log replayed in the room. The phone’s video app can fast-forward, rewind, and jump to the next or previous room. |
| O-37 | open | Music waits until the story is set. |
| O-38 | working | Current phone layout is enough. Tune it later. |
| O-39 | working | General audience. Terms arrive after the scene has introduced them, except AI, safety review, and alignment. Each NPC prompt has a focus and explains those words when asked. |
| O-40 | working | No separate learning score. A load-bearing gap is noticeable in a report’s summary or checklist, costs fuel if an analysis action is used, and may be spoken by an NPC after an act change. |
| O-41 | working | Phone setting (default off). When on, the room view shows one line at the bottom: `More: ` plus a very short underlined summary linking to the matching companion-site concept card. URLs are compiled from in-game concept ids and the repo knowledge graph (`metadata/concepts.yml`, concept-graph). Only the most recently relevant link is shown; it stays until the player leaves the room. |
| O-45 | open | NPC model numbers: goal cooldown, stall length for the director, agenda band boundaries inside an act. |
| O-46 | open | Whether `pendingQuestion` goes on `ClientState` so grammar can offer reply openings to an NPC’s question (contract change). Recommended in [npcs.md](npcs.md). |
| O-47 | open | Playtest thresholds for work-only rate, repeat rate, and stall interventions. Frozen before the first LLM run ([playtest.md](playtest.md)). |
| O-43 | working | Access explorer: top folders and services; list/read/write; children hidden until list. Amendments (e.g. Justine) may grant a specific file plus Chat. No camera-archive node. Files are not autocomplete picks. Delay order: reject < grant < walk-and-ask. [access.md](access.md). |

## Open questions

O-12 substantiation. O-22 concealment lists. O-45 NPC model numbers. O-46 `pendingQuestion` in the contract. O-47 playtest thresholds. O-27 whether a coherent wrong decision is needed. O-28 whether the simplified lab-sim is actually needed; pipeline TBD. O-37 music, after the story is set. O-42 duration (earlier hopes: 20–30 minutes for a first playable slice, 20–45 for a full investigation; untested). The 100-character cap (O-32) is tentative.

Player terminal: O-44 how long a human reply waits, and how that differs for NORA. Access grants use a separate delay (reject < grant < walk-and-ask; [access.md](access.md)). Placement is a generic phone overlay—working. The pipeline stays off the terminal. See [terminal.md](terminal.md).

## Later

A transfer check is out of scope for this build: after the game, a short unrelated case (a hospital system, a research assistant) with a reassuring safety report, scored on whether the player names a missing boundary, a bad evidence source, or an incentive. It is not a gate and not a scene inside the lab. Do not author it while the shutdown model is unfinished.

## Lab-sim

The design reuses the lab-simulation idea of separate planes: oracle, what a role can see, and audit surfaces. O-28 is a simplified copy under the game, isolate kept, not an import of `experiments/lab-simulation`. Do not add that copy until a pack needs a handle the pack-table flags cannot express. Pipeline TBD.

The player computer is specified against that isolate tool list anyway. See [terminal.md](terminal.md). That does not import the Python sim.
