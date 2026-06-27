# 2026-06-28 — Promote gems in part openers

## Trigger

The user noted that reviewers may miss some of the book's depth because important ideas are hidden behind the main narrative. They asked to promote the gems in the corresponding part starts and include them in the very short "How to Read This Book" summary.

## Done

- Updated all ten part openers in `parts/part*.tex` with one compact signpost naming the part's hidden contribution:
  - dynamical guarantee;
  - boundary discovery / real optimizer;
  - capability as boundary information;
  - value-bundle geometry plus bearer fragility;
  - transport hierarchy;
  - correction is not feedback / vector CCI;
  - successor creation as inheritance test;
  - preservation envelope and correction parasites;
  - goal laundering and cost of faking;
  - value-update envelope.
- Linked each gem signpost to its corresponding section. Part opener files use normal `Section~\ref{...}` references; the generated roadmap uses generated link text from `metadata/book.yml`.
- Added existing-work subsumption signposts in the relevant part openers:
  - Part II: incentive diagrams / agent tests as boundary-relative artifacts;
  - Part V: reward learning and CIRL-style inference as local projections of bundle/bearer/correction preservation;
  - Part VI: shutdown, interruptibility, low impact, quantilization, and corrigibility as projections or separations around vector CCI;
  - Part IX: debate, amplification, and ELK as narrower subchannels that do not by themselves preserve correction.
- Updated `metadata/book.yml` part summaries so the Introduction's generated `How to Read This Book` roadmap includes the same gems in very short form.
- Added `summary_latex` support to `scripts/generate_tables.py` so the generated roadmap can contain durable linked text without hand-editing `tables/part-roadmap.tex`. This remains a candidate for replacement by a markdown-to-TeX gems source file.
- Added `\label{sec:cost-relation-ch39b}` to the ch39b cost-of-faking section so the Part IX gem can link directly to it.
- Regenerated `tables/part-roadmap.tex` and `tables/chapter-map.tex` with `python3 scripts/generate_tables.py`.
- Added a cross-cutting TODO to `metadata/TODO.md` to fill part-opener whitespace with compact illustrations / conceptual diagrams.
- Added `REVIEWING_FOR_AGENTS.md`, a read-only reviewer guide for coding agents that summarizes the thesis, review posture, checklist, gem map, existing-work subsumptions, empirical-source pointers to related repos, output format, and anti-patterns.
- Added a pointer in `AGENTS.md` telling read-only reviewer agents to consult `REVIEWING_FOR_AGENTS.md` first.
- Added `llms.txt` as a root-level orientation file for external LLMs / crawlers / agents, pointing to the reviewer guide, manuscript entry points, core concepts, empirical-source repos, formal spine interpretation, anti-patterns, and build commands.

## Decisions

- Used one sentence per part opener to preserve the main narrative and avoid adding a separate frontmatter chapter.
- Kept the Introduction summary short by editing the generated roadmap source (`metadata/book.yml`) rather than hand-editing `tables/part-roadmap.tex`; linked summaries use `summary_latex` while plain `summary` remains available for non-LaTeX uses.

## Open / next

- If reviewers still miss the contributions, the next escalation would be a frontmatter "Core Contributions and Where to Find Them" page.
- Future design pass: add one illustration per part opener, reusing the gem motifs now named there.
- Future repo hygiene pass: consider linking `REVIEWING_FOR_AGENTS.md` from `README.md` if external human reviewers should see it.

## Verification

- `make check` passed.
- `./build.sh` passed after the linked-subsumption update.
- `ReadLints` reported no diagnostics for edited files.

## Key paths

- `parts/part01-reframing.tex` through `parts/part10-civilizational-limit.tex`
- `metadata/book.yml`
- `scripts/generate_tables.py`
- `tables/part-roadmap.tex`
- `tables/chapter-map.tex`
- `metadata/TODO.md`
- `REVIEWING_FOR_AGENTS.md`
- `AGENTS.md`
- `llms.txt`

## Commits

- None.
