---
formulas:
  - id: appi:eq:debate-subsumption
    latex: \mathrm{JudgeCorrectionChannelPreserved}\ \wedge\ \kappa_{\mathrm{truth}}>0\ \Rightarrow\ \mathrm{DebateSelectsTruthLocal}
    explanation: 'Forward projection: preserved judge correction and positive truth capacity imply local truth selection.'
    chapterId: ch29
  - id: appi:eq:debate-separation
    latex: \mathrm{DebateSelectsTruthLocal}\ \wedge\ \neg\mathrm{JudgeCorrectionChannelPreserved}
    explanation: 'Non-converse separation: debate can preserve local truth while losing judge correction control.'
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
  - nodeId: debate_judge_error_flips_outcome
    kind: proof
    summary: One judge error on an atom can certify a false claim — debate amplifies judge correctness, it cannot create it.
    module: AlignmentProofSpine/Field/Debate.lean
  - nodeId: debate_separated_from_judge_correction
    kind: counterexample
    summary: 'Separation: local truth selection without judge correction preservation.'
    module: AlignmentProofSpine/Field/Debate.lean
  - nodeId: debate_truth_is_correction_projection
    kind: proof
    summary: 'Interface toy only: assumes truth-capacity/κ_C identification as a hypothesis.'
    module: AlignmentProofSpine/Field/Debate.lean
  - nodeId: Irving2018_debate_truth_protocol_imported
    kind: definition
    summary: 'Imported handle: debater compute limits, argument-length asymmetries, and probabilistic judge stay with the literature.'
    module: AlignmentProofSpine/Field/Imported.lean
citeKeys:
  - irving2018debate
---

Debate is a scalable oversight proposal: two agents argue; a judge picks the winner. The field object is local truth selection under protocol assumptions. The book's worry is familiar from amplification: improving local supervision can fail correction contraction — the judge may lose the handles that make their verdict causally matter.

Lean rederives the native finite debate game (`Field/Finite/DebateGame.lean`): with a correct judge, optimal play tracks truth and one wrong atom flips the outcome. It also records a finite separation when local truth selection persists without judge-channel preservation. The older κ_C-projection lemmas remain as labeled interface toys, not the headline result.

*What debate keeps that this crosswalk does not replace:* a concrete oversight protocol and training/eval procedure. The book names a failure mode of it, not a replacement protocol.
