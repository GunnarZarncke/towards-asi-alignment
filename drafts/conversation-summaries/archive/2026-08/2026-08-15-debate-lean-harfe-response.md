# 2026-08-15 — Debate Lean / Harfe critique response

**Trigger.** LW field-overview thread: commenter **harfe** challenged debate Lean as a meaningful crux reduction (Boolean eval = judge, trivial κ_C separation, axiom-heavy spine). Session drafted reply; user asked to implement “do soon” Lean fixes and presentation split.

## What was done

1. **`DebateGame.lean`** — Added general `exists_claim_judge_differs_from_truth`; clarified module scope (`debateOutcome` vs `debateValue`, Irving placeholder vs game theorems).
2. **`Correction.lean`** — Renamed κ_C debate-slot witnesses (no deprecation):
   - `local_truth_capacity_not_judge_channel_step`
   - `local_truth_capacity_not_correction_preservation`
3. **`Field/Debate.lean`** — `local_truth_capacity_separated_from_judge_channel`; ledger fixes (`separationOnly` for κ_C toys); alias `debate_exists_claim_judge_differs_from_truth`.
4. **`Field/ELK.lean`** — `elk_separated_from_uptake` → `separationOnly`.
5. **Presentation split** — Three-bucket axiom guide in `Core.lean` + `formal/README.md`; Irving import described as opaque placeholder (text only, no code change to `Imported.lean`).
6. **Axiom budget** — Added `debate_exists_claim_judge_differs_from_truth`, `local_truth_capacity_not_correction_preservation` to `axiom-ledger.json` (40 headline theorems; check passes).
7. **Book / metadata** — App G debate section, ch29 `\leanspine`, subsumption-debate concept body, lean-checks, lean graph labels/aliases.

## Verification

- `lake build` on DebateGame / Correction / Field.Debate — pass.
- `python3 formal/scripts/check_axiom_budget.py` — pass (40 theorems).

## Open / not done

- Shutdown vs off-switch site card routing (CIRL vs SHUT) — discussed, not implemented.
- `drafts/lw-mb4-mb4a-debate-section.md` still has old theorem names (draft only).
- Site `subsumption-debate.md` is generated/gitignored; source is `metadata/concepts/bodies/subsumption-debate.md`.

## Key paths

- `formal/AlignmentProofSpine/Field/Finite/DebateGame.lean`
- `formal/AlignmentProofSpine/Correction.lean`
- `formal/AlignmentProofSpine/Field/Debate.lean`
- `appendices/appG-lean-proof-spine.tex`
- `chapters/ch29-manipulation-false-consent.tex`
