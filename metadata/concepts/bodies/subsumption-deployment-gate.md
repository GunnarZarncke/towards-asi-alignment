---
formulas:
  - id: appi:eq:deploy-case-pass
    latex: \text{SafetyCasePass}\ \wedge\ \text{WithinDeploymentRiskTolerance}\ \not\Rightarrow\ \text{Safe}
    explanation: 'Non-converse separation: case-green within stated tolerance does not imply Safe without scope discipline (MB11 defeater).'
    chapterId: ch42
  - id: appi:eq:deploy-regret-separation
    latex: \text{ZeroRegretBound}\ \not\Rightarrow\ \text{HarmBound}
    explanation: 'Regret separation: zero or bounded regret does not discharge harm bounds on finite interface.'
    chapterId: ch44
  - id: appi:eq:deploy-mb11-bridge
    latex: \text{SafetyCaseAdequacy}\ \Rightarrow\ \text{Safe}
    explanation: 'Forward bridge: MB11 safety-case adequacy supports Safe when bridge assumptions hold.'
    chapterId: ch42
leanNodes:
  - nodeId: MB11_defeater_toy_scope_exceeded
    kind: counterexample
    summary: 'MB11 toy defeater: safety case scope exceeded while case reads green within tolerance.'
    module: AlignmentProofSpine/Defeaters.lean
  - nodeId: zero_regret_not_harm_bound
    kind: counterexample
    summary: 'Finite separation: zero regret does not imply harm bound (RegretSafety toy).'
    module: AlignmentProofSpine/Field/Finite/RegretSafety.lean
  - nodeId: regret_evidence_not_deployment_safe
    kind: counterexample
    summary: 'Interface separation: regret evidence alone does not imply deployment safe.'
    module: AlignmentProofSpine/FieldInterfaces.lean
  - nodeId: MB11_safety_case_adequacy
    kind: bridge
    summary: 'Bridge MB11: safety-case adequacy supports deployment-level Safe.'
    module: AlignmentProofSpine/Certification.lean
citeKeys:
  - dalrymple2024gsai
---

Deployment safety and safety-case agendas ask whether evidence supports scaling compute, release, or pivotal deployment. This project treats episode-battery pass, regret bounds, and case-green status as projections of deployment-level Safe — not as substitutes for scope discipline.

Lean proves finite defeaters: `MB11_defeater_toy_scope_exceeded` when case reads green but scope is exceeded, and `zero_regret_not_harm_bound` showing regret alone does not discharge harm bounds. MB11 forward assembly remains an explicit bridge; the separations calibrate what case-green actually certifies.

*What safety-case engineering keeps that this crosswalk does not replace:* concrete hazard analysis templates, organizational sign-off workflows, and empirical validation batteries. The projection records logical dependencies; it does not replace a safety case document.
