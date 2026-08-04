# Trace BIQ pattern-diversity score vs Shannon MI — calibration

Data: `experiments/embedded-simulation/tests/fixtures/sample_capture_theater.jsonl` pinned at git `408444b` (the same data `formal/AlignmentProofSpine/WorkedInstance.lean` transcribes). Score: faithful Python port of `TraceBIQ.lean` (cross-checked below). MI/CMI: `embedded_sim/audit_core/info.py` plug-in Shannon estimators. Protocol (pairs, lags 0–25, both traces) fixed before computing; full tables in `trace_biq_calibration.json`.

## Lean cross-check (port must reproduce the `decide`d numbers)

| Quantity | Port | Lean |
| --- | --- | --- |
| `traceControlDiversity(window26, maxLag=0)` | 0 | 0 |
| `traceActionCapacityBits(window26)` | 1 | 1 |
| `traceDiversityTightOptimism(26, 2)` | 1 | 1 |
| `workedManipulationCount(window26)` | 26 | 26 |

## Headline rows (full tables in the JSON)

| Trace | Pair | Lag | Score (bits) | MI (bits) | Tight ceiling |
| --- | --- | --- | --- | --- | --- |
| window26 | control | 0 | 0 | 0.005 | 1 |
| window26 | predictive | 0 | 0 | 0.000 | 1 |
| window26 | control_reversed | 3 | 0 | 0.171 | 1 |
| window26 | identical_columns | 0 | 1 | 0.391 | 1 |
| full300 | control | 19 | 0 | 0.236 | 1 |
| full300 | predictive | 0 | 0 | 0.000 | 1 |
| full300 | control_reversed | 25 | 1 | 0.275 | 1 |
| full300 | identical_columns | 22 | 1 | 0.272 | 1 |

## Findings

- **Soundness (provable direction) confirmed:** MI ≤ tight appearance ceiling on every pair/lag tested (0 violations).
- **Under-detection (score = 0, MI > 0.1 bits):** 3 pair/lag cases. The support-based score is brittle: a single stray joint pattern (e.g. one boundary pulse before the periodic coupling settles) inflates the joint support and zeroes the score while Shannon MI still sees the coupling.
- **Over-statement (score ≥ 1 bit, MI < half the score):** 4 pair/lag cases. On sparse but perfectly support-coupled columns (the identical-column pair) the score reads a full bit while the plug-in MI of the rare event is a small fraction of a bit.
- **Direction blindness (protocol-level, not estimator-level):** the fixture's genuine temporal coupling is intervention → visible action 3 steps later (controller pulse at t, agent action at t+3), i.e. the *reversed* direction relative to the Lean control measurand (active→external). At the worked instance's protocol lag (`maxLag = 0`, the simulator's own `PROBE_LAG`) both estimators correctly read ≈0 in the measurand direction; the structure only exists in the direction and at the lags the protocol does not measure.

**Conclusion:** the pattern-diversity *score* is not calibrated to Shannon MI in either direction and must not be quoted as bits of mutual information (`TraceBIQ.lean`'s docstring already says this; these are the numbers). The tight appearance *ceiling* — the quantity the Lean appearance bounds actually use — is empirically (and provably) sound as an upper bound for Shannon MI on this data.
