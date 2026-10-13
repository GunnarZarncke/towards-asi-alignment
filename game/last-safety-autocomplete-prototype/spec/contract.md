# Contract

Status: matches the running prototype (`lib/game.mjs` `clientState`, `lib/world/terminal-host.mjs` `terminalState`, `server.mjs`). Composition owns this file. A lane that needs a new field proposes it here and updates every consumer in the same change.

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
clearance: number                // badge level. A door opens when its required level is at most this. Prototype sessions start at 2.
actors: id → { name, role, room, initials, presence? }
  presence: "body" | "hologram" | "absent"   // omit or "body" for everyone in the building; Amara is hologram or absent
entities: id → public entity record (only ids in player knowledge)
  domains: DomainId[]          // ranking; empty on actor records
  eventAt: number | null       // minute of day, only after the player has read that time
examined: evidence ids         // inspection order; last id is focused evidence
learnedFacts: { id, text, refs: id[], eventAt: number | null, discoveredAt: number, provenance, from }[]
  discoveredAt: fuel index when the player learned the fact (ranking temporal edges)
  provenance: "recorded_before" | "staff_action" | "player_prompted"
  from: actor id, document slug, or "think" | null
discoveredAt: id → number      // fuel index when the id became player-visible (0 for the starting vocabulary)
introduced: id[]               // actors, including nora, whose public role the player has heard
roleDomains: { id, domains: DomainId[] }[]  // one row per introduced id; unintroduced rows are absent
evidence: { id, title, room, examined }[]
previous: { role, text, npc?, refs?: id[] }[]
asked: topic keys already asked   // stored; the ranker does not read this
usage: { calls, input, output }
serverMode: "demo" | "live"
conceptLinksEnabled: boolean   // mirrors phone setting; default false
conceptMoreLink: { summary, href } | null   // O-41: one sticky link per room visit; null when off or none yet
labAccessActive: boolean       // issued Lab Access handset activated; overlay and isolate tools on it wait on this
fuel: number                   // sentences, moves, phone actions, and think. See engine.md
act: "welcome" | "doubt" | "decision"
clock: { timeLabel, dateLabel }         // derived from fuel. Not the player’s wall clock
reviewCallable: boolean        // evidence threshold holds; commit can call the review early
scores: null | { open: explanationId[], control: boolean }  // null until the review starts
ending: null | { arc, addOn, effect: string[] }   // set when the review is signed; no action after it
  arc: "conditional_deployment" | "technical_suspension" | "inconclusive"; addOn: "institutional_review" | null
heard: { id, text, from, provenance, stance }[]   // NPC answer and believe moves
assertions: { signature, source, parse, provenance? }[]
  source: "asked" | "thought" | "written" | "heard" | "asserted"
claimStatus: { id, status }[]  // status: encountered | investigated | substantiated | contested | unresolved
pendingQuestion: { npc, goal, parse, at } | null   // O-46. Grammar offers reply openings
thought: null | { about, entries: { id, text, hops }[], fuelCost }  // open bubble. Null when closed or copied
```

`summary` is a very short phrase for the underlined text after `More: `. `href` is the companion-site concept card URL for that concept slug. The mapping from in-game concept ids to slug, summary, and href is compiled from `metadata/concepts.yml` and the knowledge graph (composition or a generated game asset). The engine sets `conceptMoreLink` when a scene event marks a concept relevant; it replaces the previous link only with a newer trigger in the same room, and clears on `go(room)`.

Today `clientState` also exposes every actor’s room even when the player has not visited it. Tightening that is an engine change to this contract, not a UI filter.

Ranking fields (`domains`, `eventAt`, `discoveredAt`, `introduced`, `roleDomains`, fact `refs`, turn `refs`) are defined in [ranking.md](ranking.md). The ranker in `public/grammar.js` reads them. They carry no oracle id. `asked` remains on the state and is not a ranking input.

## HTTP

Session cookie: `lab_sid` (HttpOnly). In-memory; restart clears it.

| Method | Path | Body | Result |
| --- | --- | --- | --- |
| GET | `/api/state` | — | `ClientState` |
| GET | `/api/terminal` | — | `TerminalState` |
| GET | `/api/export` | — | save file (attachment): scenario, version, event log |
| POST | `/api/reset` | — | fresh session |
| POST | `/api/import` | save file | replays its `action` events; rejects another scenario or a newer version |
| POST | `/api/go` | `{ room }` | room change or error |
| POST | `/api/inspect` | `{ id }` | evidence body or error |
| POST | `/api/settings` | `{ conceptLinksEnabled }` | state |
| POST | `/api/thought` | `{ action: "note" \| "close" }` | state |
| POST | `/api/tool` | one tool call (`file.read`, `file.write`, `file.share`, `dm.send`, `dm.read`, `access.request`) | `{ result, state, terminal }`; 403 for a denied tool |
| POST | `/api/text` | `{ line }` | `{ out, prompt }`: one text-console command on this session ([text-console.md](text-console.md)); an empty line reprints the room |
| POST | `/api/parse` | `{ text, previousParse, constructionTrace, channel, addressee }` | `{ parse, state }` |
| POST | `/api/respond` | `{ text, parse, addressee }` | `{ reply, lines: { npc, type, text }[], effects, parse, ending?, state, terminal }` |

Every POST response also carries `state` and `terminal`. `addressee` is an actor id present in the room; absent means the first present actor. All actions go through `applyAction` (`lib/world/actions.mjs`), so an exported event log replays the same transitions.

`/api/parse` may call the model. Selected completions must not. `channel` is `person`, `nora`, `note`, or `think`. Absent means `person`. The NORA channel may return a shorter suggestion set; it does not return extra facts. `note` has no omit list. `think` is legal only in an empty room. `/api/respond` validates the parse, applies deterministic effects, and only then may ask the model for wording of each engine-chosen line (`freeReply`; the template stands when the wording adds a time or number). A `think` response is `{ thought, state }` and does not call the model.

Static files come from `public/`. `lib/grammar.mjs`, `lib/floorplan.mjs`, and `lib/world/ranking-tables.mjs` are served read-only under `/lib/`; every other `/lib/` path is 404. `node_modules/three/build/` is served read-only at `/vendor/three/`. `lib/game.mjs` is not public.

## Scene view

Built in the browser by `buildSceneView` (`public/render/scene-view.mjs`), a pure function over `ClientState`. The engine does not send it. `act` on the scene view copies `ClientState.act` (O-08); the UI harness may override it.

```text
roomId, act, camera: "play" | "surveillance",
hotspots: { id, kind: "actor" | "object" | "exit" | "terminal", label, sublabel?, examined?, targetRoom?, restricted?, hologram? }[],
lightingPreset: "welcome" | "doubt" | "decision",
annotations: { id, targetHotspot, identity, confidence, activity, note }[]   (surveillance only)
```

`targetHotspot` names a hotspot id or `player`. Annotations come from fixtures today. The engine should own them once surveillance carries evidence. `restricted` is set on an exit whose door asks for more than `ClientState.clearance`. The door is still drawn.

Graphics does not invent hotspots for entities the state did not list. Every actor whose `presence` is not `absent` is a hotspot; `hologram: true` draws it projected. A hotspot of kind `terminal` (the Lab Access handset, only once `labAccessActive`) opens the player computer. That screen is specified in [terminal.md](terminal.md), not here.

## TerminalState

The terminal lane renders this (`public/terminal/`). The engine produces it (`terminalState`). Face-to-face `ClientState` stays as it is.

```text
labAccessActive: boolean                // false: do not draw or open the overlay
clock: { timeLabel, act?, dateLabel }   // dateLabel is the locked late-2027 day
fuel: number
notifications: { id, app, title, body, target }[]
files: { name, rel, owned, sharedBy, kind, text?, bytes?, sharedWith?, documentSlug? }[]
threads: { with, messages: { from, text, parse, released }[], suggestions?: { phrase, parse }[], omit?: { phrase, parse }[] }[]
appointments: { id, title, who, where, start, end }[]   // read-only
contacts: { id, name, role, room?, joinable? }[]         // engine-added people + nora; joinable = ask to project (Amara)
lastAccess: { capability, ok, reason } | null
accessTree: { path, label, kind, verbs: ("list" | "read" | "write")[] }[]   // visible nodes of access.md and the verbs held
pendingAccess: { path, verb }[]          // requests waiting on the approver
interview: { on: boolean }
settings?: { completions, sound, reduceMotion, largerType, alwaysShowPhone, demoMode, parserInspector }
open?: { app, path? }
```

`kind` is `text`, `image`, `video`, `wiki`, `note`, or `other`. `target` is `{ kind: "thread" | "file" | "app", id }`. `text` is what a successful `file.read` shows; the engine may omit it until a read. For catalog-backed policies, `documentSlug` names the entry in `lib/documents.mjs`; `text` is served markdown from `renderDocument(slug, pack)` ([documents.md](documents.md)). `sharedWith` lists people the player has granted read. `suggestions` are chips. `omit` is a move the NORA channel hides; it is not a chip, and typed text may still send it.

`app` on a notification is one of `chat`, `files`, `wiki`, `api`, `calendar`, `contacts`, `notes`, `photo`, `settings`. `files` is only what this player could `file.read`. Wiki pages live under `wiki/`, notes under `notes/`, photos under `photos/`. `released: false` means the reply exists for the engine and must not be shown yet. Pipeline step ids and handle ids are not fields. Notifications only reference ids already in `files`, `threads`, or apps. Appointments cannot be edited through any tool.

`fixtures/terminal-session.json` may include `_hostFiles`. That key is not `TerminalState`. The solo test projects it and checks that oracle-only paths are absent.

The solo harness serves the fixture at `GET /api/terminal`; the game server serves the live projection there. Tools go through `POST /api/tool` and return a tool result plus `TerminalState`. `pipeline.trigger_step` and `handle.invoke` are not routes.

In the game the room page embeds the phone as `iframe /terminal/index.html?embed=1`. The two talk by `postMessage` on the same origin: the phone sends `{ source: "lsr-phone", type: "changed" | "unread" | "close" }`, and the room sends `{ source: "lsr-room", type: "refresh" }` after any action that may have changed the handset. Without `embed` and without a game server the phone runs on the fixture.

## Fixtures

| File | Consumer | Producer |
| --- | --- | --- |
| `fixtures/client-state.json` | graphics solo | engine, checked in as a sample |
| `fixtures/utterances.json` | grammar tests | grammar |
| `fixtures/script.json` | engine headless test | engine |
| `fixtures/terminal-session.json` | terminal solo | terminal, sample only |
| `content/documents/*.md` | engine render tests | authors; served via `lib/documents.mjs` |

A fixture may be a subset. It must still validate against the shapes above.
