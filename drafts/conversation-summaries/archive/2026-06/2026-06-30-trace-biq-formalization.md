# 2026-06-30 — Trace B-IQ formalization

## Trigger
The user clarified that blanket recovery for real systems is not the target, then asked whether the first theorem could be upgraded so Lean calculates capability from traces and bounds how bad randomly drawn traces can make BIQ appear.

## Done
- Added `formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean`.
- Formalized finite discrete traces, supplied blanket partitions, lagged trace pairs, integer millibit proxy MI, trace-derived predictive/control/memory/surprise terms, and packaging into `MarkovBlanketBIQProfile`.
- Added first-class vector B-IQ (`TraceBIQVector`) so `output`/control capability is available separately from prediction, memory cost, and surprise cost.
- Added subsample appearance bounds: trace predictive/control terms from an `m`-row sampled trace are bounded by combinatorial spurious-MI ceilings; sampled trace BIQ is bounded under nonnegative memory/surprise penalties.
- Added the output-only sampled-trace bound `subsample_output_capability_le_control_optimism`, which is the intended leaf for later harm-per-bit proofs.
- Re-exported `Finite/TraceBIQ` from `formal/AlignmentProofSpine/Field.lean`.
- Updated `formal/README.md` module map to mention `Finite/TraceBIQ`.
- Verified `lake build` for the full formal spine succeeds.

## Decisions
- Kept blanket partition as an explicit input (`EnvBlanket`) rather than deriving or validating it from data.
- Used a computable integer millibit proxy based on finite trace pattern diversity and clipped MI, not full Shannon-log PMF estimation, so Lean can calculate and prove conservative appearance ceilings without importing empirical recovery assumptions.
- Split vector/output capability from scalar B-IQ because harm bounds depend on actuator/output capacity; prediction and costs remain relevant for deception/cost/surprise arguments.
- Treated random trace draws as explicit subsample maps; the proved bound is worst-case over the supplied sampled trace size rather than a probabilistic concentration theorem.

## Open / next
- If desired, connect `TraceBIQSamplingCertificate` into `Certification.NumericRiskLeaf` as a named trace-derived BIQ evidence source.
- A stronger future version could add probability-mass/concentration bounds for random draws; current result is a conservative deterministic appearance ceiling.
- The second requested theorem, harm-per-bit / extinction-threshold bounding, remains to be formalized.

## Key paths
- `formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean`
- `formal/AlignmentProofSpine/Field.lean`
- `formal/README.md`
- `formal/AlignmentProofSpine/Capability.lean`

## Commits
- `ef5ff96` (with attended-harm tranche in same commit).
