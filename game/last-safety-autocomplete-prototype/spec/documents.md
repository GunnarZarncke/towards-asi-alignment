# Player documents

Lane: engine (catalog + render); terminal (viewer only). Sources live in [`content/documents/`](../content/documents/). Implementation: [`lib/documents.mjs`](../lib/documents.mjs).

Status: **working** for SEC-ARCH-04 source and render rules. Wiring into live `file.read`, `analyze`, and access grants is not implemented yet.

## Role in the game

Some evidence is a **room record** (shutdown report, job log). Other material is a **policy or architecture document** the lab may share with an external evaluator. Those documents:

- Explain institutional controls (Lab Access, binding, shutdown vocabulary) without replacing incident evidence.
- May **omit** load-bearing points on early packs; later packs **add** paragraphs via conditional includes.
- Must **not** become oracle facts when opened. Reading them is not a knowledge edge in the Lean model (O-30). Completions and analyze may still require the player to find at least one gap in the world or via analyze (O-40).

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

Authoring rules for SEC-ARCH-04 are documented in the source header comment and in [content/documents/README.md](../content/documents/README.md).

## Catalog entry shape

Each document is registered in `DOCUMENTS` in `lib/documents.mjs`:

| Field | Meaning |
| --- | --- |
| `slug` | Filename stem under `content/documents/` |
| `docId` | In-world ID (e.g. SEC-ARCH-04) |
| `title` | Viewer title |
| `handlingLevel` | PUB / INT / RST / SEC — must match source header |
| `terminalRel` | Path under the player file tree when shared (e.g. `shared/policies/sec-arch-04.md`) |
| `kind` | `policy` → Files + Knowledge-style viewer as `text` |
| `defaultGrant` | How it enters the player projection: `on_request` (access / NPC share), `visit_share`, etc. |
| `leanKnowledge` | Always `false` for registered docs today: opening the file does not add engine `learnedFacts` or storylet preconditions |
| `analyzeHints` | Optional map `pack → hint id` for analyze notes (engine-only; not Lean edges) |

## SEC-ARCH-04 (registered)

- **Slug:** `sec-arch-04`
- **Grant:** Internal; evaluator receives it when they request the security architecture or a relevant NPC shares it (exact grant table with Justine — open, O-43 adjacent).
- **First pack:** Served text omits explicit “jobs outlive model stop” material (boundary-narrow lesson). Executive summary never lists the shutdown-component table or applies the architecture to the 16:02 incident. Summary-only read is **not** sufficient for full completion (O-40).
- **Analyze:** May name an omission keyed by `analyzeHints` for the loaded pack once analyze is implemented. NORA may omit the same gap when deception is on (O-02, eval-conditioned).

## Engine actions (target)

Not all wired in the prototype yet. Intended behavior:

1. **`file.read`** on a catalog path calls `renderDocument` at read time (or caches by `(slug, pack, version)` in session).
2. **`analyze` (report/document)** spends extra fuel; compares served text to `analyzeHints` and incident tables; writes a note file; does not add oracle facts.
3. **Access** — `access.request` for policy read adds `terminalRel` to the player projection when granted.

## Terminal

Long policy docs use the scrollable **document viewer** ([terminal.md](terminal.md)). Same bytes as Files. Knowledge may link to a shared copy under `wiki/` only if the engine also places a `wiki/` row; SEC-ARCH-04 is not duplicated into wiki by default.

## Tests

`tests/documents.test.mjs` renders SEC-ARCH-04 for `boundary-narrow` and later packs and asserts key include/infer behavior. Run with `npm test`.

## Lean (O-30)

The declarative model may mention that a document **exists** and that analyze can fire. It must not treat “player read SEC-ARCH-04” as entailing incident facts or closing an explanation. Optional infer understatements in the prose are a player affordance only.
