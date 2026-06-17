# AGENTS.md

Guidance for AI agents working in **towards-asi-alignment**:
a book on steps toward aligning superintelligence based on the works of Gunnar Zarncke and others.

## Agent behavior

Behavioral guidelines adapted from [Karpathy-inspired CLAUDE.md](context/references/karpathy-inspired-claude-md.md) (Forrest Chang's distillation of Andrej Karpathy's observations on LLM agent pitfalls). Bias toward caution over speed; use judgment on trivial tasks.

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

### Surgical changes

**Touch only what you must. Clean up only your own mess.**

When editing existing text:

- Do not rewrite adjacent paragraphs, hedges, or voice when fixing a localized issue.
- Do not refactor manuscript structure that is not broken.
- Match `context/writing-style-gunnar.md` style.
- Do not rewrite files under `context/` unless the user asks; treat them as source-of-truth for tone and framing.
- If you notice unrelated dead prose or inconsistent terminology, mention it; do not delete or rename without approval.

Every changed line should trace directly to the user's request.

### Goal-driven execution

**Define success criteria. Loop until verified.**

Transform writing tasks into verifiable goals:

- "Draft section X" → covers outline items Y; terms defined or paraphrased; legibility checklist satisfied.
- "Revise for funders" → executive surface, decision triggers, and artifact conductivity present.
- "Fix LaTeX/build" → `build.sh` succeeds; citations and figures resolve.

For multi-step tasks, state a brief plan with verification at each step.

### Conversation continuity

**Read the latest log before you work. Write a log before you stop.**

Each agent session is ephemeral. Durable handoff lives in `drafts/conversation-summaries/`.

**At session start (non-trivial tasks):**

1. Read `drafts/conversation-summaries/INDEX.md` and the most recent log file.
2. Check `metadata/book.yml` for chapter status and the open items in that log.

**At session end (required when the session changed the repo, drafted text, or made project decisions):**

1. Add `drafts/conversation-summaries/YYYY-MM-DD-short-topic.md` using the template in `drafts/conversation-summaries/README.md`.
2. Update `INDEX.md` with a new row (most recent first).
3. Record: trigger, what was done, non-obvious decisions, open/next steps, key paths, and commit hashes if any.

Do not rely on chat history alone for resume context.

## Project layout

### Context (`context/`)

- Human-edited notes on project goals, executive summaries, and messaging constraints.
- **`legible-alignment-messageing.md`** — legibility-first writing for funders and policy-adjacent audiences (operational definitions, decision triggers, artifact conductivity).
- **`writing-style-gunnar.md`** — author voice, calibration signals, and genre-specific guidance.
- **`references/`** — external reference files
- PDFs and notes in `context/` are source canon; do not assume the reader knows them. Introduce concepts from first principles in the manuscript.

### Manuscript instructions

- **`INSTRUCTIONS.md`** — full book mission, audience, style, chapter structure, and source clusters. Read relevant sections before large writing tasks.

### LaTeX

Place figures in `figures/` and reference as `figures/<file>`. External `.bib` files need `pdflatex → biber → pdflatex ×2`. Add `\usepackage{graphicx}` when including images. Root file: `book.tex`.

### Build scripts

```bash
./build.sh        # or: make pdf
./clean.sh        # or: make clean
make check        # structure + citation checks
```

Output: `dist/pdf/towards-superintelligence-alignments.pdf`

### README

See `README.md` for thesis, manuscript status, chapter map, build instructions, and review guidelines.

### Conversation logs (`drafts/conversation-summaries/`)

- **`INDEX.md`** — chronological list; read the top entry when resuming work.
- **`README.md`** — log format and handoff rules.
- One markdown file per agent session (changes, decisions, open items, commits).

## Git

- **Do not commit unless the user asks.**
- Do not commit venv directories, LaTeX aux/log files, or secrets.
- Commit source `.tex`, `.py`, and `build.sh`; PDFs are build outputs (regenerate with `build.sh`).
