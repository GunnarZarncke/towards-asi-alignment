---
formulas:
  - id: appi:eq:basin-forward
    latex: \text{BasinStable}(B)\ \wedge\ \text{CorrectionPreserving}(B)\ \Rightarrow\ \text{MB6b\_basin\_stability\_to\_correction\_integrity}
    explanation: 'Forward bridge shape: basin stability plus correction preservation supports correction integrity (bridge MB6b).'
    chapterId: ch35
  - id: appi:eq:basin-lock-in-separation
    latex: \text{BasinStable}(B_{\text{bad}})\ \wedge\ \neg\text{CorrectionIntegrity}
    explanation: 'Non-converse separation: a stable basin can be stably bad — lock-in without correction preservation.'
    chapterId: ch37
  - id: appi:eq:selection-against-safe
    latex: \text{SafeAgent}(A)\ \Rightarrow\ \text{SelectedAgainst}(A)
    explanation: 'Selection separation: deployment ecology can select against correction-preserving agents (P31).'
    chapterId: ch34
leanNodes:
  - nodeId: MB6b_defeater_toy_lock_in
    kind: counterexample
    summary: 'MB6b toy defeater: locked-in bad basin with stable selection against correction.'
    module: AlignmentProofSpine/Defeaters.lean
  - nodeId: P31_safe_agent_selected_against
    kind: counterexample
    summary: 'Finite separation: safe agents can be selected against under adversarial selection.'
    module: AlignmentProofSpine/Adversarial.lean
  - nodeId: MB6a_percolation_evidence_to_basin_stability
    kind: bridge
    summary: 'Bridge MB6a: percolation evidence supports basin stability (empirical handoff).'
    module: AlignmentProofSpine/Core.lean
  - nodeId: MB6b_basin_stability_to_correction_integrity
    kind: bridge
    summary: 'Bridge MB6b: basin stability supports correction integrity when selection preserves correction.'
    module: AlignmentProofSpine/Core.lean
citeKeys:
  - kulveit2025gradualdisempowerment
  - goodhart1984problems
---

Goodhart selection and gradual-disempowerment framings emphasize deployment ecology: which systems get copied, promoted, and resourced — not weights alone. This project's basin-stability layer asks whether socio-technical selection supports a basin that preserves correction rather than hollow it out.

Lean records bridge shapes MB6a/MB6b as empirical handoffs and proves finite defeaters: `MB6b_defeater_toy_lock_in` witnesses stable bad basins, and `P31_safe_agent_selected_against` shows correction-preserving agents can lose under selection pressure. Basin stability is therefore a projection of alignment outcomes, not a substitute for correction-channel integrity.

*What selection-focused agendas keep that this crosswalk does not replace:* institutional design cases, compute-governance levers, and empirical measurement of disempowerment trajectories. The projection clarifies claim strength; it does not replace field selection research.
