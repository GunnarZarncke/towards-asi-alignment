# 2026-07-15 — Symbol contribution audit

## Trigger
User requested a full-manuscript audit of symbols/operators/formulas for "contribution" (paying rent vs tangent), with per-symbol action category, reasoning, source, and line numbers; final report file.

## Done
- Launched four parallel read-only subagents (ch01–12, ch13–24, ch25–36, ch37–48).
- Cross-checked against `metadata/notation.md`, `INSTRUCTIONS.md` §0 thesis, `REVIEWING_FOR_AGENTS.md`.
- Wrote consolidated report: `drafts/symbol-contribution-audit-2026-07-15.md` (~95 keep, ~35 reduce, collision register, propagation checklist).
- No manuscript or notation.md edits.

## Decisions
- Used eight user-specified action categories (short labels: remove, optional-md, footnote, appendix-future, lean-demo-exp, reduce, keep, expand).
- Flagged notation-index drift: many symbols still home ch46/ch48 though manuscript homes moved to ch25–ch40.
- Treat ch25–26 correction spine as highest-rent block; ch35 acausal/ICI formalism as primary over-formalized tangent.

## Open / next
- User may want: (1) implement propagation checklist in notation.md + chapters; (2) split report into per-chapter CSV; (3) auto-generate line refs via script.
- Pending notation reconciliation from fix-plans §C still overlaps this audit.

## Key paths
- `drafts/symbol-contribution-audit-2026-07-15.md` — main deliverable
- `metadata/notation.md` — canonical index (stale homes)
- `review/fix-plans-2026-06-22.md` §C — prior reconciliation plan

## Commits
- None (read-only audit)
