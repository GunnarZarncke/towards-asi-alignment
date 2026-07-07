# Towards Superintelligence Alignment

**Boundaries, Values, and Correction**

A research manuscript on preserving **human-correctable value-bearing processes** as capability grows, ontologies shift, successors are created, and multi-agent selection pressure intensifies.

> This is work in progress—not a claim that alignment is solved. Claims are marked as established, plausible, or open throughout the ledgers and chapter structure.

**Authorship:** Most manuscript text is AI-drafted under Gunnar Zarncke's direction, with human review, revision priorities, and source canon set by the author. See the [Preface authorship note](frontmatter/preface.tex) and the [companion site About page](https://gunnarzarncke.github.io/towards-asi-alignment/about/). Reuse passages with attribution.

---

## Standalone claims (start here for researchers)

Four extractable notes from the manuscript — each is a citable claim without the full book argument. Full derivations and caveats remain in the PDF chapters linked from each card.

| Claim | Companion card |
|-------|----------------|
| Anti-capture validity of correction | [anti-capture-correction-validity](https://gunnarzarncke.github.io/towards-asi-alignment/cards/anti-capture-correction-validity/) |
| Bearer-map commutation failure | [bearer-map-commutation-failure](https://gunnarzarncke.github.io/towards-asi-alignment/cards/bearer-map-commutation-failure/) |
| Goodhart as selector (not just proxy drift) | [goodhart-as-selector](https://gunnarzarncke.github.io/towards-asi-alignment/cards/goodhart-as-selector/) |
| Certification-Under-Manipulation Problem | [certification-under-manipulation](https://gunnarzarncke.github.io/towards-asi-alignment/cards/certification-under-manipulation/) |

Also on the [companion site homepage](https://gunnarzarncke.github.io/towards-asi-alignment/) under **Standalone claims**.

---

## What this is (and is not)

This repository is a **requirements decomposition with in-principle estimands**: a structured map of what would need to be true, measured, and governed for superintelligence alignment under human-correctable value update. It is **not** a proof that alignment is solved, not a machine-checked safety certificate for frontier systems, and not a substitute for adversarial review. Lean checks conditional structure; experiments are sanity checks with recorded negatives ([`experiments/embedded-simulation/results/NEGATIVE_RESULTS.md`](experiments/embedded-simulation/results/NEGATIVE_RESULTS.md)).

---

## Start here

| | |
|---|---|
| **Companion website** | **[gunnarzarncke.github.io/towards-asi-alignment](https://gunnarzarncke.github.io/towards-asi-alignment/)** — guided reading paths, concept cards, chapter pages, Lean playgrounds, demos |
| **PDF** | [Read in browser](https://gunnarzarncke.github.io/towards-asi-alignment/towards-superintelligence-alignment.pdf) · [GitHub release](https://github.com/GunnarZarncke/towards-asi-alignment/releases/latest) · build locally: [`docs/BUILD.md`](docs/BUILD.md) |

**New reader?** Open the [**Guided tour**](https://gunnarzarncke.github.io/towards-asi-alignment/paths/) on the companion site. Pick a path (generalist, researcher, engineer, funder, philosopher); each lists what you will learn, in what order, and why—without assuming you already know the book's vocabulary.

---

## Thesis (one paragraph)

Superintelligence alignment is the problem of preserving grounded, human-correctable value update across capability growth, ontology shift, successor creation, and strategic selection pressure—under the assumption that civilization still has enough **correction capacity** to participate.

The book tracks six linked preservation problems: **grounding viability**, **value-bundle transport**, **bearer persistence**, **correction-channel integrity**, **successor stability**, and **socio-technical attractor control**. Load-bearing assumptions are explicit **bridges** (`A-001`–`A-014`; formal axioms `MB1`–`MB9`), mapped to field cruxes in [Appendix B (bridge crosswalk)](appendices/appB-bridge-crosswalk.tex).

External doom taxonomies appear late as adversarial checklists (Chapter 44), not as a second organizing ontology.

---

## Who this is for

| Audience | Start here |
|----------|------------|
| Anyone new | [Guided tour](https://gunnarzarncke.github.io/towards-asi-alignment/paths/) on the companion site |
| Alignment researchers | [Researcher — Applied](https://gunnarzarncke.github.io/towards-asi-alignment/paths/researcher-applied/) → [Formal](https://gunnarzarncke.github.io/towards-asi-alignment/paths/researcher-formal/) |
| Safety engineers / eval builders | [Engineer / Evals path](https://gunnarzarncke.github.io/towards-asi-alignment/paths/engineer-evals/) |
| Funders / policy-adjacent | [Funder / Policy path](https://gunnarzarncke.github.io/towards-asi-alignment/paths/funder-policy/) — includes [institutional histories overview](https://gunnarzarncke.github.io/towards-asi-alignment/cards/chapters/appm/) |
| Philosophers / civilizational limits | [Philosopher path](https://gunnarzarncke.github.io/towards-asi-alignment/paths/philosopher/) — includes institutional histories after the selection/attractor material |

In the PDF: **Executive Overview** (two pages) → **Introduction** (six claims) → **Part I** (Chapters 1–5). Policy-adjacent readers may prefer **Appendix C** ([institutional translation](appendices/appC-institutional-translation.tex)), then **Appendix D** ([institutional genesis, memory, and decay](appendices/appM-institutional-histories.tex) — eleven historical case studies of how safety institutions are founded, kept alive, and fail). On the companion site, the [Appendix M overview hub](https://gunnarzarncke.github.io/towards-asi-alignment/cards/chapters/appm/) is the plainer entry path (case-study cards); [full on-site text](https://gunnarzarncke.github.io/towards-asi-alignment/cards/chapters/appm/full/) and the PDF hold the complete narrative.

---

## Manuscript at a glance

| Item | Detail |
|------|--------|
| Status | v1.0.0 release; third milestone in progress — 48 chapters reviewed (not final) |
| Structure | 10 parts, 48 chapters, 8 appendices in the PDF (A–H) |
| Chapter list | [`metadata/book.yml`](metadata/book.yml) · [site book index](https://gunnarzarncke.github.io/towards-asi-alignment/book/) |
| Experiments | Tentative sanity checks only — [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) |
| Formal spine | Lean 4 conditional skeleton — [`formal/README.md`](formal/README.md) |

Full editorial reference: [`docs/MANUSCRIPT.md`](docs/MANUSCRIPT.md).

---

## Documentation

| Doc | Contents |
|-----|----------|
| [`docs/BUILD.md`](docs/BUILD.md) | PDF build, Lean, companion site |
| [`docs/MANUSCRIPT.md`](docs/MANUSCRIPT.md) | Status, parts, bibliography, ledgers, contributing |
| [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) | Toy sim, embedded sim, agency-detect |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute (Lean, sims, writing) |
| [`INSTRUCTIONS.md`](INSTRUCTIONS.md) | Editorial mission and style |
| [`AGENTS.md`](AGENTS.md) | Agent handoff rules |

---

## Related repos

[`agency-detect`](https://github.com/GunnarZarncke/agency-detect) (boundary discovery) · [`brain-to-values`](https://github.com/GunnarZarncke/brain-to-values) (value bundles)

---

## License

MIT — see [LICENSE](LICENSE).
