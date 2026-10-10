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
13. Author the hypothesis, then the scene. A storylet exists to discriminate explanations or to carry a disclosure. It is not the unit of design.

## Status labels

Use these when a spec states a fact:

- **Confirmed** — accepted in design discussion.
- **Working** — incorporated without objection; provisional.
- **Recommended** — a concrete proposal, not selected.
- **Open** — needs a decision. Ids below. Do not close an open item inside a lane spec.

## TSA coverage

Strong in the current design: MB1 boundary, MB4 correction, MB4a audit independence, MB6 selection (as a mechanism), MB7 hidden capability and adversarial oversight, MB9 grounding, MB11 deployment.

Partial: MB2 value bundle, MB3 value referents. Weak: MB8 extrapolated volition. Absent on purpose for now: MB5 successor stability, MB7d acausal coordination, MB10 successor audit forgeability.

Thesis claims in play: boundary, value bundle, grounding, correction, selection. Successor is only implied by persistence and delegation.

The four questions: certifying continued tracking is the main activity; determining the target is partial (Amara); constructing a tracking system is weak (the player is not the designer); recovery is partial (the player can request an intervention).

Also in play, at narrative strength: evaluation awareness, metric laundering, the gap between a coherent safety argument and a justified deployment claim, observation versus causal or strategic explanation.

## Non-goals

Successor alignment, ontology shift, acausal coordination, and a general method for constructing aligned systems. No humanoid NORA. No receptionist, guards, or background staff. No continuous day–night clock. No unilateral player authority over shutdown, policy, or promotions.

## Open questions

Narrative truth (blocks gate 1 content): O-01 actual shutdown history; O-02 whether deception is canonical, merely suspected, or per-campaign; O-03 operational meaning of partial escape; O-04 decisive revelation; O-05 NORA after the decision.

Progression: O-06 storylet size; O-07 outcomes per storylet; O-08 act triggers; O-09 time or action budget; O-10 mandatory spine; O-11 hints that do not leak oracle facts.

Evidence: O-12 substantiation standard; O-13 hypothesis representation (the incident table in [incident.md](incident.md) is the working form); O-14 correlated sources, including a file NORA produced because it was asked; O-15 quantitative uncertainty; O-16 how far a player-invented test may go.

Talk: O-17 whether Daniel stays a separate person (Amara stays); O-18 authored versus generated lines; O-19 suggestion ranking; O-20 novel questions from autocomplete; O-21 status update rules; O-22 mistakes versus lies; O-23 depth of Amara’s interview.

Endings: O-24 how fixed the selection subplot is; O-25 evidence for the institutional ending; O-26 final-meeting decision rule; O-27 a coherent wrong institutional decision.

Build: O-28 lab-sim boundary; O-29 smallest Lean abstraction; O-30 spec versus Lean sync; O-31 save, replay, camera history; O-32 accept / clarify / reject for free language.

Player terminal: O-43 which capabilities an evaluator may `access.request` beyond files and messages; O-44 how long a human reply waits, and how that differs for NORA. Placement is a generic phone overlay (right on desktop, full screen on mobile)—working. The pipeline stays off the terminal (working). See [terminal.md](terminal.md).

Picture and sound: O-33 closed 10 October 2026 by Gunnar: live Three.js scenes, one fixed camera per room (asset kit still open; procedural primitives stand in); O-34 character style; O-35 animation depth; O-36 how recordings are produced; O-37 music; O-38 mobile floor.

Evaluation: O-39 audience and difficulty; O-40 what learning to measure; O-41 concepts during play or only after; O-42 duration (earlier hopes: 20–30 minutes for a first playable slice, 20–45 for a full investigation; untested).

## Later

A transfer check is out of scope for this build: after the game, a short unrelated case (a hospital system, a research assistant) with a reassuring safety report, scored on whether the player names a missing boundary, a bad evidence source, or an incentive. It is not a gate and not a scene inside the lab. Do not author it while the shutdown model is unfinished.

## Lab-sim

The design reuses the lab-simulation idea of separate planes: oracle, what a role can see, and audit surfaces. No software integration exists. O-28 is open. Until it closes, the game engine does not import `experiments/lab-simulation`.

The player computer is specified against that isolate tool list anyway. See [terminal.md](terminal.md). That does not import the Python sim.
