# Access requests

Lane: engine (tree, grants, delay, amendments); terminal (API explorer). Implementation: [`lib/access.mjs`](../lib/access.mjs).

Status: **working**. Closes O-43 for the evaluator isolate. Camera **archive** is not a node (no document, no folder). Camera remains a conversational topic.

## Tree

The API app lists **top-level folders and the services group** only, until a `list` grant on a parent reveals children.

Shape: `folder/` → semantic subfolder → file. `services/` → named services (execution queue, Lab Access binding, door access, NORA Assist, evaluation runtime).

Verbs: **list**, **read**, **write**. Write is only on player-owned `notes/` and `photos/`. Evaluator write on lab folders is denied.

Hidden means **absent**, not a locked row (same as [terminal.md](terminal.md) files pane).

## Request, amend, chat

`access.request` carries `{ path, verb }`.

The engine may **amend**: a list/read on a wide folder becomes list/read on a specific child, often with a **Chat** from the approver (Justine, Pavel, Elena). Amendment is a grant, not a silent substitute of the original path.

Example (all packs, until a pack table overrides): `list` on `evaluation/` → list `evaluation/shutdown/` and read EVAL-SD-47, plus Justine’s message that Evaluation-wide list is too wide.

Face-to-face asking the same person can still yield a wider grant; it costs more (below).

**Pack gates (boundary-narrow).** Wide `list`/`read` on `evaluation/`, `people/`, and `policies/` stays denied until `visitor_introduced_justine` (Ian vouch in Commons) or the player has told Justine a review reason on the handset. `platform/` needs the job log examined or a stated reason to Pavel. If the approver is in the player’s room when the grant releases, delay uses `walk_and_ask`. Implementation: [`lib/world/access-gates.mjs`](../lib/world/access-gates.mjs), pack table in [`lib/world/packs/boundary-narrow.mjs`](../lib/world/packs/boundary-narrow.mjs).

## Delay (fuel)

Exact numbers wait on O-09. **Order is fixed:**

`reject` < `grant` (including amend) < walk to the person and ask.

Rejecting is the fastest result. A phone grant is slower than a reject and faster than going to the room.

## How a file enters Lab Access

Not by picking it in autocomplete.

1. **NPC share** — they mention it and `file.share` (or engine places the row) into the player projection. Salient after the mention.
2. **Story beat** — a screen or presentation is inspected; at a matching time the engine shares the file, **or** the player `access.request`s it.
3. **Visit share** — e.g. `wiki/glossary` after Lab Access activation.

Inspecting a **room screen** is not acquiring the file. The display can be a short extract; the catalog document is the full text after share or grant.

## Completions

Document and file ids are **not** completion pick targets ([grammar.md](grammar.md)). After a screen is examined or a file is mentioned, rank **request** (access path) and **ask** (topic) higher ([ranking.md](ranking.md)). Typed `show` of a file the player already holds still parses.

## Pipeline

Pipeline capabilities stay denied. They are not folders in this tree.
