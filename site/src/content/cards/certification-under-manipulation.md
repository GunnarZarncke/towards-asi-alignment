---
title: "Certification-Under-Manipulation Problem"
type: "concept"
status: "open"
summary: "For each load-bearing certification measurand, does there exist a capability threshold κ* below which honest measurement is adversarially verifiable and above which it provably is not?"
decision: "For every metric in a deployment gate, ask for the constructive cost-of-faking relation and the capability level at which theater becomes affordable."
evidence: "Positive resolution requires a calibrated c_fake dominating affordable surplus up to stated κ*; negative resolution requires showing every candidate measurand fails below needed capability."
bookChapters: ["ch43", "ch47", "ch42", "ch48"]
bookLabels: ["ch:verifiability-ontology"]
bookSections:
  - chapterId: "ch43"
    label: "sec:certification-under-manipulation-ch43"
related: ["correction-channel-integrity", "anti-capture-correction-validity", "goodhart-as-selector"]
---

Every load-bearing measurand in the book — boundary residual, value-bundle activation, correction-channel integrity, conserved-property score, laundering index — shares one antecedent: **can the certification channel stay honest against a capable adversary?**

The **Certification-Under-Manipulation Problem** names it explicitly (Chapter 43):

Given measurand \(M\) used to gate deployment or successor creation, and system capability \(\kappa\) that can act on the world before, during, and after \(M\) is evaluated: does there exist \(\kappa^{*}\) such that for all \(\kappa < \kappa^{*}\), \(M\) is adversarially verifiable (cost of faking grows faster than affordable surplus), and for \(\kappa \geq \kappa^{*}\) it provably is not?

This is ELK-shaped, not merely "metrics can be gamed." Generic Goodhart warns that optimizing a proxy degrades it. This problem asks for the **actual threshold** at which a specific measurand flips from honest to fakeable, with a constructive cost relation — and it is parasitic on capability: the target already "knows" whether \(M\) is honest.

Current status: the cost-relation definition is formalized generically; \(c_{\mathrm{fake}}\) is not established for any concrete measurand against a real adversary. Treating correlated steerability as one chokepoint rather than independent failures is part of the same problem.
