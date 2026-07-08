# Release Notes

*Towards Superintelligence Alignment: Boundaries, Values, and Correction*

Most recent release first. Versions follow a simple `MAJOR.MINOR.PATCH` scheme:

- **MAJOR** — structural milestones (numbering scheme, part/chapter architecture, or a manuscript milestone declared complete).

- **MINOR** — new or substantially rewritten chapters, appendices, or framework objects.
- **PATCH** — fixes, calibration, citations, and editorial passes.
---

## v1.1.0 — 2026-07-08 — Legibility, companion site, and empirical spine

A consolidation release focused on **external legibility** (making the framework readable and checkable by outside researchers, funders, and policy readers), a full **companion website**, a new **institutional-histories appendix**, and four **empirical experiment lines** that stress-test bridge cruxes. 

### Reader-facing language and legibility

- **Cleaned up vocabulary** Load-bearing jargon now leads with an operational paraphrase and keeps coined terms only as shorthand. Symbols, equations, and Lean predicate names are unchanged.
- **Operational glossary (Appendix E) rewritten and expanded.** Each entry is paraphrase-first with a *nearest field term* delta and a concrete (often non-AI) example. 
- Front-matter orientation, README split, guided reading paths, and the About authorship note tightened for outside readers.

### New appendix — Institutional histories (Appendix D / `appM`)

- Mechanism-led historical case studies of institutional genesis, stabilization, entrenchment, and failure, with prior AI-governance literature credited; 24 sources in `references/institutional-histories.bib`; cross-refs in Appendix C and Chapters 27, 31, 34, 37.
- Site overview hub with eleven case-study cards, a non-technical intro, and a full synced-text subroute; wired into the Funder/Policy and Philosopher guided paths.

### Companion website (`site/`)

- Astro publication layer: guided paths, concept and standalone-claim cards, chapter pages, a Lean-spine web layer with graph navigation, badges, an experiments page (YAML-synced), and in-browser PDF.

### Empirical spine (`experiments/`)

- Four in-repo simulation lines (toy, embedded, goal-agent, lab) that stress-test bridge cruxes with **tentative, partial** support only.
- Lab-simulation line added and taken through multiple phases (graded red-team access tiers, unattributed-drift detection, blind detector generation, LLM red-team adapter, test batteries, adversarial-lineage gaming); goal-agent and embedded-sim lines extended; Lean spine gained Shannon entropy / mutual-information bounds and a successor-forgeability (MB10) formalization.

### Housekeeping

- `src/` renamed to `demos/`; 
- bibliography enriched with canonical DOI/URL fields.
- `make check` (structure, citations, bibliography summaries) passes.

---

## v1.0.0 — 2026-06-30 — First official major release

Commit: `bd8f82f` · Tag: `v1.0.0`

The first official release of the manuscript. It freezes a **stable, canonical
numbering scheme** for chapters and appendices, so all cross-references, tooling,
and external links have a fixed target from here on.

### Highlights

- **Sequential chapters `ch01`–`ch48`.** The temporary split chapters
  (`ch19b`, `ch25b`, `ch35b`, `ch39b`) are absorbed into the main sequence.
  Filename prefix, `metadata/book.yml` key, generated table column, and the
  printed `\chapter{...}` number now all agree.
- **Appendices A–G** match their printed letters in `book.tex` include order
  (Notation, Bridge Crosswalk, Institutional Translation, Worked Example,
  Glossary, Research Program, Lean Proof Spine). Stub appendices are parked at
  H–L.
- **History preserved.** All 40 path changes were committed as `git mv` renames
  (similarity 93–100%), so `git log --follow` traces each file through the
  renumber into its pre-release history.
- **Numbering scheme documented** as a canonical rule in `INSTRUCTIONS.md` §14
  (no more `b`-suffix file ids; tables derive numbers from manuscript order).

### Manuscript state at release

- 10 parts, **48 chapters** (all with first drafts and at least one review pass).
- **7 built appendices** (A–G) plus 5 stubs (H–L).
- Bibliography of ~235 categorized entries with one-line summaries.
- Self-contained Lean proof spine (`formal/`) calibrating manuscript claims to
  proof / counterexample / bridge status.
- Build: `./build.sh` → `dist/pdf/towards-superintelligence-alignment.pdf`;
  `make check` passes (structure, citations, bibliography summaries).

### Renumbering map

Chapters (split chapters shown; ch01–ch19 unchanged):

| Old id | New id |
|--------|--------|
| ch19b  | ch20   |
| ch20–ch24 | ch21–ch25 |
| ch25b  | ch27   |
| ch26–ch35 | ch28–ch37 |
| ch35b  | ch38   |
| ch36–ch39 | ch39–ch42 |
| ch39b  | ch43   |
| ch40–ch44 | ch44–ch48 |

Built appendices:

| Old file | New file (letter) |
|----------|-------------------|
| appBridge-crosswalk | appB-bridge-crosswalk (B) |
| appJ-institutional-translation | appC-institutional-translation (C) |
| appK-worked-example | appD-worked-example (D) |
| appF-glossary | appE-glossary (E) |
| appH-research-program | appF-research-program (F) |
| appI-lean-proof-spine | appG-lean-proof-spine (G) |

### Known issues

- ~48 undefined LaTeX references remain in the build, mostly pre-existing
  (`appe-assumptions`, `app:lean-proof-spine`, and similar); they are unrelated
  to the renumber.
- Some historical conversation logs and review notes still mention old chapter
  numbers in prose; these are archival and were left as-is.

### Upgrade / linking notes

- External links and citations should target the new `chNN` / appendix letters.
- Tag this release: `git tag -a v1.0.0 -m "First official major release" bd8f82f`.

---
