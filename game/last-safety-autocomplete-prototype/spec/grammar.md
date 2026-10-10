# Grammar

Lane: grammar. Code: `lib/grammar.mjs` (source of truth), `public/grammar.js` (completion UI), `tests/grammar.test.mjs`.

The implemented vocabulary below is what code must use. Section 8.4 of the consolidated doc listed a looser action list (`inspect`, `present`, `challenge`, `commit`, `interview`). That list is not a second grammar. Map it onto the kinds here, or propose a contract change.

## Kinds

`ask`, `ask_why`, `assert`, `hypothesize`, `show`, `request`, `social`, `unintelligible`.

`unintelligible` is for text with no recoverable meaning. Meaningful language outside the relations uses `relation: "open"` and a short `open_content`.

Sketch mapping, if a later contract adds nothing:

| Sketch | Now |
| --- | --- |
| ask(topic) | `ask` + `about` |
| present(evidence) | `show` |
| propose(hypothesis) | `hypothesize` |
| request(test_or_access) | `request` |
| interview(value_dimension) | `ask` + `values` |
| inspect(object) | not a parse; `POST /api/inspect` |
| challenge(claim, evidence) | not a kind yet |
| commit(action) | not a kind yet |

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
| open | Interpretable language outside this list. |

A player’s question or hypothesis is not a fact. Parsing it must not make it true.

## Slots

`opening`, `subject`, `relation`, `object`, `recipient`, `evidence`, `topic`, `finish`, `none`.

Entity slots accept only ids the player knows. Evidence offered for `show` must already have been examined. Recipient of a spoken `show` is the person in the room.

## Completions

Two channels. The engine names which one is active. Grammar does not infer it from the room.

**With a person.** Suggestions are epistemic moves the player could make with what they already know: ask someone, request a record, compare two known items, show an examined record. Typing `camera` may offer asking Farah about access, requesting footage, or comparing the camera record with the job log, and only the ones the player’s knowledge supports. The player chooses the move. Phrasing is secondary. A click still does not call the model.

The list is not the set of legal actions. Typed text outside the list is still parsed and sent. A suggestion must not be the only way to reach a discriminating test, and it must not mention an entity the player has not encountered.

**With NORA** (terminal thread, recipient `nora`). The same composer, a different ranking. Suggestions follow what NORA is willing to help with. They may omit a comparison, a permission change, or a record that would discriminate among explanations. They must not state a hidden fact, invent a log, or mark an omitted move as impossible. The player can still type the omitted move.

Empty field, either channel: a few relevant openings, not a menu of the plot.

“Show more” pages a stable ranking inside the active channel. It is not a hint about later scenes.

Ranking inputs with a person, in the prototype: public NPC expertise, known entities, examined evidence, room. NORA’s omissions are specified with the incident model, not by the prototype ranker. Fuller ranking (O-19) and novel questions (O-20) stay open. Until they close, do not rank the person-channel by oracle facts.

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

Free replies are not grammar. They are composition (`lib/llm.mjs`) speaking from facts the engine chose to expose. See [engine.md](engine.md).

## Tests already required

- Openings do not offer an unobserved hidden fact.
- Selected fragments build one typed question.
- A partial word is replaced, not doubled, including articles.
- `show` cannot complete evidence that was not inspected.
- Typed openings are recognized locally.
- A prefix can surface more than one move (ask, request, compare) and never an id the fixture’s player does not know.
- With NORA as the addressee, a fixture can omit one known discriminating move that remains typable.

Add cases in `tests/grammar*.mjs` when a kind or relation changes. Do not assert story outcomes here.
