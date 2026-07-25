# Manuscript reference

Status, structure, bibliography, and source canon for *Towards Superintelligence Alignment*.

**Live draft status:** [`metadata/book.yml`](../metadata/book.yml) (chapter titles, review tags, word targets).

**Read online:** [companion site book index](https://towards-alignment.com/book/) · [PDF](https://towards-alignment.com/towards-superintelligence-alignment.pdf). Policy-adjacent readers: [institutional translation](https://towards-alignment.com/cards/chapters/appc/) (Appendix C) and [institutional histories overview](https://towards-alignment.com/cards/chapters/appm/) (Appendix D hub with eleven case-study cards; [full text on site](https://towards-alignment.com/cards/chapters/appm/full/)).

---

## Manuscript status

| Item | Status |
|------|--------|
| Release | **v1.0.0** — see [`RELEASE_NOTES.md`](../RELEASE_NOTES.md) |
| Milestone | **Third** in progress — all main chapters have first drafts and at least one review pass |
| Structure | 10 parts, **48 chapters** (`ch01`–`ch48`), **9 appendices in the PDF** (A–I; institutional histories is Appendix D, source file `appM-institutional-histories.tex`; Appendix I is the cross-line experimental-evidence index, source file `appN-experimental-evidence.tex`) + 4 unwired appendix stubs on disk |
| Chapters | **0 draft**, **48 reviewed**, **0 stub** ([`metadata/book.yml`](../metadata/book.yml); *reviewed* = feedback received, not final) |
| Bibliography | **~235 entries** across categorized `.bib` files |
| Word target | ~350k ([`metadata/book.yml`](../metadata/book.yml)) |

**Open gaps:** [`metadata/TODO.md`](../metadata/TODO.md) and [`metadata/book.yml`](../metadata/book.yml) (frontmatter stubs, appendix stubs, citation review).

For agent session continuity: [`drafts/conversation-summaries/INDEX.md`](../drafts/conversation-summaries/INDEX.md).

The PDF front matter [*Current Status*](../frontmatter/current-status.tex) summarizes work-in-progress disclaimers only; the full chapter list lives in [`metadata/book.yml`](../metadata/book.yml) and on the [site book index](https://towards-alignment.com/book/).

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
| IX. Safety Cases, Adversaries, and Open Questions | 36–40 plus 39b | Observation limits, goal laundering, safety case, lethality stress test |
| X. The Philosophical and Civilizational Limit | 41–48 | Value change, drift, bearers, closing synthesis |

Full titles and per-chapter status: [`metadata/book.yml`](../metadata/book.yml).

The part-roadmap table in `tables/part-roadmap.tex` is auto-generated for the PDF (`scripts/generate_tables.py`); outsiders should use `book.yml` or the site for the chapter list.

---

## Source canon

Prior work lives in sibling repositories and is mirrored under [`context/`](../context/):

| Repo | Topics |
|------|--------|
| [`agency-detect`](../agency-detect/docs/papers/) | Unsupervised agent discovery, capability, intentional stance, attractor basins, successors |
| [`brain-to-values`](../brain-to-values/papers/) | Value bundles, free-energy loops, unit-of-caring, consciousness/agency backbone |

Each PDF under `context/` has a markdown extract in [`context/extracts/`](../context/extracts/) (`python3 scripts/extract_pdf_to_md.py`). Full map: [`metadata/source-canon.md`](../metadata/source-canon.md).

---

## Bibliography

Citations use **BibLaTeX** (`biblatex` + `biber`). Files are split by category under [`references/`](../references/):

| File | Contents |
|------|----------|
| `internal-project-sources.bib` | Author's prior papers and project notes |
| `external-alignment.bib` | Alignment, RL, safety, decision theory |
| `neuroscience-values.bib` | Neuroscience, pain/suffering, moral psychology |
| `dynamical-systems.bib` | Information theory, agency, representation learning |
| `governance-institutions.bib` | Governance and institutions |
| `institutional-histories.bib` | Historical case studies for Appendix D (`appM-institutional-histories.tex`) |
| `philosophy.bib` | Philosophy of mind and ethics |

Refresh from source-map sibling repos: `python3 scripts/import_source_map_refs.py`. Run `make check` to verify cited keys exist.

---

## Ledgers and open problems

| File | Role |
|------|------|
| [`metadata/open-problems.md`](../metadata/open-problems.md) | Research directions |
| [`metadata/uncertainty-ledger.md`](../metadata/uncertainty-ledger.md) | What would change the view |
| [`metadata/TODO.md`](../metadata/TODO.md) | Editorial and cross-chapter chores |
| [`metadata/claims-ledger.md`](../metadata/claims-ledger.md) | Established vs. provisional claims |
| [`metadata/assumptions-ledger.md`](../metadata/assumptions-ledger.md) | Explicit scope assumptions |

Examples of open problems:

1. Are human values sufficiently low-dimensional for tractable learning?
2. Can bearer maps survive radical ontology shift?
3. Can correction-channel integrity be measured under adversarial conditions?
4. Can successor constraints be enforced before recursive capability growth?
5. Can composite agent boundaries be detected in real deployment systems?

---

## Contributing and review

1. Read [`INSTRUCTIONS.md`](../INSTRUCTIONS.md) before large writing or structural changes.
2. Follow [`AGENTS.md`](../AGENTS.md) for agent sessions; match voice in [`context/writing-style-gunnar.md`](../context/writing-style-gunnar.md).
3. Review matching Lean modules per [`formal/README.md`](../formal/README.md).
4. Use [`review/reviewer-guide.md`](../review/reviewer-guide.md) for structured feedback.
5. See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for experiments, Lean, and derivative work.

**Git workflow:** `chapter/chXX-short-name`, `review/technical`, `review/legibility`. Commit prefixes: `init:`, `chapter:`, `refs:`, `formal:`, `review:`, `build:`.
