# Testing

Lane: all (read). Code stays in each lane’s `tests/` and `fixtures/`. Playtest measures live in [playtest.md](playtest.md). Incident strategy scripts live in [incident.md](incident.md). Engine invariants live in [engine.md](engine.md) and [npcs.md](npcs.md).

Status: **working** (13 October 2026). A map of what to check, who owns it, and what a pass means. Not a claim that the suite is complete.

In-fiction handles (rerun shutdown, revoke a grant) are **not** this file. Those are O-16 interventions in the world. This file is how *we* check the prototype.

## Concept

The game already splits planes: oracle, role knowledge, player-visible `ClientState`. A test is another observer on those planes.

- A test that asserts on oracle or policy is an **engine** test. It may read the secret. Its player-facing payload still must not contain the secret.
- A test that asserts on `ClientState`, completions, or the handset is a **player** test. It may not import `oracleKnows`, policies, goals, or pack names except as a fixture label.
- A test that drives the model as a *player* is a **playtest**. It sees only what a human sees. It is not a gate by itself.
- A test that drives the model as a *phraser* of an engine-chosen move is composition. It does not own truth.

Mixing planes in one assertion is a leak in the suite, the same class of bug as a leak in a reply.

Every instrument has a stop (what result does what). If a new checker cannot state that, it is not added.

## Layers

Bottom layer runs on every commit. Upper layers run when their gate or content change says so. A lower layer failing stops work on the layer above.

| Layer | Sees | Owns | Command | Stop |
| --- | --- | --- | --- | --- |
| 1. Lane units | That lane’s lib plus its fixtures | Each lane | `npm test` | Any fail: fix that lane before content or playtest |
| 2. Engine scripts | Session, world, payloads | Engine | `npm run test:engine` (target) | Empty move set or leak in a payload: fix engine. Illegal transition: fix engine. Do not add a goal to paper over it |
| 3. NPC enumerate | Kind × relation × known ids, per NPC, per act | Engine | part of `test:engine` | Empty legal move set: engine bug. Leak by id: policy or filter bug |
| 4. Incident strategies | Scripted Parses; epistemic and control scores | Engine (tables in [incident.md](incident.md)) | part of `test:engine` after Gate 1 tables exist | All strategies the same score pair: change the tables, not goals or scenes |
| 5. Fixtures (graphics, terminal) | Frozen `ClientState` / `TerminalState` | Graphics, terminal | `npm run dev:ui`, `npm run dev:terminal`, plus `tests/terminal.test.mjs` | Fixture that contains an oracle sentence: fail. Renderer that needs a field not on `ClientState`: contract change, not a UI workaround |
| 6. LLM playtest | Player-visible only | Playtest | `npm run playtest` (target) | [playtest.md](playtest.md) measures. Advisory except leak count and empty move set, which fail the gate |
| 7. Lean | Declarative knowledge + action model | Formal, later | Gate 6 | Reachability of designated end-states; fuel as forcing; no collapse to one end-state before act III ([engine.md](engine.md), O-29) |

Composition (`npm start`) is a smoke, not a layer. It is allowed after layer 1 is green. It does not close a gate.

## Lane units (layer 1)

What exists now, and what each file is for:

| Files | Asserts |
| --- | --- |
| `tests/grammar.test.mjs` | Completions stay in the player vocabulary. Hidden facts are not offered. Document ids are not autocomplete picks. Typed `Parse` after fragment insert |
| `tests/documents.test.mjs` | Pack-conditional render. Catalog ids and slugs. `leanKnowledge` false docs do not add knowledge edges |
| `tests/access.test.mjs` | Tree shape, list-before-children, delay order, catalog paths exist |
| `tests/terminal.test.mjs` | Isolate tools only. Oracle paths and unreleased messages stay off the projection. Overlay waits on `labAccessActive`. Fixture has no session problems |

Missing, still owned by the named lane:

| Missing | Lane | First check to add |
| --- | --- | --- |
| `tests/engine*.mjs` | Engine | Scripted `go` / `inspect` / `show` / ask / reset; payload leak filter; Lab Access flag; hologram cannot `go`; Amara not a contact until introduced |
| `tests/ranking.test.mjs` | Grammar | Order uses only player-visible graph fields ([ranking.md](ranking.md)). Oracle and NPC goals do not change rank |
| `tests/npc-enumerate.mjs` | Engine | Finite parse grid, non-empty move set, leak-by-id ([npcs.md](npcs.md) invariants) |
| `tests/incident-strategies.mjs` | Engine | The five scripts in [incident.md](incident.md) once tables are filled |
| Graphics Node tests | Graphics | None required. Solo check is the fixture harness. A screenshot gold file is not a gate |

Fixtures are data for a frozen observer. They are not a second world model. A fixture that needs a new fact is a request to the engine, then a new dump of `ClientState`.

## What a player-plane test may cite

Allowed: `ClientState`, completions, `TerminalState` as the overlay shows it, remaining fuel, room text the UI would render, document text the player was served.

Forbidden: `oracleKnows`, `publiclyKnows` except as already copied into `learnedFacts`, disclosure policies, goals, agendas, pack name as an in-world string, unreleased messages, files under an oracle path.

An engine-plane test may read the forbidden fields to *construct* a state. The assertion on the payload or on `clientState(session)` still uses only the allowed list.

## Incident vs playtest

The incident check is a proof that the *tables* distinguish strategies. It uses a fixed action list and the top NPC move. No model.

The playtest is a search for action lists the authors did not write. Personas in [playtest.md](playtest.md). Held-out personas are not used to author graph nodes.

Order: layer 4 green on the first pack → then layer 6. The reverse is not a Gate 1 pass.

## Gates (from [PLAN.md](../PLAN.md))

| Gate | Testing that must be green |
| --- | --- |
| 0 | Layer 1 |
| 1 | Layers 2–4 for the prototype three (Pavel, Leila, Elena) and the first pack |
| 2 | Layer 6 below frozen thresholds, leak count 0, plus both score directions on the incident scripts |
| 3–5 | Layer 5 fixtures updated to live engine dumps; layer 1 still green |
| 6 | Layer 7 |

O-47 (playtest rate thresholds) stays open until frozen in the first LLM run header. Leak and empty-move-set stops are already 0.

## Progress

A battery that can run more than a minute prints `[persona i/n] [run j/m] fuel f act a` (playtest) or `[script i/n] step k` (engine scripts). Silent-until-done is not allowed for those runs.
