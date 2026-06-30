# 2026-06-30 — Trace diversity honesty (drop millibits)

## Trigger
User asked to remove the factor-of-1000 millibit scale (adds nothing) and stop mislabeling the lagged pattern-count heuristic as mutual information; end-of-session commit.

## Done
- **`TraceBIQ.lean`:** Removed `millibitScale`; `log2CeilBits` uses real integer bits (`Nat.log2 (n-1) + 1`). Renamed estimator to `laggedPatternDiversity` / `laggedDiversityScore` and trace terms to `*Diversity` / `*Support`; attention weights `0≤α≤1`; attended optimism equals control optimism (no ×1000).
- **ch11** `\S\ref{sec:trace-output-attended-harm}`: `\widehat D_{\mathrm{ctrl}}` notation; explicit “not Shannon MI” sentence.
- **Appendix I** `\S\ref{appi:sec:trace-attended-harm}`: pattern-diversity definition, Lean ids, attended ceiling = control ceiling in bits.
- **`metadata/TODO.md`:** calibrate pattern-diversity score (not millibit proxy).
- `lake build` passes.

## Decisions
- Kept theorem names like `subsample_output_capability_le_control_optimism` so existing `\leanspine` tags stay valid; honesty is in defs and prose.
- Real Shannon MI remains in `Field/Finite/PMF.lean` when PMF data exists.

## Open / next
- Probabilistic concentration lemma for `TraceAttendedOutputConcentrationBridge`.
- Tighten combinatorial optimism (max-pair vs `|A|·|E|` product).
- Wire attended-harm certs into `Certification`; calibrate against `embedded_sim/audit_core/info.py`.

## Key paths
- `formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean`
- `chapters/ch11-capability-without-task-ontology.tex`
- `appendices/appI-lean-proof-spine.tex` (`appi:sec:trace-attended-harm`)

## Commits
- `c9f5ce1` Drop millibit scale and rename trace estimator as pattern diversity.
