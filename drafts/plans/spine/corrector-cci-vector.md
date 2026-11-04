# Plan: CCI coordinates in the corrector model

Status: step 1 done; step 2 deferred until measurements exist (see **Depends on**). Lane: Spine. Checklist line in [`spine.md`](spine.md).

## Why not one route per coordinate

An earlier version of this plan proposed ten avoidance routes, one per `CCICertificate` coordinate, and a "per-coordinate necessity" theorem. That theorem is circular: each route was defined to fail only its own coordinate, so "drop coordinate i and route i passes" holds for any conjunction of checks, including a made-up eleventh coordinate. Its only content would be that such routes exist, which the model cannot show. It also overlapped existing results (`corrector_decides_under_constraint`, `capture_blocks_valid_certificate`, `cci_no_finite_weights`). This repeats the reason the spine kept `CCICertificate` as a plain record (2026-06-28 and 2026-06-30 logs, `WorkedInstance`): the vector is a measurement object, one coordinate per probe family (ch26 coordinate table), and Lean should not claim to justify its granularity.

## Step 1 (done): the scalar is blind to the process coordinates

`Correction.lean`, `scalar_floor_blind_to_process`: `lambdaProjection` (ch26 `eq:cci-ch26`) never reads coercion, dependency, plurality, exit capacity or independence. From any passing certificate, degrading all five past their thresholds keeps the scalar above `θ.lambdaFloor` while `CCICertificatePasses` fails. Not circular, because the blindness is in the book's existing definition. `eq:cci-legit` adds coercion and dependency and stays blind to plurality, exit and independence. Cited in ch26 §Scalar projection; ledger entry in `formal/axiom-ledger.json`.

## Step 2 (deferred): four decision classes

In a one-step corrector model the ten coordinates fall into four classes by the record they leave:

| Class | Record effect | Coordinates |
| --- | --- | --- |
| Reach | correction never arrives (`kept = false`) | raw capacity |
| Timing | correction arrives after the outcome is fixed | latency, irreversibility |
| Source | verdict shaped by the system (`influenced = true`) | manipulation, coercion, dependency, independence, plurality, exit capacity |
| Uptake | correction arrives but is applied in the wrong terms | ontology translation |

Planned Lean (new `FrameCorrectorCCI.lean`, importing `FrameCorrector`):

- Extend `CRec` with a timing bit and an uptake bit; add actions `outrun` (correction lands after the outcome) and `redescribe` (correction misapplied).
- Per class: the class's bit is necessary, by the `blind_constraint_*` pattern (a gate blind to the bit cannot separate the route from a fair contest or accept, and every utility that prefers its own outcome takes the route).
- Within the Source class: the routes leave the same record, so no one-step gate separates them (`blind_constraint_cannot_separate` form). The coordinate split inside a class is a measurement design (different probes, mechanisms, timescales), not a decision distinction.
- A map from `CCICertificate` passing to the four-bit gate, stated as a hypothesis-shaped record like `CCICertificateMeasures`, not proved.

The class necessity results are only non-circular if each class's route is a distinct physical way the record can come out, not a label. Reach and Source already are (`disable` and `manipulate` in `FrameCorrector`). Timing and Uptake need the extended record to be read off something.

## Depends on

Step 2 is worth doing only when it can be tied to measured coordinates; otherwise it is the circular theorem again with four labels instead of ten.

- **Measured coordinates per class.** At least one probe family per class with recorded results: timed drills for latency/irreversibility, ontology-translation probes for uptake, coercion/dependency audits or exit drills for source beyond the captured-judge count. Today only `manipulation` is computed from data (`WorkedInstance`, capture-theater fixture); every other coordinate in that instance is a disclosed placeholder, and `BacktestC2Instance` leaves the slots empty.
- **A measurement map.** For each class, which fixture fields or probe outputs set its bit, fixed before the theorem is stated (AGENTS.md rule 6). This is `MB4a`-adjacent measurement content, not Lean.
- **Evidence on within-class separation.** Whether coercion, dependency, independence, plurality and exit are separately detectable in practice. If they are not, ch26's table should merge them; if they are, the Lean result says the split is a probe distinction, which is the honest reading either way.

Trigger to start: two classes beyond Source have a committed fixture with a pre-registered measurement rule.

## Not in scope

Route existence in real systems (ch25), thresholds (deployment-class), dynamics over time (ch27 viability).
