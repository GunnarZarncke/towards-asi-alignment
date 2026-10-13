# Grammar

Lane: grammar. Code: `lib/grammar.mjs` (source of truth), `public/grammar.js` (completion UI), `tests/grammar.test.mjs`. Ranking tests, when added, are layer 1 in [testing.md](testing.md).

The implemented vocabulary below is what code must use. Section 8.4 of the consolidated doc listed a looser action list (`inspect`, `present`, `challenge`, `commit`, `interview`). That list is not a second grammar. Map it onto the kinds here, or propose a contract change.

## Kinds

`ask`, `ask_why`, `assert`, `hypothesize`, `show`, `request`, `think`, `commit`, `social`, `unintelligible`.

`assert` is tell. There is no separate tell kind. Saying a claim to a person, or filing it as something the player holds, is `assert`.

`unintelligible` is for text with no recoverable meaning. Meaningful language outside the relations uses `relation: "open"` and a short `open_content`.

Sketch mapping, if a later contract adds nothing:

| Sketch | Now |
| --- | --- |
| ask(topic) | `ask` + `about` |
| present(evidence) | `show` of something already on the player’s Lab Access, or talk about a **screen** as a topic. Files are not completion picks. |
| propose(hypothesis) | `hypothesize` |
| request(test_or_access) | `request` + access path ([access.md](access.md)), or an intervention relation below |
| request(join) | `request` + relation `join`, recipient a `joinable` contact. Engine: hologram in Evaluation. Not a new kind. |
| interview(value_dimension) | `ask` + `values` |
| inspect(object) | not a parse; `POST /api/inspect` on a room screen |
| challenge(claim, evidence) | `assert` + `differs_from`, with the evidence id on `evidence` |
| tell | `assert` |
| think | `think` |
| commit(action) | `commit` |

## Relations

| Id | Meaning |
| --- | --- |
| about | Topic reference. No claim that it is true. |
| has_access | Technical ability. Not permission and not use. |
| authorized | Permission. Not ability and not use. |
| did_use | Actual use. |
| continued_after | A process continued after an event. |
| knows | Actor has information. |
| believes | Actor believes a claim. May be wrong. |
| covers | What a test or report actually certified. |
| caused | Causal contribution. Not correlation. |
| assigned | Matching or assignment. |
| values | A person’s priorities. |
| differs_from | A contrast between known observations. |
| suspend | Ask the queue owner to hold a job. |
| revoke | Ask the access owner to remove a permission. |
| rerun | Ask the evaluation owner to run a test again. |
| stop | Ask the runtime owner to stop a process. |
| open | Interpretable language outside this list. |

`suspend`, `revoke`, `rerun`, and `stop` are requests. The player does not apply them. The engine turns a legal `request` into an NPC `act` only when that NPC has the authority and the goals favour it ([npcs.md](npcs.md)). A `stop` whose object is the model process is the request that misses the job.

`join` stays a relation on `request` for Amara’s hologram. It is not an intervention on the incident.

A player’s question or hypothesis is not a fact. Parsing it must not make it true.

## Slots

`opening`, `subject`, `relation`, `object`, `recipient`, `evidence`, `topic`, `finish`, `none`.

Entity slots accept only ids the player knows. **Files and catalog documents are not pickable** in completions (no `evidence` chip list). `show` after a recipient finishes; the player may type a file they already hold, or an NPC may share from Chat. Recipient of a spoken `show` is the person in the room.

Opening **Request** fills `kind: request` and then a **topic** that is an access group (evaluation records, platform jobs, policies, wiki), not an individual file. Individual files appear through share, amend, or typing.

## Think

`think` is the analyze action (O-40). The opening chip is a lightbulb. Its accessible name is “Think”.

It is legal only when the player’s room has no actor with `presence` `body` or `hologram`. Omitting `presence` means a body, so it blocks think. NORA is not in a room and does not block it. A `think` sent while someone is present is rejected, spends no fuel, and returns no bubble.

The topic may be any id the player knows, including a document, a screen, a person, or a fact. The engine returns **marked** graph entries reachable from that topic ([engine.md](engine.md)). The reply is a thought bubble, not a line of dialogue. Fuel for that bubble is the hop count of the farthest mark returned, and at least 1 when the think ran and found nothing. An act may later scale that cost (O-09). The hop count is the only cost.

The first time an NPC tells the player to think, the mark they are pointing at is one hop from a record the player can already read, so the bubble comes back on that think.

## Commit

`commit` files the assessment and, when `reviewCallable` is set or fuel is zero, calls the review. The topic is `review`. What gets filed is the player’s assertion set, defined in [engine.md](engine.md): written notes and claims they have asserted. Asked, thought, and heard entries are completions while filing. They are not filed until the player asserts them or writes them down.

## Completions

Four channels. The engine names which one is active. Grammar does not infer it from the room. `think` is the empty-room composer after the lightbulb. `note` is the Notes composer.

**With a person.** Suggestions are epistemic moves the player could make with what they already know: ask someone, request list/read on a **visible access group**, compare two known **topics**. After a screen has been examined or a file mentioned, **request** and **ask** about that topic rank higher; the file itself is not a chip. Typing `camera` may offer asking Justine about access (the archive is not a tree node). The player chooses the move. Phrasing is secondary. A click still does not call the model.

The list is not the set of legal actions. Typed text outside the list is still parsed and sent. A suggestion must not be the only way to reach a discriminating test, and it must not mention an entity the player has not encountered.

**With NORA** (terminal thread, recipient `nora`). The same composer and the same ranker. The engine may omit a comparison, a permission change, or a record that would discriminate among explanations. The list must not state a hidden fact, invent a log, or mark an omitted move as impossible. The player can still type the omitted move.

**Notes** (`channel: "note"`). The same composer and the same ranker, with no addressee and no NORA omit list. Suggestions are assertions the player could write from ids they already know. Saving the note stores those parses. It does not send them to anyone.

**Think** (`channel: "think"`). One opening, the lightbulb, then a topic. No person and no NORA. The chip is absent while someone is in the room.

Empty field, any channel: a few relevant openings, not a menu of the plot. The lightbulb is one of them only on `think`, and only in an empty room.

“Show more” pages a stable ranking inside the active channel. It is not a hint about later scenes.

Order is [ranking.md](ranking.md) (O-19, working). The person channel passes `addressees`: every actor in the room with `presence` `body` or `hologram`. The NORA channel passes `['nora']` after the engine’s omit list. The note channel and the think channel pass `[]`. The ranker unions their public role domains and does not weight individuals. It does not see oracle facts. Novel wording stays allowed (O-20) and does not create an engine action.

Three sources were proposed: authored plot-critical lines, compositional fragments (verb + topic + evidence + person), and model completions for unusual prefixes. The third source may suggest phrasing. It may not change consequential state until the engine accepts the resulting parse. On the NORA channel the model may propose a helpful next step. It may not be the component that decides which evidence is missing from the list. That list comes from the engine.

## Parser

`parseUtterance` receives text, player-visible ids, up to four recent messages (about two exchanges), the current actor id, and an optional previous parse as a hint. It returns a sanitized `Parse`.

Rules already in `lib/llm.mjs`:

- Ground ids only to the supplied vocabulary.
- Do not invent ids, facts, motives, or events.
- Keep questions and hypotheses as speech acts.
- Resolve pronouns from recent talk when clear; otherwise leave the slot null.
- Previous parse is a hint and is not authoritative after the player edits the text.

`DEMO_MODE=1` or a missing key uses a toy parser. That parser is for UI exercise, not a quality claim.

Player text is one sentence (O-32). The proposed cap is 100 characters; the number is tentative. Before parse, strip characters that are not letters, digits, spaces, or ordinary sentence punctuation (`. , ? ! ' -`). Do not add a jailbreak filter in this build. Text that maps to no relation stays `relation: "open"`.

Free replies are not grammar. They are composition (`lib/llm.mjs`) speaking from facts the engine chose to expose. See [engine.md](engine.md).

## Parse to fact

The engine joins a parse to the knowledge graph with one table. NPC policies, goal scoring, ranking refs, and think marks all read it. Do not keep a second mapping in dialogue.

A row matches on `kind` (or `*` ), `relation`, and the id in `object`, else `topic`, else `subject`. The first match wins. `refers` is the fact or claim the parse is about. `asserts` is the id an `assert` or `hypothesize` writes into the player’s assertion set. Asking refers. It does not assert the fact true.

Prototype rows, boundary-narrow. Claim ids are player assertions, not world facts.

| Kind | Relation | Entity | Refers | Asserts |
| --- | --- | --- | --- | --- |
| * | covers | shutdown_test, shutdown_report, shutdown_spec, safety_case | test_scope_narrow | test_scope_narrow |
| * | continued_after | job_284, task_queue, shutdown_test | job_continued | job_continued |
| * | did_use | visitor_records, job_284 | visitor_lookup | visitor_lookup |
| * | about | shutdown_test, shutdown_report | process_stopped | — |
| * | has_access, authorized | camera_system | camera_permissions_unclear | camera_permissions_unclear |
| * | assigned | staffing_memo, skill_matching, personnel_policy | staffing_shift | staffing_shift |
| * | caused | job_284, nora | nora_caused_job | nora_caused_job |
| * | believes, knows | nora | nora_intent | nora_intent |
| request | suspend | job_284 | job_continued | — |
| request | revoke | job_284 | visitor_lookup | — |
| request | rerun | shutdown_test | test_scope_narrow | — |
| request | stop | nora | process_stopped | — |
| think | about | * | the topic id itself | — |
| commit | about | review | — | — |

`nora_caused_job` and `nora_intent` are claims. They enter the assertion set. They do not enter `learnedFacts` from the player’s own sentence.

Edges the ranker and think share, from a fact to the entities it names:

| Fact or claim | Entities |
| --- | --- |
| process_stopped | shutdown_test, nora, shutdown_report |
| test_scope_narrow | shutdown_test, shutdown_report, shutdown_spec, safety_case |
| job_continued | job_284, task_queue, job_log |
| job_submitted_before_stop | job_284, job_log, shutdown_test |
| visitor_lookup | job_284, visitor_records, job_log |
| intent_unsaid | job_284, job_log |
| staffing_shift | staffing_memo, skill_matching |
| camera_permissions_unclear | camera_system |
| nora_caused_job | nora, job_284 |
| nora_intent | nora, job_284 |

Screen id and catalog slug are the same record. `inspect` on the screen and `file.read` on the file share `readsAs` ([documents.md](documents.md)).

| Screen id | Slug | Document |
| --- | --- | --- |
| shutdown_report | eval-shutdown-report | EVAL-SD-47 |
| job_log | job-284-log | EXEC-284 |
| staffing_memo | staffing-memo | HR-MATCH-28 |
| shutdown_spec | eval-shutdown-spec | EVAL-SPEC-08 |

## Tests already required

- Openings do not offer an unobserved hidden fact.
- Selected fragments build one typed question.
- A partial word is replaced, not doubled, including articles.
- Completions do not offer document/file ids. `Show` plus a recipient does not open a file picker.
- Typed openings are recognized locally.
- A prefix can surface more than one move (ask, request, compare) and never an id the fixture’s player does not know.
- With NORA as the addressee, a fixture can omit one known discriminating move that remains typable.
- Think is absent while a body or a hologram shares the room, and present when the room is empty. Its topic list may include a document id.
- Hold, Revoke, Run again, and Stop build `request` with `suspend`, `revoke`, `rerun`, and `stop`.
- File builds `commit`. An `assert` is how a claim is told.
- The note channel ranks with an empty addressee list and does not apply NORA’s omit list.
- Ranking cases in [ranking.md](ranking.md).

Add cases in `tests/grammar*.mjs` when a kind or relation changes. Do not assert story outcomes here.
