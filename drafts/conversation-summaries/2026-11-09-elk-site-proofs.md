# 2026-11-09 — ELK proofs on the site, not the report

kind: correction
uptake: local

## Trigger
User reverted the site retelling of the ELK report. They wanted the site to reflect the Lean ELK improvements, not the report and not the Barez paper.
Prompts: paraphrase

## Done
- content: Restored the finite ELK counterexamples in `ELKIdentifiability.lean` (names stay latent/observed). `lake build AlignmentProofSpine.Field.ELK` succeeded.
- content: ELK check page opens with the report's terms (direct translator, human simulator, confident questions, identical loss). The site relation is one following sentence.

## Decisions
- Public copy names theorems. It does not walk the report's examples.

## Open / next
- After commit, `cd site && npm run sync:lean-spine` so GitHub line anchors match the commit.

## Key paths
- `formal/AlignmentProofSpine/Field/Finite/ELKIdentifiability.lean`
- `metadata/projections.yml`
- `metadata/lean-checks/index.yml`

## Commits
- none
