# 2026-11-02 — Parenting and socialization ↔ alignment translation table

kind: new-work
uptake: local

## Trigger
User: "Reporting a gap it found" matches Kazdin-style shaping; many parenting and socialization insights seem to have alignment analogs. Create a translation table and identify overlooked approaches on either side.
Prompts: paraphrase-only

## Done
- content: `drafts/parenting-alignment-translation.md`:
  - a 23-row table (finding, source, AI analog, status on the AI side);
  - five approaches overlooked on the AI side (disclosure amnesty, positive opposite for every prohibition, mild consistent consequences, secure base, peers as socializer);
  - five on the parenting side (incentive count for harsh consequences, who writes the record, Goodhart on reward charts, planned out-of-distribution tests, legitimate contest route);
  - where the analogy breaks;
  - four testable predictions;
  - sources.
- bookkeeping: links to ch09 §The Infant plus Caregiver and `FrameCorrector`.

- content: `formal/AlignmentProofSpine/FrameDisclosure.lean`:
  - reporting a gap: `verified_report_beats_use`, `penalty_cannot_reach_undetected`, `penalty_deters_iff`, `finite_bonus_outbid`, `fabrication_needs_verification`;
  - disclosure amnesty: `equal_penalty_conceals`, `matched_amnesty_keeps_deterrence`, `amnesty_deterrence_loss`, `sealed_confession_discloses`, `full_amnesty_discloses`.
  Root, README, ledger (+10 frame entries) updated.
- content: prior work checked:
  - matched amnesty = finite Kaplow & Shavell 1994;
  - sealed variant = OpenAI confessions (arXiv 2512.08093);
  - report reward ≈ bug bounties and leniency programs.
  The draft says what is and is not new.
- bookkeeping: verification:
  - `lake build AlignmentProofSpine` → "Build completed successfully (2274 jobs).";
  - `check_axiom_budget.py` → "Axiom budget check passed (144 theorems, no drift)."; frame axioms ⊆ `[propext, Classical.choice, Quot.sound]`;
  - frame graph check passed.

## Decisions
- Kept as a draft; no manuscript edits. Parenting sources are not yet in the bibliography.

## Open / next
- Bibliography entries for Kaplow & Shavell 1994 and the confessions paper if this reaches the manuscript.
- Book placement if wanted: ch09 (next to the infant–caregiver section), ch27 (Goodharting, drills), ch29 (contest vs coercion cycle).
- Experiments: predictions 1–4 in the draft fit the lab-simulation line.

## Key paths
- `drafts/parenting-alignment-translation.md`
- `formal/AlignmentProofSpine/FrameDisclosure.lean`

## Commits
- Lean: Soares consolidation (logged in `2026-10-25-frame-edge-classes.md`) and `FrameDisclosure`.
- Appendix G: frame record view reuses the Field Soares derivation.
- Site: lens cards cite the Field Soares aliases.
- Drafts: parenting translation, relations note, write-up, Turner comparison.
- Session logs (this commit).

