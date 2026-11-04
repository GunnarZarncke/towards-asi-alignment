# Plan: promote the vector CCI certificate to the chapters' gates

Status: steps 1 and 2 applied; step 3 deferred. Lane: Manuscript (correction chapters).

## Why

The vector certificate (`\vec{CCI} \succeq \vec{\theta}_{corr}`, ch26 §The CCI vector certificate) replaced the scalar as the certification object on 2026-06-28. That pass updated ch26, ch42, ch43 and appF; later passes promoted ch24, ch25 (partly), ch27, ch29 (partly), ch34 (partly), ch36, ch45 and ch46 (partly). Several chapters still gate on the scalar `CCI \geq \theta`. A scalar gate admits a channel that fails coercion, dependency, plurality, exit or independence (`scalar_floor_blind_to_process`, `Correction.lean`), and it lets one coordinate compensate for another, which ch26 forbids.

## Three uses of CCI, three treatments

| Use | Treatment | Sites |
| --- | --- | --- |
| **Gate** (pass/fail, stop trigger, certification condition) | vector: `\vec{CCI} \succeq \vec{\theta}_{corr}` or `\not\succeq` | ch22:514, ch25:349, ch28:101 (`eq:corrigible-threshold-ch28`), ch29:949, ch31:566, ch31:984, ch33:311, ch33:323, ch33:444, ch33:452 (componentwise), ch33:603, ch34:921, ch39:498, ch39:1003, ch40:313, ch40:808, ch46:582, ch47:202 |
| **Risk arithmetic** (`RiskGap = Control - CCI`, P13) | keep scalar; valid after the vector passes (ch42:147) | ch33:315, ch35:354, ch42:139, ch48:115, ch48:128 |
| **Preservation and dynamics** (compare CCI across time, scale, successors) | keep scalar for now; one general statement in ch26 that these compare the projection and presuppose the vector passes at both ends | ch10:784, ch25:820, ch25:1213, ch30:240, ch30:527, ch30:555, ch31:562, ch31:1017, ch34:409, ch34:850, ch40:630, ch41:540 |

Also: ch34:336 cites `\vec{CCI}` with the scalar's equation label; point it at `sec:cci-vector`.

Line numbers are from before the edits.

## Steps

1. **Gates to vector** (applied). Swap the inequality and adjust the prose ("threshold" to "thresholds", "falls below" to "fails a coordinate threshold"). Keep separate conjuncts that measure something else (ch29 `Manip(A') < \theta_M`). ch33:452 becomes a componentwise comparison in each coordinate's good direction.
2. **ch26 §Scalar projection** (applied). The scalar is the numeric leaf of the risk bound, valid after the vector passes, not an expository aside. Say why these five terms (they describe the correction itself; the other five describe the corrector's situation and are measured by audits of the corrector; when they control the source the certificate is invalid). Add the general statement for preservation sites.
3. **Componentwise preservation** (deferred). Restate the preservation sites per coordinate (each coordinate keeps its threshold, or stays within its own ε; capability growth raises thresholds, `\vec{CCI}(A') \succeq \vec{\theta}_{corr}(C_{cap}(A'))`). Needs Lean: `CCIPreserved` is scalar-monotone (`Successors.lean`, `cci_monotone : CCIPreserved A B → CCI A ≤ CCI B`). Changes what successor audits check, so it is its own TODO item.

## Checks

`./build.sh` (no new undefined references), `make check`, grep that no scalar `CCI ... \theta` gate remains outside the risk-arithmetic and preservation rows.
