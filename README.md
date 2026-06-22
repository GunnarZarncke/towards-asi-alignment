# Towards Superintelligence Alignment

**Boundaries, Value Bundles, and the Correction of Civilization**

A self-contained framework for preserving human-correctable value-bearing processes as capability grows, ontologies shift, successors are created, and multi-agent selection pressure intensifies.

> This is a research manuscript in progress. It develops a conceptual and formal framework; it is not a claim that alignment is solved. Claims are marked as established, plausible, or open throughout the ledgers and chapter structure.

---

## Thesis

Superintelligence alignment is the problem of preserving **human-correctable value-bearing processes** across capability growth, ontology shift, successor creation, and strategic multi-agent selection pressure—under the assumption that civilization still has enough **correction capacity** to participate in the process.

The book's organizing frame asks whether, as capability grows, we can preserve:

```
value-bundle transport     — value directions survive transformation, not just labels
bearer persistence         — values still apply to the right persons, beings, situations
correction-channel integrity — human judgment still causally changes future system action
successor stability        — delegates and copies inherit correction and value geometry
socio-technical attractor control — deployment conditions keep correction viable
```

External doom taxonomies (Yudkowsky-style lethalities, Turchin-style failure maps, and similar) are **not** a second organizing ontology. They appear late as adversarial checklists and coverage audits—especially in Chapter 40 (*Lethality Stress Test and Open Issues*).

---

## Who this is for

| Audience | What they get |
|----------|----------------|
| Alignment researchers | Precise vocabulary, formal dependencies, open problems |
| Safety engineers and eval builders | Operational definitions, measurement hooks, artifact tables |
| Funders and policy-adjacent readers | Decision triggers, scope assumptions, legibility constraints |
| Capable generalists | A self-contained map without prior project jargon |

Body text introduces every central concept from first principles. 

---

## Manuscript status

| Item | Status |
|------|--------|
| Milestone | **Third** in progress — Parts I–II largely drafted (Ch. 5 partial) |
| Structure | 10 parts, **44 chapters**, 8 appendices |
| Chapters | **10 drafted**, **1 partial** (Ch. 5), **33 stub** (see `metadata/book.yml`) |
| Bibliography | **~235 entries** across categorized `.bib` files |
| PDF | [**Download latest draft**](https://github.com/GunnarZarncke/towards-asi-alignment/releases/latest) · build locally: `book.tex` → `dist/pdf/towards-superintelligence-alignment.pdf` |
| Word target | ~350k (see `metadata/book.yml`) |

**Next milestone** (`INSTRUCTIONS.md` §25–26): finish Ch. 5; preface and executive overview still stubs; appendices A and F.

For agent session continuity, see `drafts/conversation-summaries/INDEX.md`.

---

## Quick start

**Requirements:** TeX distribution with `latexmk`, `pdflatex`, `biber`, and the `memoir` class.

```bash
./build.sh          # or: make pdf
./clean.sh          # or: make clean
make check          # structure + citation key checks
make wordcount      # approximate chapter word counts
make todos          # list [STUB] / TODO markers
```

Output: `dist/pdf/towards-superintelligence-alignment.pdf`

---

## Repository map

```text
book.tex                    # root LaTeX file
INSTRUCTIONS.md             # full mission, chapter list, source canon, agent spec
AGENTS.md                   # agent behavior and handoff rules

metadata/
  book.yml                  # chapter status, word targets, reviewer tags
  open-problems.md          # research directions
  claims-ledger.md          # established vs. provisional claims
  assumptions-ledger.md     # explicit scope assumptions
  uncertainty-ledger.md     # what would change the view
  terminology.md, notation.md, preamble.tex

chapters/                   # ch01–ch44 (one .tex file per chapter)
parts/                      # 10 part include files
frontmatter/                # title page, introduction, executive overview
appendices/                 # 8 appendix stubs
references/                 # BibLaTeX by category (see below)
tables/                     # chapter map, notation, artifacts
figures/                    # source, generated, tikz

context/                    # source PDFs, extracts, messaging constraints
  extracts/                 # markdown extracts (prefer for agent reading)
  writing-style-gunnar.md
  legible-alignment-messageing.md

scripts/                    # build, check, extract, import utilities
review/                     # reviewer guide and templates
drafts/conversation-summaries/  # agent session logs

formal/                     # self-contained Lean 4 proof spine (no Mathlib)
  AlignmentProofSpine.lean  # root module; see formal/README.md
  AlignmentProofSpine/      # Core + per-layer theorem modules (P01–P45, MB1–MB8)
```

The `formal/` directory holds a compact, machine-checked Lean formalization of
the argument's **logical skeleton** (boundaries → capability → transport →
correction → successors → adversarial → certification). It proves the non-empirical
steps and keeps empirical/philosophical claims explicit as bridge `axiom`s
(`MB1`–`MB8`). Build with `cd formal && lake build`. See
[`formal/README.md`](formal/README.md) and
[`LeanProofSpineImplementationBrief.md`](LeanProofSpineImplementationBrief.md).

---

## Parts and chapters

| Part | Chapters | Focus |
|------|----------|-------|
| I. The Alignment Problem Reframed | 1–5 | Wrong object, civilization frame, dynamical guarantee, scope |
| II. Agents, Boundaries, and Real Optimizers | 6–10 | Agent definition, boundaries, composite agency, opacity |
| III. Capability Growth and Competence | 11–14 | Capability without task ontology, coordination, misalignment |
| IV. Human Values as Needs Smoothed over Time | 15–19 | Value bundles, low dimensionality, bearers, tradeoffs |
| V. Interpreting a System's Goals | 20–23 | Bundle inference, compression test, transport types |
| VI. Correction Channels | 24–27 | Causal correction, integrity, extrapolation, manipulation |
| VII. Successors, Reproduction, and Continuity | 28–31 | Successor test, conserved properties, certification |
| VIII. Attractor Basins and Socio-Technical Selection | 32–35 | Selection environment, coupling, parasites, attractor |
| IX. Safety Cases, Adversaries, and Open Questions | 36–40 | Observation limits, goal laundering, safety case, lethality stress test |
| X. The Philosophical and Civilizational Limit | 41–44 | Value change, drift, bearers, closing synthesis |

Full titles and status: `metadata/book.yml` (source of truth), `tables/chapter-map.tex` (maintainer table; not in PDF).

---

## Source canon

Prior work lives in sibling repositories and is mirrored under `context/` for offline reading:

| Repo | Topics |
|------|--------|
| `../agency-detect/docs/papers/` | Unsupervised agent discovery, capability, intentional stance, attractor basins, successors |
| `../brain-to-values/papers/` | Value bundles, free-energy loops, unit-of-caring, consciousness/agency backbone |

Each PDF under `context/` has a markdown extract in `context/extracts/` (regenerate with `python3 scripts/extract_pdf_to_md.py`). The full source map—TeX paths, PDF paths, extract paths—is in `INSTRUCTIONS.md` §3.0 and `metadata/source-canon.md`.

---

## Bibliography

Citations use **BibLaTeX** (`biblatex` + `biber`). Files are split by category:

| File | Contents |
|------|----------|
| `internal-project-sources.bib` | Author's prior papers and project notes |
| `external-alignment.bib` | Alignment, RL, safety, decision theory |
| `neuroscience-values.bib` | Neuroscience, pain/suffering, moral psychology |
| `dynamical-systems.bib` | Information theory, agency, representation learning |
| `governance-institutions.bib` | Governance and institutions |
| `philosophy.bib` | Philosophy of mind and ethics |

`book.tex` loads each category file directly via `\addbibresource`; `main.bib` is a
thin index for manual or uncategorized entries. Add new citations to the matching
category file (or regenerate them with the importer below), not to `main.bib`.

To refresh entries from the source-map sibling repos:

```bash
python3 scripts/import_source_map_refs.py
```

Every chapter should cite from at least three categories where relevant. Run `make check` to verify cited keys exist.

---

## Contributing and review

1. Read `INSTRUCTIONS.md` before large writing or structural changes.
2. Follow `AGENTS.md` for agent sessions; match voice in `context/writing-style-gunnar.md`.
3. When drafting or integrating a chapter, review the matching Lean proof-spine modules (`formal/README.md` module map; see `AGENTS.md`).
4. Use `review/reviewer-guide.md` and templates under `review/` for structured feedback.
5. Update ledgers in `metadata/` as claims and assumptions mature.

**Git workflow**

```text
chapter/chXX-short-name    # one chapter per branch
review/technical           # technical review pass
review/legibility          # policy/legibility pass
```

Conventional commit prefixes: `init:`, `chapter:`, `refs:`, `formal:`, `review:`, `build:`

---

## Known open problems

See `metadata/open-problems.md` and `metadata/uncertainty-ledger.md`. Editorial and cross-chapter chores: `metadata/TODO.md`. Inline markers: `make todos`. Examples:

1. Are human values sufficiently low-dimensional for tractable learning?
2. Can bearer maps survive radical ontology shift?
3. Can correction-channel integrity be measured under adversarial conditions?
4. Can successor constraints be enforced before recursive capability growth?
5. Can composite agent boundaries be detected in real deployment systems?

---

## License

MIT — see [LICENSE](LICENSE).
