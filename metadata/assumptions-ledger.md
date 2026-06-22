# Assumptions Ledger

**Last cross-check:** 2026-06-23 — reconciled against ch05 (Assumptions, Scope, and Failure Coverage) "Background Assumptions" + "Correction-Capacity Assumption", the chapter `chapterthesis` blocks, and the conceptual spine. Chapter numbers refer to the current 44-chapter map in `metadata/book.yml`.

A-001 and A-002 are the two load-bearing technical assumptions. A-003–A-005 are the ch05 background/scope assumptions (the framework's preconditions). A-006–A-008 are operational assumptions the measurement program depends on.

---

## Assumption ID: A-001

**Assumption:** Human values have enough low-dimensional bundle structure to be approximated and transported.

**Used in:** Chapters 4, 15–22, 24–25, 41–43

**Why needed:** Without some compressed structure, value learning and correction-channel modeling become sample-intractable.

**Failure mode if false:** The framework may preserve a simplified proxy rather than human values.

**Evidence:** moral psychology, affective neuroscience, preference PCA, low-rank alignment findings

**Confidence:** medium

**Tests:** look for elbows in preference-prediction curves; compare low-rank versus high-dimensional models on value-related behavior

**Bears on:** C-004

## Assumption ID: A-002

**Assumption:** Correction channels can be modeled as causal chains with measurable integrity.

**Used in:** Chapters 24–27, 34, 40

**Why needed:** Without a causal model, alignment reduces to post-hoc outcome evaluation.

**Failure mode if false:** Correction-channel integrity metrics may be gamed or inapplicable under adversarial opacity.

**Evidence:** institutional feedback loops, human-in-the-loop deployment patterns

**Confidence:** medium

**Tests:** audit correction chains in deployed systems; measure manipulation resistance

**Bears on:** C-005

## Assumption ID: A-003

**Assumption:** Civilization still retains enough epistemic, institutional, and physical correction capacity at the relevant time, i.e. \(C_{\text{corr}}^{\text{society}}(t_0) > \theta\); broader pre-ASI risks are treated as assumption threats, not the central object.

**Used in:** Chapter 5 (scope); presupposed throughout

**Why needed:** The theory "begins after" society can still notice, evaluate, and constrain frontier systems; if that capacity has already collapsed, the alignment theory arrives too late.

**Failure mode if false:** The framework is inapplicable — correction-based alignment has no foothold.

**Evidence:** existence of current AI governance, evaluation, and audit institutions (contested adequacy)

**Confidence:** medium-low (an explicit precondition, not argued for)

**Tests:** track institutional/epistemic correction capacity indicators over time relative to capability growth

**Bears on:** C-002, C-005, C-007

## Assumption ID: A-004

**Assumption:** Frontier systems remain observable and measurable enough for boundary discovery and adversarial measurement; agent boundaries are detectable via conditional independence / screening-off in real deployments.

**Used in:** Chapters 5, 6, 7, 9, 36, 38

**Why needed:** Boundary-finding, capability measurement, and correction all require that the relevant object can be located and probed.

**Failure mode if false:** Boundary discovery fails; capability and correction metrics attach to the wrong object.

**Evidence:** interpretability/measurement progress; conditional-independence structure in deployed pipelines

**Confidence:** medium-low (boundaries are leaky, non-stationary, and adversarially hidden — ch07, ch10)

**Tests:** validate boundary-finding procedure on systems with known structure; measure residual surprise across candidate boundaries

**Bears on:** C-001, C-003, C-010

## Assumption ID: A-005

**Assumption:** Deployment can still be conditioned on certification, and humans retain enough agency to refuse, revise, and coordinate.

**Used in:** Chapters 5, 31, 32, 35

**Why needed:** Certification-without-construction and selection-environment arguments require that certificates can gate deployment and that humans can act on them.

**Failure mode if false:** Certification is decorative; the selection environment rewards correction-eroding systems unchecked.

**Evidence:** existing deployment-gating regimes (model releases, compliance); contested under competitive pressure

**Confidence:** medium-low

**Tests:** observe whether certification/audit actually changes deployment decisions under competition

**Bears on:** C-006, C-007

## Assumption ID: A-006

**Assumption:** Intention and goal transport are inferable: modelling a system as pursuing latent objectives can compress its behaviour better than a mechanistic baseline, after paying the objective model's complexity cost.

**Used in:** Chapters 21, 22, 23, 37

**Why needed:** The compression test and transport stack presuppose that intentional structure leaves a detectable compression signature.

**Failure mode if false:** Goal preservation/laundering cannot be distinguished from mechanism; transport claims are untestable.

**Evidence:** behavioural-compression / intentional-stance modeling; counterfactual-robustness tests

**Confidence:** medium (observer-relative; gameable by adversaries)

**Tests:** measure compression gain of intentional vs. mechanistic models on adversarial and honest systems

**Bears on:** C-009

## Assumption ID: A-007

**Assumption:** Successor influence passes through an enumerable set of channels whose preservation can be specified and certified within tested tolerance.

**Used in:** Chapters 8, 28, 29, 31

**Why needed:** Successor-closure and certification require that "every channel by which influence passes to a later control system" can be identified and constrained.

**Failure mode if false:** Successors leak influence through unmodeled channels; certification gives false assurance.

**Evidence:** analogy to safety cases and conserved-quantity arguments; not yet demonstrated for self-improving systems

**Confidence:** low-medium

**Tests:** adversarial successor-creation red-teaming against the seven conserved properties

**Bears on:** C-006
