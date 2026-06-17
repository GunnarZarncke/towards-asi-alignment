# 2026-06-17 — Instructions redundancy + consistency cleanup

## Trigger
Review `README.md`, `AGENTS.md`, `INSTRUCTIONS.md` for redundancy/inconsistency, then:
trim folder listing to examples-only, split README (reader/dev-facing) vs INSTRUCTIONS
(agent-facing, eventually deleted), fix the Part IX slug/title mismatch, correct the
repo name, ensure build outputs land in `dist/pdf`, and recommend a bibliography setup.

## Done
- Renamed `parts/part09-adversarial-measurement.tex` → `parts/part09-safety-cases.tex`
  (matches part title "Safety Cases, Adversaries, and Open Cruxes"). Updated
  `book.tex` include and `scripts/init_scaffold.py`.
- `INSTRUCTIONS.md` §8: replaced the exhaustive file tree with an illustrative one
  (files only as examples/where convention matters); fixed root name to
  `towards-asi-alignment/`; removed root `book.pdf`; noted `dist/pdf` outputs; pointed
  to the README repository map as the maintained overview.
- `INSTRUCTIONS.md` §30: `cd towards-asi-alignment`.
- `INSTRUCTIONS.md` §3.0: replaced the full source-map table with a pointer to the now
  durable `metadata/source-canon.md`; moved the full table + sibling-repo notes into
  `metadata/source-canon.md` (previously it pointed back at INSTRUCTIONS — inverted).
- `INSTRUCTIONS.md` §11: resolved the "unified main.bib OR include files" either/or →
  recommend per-file `\addbibresource` (current `book.tex` setup); `main.bib` is a thin
  index/manual-entry holder. Mirrored a short note in `README.md` bibliography section.
- `INSTRUCTIONS.md` §13: trimmed duplicated build/clean/Makefile/latexmkrc source to a
  pointer (files already exist), keeping the `dist/pdf` output requirement.
- Verified: `make check` passes and `./build.sh` builds (exit 0).
- Fixed garbled equations in `INSTRUCTIONS.md` §6 and §18: converted bare `[ ]` math
  blocks to `\[ \]`, repaired markdown-mangled formulas (§6.6/§6.7, §18.3/§18.4/§18.7/
  §18.8 had `===`/`---`/`#` artifacts; §18.13 had blockquoted `> 1`/`> ]`), and changed
  inline `(I)`,`(E)`… variable refs in §6.1 to `$I$`,`$E$`. No remaining bare delimiters
  or heading artifacts (grep-verified).

## Decisions
- Renamed the Part IX file despite a prior session deliberately keeping the old name
  (logged 2026-06-17 structure sessions); user explicitly asked to fix it now.
- Durable reference data (source map) belongs in `metadata/`, not in INSTRUCTIONS,
  since INSTRUCTIONS will be deleted at project completion.
- Did NOT strip the thesis/audience/chapter-list from INSTRUCTIONS: those are the core
  writing brief, low-risk to keep; only developer/structural reference duplication was
  reduced.
- Left historical conversation logs referencing the old part09 slug unchanged.

## Open / next
- Optional: designate single-source-of-truth ownership for remaining cross-file
  overlap (thesis, audience, parts table, open-problems).

## Key paths
- `INSTRUCTIONS.md` (§3.0, §8, §11, §13, §30), `metadata/source-canon.md`,
  `parts/part09-safety-cases.tex`, `book.tex`, `README.md`.

## Commits
- none (not requested)
