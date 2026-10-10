# The Last Safety Review — development plan

Structure only. Design detail lives in [`spec/`](spec/README.md). The consolidated source is [`last-safety-review-game.md`](last-safety-review-game.md). While a lane is in progress, edit that lane’s spec, not the consolidated doc.

## Lanes

Four lanes can proceed at the same time. Composition only wires them.

| Lane | Spec | May edit | Solo check |
| --- | --- | --- | --- |
| Grammar | [spec/grammar.md](spec/grammar.md), [spec/ranking.md](spec/ranking.md) | `lib/grammar.mjs`, `public/grammar.js`, `tests/grammar*.mjs` | `npm test` |
| Graphics / UI | [spec/graphics-ui.md](spec/graphics-ui.md) | `public/index.html`, `public/style.css`, `public/app.js`, future `public/render/` | `npm run dev:ui` (fixture; see below) |
| Terminal | [spec/terminal.md](spec/terminal.md) | `public/terminal/`, `tests/terminal*.mjs` | `npm run dev:terminal` (fixture; see below) |
| Engine | [spec/engine.md](spec/engine.md), [spec/world.md](spec/world.md) | `lib/game.mjs`, future `lib/world/`, `tests/engine*.mjs` | `npm run test:engine` (headless; see below) |
| Composition | [spec/contract.md](spec/contract.md) | `server.mjs`, `lib/llm.mjs` | `npm start` |

Shared reading for every lane: [spec/meta.md](spec/meta.md) and [spec/contract.md](spec/contract.md). World content is engine-owned; graphics reads it and does not edit it.

## Rules

- A lane does not edit another lane’s files.
- Consequential facts, access, and endings change only in the engine.
- The first incident is a causal model ([spec/incident.md](spec/incident.md)). Dialogue and rooms for that incident wait until its headless check passes.
- The renderer draws `ClientState`. It does not decide outcomes.
- The terminal is a generic phone overlay ([spec/terminal.md](spec/terminal.md)): homescreen, chat, files, wiki, API, calendar, contacts, notes, photo, settings, viewers. Isolate tools only. No pipeline or overseer handles.
- Completions and the parser emit a `Parse`. Room completions do not reveal oracle-only facts. Completions addressed to NORA may omit evidence; they still must not assert a hidden fact.
- `lib/llm.mjs` interprets player text into a `Parse` and phrases replies from engine-filtered NPC facts. It does not own grammar or world truth.
- A change to shapes in [spec/contract.md](spec/contract.md) is a composition change: update the contract and every consumer in the same pass.
- Open questions stay open until recorded in [spec/meta.md](spec/meta.md). A lane must not close one inside its spec.
- Do not implement a side idea because it is written down. If it does not change what a player can justify or what they can still control, it waits.

## How to test

| What | How | Needs |
| --- | --- | --- |
| Grammar alone | `npm test` | Node. No key, no browser. |
| Engine alone | `npm run test:engine` | Scripted actions against `lib/game.mjs`. No browser, no model. Includes the incident scripts in [spec/incident.md](spec/incident.md) once that model exists. |
| Graphics alone | `npm run dev:ui` | Frozen `fixtures/client-state.json` plus a scene fixture. No engine, no key. |
| Terminal alone | `npm run dev:terminal` | Frozen `fixtures/terminal-session.json`. Phone overlay on a dummy room; no engine, no key. |
| One room, live parse | `npm start`, then the browser | Repo-root `.env` (`OPENAI_API_KEY`). `DEMO_MODE=1` skips the model. |
| All together | `npm start` | Composition server on `127.0.0.1:3000`. |

`dev:ui` loads fixture state and scene data (`npm run dev:ui` → port 3001). `dev:terminal` loads the phone fixture (`npm run dev:terminal` → port 3002). `test:engine` is still a target harness. Grammar is `npm test`; the combined app is `npm start`.

Fixtures live in `fixtures/`. Each lane may add fixtures for its solo check. A fixture is data, not a second world model.

## Gates

Gates say when a combination is worth playing. Lanes do not wait on each other between gates, as long as they honor the contract.

| Gate | Together, the build can… | Still open in meta |
| --- | --- | --- |
| 0 — now | Parse and speak in three rooms with three people and three records. | Almost everything in the full cast and plot. |
| 1 — one incident | Run the shutdown causal model: three explanations, six facts, four interventions, per-character knowledge. Different strategies justify different conclusions. No new dialogue and no new rooms. | Pack tables still unfilled. First pack is boundary-narrow. Other packs after that one checks. |
| 2 — playable model | Disclose a fact and get a new observable from the person who can act on it. Finish high on control and low on identifying intention, and the reverse. | O-26, O-27 for the full meeting. |
| 3 — one room drawn | Show Platform Operations in play and in surveillance mode, on engine state. | Music (O-37), after the story is set. Conversation detail for characters later (O-34, O-35). |
| 4 — slice | Play that incident through several rooms, with both success measures still distinct. | |
| 5 — full day | Walk the nine-room cast through three acts. | Duration (O-42). |
| 6 — language and proofs | Reject leaked facts and illegal transitions in tests. Lean on the declarative model: designated end-states reachable, fuel as the forcing parameter, no collapse to one end-state before act III. | Whether the simplified lab-sim copy is needed (O-28). |

A post-game transfer scenario (a second system, scored on whether the player spots a missing boundary) is out of this plan. See [spec/meta.md](spec/meta.md).

## Prerequisites already checked

Node for this app is 22.10+ (this machine has 23). The site app is a different tree and wants Node 24; this game stays under `game/` until a gate says otherwise. Three.js is an npm dependency (`npm install`); both servers serve it read-only at `/vendor/three/`. No image, model, or audio files are in the repo. Pack licenses and the style clash are in [spec/graphics-ui.md](spec/graphics-ui.md). O-33 is closed (live Three.js); do not download asset zips until the kit choice is closed.
