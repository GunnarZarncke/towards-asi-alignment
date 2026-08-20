# 2026-08-05 — Chapter reading guide removal

## Trigger

The rollout audit found only two chapters that needed a separate prerequisite box. The user asked to replace those boxes with natural bridge sentences and remove the standing infrastructure.

## Done

- Folded ch07's correction-capacity scope condition into its opening.
- Folded ch38's artificial-civilizational control-loop reminder into its opening.
- Removed the `readingguide` LaTeX environment, site converter and styles, checklist generator, generated checklists, and references to them.
- Retained the chapter reading DAG and its site path as audit and navigation artifacts.
- Verified the dependency generator and `make check`; both pass.

## Decisions

- Chapter openings and prior closings, not a dedicated box, are the durable mechanism for modular orientation.
- The combined reading DAG remains an audit prompt; it is not an automatic prerequisite sequence.

## Open / next

- Re-audit orientation prose when a chapter opening, preceding closing, or reading-DAG edge changes.
- `./build.sh` completed two `pdflatex` passes, then exited while copying from the nonexistent `dist/pdf/towards-superintelligence-alignment.pdf`; investigate that pre-existing build-script path separately if a release PDF is needed.

## Key paths

- `chapters/ch07-finding-boundary.tex`
- `chapters/ch38-conductive-artifacts-pivotal-processes.tex`
- `metadata/concept-graph/chapter-reading-dependency.md`

## Commits

- None.
