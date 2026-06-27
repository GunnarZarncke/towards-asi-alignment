# 2026-06-28 — Update operator refactor

## Trigger

The user asked to implement the Human Update Operator Refactor plan: avoid treating \(U_H\) as another purely philosophical, unspecified gear, especially in ch34, ch41, and `Core.lean`.

## Done

- Updated `chapters/ch34-parasites-correction-system.tex`:
  - reframed \(U_H\) as schematic notation for an auditable envelope, not a hidden mechanism;
  - replaced direct \(U_H\to\tilde U_H\) mutation as the main formal object with degradation of `ValidRef`, grounding viability, and vector CCI.
- Updated `chapters/ch41-value-change-at-stake.tex`:
  - stated that \(U_H\) is compression, not a certificate;
  - reframed domestication as failure of grounding, bundle/bearer transport, vector CCI, exit, plurality, institutional independence, or adversarial verifiability;
  - replaced the technical target \((B_t,W_t,\Phi_t,U_H)\in\mathcal S_{\text{human-correctable}}\) with an explicit envelope condition over existing framework terms.
- Updated `formal/AlignmentProofSpine/Core.lean`:
  - clarified `ValueUpdateOperator` as schematic/opaque rather than directly certifiable;
  - added `ValueUpdateEnvelope` and `ProcessPreservationOperational`;
  - added projection theorems for grounding, bundle, bearer, correction, successor, and adversarial components;
  - documented `PreservesValueUpdateOperator` and MB8 as a legacy/CEV-style alternate bridge, not the live certification route.
- Updated `metadata/TODO.md` to mark the update-operator ontology audit as partially addressed and to point future P25/P26 strengthening toward `ValueUpdateEnvelope`.

## Decisions

- Did not add structure inside `ValueUpdateOperator`.
- Did not remove MB8; it remains as an explicit CEV/process bridge for external theories that certify preservation of a value-update process.
- The operational route is now the existing envelope: grounding viability, bundle/bearer transport, correction integrity/vector CCI, successor stability, and adversarial robustness.

## Open / next

- Future pass: adjust ch26 if desired so its \(U_H\) language points more explicitly at `ValueUpdateEnvelope`, while preserving ch26 as the canonical extrapolative-correction chapter.
- Future Lean pass: strengthen P25/P26 toy counterexamples using `ValueUpdateEnvelope` / process-preservation structure rather than `Bool` toys.
- Full PDF build still reports the known undefined reference `ch:boundary-expansion` in ch40 and existing font/header warnings; build exits successfully.

## Verification

- `lake -d formal build` passed.
- `make check` passed.
- `./build.sh` passed.
- `ReadLints` reported no diagnostics for edited files.

## Key paths

- `chapters/ch34-parasites-correction-system.tex`
- `chapters/ch41-value-change-at-stake.tex`
- `formal/AlignmentProofSpine/Core.lean`
- `metadata/TODO.md`

## Commits

- None.
