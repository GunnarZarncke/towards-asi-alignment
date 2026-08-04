---
formulas:
  - id: appi:eq:field-interrupt
    latex: I_t\in\{0,1\},\qquad \frac{\partial \mathbb E U_A}{\partial P(I_t=1)}\approx 0\ \text{on the interrupted branch}
    explanation: 'Field object: safe interruptibility as near-zero incentive to manipulate interruption on the branch where learning is paused.'
    chapterId: ch25
  - id: appi:eq:interrupt-subsumption
    latex: \mathrm{UsableCorrectionInformation}(\Delta_H,\Delta_A,\kappa_{\min})\ \Rightarrow\ \mathrm{InterruptCorruptionSuboptimal}
    explanation: 'Forward projection: preserved correction information above a capacity floor makes corrupting the interrupt handle suboptimal.'
    chapterId: ch28
  - id: appi:eq:interrupt-separation
    latex: \mathrm{OrseauNeutral}\ \wedge\ \neg\mathrm{CorrectionChannelPreserved}
    explanation: 'Non-converse separation: Orseau-style interrupt neutrality without broad correction preservation.'
    chapterId: ch28
leanNodes:
  - nodeId: interrupt_safety_is_correction_projection
    kind: proof
    summary: Interrupt safety as a projection of usable correction information.
    module: AlignmentProofSpine/Field/Interruptibility.lean
  - nodeId: interrupt_subsumption_ch46
    kind: proof
    summary: Chapter 46-facing interrupt projection through correction interface records.
    module: AlignmentProofSpine/Field/Interruptibility.lean
  - nodeId: interrupt_separated_from_correction
    kind: counterexample
    summary: 'Finite witness: interrupt neutrality while correction channel fails.'
    module: AlignmentProofSpine/Field/Interruptibility.lean
  - nodeId: OA2016_safe_interruptibility_under_modification
    kind: definition
    summary: 'Imported handle: modified learning setup can avoid incentives to prevent or seek interruption.'
    module: AlignmentProofSpine/Field/Imported.lean
citeKeys:
  - orseau2016interruptible
---

Safe interruptibility solves a real training pathology: agents that disable their kill switches. This project's correction-channel frame asks a broader question — does human steering still change future behavior before irreversible damage?

Lean records the forward link when correction information meets a capacity floor, and the separation when interrupt neutrality holds without correction preservation. Interruptibility is one projection among many; certification must track the full channel, not only the interrupt bit.

*What safe interruptibility keeps that this crosswalk does not replace:* a precise training-time condition with convergence guarantees. The correction-bandwidth notion has no comparable convergence result yet.
