# Session: Lean box reframe (2026-08-17)

## What changed

- Renamed `{formalcontract}` → `{leanbox}` in `metadata/preamble.tex` (title: **Lean spine**).
- Reframed pattern: compact inline box when it elaborates Lean mapping or names crucial spine elements—not only at “contract” obligation boundaries.
- Migrated 6 pilot chapters (ch21, ch25, ch26, ch28, ch33, ch43).
- Added `{leanbox}` at Tier 1+2 anchors: ch03, ch07, ch08, ch10, ch11, ch17, ch30, ch31, ch35, ch42, ch48.

## Convention

- At most one `{leanbox}` per chapter, placed at the first high-value Lean introduction site (alongside `\leanspine`).
- Prose inside the box: contextual elaboration, module/predicate names, what is proved vs bridge vs open—not a four-field contract template.

## Open

- Remaining `\leanspine` chapters without a box (add only when a box would add value beyond the margin note).
- Field v2 cutover to live `/field/` (manual author confirm).
