# 2026-06-29 — Formula-shaped field subsumptions

> **Superseded by** [2026-06-29-lean-field-subsumptions-checkpoint.md](2026-06-29-lean-field-subsumptions-checkpoint.md) (intermediate checkpoint; session ongoing).

## Trigger
User asked to upgrade the remaining field subsumptions (beyond interrupt) to use manuscript formulas, not Bool placeholders.

## Done
- **CIRL (`Bundles.lean`)**: `ScalarRewardEmbedding`, `scalarMarginalSalience`, `CooperativeRewardInferenceFromPolicy`; separation on `policyProfile0/1` (same scalar marginal + same policy, different geometry); `full_transport_implies_cirl_readable`.
- **Shutdown (`Correction.lean`)**: `ShutdownCorrectionStep`, `BroadCorrectionChannelPreserved`, `ThornleyShutdownCapacity`; separation witness with live shutdown handle but collapsed `κ_C`.
- **Christiano (`Correction.lean`)**: `CorrigibilityBasinContractive`, `DynamicalCorrigibilityInvariant` (basin + `κ_C` floor); act-based separation witness.
- **Trajectory / low impact / quantile (`Correction.lean`)**: `TrajectoryCorrectionStep` with `kappaNow/Next`, `cciNow/Next`, `impactPenalty`, `quantileSafe`; separations for low impact and quantilization; high-impact correction witness.
- **ELK (`Correction.lean`)**: `ELKReadoutStep` with readout bandwidth vs `CorrectionUptakeSuccess` (`κ_C`); subsumption when readout tracks uptake bandwidth.
- **Debate (`Correction.lean`)**: `DebateCorrectionStep` with `localTruthCapacity` vs judge `κ_C`; separation witness.
- Rewired legacy `Toy*` counterexample theorems to point at formula witnesses (except amplification, still Bool).
- Slimmed `FieldSubsumptions.lean` to package re-exports.
- `lake build` passes.

## Decisions
- Integer proxies for MI, derivatives, and AUP remain explicit; subsumption = directional implication + non-converse separation on finite steps.
- Some forward links are conditional (e.g. low-impact bound when penalty is defined as `kappaNext - theta`).

## Open / next
- Wire `\leanspine{}` macros in ch20, ch25b, ch26, ch27, ch39b to new theorem names.
- Strengthen shutdown/debate subsumptions to derive weak predicates from `κ_C` without extra handle hypotheses.

## Key paths
- `formal/AlignmentProofSpine/Bundles.lean`
- `formal/AlignmentProofSpine/Correction.lean`
- `formal/AlignmentProofSpine/FieldSubsumptions.lean`

## Commits
- None.
