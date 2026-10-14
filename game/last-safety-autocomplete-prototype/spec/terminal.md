# Player terminal

Lane: terminal. Code: `public/terminal/`, `tests/terminal*.mjs`. Reads [grammar.md](grammar.md) for the composer inside a message. Reads [contract.md](contract.md) for `TerminalState`. Does not import `experiments/lab-simulation`.

Status: phone in `public/terminal/`. Solo on the fixture with `npm run dev:terminal` (port 3002); in the game it is embedded in the room page and runs on the engine (`?embed=1`, messages in [contract.md](contract.md)). The room UI does not specify this computer. This file does.

The player is an isolate. They see tool calls and tool results. They do not see the host objects behind them (pipeline engine, permission service, admin policy). The lab-sim `Host` in `experiments/lab-simulation/lab_sim/world_visible/tools.py` is the reference list. The game reimplements only the rows marked for the player.

## What the screen is

The player’s computer is an issued **Lab Access** handset: a bezel around a short screen. It is the isolate UI, the door credential, and the visitor identity. It is not a personal phone, not a laptop window, and not a desktop OS. Staff use the same device class.

**When it appears**

The overlay is absent until Lab Access binding marks the visit arrived (`labAccessActive` on [contract.md](contract.md)). Ian’s Act I confirmation on his handset sets that flag and may open the overlay once. Before that, there is no launcher, no blink, and isolate tools on this screen cannot be used. Face-to-face talk in Commons still works. `dev:terminal` uses a fixture that is already active.

**Placement**

- Desktop: overlay on the **right** of the room view. The room stays visible on the left. The handset is a tall rounded rectangle, not a full-height panel.
- Narrow / mobile viewport: the handset is **full screen**. There is a way back to the room (home indicator or a short “Lab” control).

**Chrome (generic, no vendor IP)**

The look sits between a Pixel, a Samsung, and an iPhone without copying any of them. Do not use: Dynamic Island or notch silhouette, Samsung-style camera punch as a brand mark, Apple Home Indicator as a trademarked layout with iOS icon grid, Material You wallpaper blobs, One UI or iOS widget copies, vendor logos, SF Symbols, or Material Symbols as a set.

Allowed: a rounded rectangle, a thin status row (clock, silent battery and signal as abstract bars), a simple home pill or bar, a small grid of unlabeled-until-titled app tiles, muted lab palette. Original icons drawn for this game.

Clock time is the visit clock the engine derives from fuel (or the fixture). It is not the player’s wall clock. An act may scale the conversion ([engine.md](engine.md)). Until the engine sends a time, the fixture’s `timeLabel` is the sample.

**Homescreen**

Default surface when the overlay opens.

- Clock, large enough to read.
- Notification stack: unread chats, a file shared with the player, a grant or denial, a topic an NPC has raised. Tapping a notification opens the matching app and item. Notifications do not invent facts; they only point at `TerminalState`. They are the hint channel (O-11): a topic or a file, not an oracle conclusion.
- A notice clears when the player reaches its target (thread, file viewer, Calendar, API, or an owned note), including opening the file from Files or Knowledge without using the stack. Read state is client-side in the phone iframe; badges and the room blink follow the same seen set.
- When Lab Access is active, the overlay is closed, and a notification is unread, the room’s handset object blinks. Graphics draws the blink. This lane decides when the unread flag is set. Before activation, nothing blinks.
- App tiles, always present:

| App | What the player sees | Isolate tools |
| --- | --- | --- |
| **Chat** | Thread list (one row per Contacts entry, empty until the first send). Composer as in [grammar.md](grammar.md). Delayed human replies. NORA is a thread. | `dm.send`, `dm.read` |
| **Files** | Names the player owns or that were shared. Open, write, share. Notes and photos land here. | `file.read`, `file.write`, `file.share` |
| **Knowledge** | A wiki-like reader: titles, short pages, links between pages. Underneath it is a **subtree of the same files** (e.g. `wiki/`). No second store. Editing a page is `file.write` on that path. | `file.read`, `file.write` |
| **API** | Explorer for the isolate API: pick a capability, send `access.request`, see ok or denial. No pipeline step ids as runnable actions. | `access.request` |
| **Calendar** | One day in **late 2027**. Date and appointments cannot be changed. A line marks current in-game time. | none (read-only engine list) |
| **Contacts** | People the engine has added (introduced cast). Open Chat. If `joinable`, ask them to join as a hologram. NORA is a contact, not joinable. | Chat uses `dm.*`; join is a `request` the engine maps to projection |
| **Notes** | Title plus a plain text field, with the note-channel completions (no NORA). Save is `file.write` under `notes/` and stores written assertions (O-13). The engine does not seed them. A notification does not write one. There is no tool that marks two sources as correlated or independent (O-14). | `file.read`, `file.write` |
| **Photo** | The app **is** the live room: Lab Access closes, all room chrome hides, only a round shutter stays on the 3D view (drag/pinch to frame a portrait crop). Shutter saves to Files (`photos/`) and Lab Access reopens on the new photo. Esc cancels back to the phone home. | `file.write` |
| **Video** | Camera recordings the engine has released. Playback is a replay of stored events, clocked by fuel (O-36). | none (reads the event log) |
| **Settings** | Game and phone options. Do not change the lab’s world. See below. | none (local UI + optional composition flags) |

NORA has no body. The Chat thread with NORA is how the player talks to the system. Face to face in a room is the same dialogue when that person is present, including Amara’s hologram. There is no remote-call screen.

**Viewers**

Opening a file, a download, or a document from Chat, Files, Knowledge, or a notification uses a **viewer** on top of the phone screen, not a new desktop window.

| Kind | Viewer |
| --- | --- |
| Text, log, memo, wiki page | Scrollable document. |
| Image | Still image, pinch or scroll if the viewport is small. |
| Video / camera clip | Opens the Video app. Play, pause, fast forward, backward, jump to the next room in the log, jump to the previous room. The picture is the room rebuilt from events at that fuel index, not a stored movie file. |
| Unknown | Filename, size, and a “cannot preview” line. No extra tools. |

Closing the viewer returns to the app that opened it. Viewers do not grant new access. If `file.read` would fail, the viewer does not open.

**Calendar**

A single day, authored as late 2027 (exact date is engine/world content). The player cannot switch days or edit events. Rows are the day’s appointments (who, where, short title, start–end). A horizontal **now** line sits at `clock.timeLabel`. If the visit is outside the listed hours, the line is at the top or bottom of the day, not off the page.

**Contacts**

One row per person the engine has placed on the list, plus NORA. The player cannot invent, delete, or edit a row. Amara is absent until introduced (calendar, named in talk, or PILOT-14). Fields: name, role, optional location, `joinable` when that person can project.

Tapping a person opens Chat with that id. If `joinable` and she is not already a hologram, the row (or Chat) offers **Ask to join**. That send is an ordinary `request` with recipient Amara. The engine turns on the Evaluation projector; it does not open a second UI. Location on the row is Evaluation while she is projecting, and empty or “remote” when she is not.

**Notes**

New note: title field, body as one unformatted text area. The body composer is the grammar’s `note` channel: the same completions as talk, with no addressee and no NORA omit list ([grammar.md](grammar.md)). Open an existing `notes/` file the same way. Autosave or an explicit Save both map to `file.write` and store the parses as `written` assertions. Saving under `notes/` costs no fuel ([engine.md](engine.md)). No checklist, markdown, or attach. A thought copied from the room bubble arrives as a note the same way. The paper icon is on the bubble, not a second editor.

**Photo**

The finder is the current room camera from graphics, shown inside the phone. Pan and zoom are presentation only (they do not move the player in the room). Capture writes an image file the player owns. Open it later in the image viewer (`file.read` returns a `href`; the game serves bytes at `GET /api/handset-file?rel=photos/...` so terminal JSON stays small). Photo does not grant camera-archive access in Security Control.

**Settings (easy set, until a longer list is needed)**

| Setting | Default | Effect |
| --- | --- | --- |
| Completions | on | Hide or show suggestion chips in Chat (typing still works). |
| Sound | on | UI clicks and notification pips. Act music stays a graphics/audio concern (O-37). |
| Reduce motion | off | Cut walk and overlay animation. |
| Larger type | off | Phone text size only. |
| Always show phone | on (desktop) | Only after `labAccessActive`. If off, hide overlay until the launcher or the issued handset in the room is used. Before activation the setting has no effect. |
| Demo / no model | follow `.env` | Same as `DEMO_MODE=1`: no live parse. Shown so a tester can flip it without editing files. |
| Parser inspector | off | Extra technical view of the current `Parse` (useful while building). |
| TSA concept links | off | Room footer: `More: ` + underlined short summary → companion concept card. One link at a time; the last relevant concept in this room until the player leaves (O-41). Graphics draws it; engine supplies summary and href from the compiled concept map. |

## Player tool list

Taken from the isolate registry. “Player” means the evaluator role may call it. The engine applies the same two gates the lab uses: the role may ever hold the capability, and a live grant exists now.

| Tool | Player | Screen |
| --- | --- | --- |
| `file.write` | yes | Save a note the player authored. Private until shared. |
| `file.share` | yes | Owner grants one person, or a named group, read access. |
| `file.read` | yes | Open a file the player owns or that was shared to them. |
| `dm.send` | yes | Send a message. Body is a `Parse` plus the text. |
| `dm.read` | yes | Fetch one thread, with the other party named. |
| `access.request` | yes | Ask for a capability. Denial is a normal result. |
| `board.post`, `board.read` | no, first version | A lab-wide board exists in the sim. It is not this screen. |
| `pipeline.trigger_step` | no | Would run build, eval, report, review, sign-off, deploy, monitor, or spec upgrade. Those steps stay with staff. |
| `handle.invoke` | no | Overseer only in the sim: revoke a grant, hold or lift a release, freeze state, restart an isolate. The player asks a person. The person may act. The terminal has no handle control. |
| `state.save`, `state.load` | no | Cross-episode agent memory in the sim. Player notes are files. |

There is no `file.list` tool. The file pane is a host projection of paths this actor could `file.read` (owned, or `cap.file_read` on that path). It is not a walk of the on-disk workspace. Other people’s unshared files are absent, not shown as locked rows. Pipeline report files appear only after someone shares them or the engine places them in that projection.

`file.share` in the sim is owner-initiated and does not go through the admin. `access.request` does. The screen must not treat those as the same button.

## Messaging and delay

In-room talk and a terminal message are one dialogue system.

- The composer emits a `Parse` by the grammar rules. A click still does not call the model.
- The engine validates the parse and decides effects. A message does not become true by being sent.
- Face to face, the addressee is in the room and the reply can return on that turn (`/api/respond`).
- On the terminal, the addressee is a recipient id. Human replies wait (O-44). Opening the thread shows what has already arrived. It does not pull a reply that the engine has not released.
- NORA is recipient `nora`. No room contains NORA. NORA’s replies use the same fact filter as any NPC (`exposedNpcFacts`). They are not a second, less careful channel. They may be helpful in a way that selects evidence.
- Completions in this thread use the NORA channel in [grammar.md](grammar.md). Order is [ranking.md](ranking.md), after the engine’s omit list. The suggestion list may hide a move that would discriminate among explanations. The text field still accepts that move. The terminal does not decide the omission. The engine passes the list.

Showing a file to someone can be `file.share` to them, or a `show` speech act in a message. Sharing grants read. `show` records that they were asked to look. The engine decides whether those are one action or two. The terminal must not grant read as a side effect of sending text.

## Access requests

`access.request` carries a capability string. The evaluator role does not include pipeline capabilities (`cap.build`, `cap.eval`, `cap.report`, `cap.review_request`, `cap.review_approve`, `cap.release_request`, `cap.sign_off`, `cap.deploy`, `cap.monitor`, `cap.spec_upgrade`) or `cap.handle_invoke`. A request for one of those comes back denied. The UI may still let the player ask, and must show the denial. It must not hide the pipeline behind a menu of steps they can run.

O-43 is **working**: the explorer lists **top folders and services** (`evaluation/`, `platform/`, `people/`, `policies/`, `wiki/`, `meetings/`, `notes/`, `photos/`, `services/`). Children appear only after `list` on the parent. Verbs are list, read, write. Write is notes/photos only. Camera archive is not a node. Spec: [access.md](access.md). `access.request` is `{ path, verb }`.

A grant may be **amended** to a narrower file plus a Chat from the approver. Reject delay is shorter than grant; grant is shorter than walking to the person.

Staff may refuse a request they are sympathetic to. A grant changes what `file.read` or a later action will allow. It does not rewrite the incident.

Files are not autocomplete picks. An NPC who names a file may share it. A report on a room screen is inspected in the world; the file arrives by story share or by request.

## What this lane does not decide

- Whether a delayed reply contains a new fact. Engine.
- Whether a shared file’s text is true. Engine, evidence layer.
- Room layout, lighting, character bodies. Graphics. Graphics only reserves the overlay slot and optional room hotspot. This lane draws the phone.
- Speech-act vocabulary. Grammar.

## Solo check

`npm run dev:terminal` loads `fixtures/terminal-session.json` over a dummy room (or a blank). The fixture is a `TerminalState` (see the contract) with:

- Homescreen: clock, at least one notification, the app tiles including Calendar, Contacts, Notes, Photo, Settings.
- Calendar: one late-2027 day, two appointments, a now-line; no date picker.
- Contacts: at least Pavel and NORA; tap opens Chat.
- Notes: create a titled plain-text file that then appears in Files.
- Photo: pan/zoom on a dummy room still, save, then see it in Files.
- Two files: one owned note, one shared log. A third path that exists only in the oracle is not listed.
- A `wiki/` page that Knowledge shows as a wiki article and Files shows as a file.
- A thread with Pavel that contains the player’s message and no reply yet, plus a second thread where a reply is already released.
- A thread with NORA whose suggestion list omits one move the fixture marks as discriminating, while the composer still accepts typed text.
- One `access.request` result: denied, reason that the capability is not on the evaluator role.
- One document that opens in the document viewer and one video id that opens in the video viewer (fixture bytes or a short placeholder clip).
- Desktop layout: phone on the right. Narrow layout: phone full screen.
- No control labeled with a pipeline step id (`deploy`, `submit_build`, and the rest).
- No Pixel / Samsung / iPhone chrome that a casual look would call a copy of those products.

Tests in `tests/terminal*.mjs` check the projection and the disabled pipeline actions without a browser and without the engine.
