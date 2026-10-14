# Text console

Lane: text console. Code: `lib/text/console.mjs` (commands and change printing), `lib/text/view.mjs` (player-visible text view, shared with the playtest harness), `scripts/text-play.mjs` (terminal), `public/text.html` (browser page on `POST /api/text`), `tests/text-console.test.mjs`.

The same game as the room view, with words for the picture. It plays one session through `applyAction` and reads only `ClientState` and `TerminalState` ([contract.md](contract.md)). It never reads oracle facts or NPC records. The browser page shares the cookie session with the graphical UI, so a player can switch between the two mid-visit.

## What it shows

- **Room:** title, the floorplan `role` text, windows, people present (projected people marked), doors with compass wall and whether the badge opens them, screens with read/unread. The floorplan `people` field is not shown; presence comes from state.
- **Talk:** NPC lines as `Name: text`. The player's own line is not echoed.
- **Movement:** arrivals `Name is here now.`; departures `Name heads to {room title}.` (same destination the graphical room list shows on door buttons).
- **Phone:** lines prefixed `[phone]` for new thread messages, notifications (thread notifications are skipped; the message itself prints), and access replies.
- **Prompt:** clock, fuel, room, and the person you face.

## Not reshowing

After each command the console prints the command's own result, then only what changed since the last command: act, room, arrivals and departures, new NPC lines, newly learned facts (`(noted)`), handset activation, phone traffic, a new thought, a new open question, review callable, ending. A first visit prints the full room; a revisit prints the title, people, and doors. Anything else reprints only on request (`look`, `phone`, `know`, `records`, `status`). An empty line reprints the room.

## Commands

`help` lists them. A bare number picks from the last numbered list (suggestions, screens, files, doors, topics, access paths, thread sends). Unknown input is said to the person you face, through the same parser as the composer (`parseUtterance`; demo grammar without a key).

| Command | Effect |
| --- | --- |
| `look`, `exits`, `records`, `who` | room, doors, every screen with its room, people |
| `go <room>` | walk; several doors if needed (one `go` action per door, so fuel and clock match the room view) |
| `read <screen>` | inspect a screen in this room; names the room if it is elsewhere |
| `to <name>` | face someone present |
| `s [words]` | complete sentences from the O-19 ranker, filtered by words |
| `say <text>` | typed sentence |
| `think [topic]`, `keep`, `close` | thought in an empty room; keep writes the note |
| `know`, `status`, `file` | learned facts, clock and act, file the review |
| `phone`, `files`, `open`, `msg <who> [text]`, `access`, `request <path> [verb]`, `note`, `share`, `contacts`, `calendar` | handset, after `labAccessActive`. **`open`** lists files when bare; opens by case-insensitive prefix on display name, path, or basename (like **`go`** for rooms). |

The terminal script adds `save [file]`, `load <file>`, `reset`, `quit`. In the browser, save and load stay in the room view menu.

**Save and resume (terminal only):** `save` writes the same JSON as `GET /api/export` (`version`, `scenario`, `events`). With no filename it uses the session save path (default `last-safety-review-save.json`). Tab after `save` or `load` fills that path for editing. Starting `npm run text` loads that file when it exists; use `--file <path>` or `-f` or a positional path to resume another file. `load <file>` switches the session save path to that file.

## Debug knowledge

After each command, a **`[debug knowledge]`** block lists what changed in the player projection: new **`learnedFacts`** (id, text, provenance, `from`, refs), newly visible **entities**, **examined** screens, **introduced** actors, and **heard** rows. Not oracle truth. Code: `lib/text/kb-debug.mjs`.

| Surface | Flag |
| --- | --- |
| Browser `/text.html` | `?debug=1` |
| Terminal `npm run text` | `--debug` (combine with `--demo` as needed) |

Normal play still shows new facts inline as **`(noted)`** in the command output (`lib/text/console.mjs` `changes()`).

## `know`

Prints the full player **learned-facts** list: every row in `learnedFacts` as `- {text}`. It does not show fact ids, provenance, or entities that are visible only as vocabulary without a learned fact row. Same data the room UI’s knowledge strip uses, in plain text.

## Tab completion

Same **fragment** ranker as the room composer (`public/grammar.js`, O-19). Up to **five** options per page. Shared logic: `lib/text/tab-complete.mjs`.

| Surface | Behavior |
| --- | --- |
| **`npm run text`** | Node readline **Tab** (no literal tab): completes **`go` / `to` / `read`** arguments and speech; **`msg` / `dm`** contact names, then the same grammar chips as the phone thread (**`msg nora `**, **`msg leila `**, …); **Tab** again on the same line shows the next page. |
| **`/text.html`** | **Tab** opens an overlay: best match in the input, four alternatives above; **↑/↓** cycle; **Tab** next page; **Esc** close. Command lines (including **`msg`**) use **`POST /api/tab-complete`**; bare speech uses the fragment ranker. Code: `public/text-input.mjs`. |

## Check

`node --test tests/text-console.test.mjs`: the first room view prints in full and later commands do not reprint it; a picked sentence prints only the change; first visit and revisit differ; no fact text reaches the console unless the player learned it or thought it.
