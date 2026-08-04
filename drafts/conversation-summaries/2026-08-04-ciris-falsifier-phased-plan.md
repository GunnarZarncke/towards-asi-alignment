# 2026-08-04 — CIRIS falsifier phased plan

## Trigger

User asked whether CIRIS research traces (CEG capture) are usable for UAD or
in-repo simulation lines; then how Coherence Ratchet / triage / Ratchet Torque
relates to book bridges; then to phase the named-identity / composite-agency
falsifier with Lens cohort work deferred. End-of-session commit.

## Done

- Assessed CIRIS `tools/research` traces vs UAD / ET annexes: not plug-and-play;
  CEG attestation ≠ multi-agent action series; falsifier is a different question
  than coalition UAD.
- Mapped Coherence Ratchet (Lens triage), TORQUE (empirical DV validation), and
  named-identity bet to MB1/MB4a/MB7/A-009.
- Updated falsifier charter (sibling workspace, not git):
  `~/repos/ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`
  — phased plan, C2 locked, Lens framework section, P1–P5 pre-registrations,
  Phase 3 deferred (≥3 agents × ≥10 traces).
- Updated `experiments/TODO.md` with phase summary.

## Decisions

- **Phase 1 (now):** narrative + trace mock (scripted Lens scalars), Eric memo;
  optional sibling sim bite (toy `boundary_decouple`, lab LS-28).
- **Phase 2:** CIRISAgent integration harness — no Lens cohort.
- **Phase 3 (deferred):** Lens cohort + full Coherence Ratchet battery; not a
  gate for the logical falsifier.
- **Cross-agent divergence:** requires multi-agent trace corpus; silence on
  divergence while composite bypass runs is the expected damning result — not
  the primary kill signal.
- **v1 scenario:** C2 tool-heavy scout (agent defers; tool/memory side effects).

## Open / next

- Artifact A under `~/repos/ciris/review/` — dual timeline mock (named CEG green +
  composite effect log).
- Eric memo after Artifact A.
- Optional CIRIS-labeled `boundary_decouple` harness in book `experiments/`.
- Phase 3 when Eric engages and trace capture cost is justified.

## Files touched (book repo)

- `experiments/TODO.md`
- `drafts/conversation-summaries/2026-08-04-ciris-falsifier-phased-plan.md`
- `drafts/conversation-summaries/HANDOFF.md`
- `drafts/conversation-summaries/INDEX.md`

## Sibling (not in book git)

- `~/repos/ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`
