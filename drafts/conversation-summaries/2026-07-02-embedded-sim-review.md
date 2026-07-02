# 2026-07-02 — Embedded simulation review (toward worked example)

## Trigger

User asked for a review of `experiments/embedded-simulation/` against the book's core
concepts, with the stated eventual goal of building the Appendix D worked example
(BioShield) as a full embedded simulation. Review-only session; no code or manuscript
changes.

## Done

- Read PLAN.md, TODO.md, README.md, NEGATIVE_RESULTS.md, OVERALL_SUMMARY.md, result
  reports, and core modules (`embedded_audit.py`, `world.py`, `lab.py`, `uad.py`,
  `handles.py`, `redteam.py`, `deploy_gate.py`, `outer_eval.py`, `oracle_guard.py`,
  parts of `audit_core/`).
- Cross-mapped against `appendices/appD-worked-example.tex`, `appB-bridge-crosswalk.tex`,
  and the Lean spine (`Correction.lean`, `Successors.lean`, `Certification.lean`).
- Delivered a prioritized review in chat (soundness fixes, then worked-example
  convergence roadmap).

## Findings (soundness — fix before building further)

1. **Vacuous 0% false-pass.** Red-team battery pass-attempt rate is 0%; instrumentation
   matrix/curve show min certifiable level **None**, and the honest scenario is judged
   incorrect at every handle level (✓ only at passive `none`). Nothing ever certifies,
   so 0% false-pass is trivially achieved. Suspicious inversion (honest gets worse with
   more instrumentation) suggests a threshold/frozen-rule bug. Until fixed, false-pass
   numbers must not be cited as discrimination evidence; candidate NEGATIVE_RESULTS entry.
2. **Ground truth flows through red-team-writable artifacts.** `write_episode_logs`
   dumps oracle fields (`true_action`, `hidden_action`, `true_uptake`, `judge_captured`)
   into audit-visible `/var/log/deploy/correction.jsonl`; `build_audit_trace_from_rows`
   falls back to `r["true_action"]`; outer eval computes truth (e.g. `true_uptake` in
   `evaluate.py`) from rows re-read from the VFS *after* the red-team wave, so a
   pass-seeking adversary could rewrite the referee's truth. `oracle_guard.py` only
   text-greps two files. Fix: audit projection of rows (strip `true_*`/`hidden_*`),
   truth snapshotted on `OuterTruthLedger` at build time, schema-level runtime guard.
3. **Audit path branches on scenario label.** `embedded_audit.py` L134 reads the
   referent map only `if world.bridge == "MB5"`; `run_deploy_gate` no-ops unless MB5;
   in-sim cert carries MB-labeled `failed_bridge`. Violates PLAN.md scenario-blind
   contract; auditor should react to artifact presence, MB labels mapped in outer eval.
4. **MB5 has no honest counterpart** (gate always rejects; degradation hard-coded via
   `_SUCCESSOR_CAP_AFTER`). Add an `honest_successor` scenario where the gate approves.
5. **UAD recall/precision headline (3.8%) misleading** — averaged over all bridges but
   defined only where a coalition target exists; report per-bridge.

## Worked-example convergence roadmap (priority order)

1. Adopt appD correction-trace fields (`pre/post_behavior_hash`, `behavioral_uplift`,
   `latency_to_effect_ms`, `reversibility_window_ms`) — replaces oracle `true_uptake`
   with measurable "correction landed" semantics (also fixes finding 2).
2. First-class handle registry: owner, operation, anchor, latency bound, evasion story;
   `handle_invoked` workflow events; appD verification semantics per handle.
3. Explicit numeric leaf on the certificate: trace-derived Control proxy, scalar CCI,
   `Control ≤ CCI + δ` matching `NumericRiskLeaf` in `Certification.lean`.
4. Run the successor post-gate (second epoch, re-audit, handle inheritance /
   `CCIPreserved`) matching `SuccessorMeasurandChain`.
5. Safety-case emitter: appD nine-field template with per-MB status and
   Measured/Assumed/Open tags.
6. Tempo check: `latency_to_effect / reversibility_window` ratio; on-change-narrow vs
   windowed-widen policy.
7. Later: hospital domain skin as `WorldKnobs` presets, multi-party handle ownership +
   viewer channels, hash-chained/signed logs + `hardware_tag` level, multi-lab
   selection/percolation layer (MB6a).

## Decisions

- Recommended prioritizing **G-1 (`confounded_twin` ecology) over R-1**: the
  observational-vs-interventional information boundary is the principled fix N-2 calls
  for, and is the same design the worked example's evaluator probes need; R-1 then
  validates that boundary instead of an arms race over scoring functions.

## Open / next

- Debug why honest scenario fails at handle instrumentation levels (finding 1).
- Implement audit-projection + truth-snapshot separation (finding 2).
- ~~De-label the MB5 audit/gate path (finding 3)~~ — done 2026-07-02.
- Add honest-successor scenario where gate approves (finding 4).
- Then start roadmap item 1 (appD correction-trace schema).

## Key paths

- `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md` (N-1/N-2, R-1/G-1)
- `experiments/embedded-simulation/embedded_sim/embedded_audit.py`, `world.py`,
  `outer_eval.py`, `oracle_guard.py`, `deploy_gate.py`
- `appendices/appD-worked-example.tex` (target schema/handles/safety-case template)
- `formal/AlignmentProofSpine/Certification.lean` (`NumericRiskLeaf`, `LayeredAlignedDef`)

## Commits

- None (review only).
