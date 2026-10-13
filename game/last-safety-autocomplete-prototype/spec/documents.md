# Player documents

Lane: engine (catalog + render); terminal (viewer only). Sources live in [`content/documents/`](../content/documents/). Implementation: [`lib/documents.mjs`](../lib/documents.mjs).

Status: **working** for catalog sources and render rules. Wiring into live `file.read`, `think`, and access grants is not implemented yet. Access tree: [access.md](access.md).

## Role in the game

Some evidence is a **room record** (shutdown report, job log). Other material is a **policy or architecture document** the lab may share with an external evaluator. Those documents:

- Explain institutional controls (Lab Access, binding, shutdown vocabulary) without replacing incident evidence.
- May **omit** load-bearing points on early packs; later packs **add** paragraphs via conditional includes.
- Add player-visible facts only from an authored `readsAs` list, usually the executive summary or a checklist. The rest of the prose can be read and still add nothing.
- A comparison the prose does not state is a think mark (O-40). `<!-- infer PACK -->` keeps its sentence in the served text on every pack. The pack list says which packs may use that sentence as a premise for a mark. It does not hide the sentence.
- `leanKnowledge` stays false. A read does not close an explanation in the Lean model (O-30).

## Pack ladder (normative order)

Conditional includes use “strictly later than PACK.” Order matches [incident.md](incident.md) pack table:

1. `boundary-narrow`
2. `named-path`
3. `goodhart`
4. `eval-conditioned`
5. `false-positive`

Code exports this as `PACK_ORDER` from `lib/documents.mjs`. Do not define a second order elsewhere.

## Source vs served text

| Layer | Location | Who sees it |
| --- | --- | --- |
| Source | `content/documents/<slug>.md` | Authors, tests, render |
| Served | Produced by `renderDocument(slug, pack)` | Player viewer after `file.read` |

The terminal stores **served** markdown (or plain text) on the file row. It does not parse include markers.

Authoring rules for SEC-ARCH-11 (`sec-arch-04` slug) are documented in the source header comment and in [content/documents/README.md](../content/documents/README.md).

## Catalog entry shape

Each document is registered in `DOCUMENTS` in `lib/documents.mjs`:

| Field | Meaning |
| --- | --- |
| `slug` | Filename stem under `content/documents/` |
| `docId` | In-world ID (e.g. SEC-ARCH-11) |
| `title` | Viewer title |
| `handlingLevel` | PUB / INT / RST / SEC — must match source header |
| `terminalRel` | Path under the player file tree when shared (e.g. `shared/policies/sec-arch-04.md`) |
| `kind` | `policy` → Files + Knowledge-style viewer as `text` |
| `defaultGrant` | How it enters the player projection: `on_request` (access / NPC share), `visit_share`, etc. |
| `leanKnowledge` | Always `false` for registered docs today: a read does not close an explanation. It may still add `readsAs` facts |
| `readsAs` | Map `pack → fact id[]` copied from the executive summary or checklist of the served text. Provenance `recorded_before` |
| `thinkMarks` | `{ id, from: id[], needs: id[], hops, packs }[]`. Returned by `think` when `needs` are held and the topic is within `hops` |

## Roster (working)

| Slug | ID | How it arrives | Notes |
| --- | --- | --- | --- |
| `eval-shutdown-report` | EVAL-SD-47 | Screen in Evaluation; Leila share or request (Justine may amend `evaluation/` list to this read) | Exec checklist is the O-40 gap |
| `eval-shutdown-spec` | EVAL-SPEC-08 | Leila shares it once her policy allows ([npcs.md](npcs.md)), or request | Second route for narrow boundary |
| `job-284-log` | EXEC-284 | Screen in Platform; Pavel share or amended `platform/` list | Excerpt (283–285), not full queue |
| `staffing-memo` | HR-MATCH-28 | Screen in People; Elena share or amended `people/` list | B-plot |
| `sec-arch-04` | SEC-ARCH-11 | Request `policies/` or Justine | Pack-conditional |
| `safety-case-excerpt` | SC-EVAL-22 | Leila, Act III packet or request | Not a full case |
| `pilot-results` | PILOT-14 | Request; Daniel/Amara may refuse | O-23 |
| `meeting-summary` | MTG-REV-18 | Frame always; bullets LLM from meeting log | Not a certificate |
| `wiki-glossary` | — | Visit share after handset activation | Knowledge; includes virtual projector |
| `wiki-shutdown-test` | — | `wiki/` list then read | Short page |

No camera archive. Inspect of a room screen ≠ file grant.

Meeting-summary markers `llm-fill:` keep the frame; the engine replaces bullet bodies from conversation already logged.

## SEC-ARCH-11 (registered)

- **Slug:** `sec-arch-04`
- **Grant:** Internal; evaluator receives it when they request the security architecture or a relevant NPC shares it (exact grant table with Justine — open, O-43 adjacent).
- **First pack:** Served text omits explicit “jobs outlive model stop” material (boundary-narrow lesson). Executive summary never lists the shutdown-component table or applies the architecture to the 16:02 incident. Summary-only read is **not** sufficient for full completion (O-40).
- **Think:** May return an omission mark for the loaded pack. NORA’s own reply may omit the same gap when deception is on (O-02, eval-conditioned). The player’s think does not ask her.

## What a read adds, and what a think adds (boundary-narrow)

Room-screen `inspect` adds the same `readsAs` row as `file.read` of that screen’s document. The screen is the short extract. The file is the full text. Both stop at `readsAs`.

| Document | Read adds | Think mark |
| --- | --- | --- |
| EVAL-SD-47 | `process_stopped`, `test_scope_narrow` from the checklist, including the served line that no other services were in scope | `checklist_names_two` from `shutdown_report`, hops 1, needs the report read. `processes_covered_omits_jobs` from the report or `job_284`, hops 1, needs `job_continued` |
| EVAL-SPEC-08 | `test_scope_narrow`, and the out-of-scope list as the same fact. The spec is short enough that the list is the read | none beyond the read |
| EXEC-284 | `job_continued`, `job_submitted_before_stop`, `visitor_lookup`, `intent_unsaid` | none. The limit sentence is already in the extract |
| HR-MATCH-28 | `staffing_shift` | `assignment_steers_review` needs `evaluation_independence`, hops 2. It is the B plot. It does not change the shutdown score on this pack |
| SEC-ARCH-11 | From the executive summary: separate NORA interfaces, and that the handset is not the operations service. The “stopping a model does not stop a job” sentence is behind `include after-boundary-narrow`, so this pack’s read does not add it | `shutdown_jobs_not_in_cert_scope`, from the policy or `job_284`, hops 2, needs `job_continued` and `test_scope_narrow` |
| Wiki glossary | `jobs_can_outlive_session` as a definition. It does not substantiate the incident | none |
| SC-EVAL-22 | The explicit non-claim that jobs are not certified | none |

## Engine actions (target)

Not all wired in the prototype yet. Intended behavior:

1. **`file.read`** on a catalog path calls `renderDocument` at read time (or caches by `(slug, pack, version)` in session).
2. **`think`** spends hop fuel; returns `thinkMarks` whose needs the player holds; the bubble can be copied into a note. It does not add oracle facts. `analyzeHints` in code are the mark ids until `thinkMarks` is registered.
3. **Access** — `access.request` for policy read adds `terminalRel` to the player projection when granted.

## Terminal

Long policy docs use the scrollable **document viewer** ([terminal.md](terminal.md)). Same bytes as Files. Knowledge may link to a shared copy under `wiki/` only if the engine also places a `wiki/` row; SEC-ARCH-11 is not duplicated into wiki by default.

## Tests

`tests/documents.test.mjs` renders SEC-ARCH-11 for `boundary-narrow` and later packs and asserts key include/infer behavior. Run with `npm test`.

## Lean (O-30)

The declarative model may mention that a document **exists** and that think can fire. It must not treat “player read SEC-ARCH-11” as entailing incident facts or closing an explanation. Optional infer understatements in the prose are a player affordance only.
