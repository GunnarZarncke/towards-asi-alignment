# Contract

Status: matches the running prototype. Composition owns this file. A lane that needs a new field proposes it here and updates every consumer in the same change.

The browser never receives the API key, oracle-only facts, or unfiltered NPC knowledge.

## Parse

Produced by completions (`source: "completion"`) or by `parseUtterance` (`source: "llm"`). Consumed by the engine on `/api/respond` after server-side cleaning.

```text
kind, relation, subject, object, recipient, evidence, topic,
open_slot, unfinished, open_content, confidence, source
```

Entity fields are ids from the player-visible vocabulary, or null. `confidence` is 0–1. Definitions of the allowed strings are in [grammar.md](grammar.md).

## ClientState

Returned by the engine on every API response as `state`. The UI renders this and does not keep a second copy of world truth.

```text
room
actors: id → { name, role, room, initials }
entities: id → public entity record (only ids in player knowledge)
examined: evidence ids
learnedFacts: { id, text }[]
evidence: { id, title, room, examined }[]
previous: recent conversation turns
asked: topic keys already asked
usage: { calls, input, output }
serverMode: "demo" | "live"
```

Today `clientState` also exposes every actor’s room even when the player has not visited it. Tightening that is an engine change to this contract, not a UI filter.

## HTTP

Session cookie: `lab_sid` (HttpOnly). In-memory; restart clears it.

| Method | Path | Body | Result |
| --- | --- | --- | --- |
| GET | `/api/state` | — | `ClientState` |
| POST | `/api/reset` | — | fresh session |
| POST | `/api/go` | `{ room }` | room change or error |
| POST | `/api/inspect` | `{ id }` | evidence body or error |
| POST | `/api/parse` | `{ text, previousParse, constructionTrace, channel }` | `{ parse, state }` |
| POST | `/api/respond` | `{ text, parse }` | `{ reply, effects, parse, state }` |

`/api/parse` may call the model. Selected completions must not. `channel` is `person` or `nora`. Absent means `person`. The NORA channel may return a shorter suggestion set; it does not return extra facts. `/api/respond` validates the parse, applies deterministic effects, and only then may ask the model for wording.

Static files come from `public/`. `lib/grammar.mjs` is served read-only at `/lib/grammar.mjs`. `node_modules/three/build/` is served read-only at `/vendor/three/`. `lib/game.mjs` is not public.

## Scene view

Built in the browser by `buildSceneView` (`public/render/scene-view.mjs`), a pure function over `ClientState`. The engine does not send it yet. `act` is fixed at `doubt` until the engine reports an act (O-08).

```text
roomId, act, camera: "play" | "surveillance",
hotspots: { id, kind: "actor" | "object" | "exit" | "terminal", label, sublabel?, examined?, targetRoom? }[],
lightingPreset: "welcome" | "doubt" | "decision",
annotations: { id, targetHotspot, identity, confidence, activity, note }[]   (surveillance only)
```

`targetHotspot` names a hotspot id or `player`. Annotations come from fixtures today. The engine should own them once surveillance carries evidence.

Graphics does not invent hotspots for entities the state did not list. A hotspot of kind `terminal` opens the player computer. That screen is specified in [terminal.md](terminal.md), not here.

## TerminalState

Draft. The terminal lane renders this (`public/terminal/`). The engine does not produce it yet. Face-to-face `ClientState` stays as it is.

```text
clock: { timeLabel, act?, dateLabel }   // dateLabel is the locked late-2027 day
notifications: { id, app, title, body, target }[]
files: { name, rel, owned, sharedBy, kind, text?, bytes?, sharedWith? }[]
threads: { with, messages: { from, text, parse, released }[], suggestions?: { phrase, parse }[], omit?: { phrase, parse }[] }[]
appointments: { id, title, who, where, start, end }[]   // read-only
contacts: { id, name, role, room? }[]                   // player-visible people + nora
lastAccess: { capability, ok, reason } | null
settings?: { completions, sound, reduceMotion, largerType, alwaysShowPhone, demoMode, parserInspector }
open?: { app, path? }
```

`kind` is `text`, `image`, `video`, `wiki`, `note`, or `other`. `target` is `{ kind: "thread" | "file" | "app", id }`. `text` is what a successful `file.read` shows; the engine may omit it until a read. `sharedWith` lists people the player has granted read. `suggestions` are chips. `omit` is a move the NORA channel hides; it is not a chip, and typed text may still send it.

`app` on a notification is one of `chat`, `files`, `wiki`, `api`, `calendar`, `contacts`, `notes`, `photo`, `settings`. `files` is only what this player could `file.read`. Wiki pages live under `wiki/`, notes under `notes/`, photos under `photos/`. `released: false` means the reply exists for the engine and must not be shown yet. Pipeline step ids and handle ids are not fields. Notifications only reference ids already in `files`, `threads`, or apps. Appointments cannot be edited through any tool.

`fixtures/terminal-session.json` may include `_hostFiles`. That key is not `TerminalState`. The solo test projects it and checks that oracle-only paths are absent.

The solo harness serves the fixture at `GET /api/terminal`. That is not a tool route. When composition adds one, it is a tool-shaped call (`file.read`, `file.write`, `file.share`, `dm.send`, `dm.read`, `access.request`) and the response is a tool result plus `TerminalState`. `pipeline.trigger_step` and `handle.invoke` are not routes.

## Fixtures

| File | Consumer | Producer |
| --- | --- | --- |
| `fixtures/client-state.json` | graphics solo | engine, checked in as a sample |
| `fixtures/utterances.json` | grammar tests | grammar |
| `fixtures/script.json` | engine headless test | engine |
| `fixtures/terminal-session.json` | terminal solo | terminal, sample only |

A fixture may be a subset. It must still validate against the shapes above.
