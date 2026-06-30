# 2026-06-28 — CCI calibration vectorization

## Trigger

The user asked to implement the revised plan for grounding/calibrating/vectorizing the scalar CCI projection after recent independent grounding-viability changes had already touched CCI.

## Done

- Updated `chapters/ch26-correction-channel-integrity.tex`:
  - synced the Lean note with the new distinction between scalar `CCI` and vector/status CCI;
  - added a calibration policy: thresholds and coordinate scales come before any \(\lambda\)-weighted scalar projection;
  - added a coordinate/probe/threshold table for `ValidRef`, \(C_{\mathrm{raw}}\), \(L\), \(M\), \(R\), \(O_{\mathrm{trans}}\), coercion, dependency, plurality, exit, and independence.
- Updated `chapters/ch42-safety-case.tex` to state that `Control <= CCI + δ` is only the scalar projection leaf and is usable only after `ValidRef`, grounding viability, and vector CCI thresholds are established.
- Updated `chapters/ch43-verifiability-and-ontology-adequacy.tex` so the CCI cost-of-faking discussion is coordinate-specific rather than a generic corrigibility-theater warning.
- Updated `appendices/appF-research-program.tex` to make vector-coordinate calibration, uncertainty bands, and adversarial detection power explicit research targets before scalar projection.
- Updated Lean:
  - `formal/AlignmentProofSpine/Correction.lean` now defines `SystemPathValidRef`, proves `CorrectionIntegrity_implies_systemPathValidRef`, adds `CCIStatus`, `CCICertificate`, `CCIThresholds`, `CCICertificatePasses`, `CCICapturedOrInvalid`, and `CCIVectorSupportsScalarFloor`;
  - `formal/AlignmentProofSpine/Capability.lean` adds `CCIVectorSupportsScalarSlack`, the arithmetic handoff to scalar `CCI`, and a risk theorem from vector-supported slack;
  - `formal/AlignmentProofSpine/Certification.lean` exposes `risk_bound_from_vector_cci_certificate`;
  - `formal/README.md` and `formal/AlignmentProofSpine.lean` document scalar `CCI` as the numeric projection and `CCICertificate` as the vector/status object.

## Decisions

- Did not rename scalar Lean `CCI`; too many risk/successor lemmas intentionally use it as the numeric projection leaf.
- Kept empirical calibration as bridge-shaped evidence: Lean checks the handoff from a passed vector certificate to a scalar floor/slack, not whether real systems satisfy the vector certificate.
- Treated grounding failure and captured reference processes as invalidation/status failures, not large residual ontology penalties.

## Open / next

- Optional later pass: replace or supplement `CCIPreserved` with componentwise certificate preservation for successor audits.
- Optional later pass: add deployment-class objects for required correction cases \(\mathcal Q\) and certified trace families \(\mathcal P_q\) in Lean; current Lean still uses the older weakest-link scalar internally for arithmetic.
- Full PDF build still reports the pre-existing undefined reference `ch:boundary-expansion` in ch48 and existing font/header warnings; build exits successfully.

## Verification

- `lake -d formal build` passed.
- `make check` passed.
- `./build.sh` passed.
- `ReadLints` reported no diagnostics for edited manuscript/formal files.

## Key paths

- `chapters/ch26-correction-channel-integrity.tex`
- `chapters/ch42-safety-case.tex`
- `chapters/ch43-verifiability-and-ontology-adequacy.tex`
- `appendices/appF-research-program.tex`
- `formal/AlignmentProofSpine/Correction.lean`
- `formal/AlignmentProofSpine/Capability.lean`
- `formal/AlignmentProofSpine/Certification.lean`
- `formal/README.md`

## Commits

- None.
