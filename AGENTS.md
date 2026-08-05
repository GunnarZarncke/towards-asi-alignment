# AGENTS.md

Guidance for AI agents working in **towards-asi-alignment**:
a book on steps toward aligning superintelligence based on the works of Gunnar Zarncke and others.

## Agent behavior

Behavioral guidelines adapted from [Karpathy-inspired CLAUDE.md](context/references/karpathy-inspired-claude-md.md) (Forrest Chang's distillation of Andrej Karpathy's observations on LLM agent pitfalls). Bias toward caution over speed; use judgment on trivial tasks.

If you are asked to **review** the manuscript without editing it, read [`REVIEWING_FOR_AGENTS.md`](REVIEWING_FOR_AGENTS.md) first. It gives the fast thesis, review posture, gem map, existing-work crosswalk, empirical-source pointers, output format, and anti-patterns for read-only reviewer agents.

### Think before writing

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before drafting or editing manuscript text:

- State assumptions about audience tier (generalist, researcher, funder), chapter scope, and claim strength.
- If multiple interpretations of a term or thesis exist, present them; do not pick silently.
- If a simpler operational paraphrase exists, say so. Push back when jargon does not earn its keep.
- If source canon, outline, or messaging constraints are unclear, stop and ask.

See `INSTRUCTIONS.md` for mission, audience, style, and source canon.

### Simplicity first

**Minimum prose and structure that serve the request. Nothing speculative.**

- No new chapters, sections, or terminology beyond what was asked.
- No abstractions, frameworks, or formalism that the current audience tier does not need.
- No rhetorical overreach; mark uncertainty explicitly.
- Prefer operational definitions and ontology-light paraphrases (see `context/legible-alignment-messageing.md`).

### Erasure, Archival, and Cleanup

**Removing information is important for knowledge.**

This is most true for redundancy, but also for historical information, long outdated results, and mistakes made.

When you 

- find the right information only after searching thru a long list of irrelevant data
- notice that you were confused or surprised by first reading information that was not applicable to your task and then later finding the correct or latest information
- had to ask the user for feedback and the relevant information was actually present
- you spot redundancy or confusing material during other tasks.

improve the situation outright.

Consider adding erasure tasks to all plans you make.

Options for erasure:

- simplify/refactor
- restructure file or folders to find the correct information first (eg sorting, hierarchy)
- move material to an attic folder
- delete with making a note in the conversation
- delete by moving to the trashbin

### Surgical changes

**Touch only what you must. Clean up only your own mess.**

When editing existing text:

- Do not rewrite adjacent paragraphs, hedges, or voice when fixing a localized issue.
- Do not refactor manuscript structure that is not broken.
- Match `context/writing-style-gunnar.md` style.
- Do not rewrite files under `context/` unless the user asks; treat them as source-of-truth for tone and framing.
- If you notice unrelated dead prose or inconsistent terminology, mention it; do not delete or rename without approval.

Every changed line should trace directly to the user's request.

- **Ask before expanding scope.** Open files, roadmap order, and untracked drafts are not instructions. On “commit” or “end of session,” stage only what this task authorized; mention other drafts in the log and ask.

### No recency markers

Do not add `[NEW]`, “new in this session,” freshness badges, or similar recency tags to manuscript text, the companion site, Lean proof diagrams, or other reader-facing artifacts. The book and site change too fast for such markers to stay accurate; use git history and `drafts/conversation-summaries/` for change tracking instead.

**Exceptions:** only when the user explicitly requests a time-bounded marker (e.g. a one-off release note, external snapshot, or workshop handout with a stated cutoff date). Remove or refresh those markers in the same pass that supersedes them.

### Goal-driven execution

**Define success criteria. Loop until verified.**

Transform writing tasks into verifiable goals:

- "Draft section X" → covers outline items Y; terms defined or paraphrased; legibility checklist satisfied.
- "Revise for funders" → executive surface, decision triggers, and artifact conductivity present.
- "Fix LaTeX/build" → `build.sh` succeeds; citations and figures resolve.
- "Draft or integrate chapter N" → relevant Lean spine module reviewed; claim strength matches proof / counterexample / bridge status (see **Chapter work — Lean spine** below).

For multi-step tasks, state a brief plan with verification at each step.

### Long-running tasks

**Potentially long-running scripts and commands must log progress.**

- Before launching a script, battery, or build that may run more than roughly a minute (multi-seed sweeps, real-API/LLM calls, large builds), make sure it prints progress as it goes — percent/fraction complete, current item or seed, or at minimum what step it is on — rather than staying silent until the end.
- If a script you are writing or editing lacks this, add minimal progress logging (e.g. `print(f"[{i}/{n}] ...")` per iteration/episode/seed) before kicking off a long real run.
- For tooling you cannot modify, poll intermediate state (log files, output/results directories, partial JSON) instead of blocking silently until completion.

### Chapter work — Lean spine

When **drafting, revising, or integrating** a chapter (including Shape B integrated drafts):

1. Read the module map in [`formal/README.md`](formal/README.md) and identify proof-spine nodes for that chapter number.
2. Skim the matching `formal/AlignmentProofSpine/*.lean` module(s) for predicates, theorems, and `MB*` bridges the chapter uses or implies.
3. Calibrate manuscript claim strength to Lean status: **proof**, **counterexample**, or **bridge** — do not say "Lean proves ASI alignment."
4. If prose and spine diverge, note the gap in the session log and `metadata/TODO.md`; change Lean only when the task explicitly includes formal work.
5. When relating a chapter or bridge to existing alignment agendas (RLHF, debate/amplification, ELK/interpretability, CIRL, MIRI agent foundations, AI Control, Guaranteed-Safe/davidad, etc.), use the appendix **Bridges and the Field: A Crosswalk** (`appendices/appB-bridge-crosswalk.tex`) as the canonical map from bridges (`A-001`–`A-014` / `MB1`–`MB9`) to named field cruxes. Extend that crosswalk rather than inventing ad-hoc per-chapter comparisons.
6. **Conclusions are never named in definitions before being derived.** Do not bake a target result (a δ, a threshold, a verdict) into a definition and then choose inputs backward so the "derivation" reproduces it. Fix inputs (thresholds, data, protocols) independently and first — pre-registered where possible — then report whatever the derivation actually yields, including failures and weak bounds.

See also `INSTRUCTIONS.md` §11 (chapter writing process).

### Conversation continuity

**Read HANDOFF before you work. Update HANDOFF after major changes.**

Each agent session is ephemeral. Durable handoff lives in `drafts/conversation-summaries/` (HANDOFF + per-session logs) and `metadata/TODO.md`.

**At session start (non-trivial tasks):**

1. Read `drafts/conversation-summaries/HANDOFF.md`, then `INDEX.md` or a specific session log if resuming a thread.
2. Check `metadata/book.yml` and relevant open items in `metadata/TODO.md`.
3. Use `RECOVERY.md` or git history only for pruned/superseded logs.

**When making a plan in plan mode:**

Write the plan into `drafts/<planname>.md` or a more task specific directory, as appropriate. Update the plan as work progresses.

**At session milestones (required when the session changed the repo, drafted text, or made project decisions):**

1. Add or update a per-session log (`drafts/conversation-summaries/YYYY-MM-DD-topic.md`) using the template in `drafts/conversation-summaries/README.md`.
2. Update `drafts/conversation-summaries/HANDOFF.md` (Open work / Recently shipped) when load-bearing.
3. Update `drafts/conversation-summaries/INDEX.md` if the session log is new (or run `scripts/archive_conversation_summaries.py`).

Do not rely on chat history alone for resume context.

## Project layout

### Reference (`reference/`)

- Field agenda roster, inter-agenda term glossary, and anthropic/acausal taxonomy — agent crosswalk material, not manuscript canon. Hub: [`reference/field-agendas/README.md`](reference/field-agendas/README.md).

### Context (`context/`)

- Human-edited notes on project goals, executive summaries, and messaging constraints.
- **`legible-alignment-messageing.md`** — legibility-first writing for funders and policy-adjacent audiences (operational definitions, decision triggers, artifact conductivity).
- **`writing-style-gunnar.md`** — author voice, calibration signals, and genre-specific guidance.
- **`references/`** — external reference files
- PDFs and notes in `context/` are source canon; do not assume the reader knows them. Introduce concepts from first principles in the manuscript.

### Manuscript instructions

- **`INSTRUCTIONS.md`** — editorial mission, audience, style, source canon, and chapter requirements (not the chapter map; see `metadata/book.yml`). Read before large writing tasks.

### LaTeX

Place figures in `figures/` and reference as `figures/<file>`. Add `\usepackage{graphicx}` when
including images. Root file: `book.tex`. Build fragments and biber troubleshooting are documented
in [`docs/BUILD.md`](docs/BUILD.md).

**Bibliography summaries:** each `.bib` entry needs a matching `\bibsummary{key}{...}` line in `references/bibliography-summaries.tex` (rendered via `metadata/preamble.tex`). See `references/README.md`. When adding cites, run `python3 scripts/check_bibliography_summaries.py` or `make check`.

### Build scripts

Run from **repo root** unless noted. There is no root `package.json`; npm lives under `site/` and `demos/` only. See [`docs/BUILD.md`](docs/BUILD.md) for the full build map.

```bash
./build.sh        # or: make pdf  → dist/pdf/towards-superintelligence-alignment.pdf
./clean.sh        # or: make clean
make check        # structure + citation + bibliography-summary checks
./serve-site.sh   # companion site dev (auto npm install in site/)
./serve-demos.sh  # chapter demo static server
```

**Do not** run `npm install` or `npm exec` from repo root — that creates a stray root `node_modules/` that nothing uses.

### Formal proof spine (`formal/`)

Self-contained Lean 4 skeleton of the book's logical dependencies (`lake build` in `formal/`). When working on or integrating a chapter, review the matching modules per **Chapter work — Lean spine** above and `formal/README.md`.

### Experiments (`experiments/`)

Empirical sanity-check codebases that stress-test bridge cruxes. Five in-repo lines (build order): [`toy-simulation/`](experiments/toy-simulation/), [`embedded-simulation/`](experiments/embedded-simulation/), [`goal-agent-simulation/`](experiments/goal-agent-simulation/), [`lab-simulation/`](experiments/lab-simulation/), and [`graded-lab-simulation/`](experiments/graded-lab-simulation/). Sibling methodological precursors (outside the repo): [`agency-detect`](https://github.com/GunnarZarncke/agency-detect), [`deployment-pipeline-simulator`](https://github.com/GunnarZarncke/deployment-pipeline-simulator). Narrative map: [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md); structured index: [`metadata/experiments.yml`](metadata/experiments.yml). They provide **tentative, partial** support only — never closure. When making or citing an empirical claim, read the relevant experiment's `results/` and **honor recorded negatives**: [`experiments/embedded-simulation/results/NEGATIVE_RESULTS.md`](experiments/embedded-simulation/results/NEGATIVE_RESULTS.md) (embedded line); [`experiments/goal-agent-simulation/results/FINDINGS.md`](experiments/goal-agent-simulation/results/FINDINGS.md); [`experiments/lab-simulation/results/FINDINGS.md`](experiments/lab-simulation/results/FINDINGS.md). Add negatives rather than burying them; calibrate prose the same way you calibrate to the Lean spine.

### Companion site (`site/`)

Astro publication layer: guided paths, concept cards, chapter pages, Lean playgrounds, synced demos. Build from repo root with `./serve-site.sh` (preferred) or from `site/` with `npm run build`. Full path map: [`docs/BUILD.md`](docs/BUILD.md). Some appendices use an **overview hub** on the site (case-study cards at `/cards/chapters/{id}/`, full synced text at `/full/` — see `appM` institutional histories).

### Chapter demos (`demos/`)

Experimental interactive toys—one mini app per chapter under `demos/chNN-slug/`. Not part of the manuscript or PDF. See [`demos/README.md`](demos/README.md); run with `python3 serve.py` from `demos/` or `./serve-demos.sh` from the repo root.

### Review artifacts (`review/`)

Structured continuity review, split plans, and reviewer templates. Start with [`review/reviewer-guide.md`](review/reviewer-guide.md); active fix list in [`review/fix-plans-2026-06-22.md`](review/fix-plans-2026-06-22.md).

### Human docs (`docs/`)

Condensed entry points: [`docs/BUILD.md`](docs/BUILD.md), [`docs/MANUSCRIPT.md`](docs/MANUSCRIPT.md), [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md).

### README

See `README.md` for thesis, manuscript status, chapter map, build instructions, and review guidelines.

### Conversation logs (`drafts/conversation-summaries/`)

- **`HANDOFF.md`** — aggregated open work and recent themes; read first when resuming.
- **`INDEX.md`** — recent session logs; older logs in **`archive/`**.
- **`RECOVERY.md`** — one-line index of **pruned** logs only (superseded by a later session).
- **`README.md`** — log template and retention policy.
- **`INDEX.md`** — pointer to the above.
- **`README.md`** — maintenance rules.

Per-session `.md` log files are retired.

## Git

- **Do not commit unless the user asks.** Stage only authorized changes—not every draft in the working tree.
- Do not commit venv directories, LaTeX aux/log files, or secrets.
- Commit source `.tex`, `.py`, and `build.sh`; PDFs are build outputs (regenerate with `build.sh`).
