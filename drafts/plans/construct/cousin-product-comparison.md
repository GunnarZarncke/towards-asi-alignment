# Cousin “product comparison” (spec sheet)

Status: **implemented** (2026-09-02). Site page live at `/start/spec-sheet/`.

Tongue-in-cheek **spec sheet** for research programs. Nobody is selling aligned ASI. TSA is not a product; the joke is treating manuals as if they were SKUs so differences become scannable. No overall winner, no stars, no CTA that implies a purchase.

**Placement:** near [Start Here](../../site/src/pages/start/index.astro) (`/start/spec-sheet/` or `/start/compare/`), not on the Field hub. The Field overview is a serious map of problems. Start Here already says the problem is unsolved; that is the right shelf for a spec-sheet page whose joke is chrome, not copy. Link from the Start Here side panel; agenda cards can still point at a column. **Do not** add a Field hub tile.

Related: agenda YAML [`reference/field-agendas/data/agendas/`](../../reference/field-agendas/data/agendas/); App B [`appendices/appB-bridge-crosswalk.tex`](../../appendices/appB-bridge-crosswalk.tex); Iliad sketch [`iliad-communal-canon.md`](iliad-communal-canon.md); LW-tag pilot [`lw-wiki-tags.md`](lw-wiki-tags.md); parked Ngo reverse column in [`field.md`](field.md).

---

## What this page is not

- **Not the coverage matrix.** Agenda × bridge cells stay on `/field/coverage/`. Content cuts stay there and in App B.
- **Not a claim that TSA renamed the field’s problems.** Say: *these programs work on overlapping unsolved problems; they differ in what they ship.*
- **Not a sales page.** No ranking. Aligned ASI is still unsolved even when a column ships a usable product (see that row).

Do not put “typed bridges” or “explicit non-converses” on the spec sheet.

---

## Feature rows (v1)

General enough that a cousin can honestly score Yes / Some / —.

| Row | Means | Notes |
|-----|--------|--------|
| **Ships a usable product** | Something a user or lab can actually run or buy *today*, even if alignment is unsolved. | Labs: frontier models with safety stacks (Some-to-Yes; “partly aligned”). CIRIS: shipped agent. Goodfire: SAE/Ember product (Anthropic/Goodfire row). TSA: companion site is a knowledge product, not an aligned-AI product — Some at most. Score the *kind* of object, not “alignment works.” |
| **Breadth** | One artifact tries to cover many agendas or problem clusters, not one lineage. | Iliad, CAIS/AISES, TSA field hub. Kosoy/GSAI/Redwood usually —. |
| **Long-form argument** | A readable through-line (book, sequence, survey) with a thesis, not only a TOC or a paper pile. | TSA book; Russell *Human Compatible*; MIRI sequences (historical). Iliad is Some until chapters exist. |
| **Living communal canon** | A skeleton others are invited to fill; authorship is not one lab. | Iliad’s explicit bet. **MIRI: Yes via LW wiki** (Arbital fold-in) — not intelligence.org. TSA’s site is one project’s publication layer — not communal. |
| **Formalization** | Mathematical or machine-checked structure for claims **or** specs. Proof assistant brand is irrelevant. | TSA claim-spine, Kosoy learning theory, GSAI/ARIA intended certificates. |
| **Translation** | How far the program maps *other* roster rows into its own terms without absorbing them. | TSA and Iliad/CAIS high; Kosoy/GSAI/Redwood low. Parked reverse direction: Ngo column in [`field.md`](field.md). |
| **Public knowledge site** | A maintained web layer for the program (wiki, cards, paths, news), not only PDFs. | **URLs live on agenda cards.** This row only records whether they *have* that layer. MIRI: Yes (LW wiki). TSA: Yes (this site). Iliad: Some (FAQ + projects, not a filled textbook). CHAI: org site, not a companion — Some or —. See [Sites](#sites). |
| **Constructive theory** | Offers a way to *build* or guarantee: agent theory, training/oversight recipe, spec+world-model stack. | Distinct from **ships a usable product**. TSA: — or weak Some (requirements decomposition, not a builder). |

Optional later: empirical evals; pause/governance as the program. Default: not in v1.

Scoring: **Yes** = that kind of object is load-bearing. **Some** = neighborhood. **—** = not their product. YAML `because` lines; human pass on marks.

Subhead, if kept: *Aligned ASI is not a product anyone ships. Some programs do ship something you can use.* Do not say “nobody has a working product.”

---

## Columns = existing agenda rows

No cousin taxonomy. Roster slugs, same titles, same cards ([`data/roster.yml`](../../reference/field-agendas/data/roster.yml)).

Do not merge GSAI with ARIA, or Christiano with ARC. Do not invent a Surveys column (CAIS already holds AISES).

**Default view:** `inMatrix` (existing flag). Iliad is off-matrix; show it via the same picker or flip `inMatrix` if we want it on both grids. Narrow screen: swipe with features fixed on the left.

Draft-column mapping (historical; not a second cut) is in git history of this file.

---

## Sites

Do not keep a parallel link list here. **Official URLs belong on agenda YAML `links:`** (generated cards). This spec sheet only scores the **Public knowledge site** and **Ships a usable product** rows.

Census at plan time (incomplete; verify on YAML):

| Roster | Knowledge site on the card? | Usable product (sketch) |
|--------|-----------------------------|-------------------------|
| TSA | Yes — towards-alignment.com | Knowledge site only |
| `miri` | Yes — [LW wiki](https://www.lesswrong.com/w) (Arbital import), AF, intelligence.org, StopWatch | — (advocacy + canon) |
| `iliad-textbook-from-the-future` | Some — textbook FAQ/projects, iliad.ac (already on card) | — |
| `chai-russell` | Some — humancompatible.ai, far.ai (already on card) | — |
| `cais-field-building` | Some — safe.ai; AISES textbook link on card | Course/textbook, not an AI product |
| `anthropic-lab` | Research index + Goodfire/Transluce/Neuronpedia (already on card) | Yes — models; Goodfire SAE/Ember |
| `google-deepmind-safety` | Lab research site | Yes — models |
| `ciris` | ciris.ai + GitHub (already on card) | Yes — shipped agent |
| Others | Score from existing `links:` | Usually — |

v1 copy: “Few programs ship a site that *is* the argument. MIRI’s explainer wiki is the LessWrong wiki (Arbital folded in). This site is TSA’s companion, not the field’s Wikipedia.”

**v2 (not this page):** offer TSA object-splits to that wiki — [`lw-wiki-tags.md`](lw-wiki-tags.md).

---

## Voice and UI

**Locked:** parody **title** and parody **visual**; quieter **wording**.

- **Title:** “Spec sheet” (or “Compare manuals”). The joke stops there plus the chrome.
- **Visual:** consumer spec-sheet / comparison-grid parody — product columns, feature rows, Yes / Some / — marks, sticky feature labels, maybe a thin “SKU” header using roster short names. Not a Field-matrix clone and not a blog post with a table glued on.
- **Wording:** dry. Captions, cell `because` text, FAQ, and Best for / Skip if read as ordinary Start Here copy. No Wirecutter voice, no fake prices, no “Buy,” no “nobody has a working product” (the usable-product row carries that fact).
- **TSA self-own:** Constructive theory is not Yes. Usable product is at most the site. Same type size as other columns.

Do not reopen “quiet table vs parody.” The split is chrome vs prose.

---

## Site placement

- Page: `/start/spec-sheet/` (or `/start/compare/`).
- Link from Start Here side panel, next to “What we are not claiming.”
- FAQ Q on Start Here: “Is this a product comparison?” — no product; spec sheet for manuals; some columns ship usable tools; none ship aligned ASI.
- **Do not** add a Field hub *tile* (the spec sheet is not a second field map). **Do** link *into* Field, App B, and agenda cards from the sheet — it is an on-ramp, not a silo. **Do not** put this in the PDF.

### Deeper links

The joke is chrome. The page still has to conduct. Quiet links, not a second essay:

| From | To |
|------|-----|
| Column header / short name | That agenda’s card (`/cards/field-agendas/{slug}/`) |
| Caption or footer | Field overview (`/field/`), coverage matrix (`/field/coverage/`), App B (`/cards/chapters/appB/` or `/full/appB/`) |
| Formalization row gloss | Lean spine (`/lean/`) where the cell is about a claim-spine or certificates |
| Translation row gloss | App B (bridges ↔ field cruxes); optional “on the matrix” for that column |
| Public knowledge site = Yes | The official URL already on the agenda card (LW wiki, this site, …) — do not duplicate a link dump on the sheet |
| Best for / Skip if | At most one extra in-site link (card or Field), not a paragraph |

Start Here → spec sheet → Field/App B/cards is the intended path. Spec sheet → Start Here is already covered by nav.

### Data

[`reference/field-agendas/data/product-comparison.yml`](../../reference/field-agendas/data/product-comparison.yml):

- `features[]` — id, label, gloss
- `columns[]` — one roster `slug` each, `bestFor`, `skipIf` (links from agenda YAML, not duplicated)
- `cells` — `{ feature, column, mark, because }`

Sync with field-agenda sync or a sibling. Human pass on marks.

---

## Implementation steps

1. Freeze feature rows (including **ships a usable product**). Columns = roster slugs; default `inMatrix`.
2. Draft YAML `because` lines; Gunnar edits marks.
3. `/start/spec-sheet/` as a spec-sheet grid (parody chrome). Mobile: horizontal swipe, features sticky. Best for / Skip if: two dry lines per column.
4. Start Here link + FAQ sentence + agenda-card footer (“On the spec sheet”).
5. Caption: judgments, not a ranking; usable product ≠ aligned. Footer links: Field, coverage, App B.

### Verification

- Site build. No Field hub tile; Field / coverage / App B / agenda cards linked from the sheet.
- Knowledge-site URLs resolve from agenda cards, not a second list.
- Constructive-theory cell for TSA is not Yes.
- Coverage matrix unchanged.

---

## Non-goals

- Rewriting App B or the matrix.
- Iliad-style communal editing of the book ([`iliad-communal-canon.md`](iliad-communal-canon.md)).
- Implementing the LW-tag pilot in the same PR ([`lw-wiki-tags.md`](lw-wiki-tags.md)).
- Cursor canvas.

---

## Open

- Default visible set: `inMatrix` vs that plus Iliad.
- URL slug: `spec-sheet` vs `compare`.
