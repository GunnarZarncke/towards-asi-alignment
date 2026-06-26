# 2026-06-26 — Part openers and ch40 fixes

## Trigger

The author asked to do the part openers and Chapter 40 fixes, treat the Introduction's "Where the Argument Is Shaky" refresh as obsolete, and skip the rest for now.

## Done

- Added one-paragraph opener prose to all ten `parts/partNN-*.tex` files, connecting each part to the book arc without changing chapter inputs.
- Expanded `chapters/ch40-lethality-stress-test-open-issues.tex` with a prose reading for each lethality/checklist row.
- Replaced the two inline `% TODO[open-crux]` markers in ch40 with body prose on reflective stability of correction and delegated evaluation of superhuman plans.
- Updated `metadata/TODO.md`: removed the resolved part-opener, ch40 requested-fixes, and obsolete intro "Where the Argument Is Shaky" TODO rows.
- Added a new active TODO to decide between part-relative numbering and global renumbering after the insertion of `ch39b`.
- Fixed stale manuscript status in `README.md`: chapter count/status now matches `metadata/book.yml` (27 draft, 18 reviewed, 0 stub), and Part IX explicitly lists `ch39b`.
- Added a TODO for auditing update operators that may import ontology through fixed state variables or semantic coordinates.
- Integrated reviewer feedback on under-engagement with Hubinger-style inner alignment: added `ch40` Section `Mesa-Optimization and Inner Alignment` with formal definitions, equations, and a translation table mapping outer/inner alignment, mesa-objectives, pseudo-alignment, deceptive alignment, gradient hacking, and sharp-left-turn concerns into the book's framework; added a body-level `ch10` bridge from strategic opacity to mesa-optimization; updated `ch40` chapter references for `hubinger2019risks`.
- Refreshed `metadata/claims-ledger.md` header/status language for the 45-entry map and draft-complete conclusion; added manual-maintenance notes to both claims and assumptions ledgers; added a TODO to consider structured automation for both ledgers.
- Verified with `ReadLints`, `rg 'TODO\[open-crux\]'` on ch40, and `make check`.

## Decisions

- Kept the existing ch40 table as a compact index and added prose after it instead of expanding every table cell.
- Did not edit `frontmatter/introduction.tex`; the obsolete intro task was removed from the active TODO list.
- Left ch40 below the earlier 9,000-word target, because this pass addressed the requested fixes rather than a full long-form chapter expansion.

## Open / next

- If ch40 is later expanded to full target depth, the new per-lethality prose can become section scaffolding.
- Remaining manuscript TODOs not requested in this pass were left untouched.

## Key paths

- `parts/part01-reframing.tex`
- `parts/part02-agents-boundaries.tex`
- `parts/part03-capability-growth.tex`
- `parts/part04-value-bundles.tex`
- `parts/part05-goal-inference.tex`
- `parts/part06-correction-channels.tex`
- `parts/part07-successors.tex`
- `parts/part08-attractor-basins.tex`
- `parts/part09-safety-cases.tex`
- `parts/part10-civilizational-limit.tex`
- `chapters/ch40-lethality-stress-test-open-issues.tex`
- `metadata/TODO.md`

## Commits

- None.
