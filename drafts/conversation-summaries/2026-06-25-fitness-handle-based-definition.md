# 2026-06-25 — Fitness handle-based definition

## Trigger
User asked to rewrite ch32 and update Lean so fitness is defined systematically through selection handles and deployment mass, parallel to the correction-channel refactor, instead of ad-hoc terms like regulatory risk and revenue.

## Done
- Rewrote `chapters/ch32-selection-environment.tex` § minimal model: canonical `\mu_E(A)`, `\mathrm{Fit}_E(A)`, and `P(A)` with labels `eq:deployment-mass-ch32`, `eq:fitness-ch32`, `eq:preservation-score-ch32`, `eq:selection-divergence-ch32`.
- Updated ch32 uses of fitness/deployment mass throughout (training vs selection, selector influence, artifacts, competitive pressure, worked example, alignment condition, summary).
- Added to `formal/AlignmentProofSpine/Core.lean`: `Environment`, `defaultEnvironment`, `DeploymentMass`, `SelectionHandleFor`, `SelectionChannel`.
- Updated `formal/AlignmentProofSpine/Adversarial.lean`: `ToyDeploymentMass` replaces `ToyFitness`; P31 comments tie to ch32.
- Updated `appendices/appI-lean-proof-spine.tex`: selection-channel definition block and P31 chapter links.
- Updated `metadata/notation.md`, `metadata/terminology.md`, `formal/README.md`.
- `lake build` succeeds.

## Decisions
- Fitness is **not** defined as BIQ; BIQ/Control are drivers of handle exercise, not primitive fitness.
- Revenue, regulatory risk, benchmark scores, and apparent safety are **proxies** for selection-handle effects, not terms in `\mu_E`.
- Preservation `P(A)` is built from spine quantities already in the book (CCI, bundle/bearer drift, hidden BIQ excess, manipulation, irreversible risk).
- Lean keeps integer `DeploymentMass` as the exported abstraction; full `\kappa_{\mathrm{sel}}` sum stays in book notation.

## Open / next
- Propagate `\mu_E` / `\mathrm{Fit}_E` cross-refs if other chapters later adopt fitness notation (currently concentrated in ch32).
- Optional: sync `appendices/appA-notation.tex` stub when notation table is populated.

## Key paths
- `chapters/ch32-selection-environment.tex` (canonical fitness home)
- `formal/AlignmentProofSpine/Core.lean`, `Adversarial.lean`
- `appendices/appI-lean-proof-spine.tex` (`appi:def:spine-selection-channel`, `appi:thm:p31`)

## Commits
- (none this session)
