# Towards Superintelligence Alignments

**Boundaries, Value Bundles, and the Correction of Civilization**

LaTeX monograph by Gunnar Zarncke on superintelligence alignment: a self-contained framework for preserving human-correctable value-bearing processes as capability grows, ontologies shift, successors are created, and multi-agent selection pressure intensifies.

> This is a research manuscript in progress. It develops a conceptual and formal framework; it is not a claim that alignment is solved. Claims are marked as established, plausible, or open throughout the ledgers and chapter structure.

---

## Thesis

Superintelligence alignment is the problem of preserving **human-correctable value-bearing processes** across capability growth, ontology shift, successor creation, and strategic multi-agent selection pressure—under the assumption that civilization still has enough **correction capacity** to participate in the process.

The book's organizing frame:

```
superintelligence alignment
  = value-bundle transport
  + bearer persistence
  + correction-channel integrity
  + successor stability
  + socio-technical attractor control
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

Body text introduces every central concept from first principles. Internal project names (e.g. "UAD") may appear only in references, not as explanatory shortcuts.

---

## Manuscript status

| Item | Status |
|------|--------|
| Milestone | **First** — scaffold complete |
| Structure | 10 parts, **44 chapters**, 8 appendices |
| Chapters | All **stub** (see `metadata/book.yml`) |
| Bibliography | **~235 entries** across categorized `.bib` files |
| PDF | Builds from `book.tex` → `dist/pdf/towards-superintelligence-alignments.pdf` |
| Word target | ~350k (see `metadata/book.yml`) |

**Next milestone** (`INSTRUCTIONS.md` §25): preface, executive overview, roadmap, Chapters 1–2, appendices A and F.

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

Output: `dist/pdf/towards-superintelligence-alignments.pdf`

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
frontmatter/                # title page, executive overview, roadmap
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
```

---

## Parts and chapters

| Part | Chapters | Focus |
|------|----------|-------|
| I. The Alignment Problem Reframed | 1–5 | Wrong object, civilization frame, dynamical guarantee, scope |
| II. Agents, Boundaries, and Real Optimizers | 6–10 | Agent definition, boundaries, composite agency, opacity |
| III. Capability Growth and Competence | 11–14 | Capability without task ontology, coordination, misalignment |
| IV. Human Values as Bundle Geometry | 15–19 | Value bundles, low dimensionality, bearers, tradeoffs |
| V. Goal Inference | 20–23 | Bundle inference, compression test, transport types |
| VI. Correction Channels | 24–27 | Causal correction, integrity, extrapolation, manipulation |
| VII. Successors, Reproduction, and Continuity | 28–31 | Successor test, conserved properties, certification |
| VIII. Attractor Basins and Socio-Technical Selection | 32–35 | Selection environment, coupling, parasites, attractor |
| IX. Safety Cases, Adversaries, and Open Cruxes | 36–40 | Observation limits, goal laundering, safety case, lethality stress test |
| X. The Philosophical and Civilizational Limit | 41–44 | Value change, drift, bearers, closing synthesis |

Full titles and file names: `tables/chapter-map.tex`, `INSTRUCTIONS.md` §7, `metadata/book.yml`.

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
3. Use `review/reviewer-guide.md` and templates under `review/` for structured feedback.
4. Update ledgers in `metadata/` as claims and assumptions mature.

**Git workflow**

```text
chapter/chXX-short-name    # one chapter per branch
review/technical           # technical review pass
review/legibility          # policy/legibility pass
```

Conventional commit prefixes: `init:`, `chapter:`, `refs:`, `formal:`, `review:`, `build:`

---

## Known open problems

See `metadata/open-problems.md` and `metadata/uncertainty-ledger.md`. Examples:

1. Are human values sufficiently low-dimensional for tractable learning?
2. Can bearer maps survive radical ontology shift?
3. Can correction-channel integrity be measured under adversarial conditions?
4. Can successor constraints be enforced before recursive capability growth?
5. Can composite agent boundaries be detected in real deployment systems?

---

## License

MIT — see [LICENSE](LICENSE).
