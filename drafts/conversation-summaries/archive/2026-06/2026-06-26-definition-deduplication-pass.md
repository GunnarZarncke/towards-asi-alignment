# 2026-06-26 — Definition deduplication pass (§A)

## Trigger
User asked to proceed with deduplicating repeated definitions across chapters (follow-up to audit).

## Done
- **Boundary ε:** labeled `eq:epsilon-boundary-ch07` in ch07; ch10/ch12 cross-ref only (removed `eq:blanket-epsilon-ch10`, `eq:epsilon-boundary`).
- **U_H:** labeled `eq:human-value-update-ch04` in ch04; removed duplicate display in CEV section; ch46/ch46/ch46 cross-ref ch04 (removed ch46/ch46/ch46 labels).
- **Correction chain:** canonical `eq:correction-chain-ch46` only; replaced full re-displays in ch14/ch46/ch46/ch46/ch46/ch48 with cross-refs; ch46 opening now points to ch46 preview + canonical rebuild.
- **G_B:** ch14/ch46/ch46/ch46/ch46 cross-ref ch19 `sec:value-bundle-response-geometry` (removed parallel `eq:bundle-geometry`, `eq:value-bundle-geometry-ch*`).
- **Bundle inference:** ch10/ch46/ch46 cross-ref ch16 `eq:bundle-inference`.
- **Transport gain/decomposition:** ch46 cross-refs ch46 `eq:transport-gain`, `eq:transport-decomposition` (removed ch46 labels).
- **Sample complexity:** ch16 one-line cross-ref to ch17.
- **Appendix I:** book bridges updated for ε-boundary, U_H, transport gain.

## Decisions
- ch08 `eq:blanket-leakage` kept (conditions on $I_t$; distinct from ch07 ε form).
- ch46 compact formal summary left as deliberate in-chapter recap (per fix-plans §A1).
- ch46 transport section keeps risk-weighted score only; plain decomposition referenced, not re-displayed.

## Open / next
- ch46 internal repeat of transport-gain in pipeline Step 4 (fix-plans §B12).
- ch45/ch46 value-tuple and CEV duplication (fix-plans §B2/B3).
- ch46/ch48 goal-laundering layer reconciliation (§C9).
- Optional: add `eq:human-value-update-ch04` to `metadata/notation.md` row for $U_H$.

## Key paths
- `chapters/ch07-finding-boundary.tex`, `ch04-fixed-values-wrong-target.tex`, `ch46-correction-causal-channel.tex`
- `chapters/ch14`, `ch46`–`ch46`, `ch46`–`ch48`, `ch10`, `ch12`, `ch16`
- `appendices/appG-lean-proof-spine.tex`

## Build
- `./build.sh` succeeded → `dist/pdf/towards-superintelligence-alignment.pdf`

## Commits
- `02f411d` Deduplicate repeated formal definitions.
