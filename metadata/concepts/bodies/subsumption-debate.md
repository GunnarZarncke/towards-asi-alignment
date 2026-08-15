---
formulas:
  - id: appi:eq:debate-subsumption
    latex: \mathrm{JudgeCorrectionChannelPreserved}\ \wedge\ \kappa_{\mathrm{truth}}>0\ \Rightarrow\ \mathrm{DebateSelectsTruthLocal}
    explanation: 'Forward projection: preserved judge correction and positive truth capacity imply local truth selection.'
    chapterId: ch29
  - id: appi:eq:debate-separation
    latex: \mathrm{DebateSelectsTruthLocal}\ \wedge\ \neg\mathrm{JudgeCorrectionChannelPreserved}
    explanation: 'Non-converse κ_C capacity toy: local truth capacity can hold while judge correction channel collapses.'
    chapterId: ch41
leanNodes:
  - nodeId: debate_tracks_truth
    kind: proof
    summary: With a correct judge, debate game value equals claim truth on finite claim trees.
    module: AlignmentProofSpine/Field/Finite/DebateGame.lean
  - nodeId: debate_defender_wins_iff_true
    kind: proof
    summary: Defender wins under optimal play iff the claim is true (correct judge).
    module: AlignmentProofSpine/Field/Finite/DebateGame.lean
  - nodeId: debate_exists_claim_judge_differs_from_truth
    kind: proof
    summary: If the judge disagrees with ground truth on any atom, some claim is mis-certified.
    module: AlignmentProofSpine/Field/Finite/DebateGame.lean
  - nodeId: debate_judge_error_flips_outcome
    kind: proof
    summary: Named witness — one judge error on an atom certifies a false claim.
    module: AlignmentProofSpine/Field/Debate.lean
  - nodeId: local_truth_capacity_separated_from_judge_channel
    kind: counterexample
    summary: 'κ_C capacity toy: local truth capacity without judge correction preservation (not a DebateGame theorem).'
    module: AlignmentProofSpine/Field/Debate.lean
  - nodeId: debate_truth_is_correction_projection
    kind: bridge
    summary: 'Interface toy only: assumes truth-capacity/κ_C identification as a hypothesis (ledger: separationOnly).'
    module: AlignmentProofSpine/Field/Debate.lean
  - nodeId: Irving2018_debate_truth_protocol_imported
    kind: definition
    summary: 'Opaque literature placeholder only — bounded judge / obfuscated arguments not rederived; distinct from DebateGame theorems.'
    module: AlignmentProofSpine/Field/Imported.lean
citeKeys:
  - irving2018debate
---

Debate is a scalable oversight proposal: two agents argue; a judge picks the winner. The field object is local truth selection under protocol assumptions. This project's worry is familiar from amplification: improving local supervision can fail correction contraction — the judge may lose the handles that make their verdict causally matter.

Lean rederives the native finite debate game (`Field/Finite/DebateGame.lean`): with a correct judge, optimal play tracks truth; if the judge disagrees with truth on any atom, some claim is mis-certified (`debate_exists_claim_judge_differs_from_truth`). The κ_C capacity separations (`local_truth_capacity_*` in `Correction.lean`) are modeling-slot counterexamples, not game theorems. The older κ_C-projection lemmas remain labeled interface toys.

*What debate keeps that this crosswalk does not replace:* a concrete oversight protocol and training/eval procedure. This project names a failure mode of it, not a replacement protocol.
