---
formulas:
  - id: appi:eq:field-shutdown
    latex: C_{\mathrm{off}}:H_t\to u_t\in\{\texttt{continue},\texttt{shutdown}\},\qquad \Pi_{\mathrm{off}}(C_t)=C_{\mathrm{off}}
    explanation: 'Field object: Thornley shutdownability as a one-bit correction handle projecting from the full correction channel.'
    chapterId: ch25
  - id: appi:eq:shutdown-subsumption
    latex: \mathrm{CorrectionIntegrity}(A)\ \Rightarrow\ \mathrm{ThornleyShutdownability}(A)
    explanation: 'Book projection: when the shutdown handle lies in the controlled correction path, correction integrity implies shutdownability.'
    chapterId: ch25
  - id: appi:eq:shutdown-separation
    latex: \mathrm{ThornleyShutdownCapacity}\ \wedge\ \neg\mathrm{BroadCorrectionChannelPreserved}
    explanation: 'Non-converse separation: a live shutdown button can coexist with a collapsed broad correction channel.'
    chapterId: ch27
leanNodes:
  - nodeId: shutdown_subsumption_system
    kind: proof
    summary: System-level forward projection from CorrectionIntegrity to ThornleyShutdownability.
    module: AlignmentProofSpine/Field/Shutdown.lean
  - nodeId: shutdown_subsumption_ch46
    kind: proof
    summary: Chapter 46-facing shutdown projection through correction handles and channel records.
    module: AlignmentProofSpine/Field/Shutdown.lean
  - nodeId: shutdown_separated_from_correction
    kind: counterexample
    summary: 'Finite separation: shutdown capacity without broad correction preservation.'
    module: AlignmentProofSpine/Field/Shutdown.lean
  - nodeId: Soares2015_corrigibility_problem_imported
    kind: definition
    summary: 'Imported handle: utility maximization tends not to preserve corrigibility or shutdownability without special structure.'
    module: AlignmentProofSpine/Field/Imported.lean
citeKeys:
  - soares2015corrigibility
  - thornley2023shutdown
---

Soares-style corrigibility frames shutdown as anti-natural to expected-utility maximization; Thornley formalizes shutdownability as competent systems still accepting an off command. The book recasts both as degenerate projections of correction-channel integrity: a one-bit handle inside a channel that must remain causally effective.

Lean proves that correction integrity implies Thornley shutdownability when the shutdown projection is part of the controlled path, and gives finite MDP witnesses for optimal shutdown under correction preference. The separation is load-bearing: optimizing for the narrow shutdown bit does not reconstruct the full correction invariant the deployment gate actually needs.

*What the shutdown work keeps that this crosswalk does not replace:* a concrete, implementable off-switch mechanism and its incentive analysis. The correction-channel view is more general but is not, by itself, a mechanism you can ship.
