# 2026-06-19 — Lean certification chain + agent Lean-review rule (session end)

## Trigger
Continue formalization after initial spine commit: link `Control` to BIQ ceiling,
tie `CorrectionCapacity` to weakest-link graph capacity, then add repo guidance
to review Lean proofs when drafting or integrating chapters. User ended session
without commit.

## Done
- **BIQ → control (`Capability.lean`):** per-system profile (`IpredSys`, `IctrlSys`,
  `CactSys`, …), `Control_le_IctrlSys`, `Control_le_CactSys`, `BIQDerivedCapacitySlack`,
  `risk_bound_from_biq_ceiling`, `BIQCapacityCertificate`.
- **Weakest-link → correction (`Correction.lean`):** `CorrectionLinkCapacities`,
  `CorrectionCapacity = ChainCapacity (…)`, `P24_correction_capacity_le_each_link`;
  removed free `axiom CorrectionCapacity` from `Core.lean`.
- **Compose BIQ + graph (`Capability.lean`, `Certification.lean`):**
  `WeakestLinkDerivedCapacitySlack`, `certified_class_safety_from_biq_ceiling`,
  `…_weakest_link_slack`, spine+bridges variants, successor-chain variants.
- **Successor chains (`Successors.lean`):** `SuccessorSafeChain`, risk bound
  propagation via `SuccessorSafe_risk_monotone` (from prior pass in same arc).
- **Risk derivation (prior pass, same uncommitted tree):** `Risk = RiskGap`,
  primary certification from capacity slack not bare `hrisk`.
- **Docs:** `formal/README.md`, `metadata/TODO.md`, `metadata/source-canon.md`
  updated for toy status and completed chain items.
- **Agent / contributor guidance:** **Chapter work — Lean spine** in `AGENTS.md`;
  step 7 in `INSTRUCTIONS.md` §21; Shape B integration note; `README.md`
  contributing bullet.
- **`lake build`:** green (no `sorry`/`admit`).

## Decisions
- `CorrectionCapacity` is **defined** as graph weakest-link capacity, not an
  independent axiom — measurement supplies `CorrectionLinkCapacities`.
- BIQ and weakest-link slack certificates compose: full chain is
  `Control ≤ I_ctrl ≤ C_act ≤ WeakestLink (= CorrectionCapacity)` with bridges
  on each measurement step.
- Lean spine review is **required on chapter integrate**, but Lean changes only
  when formal work is explicitly in scope; mismatches go to log / `metadata/TODO.md`.

## Open / next
- **Commit** (user did not ask): suggested split —
  1. `formal:` BIQ + weakest-link + successor propagation + docs (`formal/`,
     `metadata/TODO.md`, `metadata/source-canon.md`, `formal/README.md`, lean logs).
  2. `docs:` AGENTS / INSTRUCTIONS / README Lean-review instruction.
- Remaining spine TODO: adversarial aliasing (`P34`/`MB7`), safety-case (`P40`),
  strengthen counterexamples, wire Ch. 39 / appendix.
- **Uncommitted elsewhere:** `ch26` committed (`c62a7d6`); ch27 at `e2c4357`;
  untracked `LeanProofSpineImplementationBrief.md`, `context/lean_proof_dependency_graph.dot`,
  `src/`, mixed edits to `INDEX.md` / frontmatter log.

## Key paths
- `formal/AlignmentProofSpine/{Core,Capability,Correction,Successors,Certification}.lean`
- `formal/README.md`, `metadata/TODO.md`, `AGENTS.md`, `INSTRUCTIONS.md`
- Prior log: `2026-06-19-lean-spine-risk-derivation.md`

## Commits
- none this session
