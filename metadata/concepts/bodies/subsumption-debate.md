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
  - nodeId: debate_subsumption_truth
    kind: proof
    summary: Judge correction preserved with positive truth capacity implies debate selects truth locally.
    module: AlignmentProofSpine/Field/Debate.lean
  - nodeId: debate_truth_is_correction_projection
    kind: proof
    summary: Local truth capacity as projection of judge-channel kappa_C.
    module: AlignmentProofSpine/Field/Debate.lean
  - nodeId: debate_separated_from_judge_correction
    kind: counterexample
    summary: 'Separation: local truth selection without judge correction preservation.'
    module: AlignmentProofSpine/Field/Debate.lean
  - nodeId: Irving2018_debate_truth_protocol_imported
    kind: definition
    summary: 'Imported handle: under idealized debate conditions, adversarial argument can make truth easier for a judge to select.'
    module: AlignmentProofSpine/Field/Imported.lean
citeKeys:
  - irving2018debate
---

Debate is a scalable oversight proposal: two agents argue; a judge picks the winner. The field object is local truth selection under protocol assumptions. The book's worry is familiar from amplification: improving local supervision can fail correction contraction — the judge may lose the handles that make their verdict causally matter.

Lean records the forward projection when judge correction and truth capacity align, and a finite separation when truth selection persists without judge-channel preservation. Native debate-game theorem matching remains deferred; the claim here is projection plus separation on the shared finite fragment.

*What debate keeps that this crosswalk does not replace:* a concrete oversight protocol and training/eval procedure. The book names a failure mode of it, not a replacement protocol.
