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

## Follow-up (2026-11-03)
- bookkeeping: optional TODO "Frame, disclosure, and parenting results into the manuscript" on the `metadata/TODO.md` Housekeeping board.
- content: `drafts/plans/spine/corrector-cci-vector.md` elaborates tying `FrameCorrector` to the full CCI vector:
  - finite mirror of `CCICertificate` with a mirror lemma to `CCICertificatePasses`;
  - one avoidance route per coordinate;
  - theorems: corrector decides under the full gate, per-coordinate necessity, scalar projection admits compensation, validity is not a coordinate, optional report action;
  - what it does not show.
  Spine checklist line added.
- correction (review on request): the ten-route plan was circular. Each route was defined to fail only its own coordinate, so per-coordinate necessity holds for any conjunction. This matches the earlier reason for keeping `CCICertificate` a plain record (2026-06-28 and 2026-06-30 logs, `WorkedInstance`). Plan rewritten:
  - step 1 done: `scalar_floor_blind_to_process` (`Correction.lean`). `lambdaProjection` never reads coercion, dependency, plurality, exit capacity or independence.
  - step 2 deferred: four decision classes (reach, timing, source, uptake). It depends on measured coordinates per class and a pre-registered measurement map.
- content: ch26 `eq:cci-legit` no longer subtracts `λ_M M` twice (it is already in `CCI_λ`). ch26 §Scalar projection gets one sentence and a `\leanspine` line. The Appendix G scalar-floor lemma states the converse fails. Also updated: README module row and axiom ledger entry.
- bookkeeping: spine P3 line marked deferred; TODO pointer updated.
- Verification:
  - `lake build AlignmentProofSpine`: "Build completed successfully (2274 jobs)."
  - `#print axioms scalar_floor_blind_to_process`: `propext`, `Quot.sound` and spine vocabulary (`System`, `SystemCorrectionPath`, `GroundingViable`, …). No `MB*`.
  - `check_axiom_budget.py`: "Axiom budget check passed (145 theorems, no drift)."
  - `./build.sh`: "Built dist/pdf/towards-superintelligence-alignment.pdf". Undefined cites (`arnstein1969ladder` and others) come from ch25/appP in commit `4e85d1a22a`, not from this change.
  - `make check` fails only on markdown links. This change's only broken link is the untracked plan file.
- correction (author question): the ch26 scalar was labelled "for exposition" but about twenty chapters use it, several as a pass/fail gate. The 2026-06-28 vectorization never promoted the vector to those gates. Plan: `drafts/plans/cci-vector-promotion.md`. It sorts each use into gate, risk arithmetic, or preservation.
- content: gates moved to `\vec{CCI} \succeq \vec{\theta}_{corr}`:
  - ch22, ch25, ch28, ch29, ch31 (two sites), ch33 (five sites; high/low stakes now per coordinate), ch34 (plus the label fix), ch39 (two), ch40 (two), ch46, ch47.
  - Risk-arithmetic sites keep the scalar.
- content: ch26 §Scalar projection rewritten:
  - the scalar is the risk-bound measurand, valid once the vector passes;
  - why these five terms (the correction itself vs the corrector's situation);
  - preservation comparisons compare the projection and presuppose the vector passes at both ends.
- bookkeeping: TODO item "Componentwise CCI preservation (M, deferred)" for the preservation and dynamics sites and Lean `CCIPreserved`.
- Verification: `./build.sh`: "Built dist/pdf/towards-superintelligence-alignment.pdf", no undefined references. A grep for scalar `CCI` threshold comparisons outside appG finds only ch26 prose about the scalar.

## Commits
- Lean: Soares consolidation (logged in `2026-10-25-frame-edge-classes.md`) and `FrameDisclosure`.
- Appendix G: frame record view reuses the Field Soares derivation.
- Site: lens cards cite the Field Soares aliases.
- Drafts: parenting translation, relations note, write-up, Turner comparison.
- Session logs (this commit).

