# 2026-06-28 — Update operator cleanup

## Trigger

The user asked to work on the suggested cleanup targets after the \(U_H\) demotion and the concern that ch32's scalar preservation score \(P(A)\) was another ad-hoc weighted sum.

## Done

- Updated `chapters/ch32-selection-environment.tex`:
  - retired scalar \(P(A)\) as the primary preservation object;
  - introduced preservation envelope \(\vec{\Pi}(A)\) with grounding, bundle/bearer drift bounds, `ValidRef`, vector CCI, hidden-control bounds, selector-manipulation bounds, irreversible-risk budget, successor safety, and adversarial verifiability;
  - rewrote selection divergence, artifact conductivity target, selection-alignment condition, and summary around envelope satisfaction rather than \(\nabla P\).
- Updated `chapters/ch26-extrapolative-correction.tex`:
  - kept \(U_H\) only as schematic notation;
  - reframed the target as `ValueUpdateEnvelope_t \succeq \theta`;
  - changed later desired-guarantee language from \(G_B,\Phi,U_H\) to \(G_B,\Phi,\mathrm{ValueUpdateEnvelope}\);
  - clarified MB8 as a legacy/CEV-style bridge in the `\leanspine` note.
- Updated `chapters/ch42-unconscious-value-drift.tex`:
  - replaced \(V_t=(B_t,W_t,\Phi_t,U_H)\) with \(V_t=(B_t,W_t,\Phi_t;\mathcal E^H_t)\);
  - replaced \(d_U(U_{H,t},U_{H,t+1})\) with envelope drift \(d_E(\mathcal E^H_t,\mathcal E^H_{t+1})\);
  - reframed attention control as control over part of the update envelope.
- Updated metadata and generated surfaces:
  - `metadata/notation.md` / `metadata/notation-index.tex`;
  - `metadata/assumptions-ledger.md` / `metadata/assumptions-index.tex`;
  - `appendices/appF-glossary.tex`;
  - `metadata/source-canon.md`;
  - `metadata/TODO.md`.

## Decisions

- Ch32 now uses a vector/status envelope rather than a weighted scalar because the old terms mixed rewards and distances with suspect signs and could hide coordinate failure.
- \(P_\lambda(A)\) remains allowed only as a scenario-specific dashboard projection after envelope thresholds pass.
- MB8 remains in the system, but as an alternate external-theory bridge rather than the live certification path.

## Open / next

- Future Lean pass: strengthen `P25`/`P26` toy counterexamples in `Correction.lean` using `ValueUpdateEnvelope` / process-preservation structure.
- Future manuscript pass: review any remaining CEV/update-process language outside ch26/ch34/ch41/ch42 for consistency.

## Verification

- `lake -d formal build` passed.
- `make check` passed.
- `./build.sh` passed.
- `ReadLints` reported no diagnostics for edited files.

## Key paths

- `chapters/ch26-extrapolative-correction.tex`
- `chapters/ch32-selection-environment.tex`
- `chapters/ch42-unconscious-value-drift.tex`
- `metadata/notation.md`
- `metadata/assumptions-ledger.md`
- `appendices/appF-glossary.tex`

## Commits

- None.
