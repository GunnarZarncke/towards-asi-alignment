# 2026-06-26 — Formalism tone pass

## Trigger

User asked to remove defensive phrasing around the book's formalism, especially "these are placeholders," while keeping caveats short and not adding a status-label system.

## Done

- Updated `chapters/ch23-transport-types.tex` to replace "not final mathematical definitions / placeholders" with a concise statement that the conditions make transport targets explicit and separately testable.
- Updated `chapters/ch31-certification-without-construction.tex` so value-bundle coordinates are described as a revisable catalogue with a precise certification role, not placeholders.
- Updated `chapters/ch39b-verifiability-and-ontology-adequacy.tex` to state that the book supplies target properties, failure separations, and bridge conditions for deployment-grade proofs or safety cases.
- Updated `chapters/ch40-lethality-stress-test-open-issues.tex` to replace "the conjectural core is a hope" with "not yet a guarantee."
- Updated `chapters/ch11-capability-without-task-ontology.tex` to frame the BIQ/capability measure's narrowness as useful rather than apologetic.
- Updated `chapters/ch32-selection-environment.tex` to make the abstract selection formulation operational: identify deployment-mass handles, measure what they reward, and change the selection environment.

## Decisions

- Did not add a formal status-label scheme; user explicitly preferred a shorter tone pass.
- Kept genuine limits, but removed language that made the formalism sound merely gestural.

## Open / next

- `make check` still fails on the existing structure issue: `Expected 10 appendix files, found 9`.
- A later pass could audit remaining "not a complete solution" phrases, but this pass intentionally touched only the highest-signal defensive wording.

## Verification

```bash
./build.sh   # success
make check   # fails: Expected 10 appendix files, found 9
```

`ReadLints` reported no diagnostics for edited files. Search confirmed the targeted phrases no longer occur in `chapters/*.tex`.

## Key paths

- `chapters/ch23-transport-types.tex`
- `chapters/ch31-certification-without-construction.tex`
- `chapters/ch39b-verifiability-and-ontology-adequacy.tex`
- `chapters/ch40-lethality-stress-test-open-issues.tex`
- `chapters/ch11-capability-without-task-ontology.tex`
- `chapters/ch32-selection-environment.tex`

## Commits

- None.
