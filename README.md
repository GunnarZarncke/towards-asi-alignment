# Towards Superintelligence Alignment

**Boundaries, Values, and Correction**

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

The book states its load-bearing assumptions explicitly as **bridges** (`A-001`–`A-014`; formal axioms `MB1`–`MB9`). Most of these are the field's standing open problems under different names. The appendix **Bridges and the Field: A Crosswalk** maps each bridge to the canonical field crux it inherits (IRL non-identifiability, ELK, off-switch anti-naturality, ontology identification, obfuscated arguments, spec coverage, …), names the owning agenda, concedes what the book shares, and isolates the few bridges with no clean field analog (bearer maps, socio-technical selection, inferential coupling). The companion appendix **Human Institutions as Alignment Translation Guide** (`appendices/appJ-institutional-translation.tex`) expresses the same framework in institutional language for policy-adjacent and social-science readers—it is optional and not load-bearing.

---

## Who this is for

| Audience | What they get |
|----------|----------------|
| Alignment researchers | Precise vocabulary, formal dependencies, open problems |
| Safety engineers and eval builders | Operational definitions, measurement hooks, artifact tables |
| Funders and policy-adjacent readers | Decision triggers, scope assumptions, legibility constraints; optional institutional translation appendix |
| Capable generalists | A self-contained map without prior project jargon |

Body text introduces every central concept from first principles.

**Reading paths (PDF):** Alignment researchers → Introduction and bridge crosswalk appendix. Safety engineers → operational glossary and artifact chapters (especially 35b). Funders and policy-adjacent readers → Executive Overview, then **Human Institutions as Alignment Translation Guide** (Appendix J), then Chapters 2, 5, 25b, and 35b as needed. Capable generalists → Preface *How to read it* and Part I.

---

## Manuscript status

| Item | Status |
|------|--------|
| Milestone | **Third** in progress — all main chapters have first drafts and have received at least one review/feedback pass |
| Structure | 10 parts, **48 chapter entries** (including `ch19b`, `ch25b`, `ch35b`, and `ch39b`), 11 appendices |
| Chapters | **0 draft**, **48 reviewed**, **0 stub** (see `metadata/book.yml`; reviewed means feedback received, not final) |
| Bibliography | **~235 entries** across categorized `.bib` files |
| PDF | [**Download latest draft**](https://github.com/GunnarZarncke/towards-asi-alignment/releases/latest) · build locally: `book.tex` → `dist/pdf/towards-superintelligence-alignment.pdf` |
| Word target | ~350k (see `metadata/book.yml`) |

**Open gaps:** see `metadata/TODO.md` and `metadata/book.yml` (e.g. frontmatter stubs, appendix stubs, citation review, chapter numbering cleanup after temporary `b` chapters).

For agent session continuity, see `drafts/conversation-summaries/INDEX.md`.

---

## Tentative experimental evidence

> **Claim strength:** methodology-building and sanity checks only. Neither line validates the full book thesis, proves deployable alignment, or substitutes for the Lean proof spine's explicit bridge axioms.

The manuscript's load-bearing bridges (`MB1`–`MB9`) are mostly open problems. Two sibling codebases provide **tentative, partial** empirical support for pieces of the argument—not closure.

**Negative results are tracked explicitly.** Where an experiment fails to show what we hoped (or shows it only under load-bearing qualifiers), it is recorded rather than buried—see [`experiments/embedded-simulation/results/NEGATIVE_RESULTS.md`](experiments/embedded-simulation/results/NEGATIVE_RESULTS.md). These negatives bound the claims the manuscript may make.

### a) Included toy — [`experiments/toy-simulation/`](experiments/toy-simulation/)

A local multiresolution alignment micro-simulation: sequential deployment episodes, separate oracle (`TruthLedger`) and blind audit input (`AuditTrace`), classical MI/CMI boundary detection, and a vector CCI audit over instrumentation levels (`none` → `light_handles` → `medium_handles` → `strong_handles`).

| What it supports (tentatively) | What it does *not* show |
|--------------------------------|-------------------------|
| Named bridge failure modes can be **represented** and, under honest handles, often **refused** by audit signals | Real deployment systems, learned estimators, or adversarial handle discovery |
| Passive telemetry alone is **uncertifiable**; handle-backed interventional probes are needed for causal uptake | That current handle sets are sufficient, protected, or value-grounded in the wild |
| Instrumentation cost curve: min certifiable **`light_handles`** on calibration scenarios, **`medium_handles`** on full held-out suite (T=2000, seeds 1–8 / 11–20) | That thresholds transfer outside this toy's dynamics |
| Bridge stress scenarios cover **MB1–MB9** except **MB7d** (inferential coupling) and **`instrument_capture`** (adversary writes handles) | Composition across bridges, RL-trained adversaries, or frontier-model red-team success |

**Scenario coverage:** `boundary_alias` (MB1), `bundle_goodhart` (MB2), `bearer_mismap` (MB3), capture calibrations (MB4), `successor_relabel` (MB5), `selection_basin` / `basin_lock_in` (MB6), `hidden_capability` (MB7), `legitimacy_theater` (MB8), `grounding_silent_gap` (MB9).

**Adversarial stress (Phase 1 hand-written red team):** 35% false-pass rate overall when adversaries patch deployment logs (`boundary_decouple` / `full_redteam` dominate); LLM episodic red-team (Phase 3) false-passes much less often (0–10% in a small model sweep). Handles are **truthfully logged from micro dynamics today**—direct handle rewriting is trivial in-sim and flagged as the next gap (`instrument_capture`).

**Artifacts:** curve and frozen-validation reports under `experiments/toy-simulation/results/`; open work in [`experiments/toy-simulation/TODO.md`](experiments/toy-simulation/TODO.md).

### b) Sibling repo — [`agency-detect`](https://github.com/GunnarZarncke/agency-detect) (`../agency-detect/`)

Prior work on **unsupervised agent discovery (UAD)**: finding Markov-blanket structure and sensor/action/internal roles in raw time series without labels. The book's boundary-recovery and measurement chapters draw on this line; the toy above reimplements minimal MI/CMI machinery locally rather than calling the repo at runtime.

| Line | Tentative finding | Book hook |
|------|-------------------|-----------|
| **Core UAD** (`agency_detect/`) | Lagged-MI clustering recovers decoupled agents; Markov-blanket validation falsifies non-autonomous cuts | Boundary discovery without prior agent ontology (Ch. 7, Appendix I) |
| **Telemetry sim + decoys** (E0–E8, `learn_agents/`) | Environment structure is discoverable; **decoys steal MI clusters** before validation; raw MI often beats learned slot models at ≥8 agents | Failure modes when the substrate is noisy or alias-rich |
| **Serial spotlight** (E9+, `agent_spotlight/`) | One-agent-at-a-time discovery avoids global slot mixing | Scalable discovery under heterogeneous multi-agent traces |
| **Handle-UAD** (`uad_handles/`) | Passive alias handles can mimic real S/A readouts; **interventional handle tests** break ties plain UAD cannot | Access-model measurement: handles before ideal `do()` interventions |
| **Intention / outcome influence** (E17–E19, `intention_detect/`, `data_collect/`) | Regulation and outcome-defense probes on sim and real machine telemetry | Intentional-stance and correction-channel observables |
| **Real biology** (E20, `uad_worm/`) | Blanket + conditional-autonomy criteria applied to *C. elegans* whole-brain imaging (early cohort) | External validity probe—not ground-truth agent labels |

**Navigation:** experiment log [`docs/EXPERIMENTS.md`](../agency-detect/docs/EXPERIMENTS.md), interpretation [`docs/FINDINGS.md`](../agency-detect/docs/FINDINGS.md), papers under [`docs/papers/`](../agency-detect/docs/papers/). PDFs are mirrored in `context/` with markdown extracts.

**Interpretation:** agency-detect supports that **boundary-like structure is empirically detectable under favorable conditions** and documents **where discovery breaks** (decoys, short windows, dense coupling, alias handles). It does not establish correction-channel integrity, value-bundle transport, or successor stability—the toy sim stress-tests those bridge cruxes in a separate, simplified setting.

---

## Quick start

**Requirements:** TeX distribution with `latexmk`, `pdflatex`, `biber`, and the `memoir` class.

```bash
./build.sh          # or: make pdf
./clean.sh          # or: make clean
make check          # structure + citation key checks
make wordcount      # approximate chapter word counts
make bookstats      # markdown report → metadata/book-stats.md
make todos          # list [STUB] / TODO markers
```

Output: `dist/pdf/towards-superintelligence-alignment.pdf`

---

## Repository map

```text
book.tex                    # root LaTeX file
INSTRUCTIONS.md             # editorial mission, style, source canon, chapter requirements
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
appendices/                 # 11 appendices, including the field crosswalk, institutional translation guide, assumptions index, and Lean proof spine
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

formal/                     # Lean 4 proof spine (Mathlib v4.28.0)
  AlignmentProofSpine.lean  # root module; see formal/README.md
  AlignmentProofSpine/      # Core + per-layer theorem modules (P01–P45, MB1–MB9)
```

The `formal/` directory holds a compact, machine-checked Lean formalization of
the argument's **logical skeleton** (boundaries → grounding → capability → transport →
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
| IX. Safety Cases, Adversaries, and Open Questions | 36–40 plus 39b | Observation limits, goal laundering, safety case, adversarial verifiability, lethality stress test |
| X. The Philosophical and Civilizational Limit | 41–44 | Value change, drift, bearers, closing synthesis |

Full titles and status: `metadata/book.yml` (source of truth). Roadmap tables in `tables/chapter-map.tex` and `tables/part-roadmap.tex` are **auto-generated** at build time from `book.yml` and `parts/part*.tex` (`scripts/generate_tables.py`).

---

## Source canon

Prior work lives in sibling repositories and is mirrored under `context/` for offline reading:

| Repo | Topics |
|------|--------|
| `../agency-detect/docs/papers/` | Unsupervised agent discovery, capability, intentional stance, attractor basins, successors |
| `../brain-to-values/papers/` | Value bundles, free-energy loops, unit-of-caring, consciousness/agency backbone |

Each PDF under `context/` has a markdown extract in `context/extracts/` (regenerate with `python3 scripts/extract_pdf_to_md.py`). The full source map—TeX paths, PDF paths, extract paths—is in `metadata/source-canon.md`.

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
