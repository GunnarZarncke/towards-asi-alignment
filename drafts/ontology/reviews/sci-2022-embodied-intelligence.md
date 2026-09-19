# Embodied/material intelligence

- **Date:** 2022-08-02
- **Field:** Engineering / robotics
- **Source:** https://www.nature.com/articles/s42254-022-00481-z
- **Source read:** abstract-only
- **TSA files consulted:** `chapters/ch07-finding-boundary.tex`, `chapters/ch12-boundary-expansion.tex`
- **Keywords grepped:** embodied; embodiment; morphology; morphological; material intelligence; soft robot; boundary; embedded; controller; physical body

## Source ontology

Mengaldo et al. (*Nat. Rev. Phys.* 2022) recarve **embodied intelligence** as a modelling object for soft robotics: “part of control and intelligence contributed by the physical body and its interaction with the environment and the task.” Body compliance is not a nuisance around a software controller; it is a control resource. The intended replacement is a fully coupled robot–environment physics description (internal actuation plus fluid/solid contact) that can support design, control, and digital twins—rather than a Cartesian split of controller code versus rigid plant. Status B: Pfeifer/Lungarella/Iida (2007) and Blickhan et al. (“intelligence by mechanics,” 2007) already had the ingredients; this paper operationalizes them as a modelling programme.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** boundary discovery / Claim 1 (ch07); boundary expansion as coupled-system capability (ch12); composite agent (ch09); MB1 / embedded agency (`appendices/appB-bridge-crosswalk.tex`); robotic grounding (ch03)
- **Overlap:** TSA already refuses a free agent/environment cut. ch07 treats the agent as a bounded dynamical process whose control locus need not be the named model; ch12 restates extended-mind / embedded-cognition and treats capability as how much of the world enters sensory–predictive–active loops, including robotic actuators as action channels. An ε-boundary over \(I,S,A,E\) could in principle include mechanical state.
- **Gap:** TSA’s composites are socio-technical (model + tools + memory + users + incentives). Robots in ch12 are affordances the software loop acquires, not co-equal computational substrates. ch07 explicitly does not require a body. TSA has no primitive that splits **controller software / body morphology / environment mechanics** as three loci of computation. Calling morphological computation “just a larger boundary” renames a software-centric cut; in the source, control was never localized in the controller.

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** For physical/robotic deployments, aligning the named controller while morphology and contact mechanics do the work is a Claim-1 boundary error. That is a useful instance, not a new alignment state variable. The paper’s load-bearing objects are FEM, fluid–structure interaction, and digital twins—orthogonal to CCI, value-bundle transport, and successor stability. Abstract-only read; score conservatively. A morphological-computation chapter would not change TSA’s cuts.
- **Ontology-stickiness risk:** Moderate. Training data maps “embodied AI” to robots-with-sensors or Clark-style extended mind, which TSA already has (ch12). An LLM will report “TSA already covers this” via boundary expansion and miss that TSA never treats passive material mechanics as the controller. The 2022 recarving (material as part of the controller; coupled physics as the intelligence description) is easy to flatten into “embodiment = having a body.”
- **Recommended action:** cite-in-crosswalk

## One-line finding

Soft-robot embodied intelligence relocates control into morphology and environment coupling, a physical instance of TSA’s boundary problem that TSA currently expresses only as software/institutional composites and robotic actuators.
