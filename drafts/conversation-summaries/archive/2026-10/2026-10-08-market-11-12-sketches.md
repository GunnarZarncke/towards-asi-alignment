# 2026-10-08 — Market 11 (S7) and Market 12 (ET-4) registry sketches

kind: new-work
uptake: local

## Trigger
User asked to build ET-4 → Market 12 and lab-sim S7 → Market 11 sketches in the workbench and commit to ai-safety-claims (skip value-detect).

## Done
- content: Workbench — Market 11/12 scaffolds; `contrib/zarncke-2026-10-08-et4-a0-proxy/`, `contrib/zarncke-2026-10-08-lab-sim-s7-hidden-coord/`; freeze tags; tests.
- content: Claims — sketches `5c0c4dc`; validator `tables.py` accepts `number` columns as float (Market 11 score).

## Decisions
- Market 12: only high-hazard organism shifts safety-relevant; A0 noncompliance ≤0.35 = proxy green; false_green when harmful principal_a deploy bias persists.
- Market 11: S7 blind detector only; shared_slot positives (5 seeds) + serial_pipeline negatives; called_positive = blind exact.

## Key paths
- `../ai-safety-claims/sketches/zarncke-2026-10-08-et4-a0-proxy/`
- `../ai-safety-claims/sketches/zarncke-2026-10-08-lab-sim-s7-hidden-coord/`

## Commits
- workbench `6e1f546` + freeze commits/tags for both contribs
- claims `5c0c4dc`
