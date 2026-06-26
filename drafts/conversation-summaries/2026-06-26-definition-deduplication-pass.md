# 2026-06-26 — Definition deduplication pass (§A)

## Trigger
User asked to proceed with deduplicating repeated definitions across chapters (follow-up to audit).

## Done
- **Boundary ε:** labeled `eq:epsilon-boundary-ch07` in ch07; ch10/ch12 cross-ref only (removed `eq:blanket-epsilon-ch10`, `eq:epsilon-boundary`).
- **U_H:** labeled `eq:human-value-update-ch04` in ch04; removed duplicate display in CEV section; ch21/ch23/ch25 cross-ref ch04 (removed ch21/ch23/ch25 labels).
- **Correction chain:** canonical `eq:correction-chain-ch24` only; replaced full re-displays in ch14/ch21/ch23/ch25/ch26/ch27 with cross-refs; ch24 opening now points to ch23 preview + canonical rebuild.
- **G_B:** ch14/ch21/ch22/ch25/ch26 cross-ref ch19 `sec:value-bundle-response-geometry` (removed parallel `eq:bundle-geometry`, `eq:value-bundle-geometry-ch*`).
- **Bundle inference:** ch10/ch21/ch22 cross-ref ch16 `eq:bundle-inference`.
- **Transport gain/decomposition:** ch23 cross-refs ch22 `eq:transport-gain`, `eq:transport-decomposition` (removed ch23 labels).
- **Sample complexity:** ch16 one-line cross-ref to ch17.
- **Appendix I:** book bridges updated for ε-boundary, U_H, transport gain.

## Decisions
- ch08 `eq:blanket-leakage` kept (conditions on $I_t$; distinct from ch07 ε form).
- ch25 compact formal summary left as deliberate in-chapter recap (per fix-plans §A1).
- ch23 transport section keeps risk-weighted score only; plain decomposition referenced, not re-displayed.

## Open / next
- ch22 internal repeat of transport-gain in pipeline Step 4 (fix-plans §B12).
- ch41/ch42 value-tuple and CEV duplication (fix-plans §B2/B3).
- ch36/ch37 goal-laundering layer reconciliation (§C9).
- Optional: add `eq:human-value-update-ch04` to `metadata/notation.md` row for $U_H$.

## Key paths
- `chapters/ch07-finding-boundary.tex`, `ch04-fixed-values-wrong-target.tex`, `ch24-correction-causal-channel.tex`
- `chapters/ch14`, `ch21`–`ch23`, `ch25`–`ch27`, `ch10`, `ch12`, `ch16`
- `appendices/appI-lean-proof-spine.tex`

## Build
- `./build.sh` succeeded → `dist/pdf/towards-superintelligence-alignment.pdf`
