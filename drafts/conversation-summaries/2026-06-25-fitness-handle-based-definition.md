# 2026-06-25 — Fitness handle-based definition

## Trigger
User asked to rewrite ch46 and update Lean so fitness is defined systematically through selection handles and deployment mass, parallel to the correction-channel refactor, instead of ad-hoc terms like regulatory risk and revenue.

## Done
- Rewrote `chapters/ch34-selection-environment.tex` § minimal model: canonical `\mu_E(A)`, `\mathrm{Fit}_E(A)`, and `P(A)` with labels `eq:deployment-mass-ch46`, `eq:fitness-ch46`, `eq:preservation-score-ch46`, `eq:selection-divergence-ch46`.
- Updated ch46 uses of fitness/deployment mass throughout (training vs selection, selector influence, artifacts, competitive pressure, worked example, alignment condition, summary).
- Added to `formal/AlignmentProofSpine/Core.lean`: `Environment`, `defaultEnvironment`, `DeploymentMass`, `SelectionHandleFor`, `SelectionChannel`.
- Updated `formal/AlignmentProofSpine/Adversarial.lean`: `ToyDeploymentMass` replaces `ToyFitness`; P31 comments tie to ch46.
- Updated `appendices/appG-lean-proof-spine.tex`: selection-channel definition block and P31 chapter links.
- Updated `metadata/notation.md`, `metadata/terminology.md`, `formal/README.md`.
- `lake build` succeeds.

## Decisions
- Fitness is **not** defined as BIQ; BIQ/Control are drivers of handle exercise, not primitive fitness.
- Revenue, regulatory risk, benchmark scores, and apparent safety are **proxies** for selection-handle effects, not terms in `\mu_E`.
- Preservation `P(A)` is built from spine quantities already in the book (CCI, bundle/bearer drift, hidden BIQ excess, manipulation, irreversible risk).
- Lean keeps integer `DeploymentMass` as the exported abstraction; full `\kappa_{\mathrm{sel}}` sum stays in book notation.

## Open / next
- Propagate `\mu_E` / `\mathrm{Fit}_E` cross-refs if other chapters later adopt fitness notation (currently concentrated in ch46).
- Optional: sync `appendices/appA-notation.tex` stub when notation table is populated.

## Key paths
- `chapters/ch34-selection-environment.tex` (canonical fitness home)
- `formal/AlignmentProofSpine/Core.lean`, `Adversarial.lean`
- `appendices/appG-lean-proof-spine.tex` (`appi:def:spine-selection-channel`, `appi:thm:p31`)

## Commits
- `c4725b6` Refine fitness and proof-spine diagrams for the book appendix.
