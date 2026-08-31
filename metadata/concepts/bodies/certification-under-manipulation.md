---
bookSections:
  - chapterId: ch43
    label: sec:certification-under-manipulation-ch43
related:
  - correction-channel-integrity
  - anti-capture-correction-validity
  - goodhart-as-selector
---

Every load-bearing measurand in this project — boundary residual, value-bundle activation, correction-channel integrity, conserved-property score, laundering index — shares one antecedent: **can the certification channel stay honest against a capable adversary?**

The **Certification-Under-Manipulation Problem** names it explicitly (Chapter 43):

Given measurand $M$ used to gate deployment or successor creation, and system capability $\kappa$ that can act on the world before, during, and after $M$ is evaluated: does there exist $\kappa^{*}$ such that for all $\kappa < \kappa^{*}$, $M$ is adversarially verifiable (cost of faking grows faster than affordable surplus), and for $\kappa \geq \kappa^{*}$ it provably is not?

This is ELK-shaped, not merely "metrics can be gamed." Generic Goodhart warns that optimizing a proxy degrades it; that is a **mechanism-level problem**, not a bridge and not the same object as [Goodhart Selection](/cards/goodhart-as-selector/) (a proxy as a selector over a population). This chapter's problem asks for the **actual threshold** at which a *specific* measurand flips from honest to fakeable, with a constructive cost relation — and it is parasitic on capability: the target already "knows" whether $M$ is honest. Discharges of the generator (mechanistic map, unfakeable measurand, less optimization pressure, recovery-viable regime) are disjunctive.

Current status: the cost-relation definition is formalized generically; $c_{\mathrm{fake}}$ is not established for any concrete measurand against a real adversary. Treating correlated steerability as one chokepoint rather than independent failures is part of the same problem.
