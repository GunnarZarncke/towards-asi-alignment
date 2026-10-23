---
title: "Model-relative proof"
type: "lens"
status: "framework"
summary: "A verifier certificate relative to a world model and a specification — it does not choose the spec."
related:
  - "specify-gsai"
  - "lenses/control-protocol"
  - "lenses/safety-case"
  - "lenses/lenses-and-frameworks"
  - "field-agendas/davidad-guaranteed-safe-ai-gsai"
  - "field-agendas/safeguarded-ai-aria-zeroth-heron"
external:
  - label: "LessWrong tag: Guaranteed Safe AI"
    url: "https://www.lesswrong.com/w/provably-beneficial-ai"
---

**Role.** Protocol. Graph node `proof`.

> The verifier can produce an auditable certificate that the system satisfies the specification relative to the model. It does not choose the specification, establish world-model coverage, or turn proof generation into a target object.
>
> — Frames draft §4.9 (Dalrymple et al. 2024, GSAI)

Proof-carrying code already splits policy, artifact, proof, and checker. Formal proof does not choose what should be proved. On the graph this is a warrant leaf into the safety case and, in variant b, coordinate evidence for the CCI certificate.
