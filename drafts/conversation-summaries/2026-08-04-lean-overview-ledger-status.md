# 2026-08-04 — Lean overview ledger status + debate row

## Trigger
Reviewer feedback on the Lean overview / field projections table: the status column over-flattened to `proof`/`counterexample`; Debate should show Lean's three-way `FieldResultStatus` ledger; the Debate headline undersold the finite claim-tree rederivation (soundness, completeness, judge-error-flip) in favor of the separation only.

## Done
- Replaced flat `leanStatus` with `ledgerStatuses` arrays in `metadata/projections.yml` (aligned to each agenda's `*_field_result_records` in Lean).
- Updated `site/scripts/sync-projections.mjs` to emit `ledgerStatuses` into `field-projections.json`.
- `FieldProjectionsTable.astro`: **Ledger** column with multi-badge display (`rederivedFinite`, `separationOnly`, `importedAssumption`; MB defeaters keep `counterexample`).
- `/lean/` footer callout uses ledger vocabulary instead of generic proof/counterexample.
- Debate headline and card summary lead with finite claim-tree game rederivation; κ_C interface toy labeled `separationOnly` in `subsumption-debate.md` body leanNodes.
- Verified `FINITE → DEB (DebateGame)` already present in `context/lean_proof_graphs/05-field-subsumptions.dot` (no graph edit needed).

## Decisions
- Keep `counterexample` only for MB defeater projection rows (embedded agency, basin, grounding, deployment gate) — not part of `FieldResultStatus` but honest for finite toy separations outside the field ledger.
- Per-agenda ledger badges list **distinct** statuses present in Lean records (not one badge per theorem).

## Open / next
- App G manuscript opener still deferred (mirror site projections table with ledger column).
- Optional: derive `ledgerStatuses` automatically from Lean `*_field_result_records` in sync script to avoid YAML drift.

## Key paths
- `metadata/projections.yml`
- `site/src/components/FieldProjectionsTable.astro`
- `formal/AlignmentProofSpine/Field/Debate.lean`
- `context/lean_proof_graphs/05-field-subsumptions.dot`

## Commits
- (this session)
