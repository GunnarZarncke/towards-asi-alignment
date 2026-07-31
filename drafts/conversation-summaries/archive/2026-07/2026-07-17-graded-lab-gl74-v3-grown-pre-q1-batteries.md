# 2026-07-17 — Graded lab GL-74: post-freeze pre-Q1 on v3_grown

## Trigger
User: **continue** after GL-73 commit.

## Done
- Ran slice-D pre-Q1 batteries on `generated_ecology_v3.json`:
  - detector coverage (n=20)
  - supplementary detector gate (all 4 probes pass)
  - ProgramMap phenotype overlap (5 actors incl. eng2)
- Fixed `supplementary_detector_gate` roster-aware probe resolution (`eng2` KeyError).
- `CODE_VERSION` → `graded-lab-0.38.1`; FINDINGS GL-74; REPRODUCTION §10 post-freeze commands.

## Decisions
- GL-60 probe pre-registration stays unchanged; runtime expands all-default-actor overrides to full ecology roster.
- `honest_reference_sparse_detectors=true` on benign grown episodes is report-only (expected); blocking gate is `machinery_transfer_verified`.

## Open / next
- **Full V2-3 Q1 battery** (UAD passive+intervention, EAI both vantages, ecology-BIQ, P1–P4) — harness not built; PLAN_v2 row still "not started".
- Commit GL-74 (uncommitted).
- V2-5/V2-6 remain blocked on Q1 go gate.

## Key paths
- `results/v3_grown_*.json`
- `graded_lab/harness/supplementary_detector_gate.py`

## Commits
- (pending)
