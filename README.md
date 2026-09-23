# Towards Superintelligence Alignment (TSA)

**Boundaries, Values, and Correction**

A knowledge base and roadmap for preserving **human-correctable value-bearing processes** as capability grows, ontologies shift, successors are created, and multi-agent selection pressure intensifies.

The book is the long-form argument. This repository also holds a Lean dependency spine, sanity-check experiments, a field-agenda crosswalk, spin-out papers, chapter demos, and a companion site built from and around that material.

> This is work in progress—not a claim that alignment is solved. Claims are marked as established, plausible, or open throughout the ledgers and chapter structure.

**Authorship:** Most manuscript text is AI-drafted under Gunnar Zarncke's direction, with human review, revision priorities, and source canon set by the author. See the [Preface authorship note](frontmatter/preface.tex) and the [companion site About page](https://towards-alignment.com/about/). On chapter pages, optional per-section chips (`AI`, `GZ`, `GZ+AI`) mirror PDF margin-bar keys—toggle via **Notes** on the site. Reuse passages with attribution.

---

## What this is (and is not)

This repository is a **requirements decomposition** of the alignment problem into independent, in-principle theoretically determinable or empirically estimatable elements. It is a structured map of what would need to be true, measured, and governed for superintelligence to remain aligned and human-correctable under changing values. Lean checks the conditional decomposition structure. Authored simulations are sanity checks with recorded negatives ([`experiments/embedded-simulation/results/NEGATIVE_RESULTS.md`](experiments/embedded-simulation/results/NEGATIVE_RESULTS.md)). **Backtests** are the distinctive empirical class: frozen safety checks on histories we did not write ([`experiments/backtest/`](experiments/backtest/)).

---

## Start here

| | |
|---|---|
| **Companion website** | **[towards-alignment.com](https://towards-alignment.com/)** — [Field hub](https://towards-alignment.com/field/), guided paths, concept/bridge cards, [field news](https://towards-alignment.com/news/), [releases](https://towards-alignment.com/updates/), chapter pages, Lean playgrounds, and demos 
| **PDF** | [Read in browser](https://towards-alignment.com/towards-superintelligence-alignment.pdf) · [GitHub release](https://github.com/GunnarZarncke/towards-asi-alignment/releases/latest) · build locally: [`docs/BUILD.md`](docs/BUILD.md) |

**New reader?** Open [**Start Here**](https://towards-alignment.com/start/). The first essay begins on that page. If you already know your role, the [**Guided tour**](https://towards-alignment.com/paths/) lists researcher, engineer, funder, and philosopher paths.

---

## Thesis

Superintelligence alignment is the problem of preserving grounded, human-correctable value update across capability growth, ontology shift, successor creation, and strategic selection pressure—under the assumption that civilization still has enough **correction capacity** to participate.

The Introduction's six connected claims: **boundary** (where is the real optimizer?), **value-bundle** (compressed values, who they apply to, and correction survive change), **grounding** (symbols stay tied to value-relevant reality), **correction** (human value-change stays causally effective), **successor** (successor systems inherit constraints), and **basin** (deployment environment selects for preservation). The argument maps these to field cruxes in [Appendix B (bridge crosswalk)](appendices/appB-bridge-crosswalk.tex) and the companion site [Field hub](https://towards-alignment.com/field/) ([`reference/field-agendas/`](reference/field-agendas/README.md)).

---

## Who this is for

| Audience | Start here |
|----------|------------|
| Anyone new | [Guided tour](https://towards-alignment.com/paths/) on the companion site |
| Alignment researchers | [Field hub](https://towards-alignment.com/field/) → [Researcher — Applied](https://towards-alignment.com/paths/researcher-applied/) → [Formal](https://towards-alignment.com/paths/researcher-formal/) |
| Safety engineers / eval builders | [Engineer / Evals path](https://towards-alignment.com/paths/engineer-evals/) |
| Funders / policy-adjacent | [Funder / Policy path](https://towards-alignment.com/paths/funder-policy/) — [Field hub](https://towards-alignment.com/field/) for agenda coverage; [institutional histories overview](https://towards-alignment.com/cards/chapters/appm/) |
| Philosophers / civilizational limits | [Philosopher path](https://towards-alignment.com/paths/philosopher/) — includes institutional histories after the selection/attractor material |

In the PDF: **Executive Overview** (two pages) → **Introduction** (six claims) → **Part I** (Chapters 1–5). Policy-adjacent readers may prefer **Appendix C** ([institutional translation](appendices/appC-institutional-translation.tex)), then **Appendix D** ([institutional genesis, memory, and decay](appendices/appM-institutional-histories.tex) — eleven historical case studies of how safety institutions are founded, kept alive, and fail). On the companion site, the [Appendix M overview hub](https://towards-alignment.com/cards/chapters/appm/) is the plainer entry path (case-study cards); [full on-site text](https://towards-alignment.com/cards/chapters/appm/full/) and the PDF hold the complete narrative.

---

## Project at a glance

| Item | Detail |
|------|--------|
| Release | **v1.6.0** (2026-09-05) — see [`RELEASE_NOTES.md`](RELEASE_NOTES.md) |
| Status | Every chapter drafted and reviewed at least once; depth varies by chapter and nothing is final; four alignment questions; backtests W-1–W-17; plain-first legibility pass |
| Structure | 10 parts, 48 chapters, 10 appendices in the PDF (A–J) |
| Field crosswalk | agenda records, concept cards; inter-agenda glossary — [`reference/field-agendas/`](reference/field-agendas/README.md) · [Field hub](https://towards-alignment.com/field/) |
| Chapter list | [`metadata/book.yml`](metadata/book.yml) · [site book index](https://towards-alignment.com/book/) |
| Experiments | Tentative sanity checks — sims, external tests (ET-1–4), backtests (W-1–W-17) — [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md), [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md); lab-layer [Lean leak-proof certificates](experiments/lab-simulation/leak-proof/); findings in Appendix J ([`appN-experimental-evidence.tex`](appendices/appN-experimental-evidence.tex)) |
| Formal spine | Lean 4 dependency spine — field-claim finite models, `BridgeCruxes`, construction interface — [`formal/README.md`](formal/README.md) |
| Predictions | Appendix H: 18 dated bridge predictions with resolution criteria — [`metadata/predictions.yml`](metadata/predictions.yml) · [site hub](https://towards-alignment.com/predictions/) |
| Symbol census | Symbol/formula census with contribution audit and dependency graphs — [`metadata/symbol-census/README.md`](metadata/symbol-census/README.md) |

Full editorial reference: [`docs/MANUSCRIPT.md`](docs/MANUSCRIPT.md).

---

## Documentation

| Doc | Contents |
|-----|----------|
| [`RELEASE_NOTES.md`](RELEASE_NOTES.md) | Versioned release history (newest first) |
| [`docs/BUILD.md`](docs/BUILD.md) | PDF build, Lean, companion site |
| [`docs/MANUSCRIPT.md`](docs/MANUSCRIPT.md) | Status, parts, bibliography, ledgers, contributing |
| [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) | Toy → graded-lab lines, external transfer, backtests, sibling precursors |
| [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) | Freeze, preregistration, blind generation, backtest failure conditions |
| [`reference/field-agendas/README.md`](reference/field-agendas/README.md) | Field agenda index, matrix, inter-agenda glossary |
| [`papers/README.md`](papers/README.md) | Spin-out papers (ET-4 secret loyalties, feedback-horizon gap, verifier construction, alignment under selection, constructing alignment attractors, path construction); frozen sources and PDFs |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute (Lean, sims, writing) |
| [`INSTRUCTIONS.md`](INSTRUCTIONS.md) | Editorial mission and style |
| [`AGENTS.md`](AGENTS.md) | Agent handoff rules |
| [`REVIEWING_FOR_AGENTS.md`](REVIEWING_FOR_AGENTS.md) | Read-only review guide for AI/coding agents |
| [`llms.txt`](llms.txt) | Bot / LLM orientation index (synced to the companion site at build) |

---

## Related repos

[`agency-detect`](https://github.com/GunnarZarncke/agency-detect) (boundary discovery) · [`deployment-pipeline-simulator`](https://github.com/GunnarZarncke/deployment-pipeline-simulator) (pipeline secret-loyalty audit) · [`brain-to-values`](https://github.com/GunnarZarncke/brain-to-values) (value bundles)

---

## License

MIT — see [LICENSE](LICENSE).
