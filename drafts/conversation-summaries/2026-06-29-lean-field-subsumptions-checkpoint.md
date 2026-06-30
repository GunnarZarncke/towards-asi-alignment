# 2026-06-29 — Lean field subsumptions (intermediate checkpoint)

**Status:** intermediate commit; session ongoing.

## Trigger
Reviewer feedback: book subsumption claims (CIRL, shutdown, corrigibility, ELK, debate, low impact/quantilization) are prose re-descriptions unless Lean encodes them. User asked to implement in Lean, then upgrade interrupt and remaining agendas to use manuscript formulas (not `Bool` placeholders).

## Done (this session arc)

1. **Scaffold (`FieldSubsumptions.lean`)** — `FieldProjection`, `SubsumedForward`, `SeparatedFrom`; packaged re-exports for all eight crosswalk agendas; imported in `AlignmentProofSpine.lean`; `formal/README.md` module row.
2. **Interrupt (ch46 formulas)** — in `Correction.lean`: `kappaC`, `UsableCorrectionInformation`, `InterruptBit`, `interruptIncentiveSlope`, `IncentiveNeutralInterrupt`, `InterruptCorrectionStep`; subsumption (`preserved_channel_no_incentive_to_corrupt_interrupt`, manipulation slope ≤ 0); separation (`interruptSeparationStep`: Orseau-neutral, `κ_C < κ_min`).
3. **Remaining agendas (formula-shaped witnesses in `Bundles.lean` / `Correction.lean`)**:
   - **CIRL**: `ScalarRewardEmbedding`, `scalarMarginalSalience`, `CooperativeRewardInferenceFromPolicy`; `policyProfile0/1` separation; `full_transport_implies_cirl_readable`.
   - **Shutdown**: `ShutdownCorrectionStep`, `BroadCorrectionChannelPreserved`, `ThornleyShutdownCapacity`; `shutdownSeparationStep`.
   - **Christiano**: `ChristianoCorrigibilityStep`, basin contractivity + `κ_C` floor; act-based separation.
   - **Trajectory / low impact / quantile**: `TrajectoryCorrectionStep` (`kappaNow/Next`, `cciNow/Next`, `impactPenalty`, `quantileSafe`); separations + high-impact correction witness.
   - **ELK**: `ELKReadoutStep` (`K_A→K̂_H` vs `Δ_H→Δ_A` proxies); uptake ⇒ readout when bandwidth tracks `kappaC`.
   - **Debate**: `DebateCorrectionStep` (`localTruthCapacity` vs judge `κ_C`); truth without judge channel.
4. Legacy `Toy*` counterexample theorems rewired to formula witnesses (amplification still Bool toy).
5. Verification: `lake build` passes; finite subsumptions axiom-free except system-level `MB4` paths.

## Decisions
- Subsumption = one-way implication + non-converse separation on finite integer proxies, not formal reduction of external programs.
- `kappaC = min(Δ_H, Δ_A)` proxies `I(Δ_H;Δ_A|h_t)`; some forward links conditional (e.g. low-impact when `impactPenalty = kappaNext - theta`).
- Do not commit `.biber-par-cache/`, `RELEASE_NOTES.md`, or manuscript `\leanspine{}` wiring in this checkpoint.

## Open / next (session continues)
- Wire `\leanspine{}` in ch46, ch46 (interrupt), ch48, ch46, ch48, ch47 to new theorem names.
- Appendix I + lean proof graph nodes for `FieldSubsumptions`.
- Strengthen shutdown/debate forward links to derive weak predicates from `κ_C` without extra handle hypotheses.

## Key paths
- `formal/AlignmentProofSpine/FieldSubsumptions.lean`
- `formal/AlignmentProofSpine/Correction.lean`
- `formal/AlignmentProofSpine/Bundles.lean`
- `formal/AlignmentProofSpine.lean`
- `formal/README.md`

## Commits
- `fd635d0` Add formula-shaped Lean field subsumptions for crosswalk agendas (intermediate checkpoint).

## Supersedes
- [2026-06-29-field-subsumptions-lean.md](2026-06-29-field-subsumptions-lean.md) (initial scaffold)
- [2026-06-29-formula-field-subsumptions.md](2026-06-29-formula-field-subsumptions.md) (formula pass)
