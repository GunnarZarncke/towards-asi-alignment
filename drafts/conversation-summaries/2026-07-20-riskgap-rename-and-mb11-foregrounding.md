# 2026-07-20 — RiskGap rename, MB11 foregrounding, and CCI-weighting finding

## Trigger
Follow-up to a 2026-07-19/20 hostile-critique thread on `Capability.lean`/`Correction.lean`'s scalar risk leaf. User asked to implement the agreed plan in `drafts/lean-risk-spine-typing-plan.md`.

## Done
- Deleted `Risk`/`Risk_eq_RiskGap` from `Capability.lean`; `RiskGap := Control − CCI` is now the sole name for the numeric risk-gap quantity.
- Removed the duplicate `Risk`-named theorems that existed only to restate `RiskGap` versions under the old name (`risk_bound_successor_safe_step`, `risk_bound_along_successor_measurand_chain`, `risk_bound_along_successor_safe_chain` in `Successors.lean`; `risk_le_delta_of_cci_slack` in `Capability.lean`).
- Renamed the remaining non-duplicate theorems `risk_* → risk_gap_*` across `Capability.lean` and `Certification.lean`; retyped every `Risk A ≤ δ` conclusion to `RiskGap A ≤ δ` in `Certification.lean`, `Forgeability.lean` (MB10's hypothesis), `Field/Finite/TraceBIQ.lean`, `WorkedInstance.lean`.
- Updated prose to match: `formal/README.md`, `AlignmentProofSpine.lean` and `Core.lean` docstrings, `metadata/assumptions-ledger.md`, `formal/axiom-ledger.json` (one ledger entry renamed).
- Found and fixed the identical "two names for one subtraction" pattern in the manuscript itself — `chapters/ch33-certification-without-construction.tex` had `\mathrm{Risk}(A) = \mathrm{RiskGap}(A)` as its own equation (`eq:risk`); removed it and updated all `appG-lean-proof-spine.tex`/`appD-worked-example.tex`/`ch42-safety-case.tex`/`ch48-towards-alignment.tex` citations to `RiskGap`.
- Added prose (P2/P3 of the plan): `CCIThresholds` (`θ`) is a deployment-specific empirical/policy input, same epistemic class as `MB1`'s estimator soundness; and `MB11_safety_case_adequacy` + `WithinDeploymentRiskTolerance` is foregrounded in `formal/README.md`/`metadata/assumptions-ledger.md` as the framework's honest (Prop-valued, not quantitative) answer to "what do you actually get."
- Verified: `lake build` (2250/2250 clean, only pre-existing unrelated warnings), `python3 scripts/check_axiom_budget.py` (37 theorems, no drift), `make check` (structure/citations/bib-summaries pass).

## Decisions
- **Stopped mid-plan on the vector-primacy refactor** (P1's other half: making `CCICertificatePasses` the primary certification object instead of weighted `CCI`). Discovered that `CCI` itself — not just the certificate's `lambdaProjection` — is *defined* at the `System` level as the λ-weighted quantity (`Correction.lean`, ch46 `eq:cci-ch46`). Removing the weighting from the primary path means introducing a new unweighted quantity and rewiring every bridge that reads `CCI` (`MB6b`, `MB7c`, `S10`), not a `Certification.lean`-local change. Asked the user; they chose to stop here and scope it as a separate backlog item rather than proceed same-session. Recorded as a "Finding" + backlog entry in `drafts/lean-risk-spine-typing-plan.md`.
- Left `formal/LeanProofSpineImplementationBrief.md` untouched: it's a superseded Lean-3-syntax design brief, not synced with the current implementation; rewriting historical planning docs was judged out of scope.
- Renamed theorem identifiers (not just types) where the old name was `risk_*`, for consistency with `RiskGap`, rather than keeping old names with new types — matches the user's "adapt reference" instruction from the prior session.

## Open / next
- Backlog item: unweight `CCI`'s primary path (new `rawCapacityFloor`-style quantity, rewire `MB6b`/`MB7c`/`S10` consumers) — needs its own sizing session before starting; see `drafts/lean-risk-spine-typing-plan.md` backlog.
- P4 (toy `WithinDeploymentRiskTolerance` instantiation from an existing episode battery) still open, optional, not started.

## Key paths
- `drafts/lean-risk-spine-typing-plan.md` — updated with done/deferred status and the CCI-weighting finding.
- `formal/AlignmentProofSpine/{Capability,Certification,Successors,Forgeability,WorkedInstance}.lean`, `formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean`
- `formal/README.md`, `metadata/assumptions-ledger.md`, `formal/axiom-ledger.json`
- `chapters/ch33-certification-without-construction.tex`, `chapters/ch42-safety-case.tex`, `chapters/ch48-towards-alignment.tex`, `appendices/appG-lean-proof-spine.tex`, `appendices/appD-worked-example.tex`

## Commits
- None yet — changes staged for user review, not committed (per repo convention of only committing on explicit request).
