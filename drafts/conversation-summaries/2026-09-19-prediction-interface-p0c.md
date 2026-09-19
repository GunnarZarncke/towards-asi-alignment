# 2026-09-19 — Prediction interface P0c

## Trigger
User asked to fold Lean-interface feedback on the 2027 bridge predictions into the larger plans, including what Lean can do now without v2; then language for a predictions appendix, site hub, and session-end commit.

## Done
- Integration checklist [`drafts/plans/predictions/prediction-interface.md`](../plans/predictions/prediction-interface.md).
- Instrument plan P0c + working criteria **0.4** (certificate-output rule; output-type addenda; §§15–18; §3 transport-only; public spec in ordinary English).
- Spine P2 certificate-layer item; `PositiveMeasuredPath → CorrectionIntegrity` marked subsumed.
- embedded-v2 + grain map: certificate adapters are **not** Lean 2.0.
- TODO Outreach/Site rows; this log.

## Decisions
- Missing object is measurement → scoped per-system certificate → unary predicate, not a broken bridge DAG. No `AlignmentContext`.
- §17 (bearer admission) is a separate 2027 market. §16 = MB6b. §18 = scoped safety-in-a-setting (`SafeIn`), not live `Safe`, not §14.
- Derive `Certified` / `SatisfiesInvariants` in Lean later. Residuals: recertification (§6/§15), eval-list vs layers (§13). No market for acceptable-risk (values vote).
- Appendix print H (after research program, before Lean); two registers (Metaculus English in boxes; glossary/research-program around them). Site `/predictions/` + Gauss symbol + coming-soon embed — **not drafted this session**.
- v2-later (not 2027 boxes): restorer, path-legality, cycle-preserve. Do not widen §1/§6/§14.

## Open / next
1. Draft `appendices/appP-bridge-predictions.tex` (print-letter plumbing).
2. Site hub and `prediction` cards.
3. Spine: `Evidence.lean`.
4. Q1/Q2/Q6 still open (listing).

## Key paths
- [`drafts/plans/predictions/prediction-interface.md`](../plans/predictions/prediction-interface.md)
- [`drafts/predictions/bridge-prediction-market-criteria.md`](../predictions/bridge-prediction-market-criteria.md)
- [`drafts/predictions/bridge-predictions-Lean-improvements.md`](../predictions/bridge-predictions-Lean-improvements.md)

## Commits
- (this session)
