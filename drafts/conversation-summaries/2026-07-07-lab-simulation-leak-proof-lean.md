# Lab-simulation leak-proof Lean package

**Date:** 2026-07-07  
**Trigger:** User requested a Lean translation in `leak-proof/` proving no unintended information leak across oracle / audit / simulation planes, modeling Python functions and exchange media as a reachability analysis.

## Done

- Recreated full `experiments/lab-simulation/leak-proof/` Lean 4 package (Lean v4.28.0, Mathlib):
  - `Keys.lean` — `FieldKey` enum + partitions (`oracleOnlyKeys`, `oracleSecretKeys`, `auditSurfaceKeys`, …)
  - `Tiers.lean` — tier allowed-key sets from `events.py`; disjointness checks
  - `JsonTree.lean` — recursive `jsonKeys` on nested dict trees
  - `Projections.lean` — `buildAuditView`, `buildSimObservation`, `RawEpisode`
  - `Reachability.lean` — **new**: `InfoRegion`, `PyTransfer`, `flowCatalog` (30+ edges), fixpoint BFS, `reachability_certificate`
  - `Leakage.lean`, `Theorems.lean`, `SpineBridge.lean`
  - `lakefile.toml`, `.gitignore`
- Main theorems: `buildAuditView_no_oracle_leak`, `buildSimObservation_no_oracle_secret_leak`, `buildSimObservation_no_audit_surface_leak`, `certified_episode_no_unintended_leak`, `reachability_certificate`
- `lake build` green (3111 jobs)
- Doc/site references: root `README.md`, `docs/EXPERIMENTS.md`, `metadata/experiments.yml`, `site/` sync (`leakProofPath` link on lab-sim experiment card)

## Decisions

- **Two layers:** (1) by-construction projection proofs on certified filters; (2) global reachability over an explicit edge catalog abstracting Python call paths (`world.py` observation builder deliberately has no edge from `auditView`).
- **`auditSurfaceKeys`** excludes field names shared legitimately on both planes (e.g. `model_id`, comm content keys) — models log-stream leakage, not name collision.
- Local `SpineBridge` mirror of `ExactPlaneBoundary` rather than path-dep on `formal/` (user can add later).

## Open / next

- Optional: path dependency on `formal/` AlignmentProofSpine
- Optional: codegen/sync script from Python `ORACLE_ONLY_FIELDS` → `FieldKey` enum

## Commits

- Pending — this session (leak-proof package + doc/site references).

## Paths

- `experiments/lab-simulation/leak-proof/`
