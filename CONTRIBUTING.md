# Contributing

Thank you for interest in *Towards Superintelligence Alignment*. This is a research manuscript in progress; contributions of many kinds are welcome.

**Before large edits:** read [`INSTRUCTIONS.md`](INSTRUCTIONS.md) (editorial mission and style), [`AGENTS.md`](AGENTS.md) (agent handoff rules), and the relevant chapter or module. For manuscript changes, match voice in [`context/writing-style-gunnar.md`](context/writing-style-gunnar.md).

**Workflow:** fork or clone [the repository](https://github.com/GunnarZarncke/towards-asi-alignment), work on a focused branch, open a pull request with a short description of what changed and why. For writing-only feedback without a PR, structured review using [`review/reviewer-guide.md`](review/reviewer-guide.md) is also helpful.

---

## Improving the Lean proofs of field results

The Lean proof spine (`formal/`) checks logical dependencies and finite separations; it does **not** prove deployed safety. Bridges `MB1`–`MB9` stay explicit axioms.

High-value work:

- Strengthening the spine per [`formal/README.md`](formal/README.md) and [`formal/LeanProofSpineImplementationBrief.md`](formal/LeanProofSpineImplementationBrief.md)
- **Field-agenda formalization** — shared finite fragment in `formal/AlignmentProofSpine/Field/` linking CIRL, AUP/relative reachability, quantilization, shutdown, and interruptibility to book invariants under explicit interface conditions (see Appendix G gem on field formalization)
- Closing chapter ↔ Lean mapping gaps listed in `metadata/TODO.md` (§ Lean proof spine)

Build: `cd formal && lake exe cache get && lake build`

---

## Building the simulations

Five experiment lines live under [`experiments/`](experiments/) (see [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) for the narrative map):

| Path | Role |
|------|------|
| [`experiments/toy-simulation/`](experiments/toy-simulation/) | Multiresolution alignment micro-sim; bridge stress scenarios MB1–MB9, instrumentation curve, red-team battery |
| [`experiments/embedded-simulation/`](experiments/embedded-simulation/) | Embedded audit experiment (v3); run via `python3 run.py` |
| [`experiments/goal-agent-simulation/`](experiments/goal-agent-simulation/) | Goal-driven agents with mechanism-derived labels and held-out goal-space regions |
| [`experiments/lab-simulation/`](experiments/lab-simulation/) | Lab-layer sim: subprocess isolates, access tiers, playbook agents, referee batteries |
| [`experiments/graded-lab-simulation/`](experiments/graded-lab-simulation/) | Graded lab runtime: institutional transfer, UAD, and graded evidence batteries |

Open tasks: [`experiments/TODO.md`](experiments/TODO.md) and per-folder `TODO.md` files. Results land in each experiment's `results/` directory.

**Embedded LLM red-teaming at scale:** the embedded audit experiment can run live LLM adversaries against the in-sim gate, but checked-in results use modest defaults (`gpt-4o-mini`, seven bridges × three seeds). **Contributions that rerun with larger seed grids and stronger frontier models would be especially valuable** — they stress-test whether the gate survives adaptive optimizers, not just the hand-written `full_redteam` battery. See [`experiments/embedded-simulation/TODO.md`](experiments/embedded-simulation/TODO.md) (§ LLM red-team scale-up) for API setup, CLI flags, example commands, and where to record results.

Related sibling repos (boundary discovery, pipeline audit, real telemetry): [`agency-detect`](https://github.com/GunnarZarncke/agency-detect), [`deployment-pipeline-simulator`](https://github.com/GunnarZarncke/deployment-pipeline-simulator), [`brain-to-values`](https://github.com/GunnarZarncke/brain-to-values).

---

## More elaborate simulations — especially the worked example

Appendix D (*A Worked Example: The BioShield Deployment Gate*, `appendices/appD-worked-example.tex`) runs the full logical spine on one fictional hospital-network deployment. It is narrative and conditional today; there is no matching executable sim.

Contributions welcome:

- Prototype simulators that instantiate layers from the worked example (boundary discovery, handles, correction-channel probes, successor gates, selection envelope)
- Bridge scenario design that stress-tests the example's tagged claims `[Measured]`, `[Assumed]`, `[Lean-conditional]`
- Honest instrumentation and adversarial red-team paths (see toy-sim patterns in `experiments/toy-simulation/`)

Start from the appendix, cross-check bridges in [`appendices/appB-bridge-crosswalk.tex`](appendices/appB-bridge-crosswalk.tex), and document claim strength in results markdown alongside JSON artifacts.

---

## Working on the research agenda

Structured open directions:

- [`metadata/open-problems.md`](metadata/open-problems.md) — measurement, theory, practice
- [`metadata/uncertainty-ledger.md`](metadata/uncertainty-ledger.md) — what would change the view
- [`metadata/TODO.md`](metadata/TODO.md) — editorial and cross-chapter chores
- [`metadata/claims-ledger.md`](metadata/claims-ledger.md) and [`metadata/assumptions-ledger.md`](metadata/assumptions-ledger.md) — calibrate claim strength

Proposals that sharpen a crux, add a falsifiable test, or map a field agenda to a bridge (`A-001`–`A-014` / `MB1`–`MB9`) are especially useful.

---

## Writing derivative works

The manuscript is [MIT licensed](LICENSE). You may:

- Write summaries, explainers, or course materials
- Port concepts to other formalisms or tooling
- Build alternative formalizations or empirical programs inspired by the gems (see gem map in [`REVIEWING_FOR_AGENTS.md`](REVIEWING_FOR_AGENTS.md))

Please distinguish your work from the official manuscript, cite the book and relevant sibling repos where appropriate, and do not imply the project claims alignment is solved.

---

## Posting about the gems

The book embeds deep machinery in a long narrative. If you write publicly:

- Point readers to specific chapters or appendix sections (boundary discovery, value bundles, bearer maps, correction-channel integrity, field crosswalk, Lean spine, worked example, etc.)
- Use the **gem map** in [`REVIEWING_FOR_AGENTS.md`](REVIEWING_FOR_AGENTS.md) as a signposting guide
- Calibrate claim strength: bridges are assumptions; Lean proves conditional logical shape; toy sims are methodology-building only

Tag or link [the repository](https://github.com/GunnarZarncke/towards-asi-alignment) if you want the author to notice.

---

## Building a website

The **official companion site** is deployed from this repository:

**https://towards-alignment.com/**

It hosts guided reading paths, concept cards, rendered chapter pages, Lean playgrounds, chapter demos, and an in-browser PDF copy.

From repo root: `./serve-site.sh` (dev) or `./serve-site.sh --preview` (production-like). Do **not** run `npm install` at repo root — dependencies live in `site/node_modules/` only. Details: [`site/README.md`](site/README.md) and [`docs/BUILD.md`](docs/BUILD.md).

You may also:

- Host reading guides, gem indexes, or interactive demos (chapter demos under [`demos/`](demos/) are a starting pattern; see [`demos/README.md`](demos/README.md))
- Mirror or excerpt with clear attribution and a link to the hosted PDF
- Integrate simulation artifacts or Lean module browsers

Coordinate in an issue or PR if you want cross-linking from this README.

---

## Other derivative work and promotion

Other contributions that help the research program reach the right readers:

- Talks, reading groups, and curated bibliographies
- Tools that operationalize artifact tables or safety-case templates from the manuscript
- Translations (coordinate first for terminology consistency)
- Policy or institutional briefings that use [`appendices/appC-institutional-translation.tex`](appendices/appC-institutional-translation.tex) as a bridge document, or [`appendices/appM-institutional-histories.tex`](appendices/appM-institutional-histories.tex) for historical genesis/decay cases (companion-site [overview hub](https://towards-alignment.com/cards/chapters/appm/) for non-technical readers)

When in doubt, open an issue describing the derivative work and which bridges or gems it targets.

---

## Acknowledgements

Named feedback on the manuscript, Lean spine, and field map is tracked in [`metadata/feedback-contributors.md`](metadata/feedback-contributors.md).

Recent field-map input includes **Tom M.** — directional encoding for evidence tags (stance / “sign bit”) and a suggestion to add lab agenda rows to the coverage matrix.
