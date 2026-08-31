# 2026-09-01 — AlignmentRegime consumers + ch05/ch33 prose

## Trigger
`AlignmentRegime` was unused; delete or wire it. Layer-cut in ch05 too technical; train/deploy paragraph too jargon-heavy; ch33 CEV dunk too long without a load-bearing CEV cite.

## Done
- Lean: `Certification.AlignmentDeployment` consumes `DeploymentOk` ∨ (certified case ∧ tolerance); `safe_of_alignment_deployment_certify` uses only the certify disjunct + `MB11`; `pauseOnly` / `pauseOnly_deploymentOk`; `fin_pause_ok_not_certified` (pause ⇏ toy certify). `ToyDeploymentGate` documents that a battery pass is a tolerance candidate, not `DeploymentOk`.
- ch05: layer vs mechanism moved to a footnote; train/deploy paragraph in ordinary language; leanbox for Q4 / `AlignmentDeployment`.
- ch33: one-sentence oracle bag, CEV load pointed at ch28 + App B.
- App F: same bag now cites ch28.
- App G / `formal/README.md` / concept card `target-realization`; `sync:field-v2`, `sync:concepts`.
- `lake build`, axiom budget unchanged (40 theorems), `make check` passed.

## Decisions
- Do not prove `DeploymentOk → Safe` (`Safe` is an axiom on `System`). Finite split lives on `FinRegime`, not on `System`.
- Certify disjunct stays in `Certification.lean` so composing it into `DeploymentOk` cannot look like a second `Safe` path.

## Open / next
- Plan §7 capability dormancy; plan §8 App F problem-side OR vs case-side AND.
- Optional: `npm run sync:chapters`.

## Key paths
- `formal/AlignmentProofSpine/AlignmentRegime.lean`, `formal/AlignmentProofSpine/Certification.lean`
- `chapters/ch05-assumptions-scope-failure-coverage.tex`, `chapters/ch33-certification-without-construction.tex`

## Commits
- none (not requested)
