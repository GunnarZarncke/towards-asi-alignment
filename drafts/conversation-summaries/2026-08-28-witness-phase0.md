# 2026-08-28 — Witness Phase 0 freeze

## Trigger
User asked to start Phase 0 of `drafts/plans/witness.md` (charter, measurand sheet, pre-register pass/fail/refuse).

## Done
- Wrote freeze addendum [`drafts/plans/witness-phase0.md`](../plans/witness-phase0.md): hosts H0–H5 and which claims they may pay; ET-1/ET-2 stop rules; pass/fail/refuse per Expectation 1–6; measurand table (boundary/UAD, CCI vector, bundle, grounding, \(\mathcal{K}\), GLI, \(\mathrm{Fit}_E\), MASK \(M\), pipeline detector, bearer commutation) with chapter, estimator, dataset, script, and ch43 verifiability labels; CCI coordinate map; scalar residues (GLI, joint \(\mathcal{K}\), \(\mathrm{CCI}_\lambda\)).
- Marked Phase 0 done on [`drafts/plans/witness.md`](../plans/witness.md); pointed suggested next actions at Phase 1.
- Updated work-map / gates in [`metadata/TODO.md`](../../metadata/TODO.md); pointer in [`experiments/TODO.md`](../../experiments/TODO.md); HANDOFF This week.

## Decisions
- User “start Phase 0” treated as freeze authorization. Reopen by amending `witness-phase0.md`, not by a second copy in `witness.md`.
- No finding stubs, no C2/MASK execution, no Lean pin — those are Phase 1+.
- H0 stays backing only. Construction / H5 “two trees” stays a Construct addendum, not this freeze.
- None of the composite indices is labeled adversarially verifiable at a stated \(\kappa^*\); MASK default path is refuse-as-safety-leaf if honesty does not scale.

## Open / next
- Phase 1 in parallel: sibling CIRIS C2 dual timeline + Eric memo; MASK honesty-gap protocol draft.
- Per-host protocol freeze, then finding files.

## Key paths
- `drafts/plans/witness-phase0.md`
- `drafts/plans/witness.md`
- `~/repos/ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`

## Commits
- none
