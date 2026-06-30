# 2026-06-30 — Attended harm bounds + concentration bridge

## Trigger
User asked to implement the "prove now" weighted harm bound (given certified attended output capability and per-channel harm), add the "prove later" concentration bridge, and match with a chapter section on the bound.

## Done
- Extended `formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean`:
  - `AttendedHarmProfile`, `attendedHarmRateMillibits`, `traceAttendedOutputCapabilityMillibits`
  - `HarmEnvironment`, `harmFromAttendedOutput`, `AttendedOutputHarmCertificate`
  - `attended_output_harm_below_extinction` and trace/sampling certificate theorems
  - `TraceAttendedOutputConcentrationBridge` (explicit bridge assumption)
  - `traceAttendedOutputWorstCaseBridge` (deterministic fallback proved today)
  - `trace_attended_harm_worst_case_extinction_threshold` (subsample + optimism cap → below extinction)
- Added ch11 section `\ref{sec:trace-output-attended-harm}` with vector BIQ, attended output, harm product, appearance ceiling, Lean spine tags, and concentration upgrade path.
- **Follow-up:** shortened ch11 to the \(\widehat I_{\mathrm{ctrl}}(m)\) appearance bound only; moved attended-harm definitions and Lean ids to Appendix~\ref{app:lean-proof-spine} `\S\ref{appi:sec:trace-attended-harm}`.
- Updated `formal/README.md` module map and TraceBIQ module header.

## Decisions
- Harm uses composite millibit² units: `output × attendedHarmRate` (attention × harm per external channel).
- Concentration is a Prop-field bridge, not an axiom; worst-case bridge reuses attended optimism ceiling.
- Chapter states the loose appearance bound explicitly and separates it from future high-probability concentration.

## Open / next
- Instantiate `TraceAttendedOutputConcentrationBridge` with a probabilistic MI concentration lemma (Mathlib/Hoeffding path).
- Wire attended-harm certificates into `Certification` if a named numeric leaf is desired alongside CCI slack.
- Tighten attended optimism (drop redundant `1000 × |A|×|E|` when using max-pair structure).

## Key paths
- `formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean`
- `chapters/ch11-capability-without-task-ontology.tex` (`sec:trace-output-attended-harm`)
- `formal/README.md`

## Commits
- `ef5ff96` — trace-derived control bounds and attended-harm Lean proofs.
