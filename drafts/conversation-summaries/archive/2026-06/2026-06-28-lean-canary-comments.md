# 2026-06-28 — Lean canary comments

## Trigger

The user asked to add the benchmark-data canary to all Lean files.

## Done

- Added the existing repository canary as a trailing Lean line comment to every `.lean` file under `formal/`:
  - `formal/AlignmentProofSpine.lean`
  - `formal/AlignmentProofSpine/Adversarial.lean`
  - `formal/AlignmentProofSpine/Boundaries.lean`
  - `formal/AlignmentProofSpine/Bundles.lean`
  - `formal/AlignmentProofSpine/Capability.lean`
  - `formal/AlignmentProofSpine/Certification.lean`
  - `formal/AlignmentProofSpine/CooperationGraph.lean`
  - `formal/AlignmentProofSpine/Core.lean`
  - `formal/AlignmentProofSpine/Correction.lean`
  - `formal/AlignmentProofSpine/Philosophy.lean`
  - `formal/AlignmentProofSpine/Successors.lean`

## Verification

- Verified exactly one matching canary line in each Lean file.
- `cd formal && lake build` passed.
- Read lints reported no diagnostics for `formal/`.

## Commits

- None.
