# Anthrobots / biobots

- **Date:** 2023-11-30 (Adv. Sci. 2024;11(4):2303575)
- **Field:** Biology / engineering
- **Source:** https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202303575 (PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC10811512/)
- **Source read:** full
- **TSA files consulted:** `chapters/ch08-grow-split-merge.tex`; `chapters/ch09-composite-agent.tex`
- **Keywords grepped:** organism; self-assembl; biobot; xenobot; morphogenes; body plan; Levin; living entit

## Source ontology

Gumuskaya et al. introduce **Anthrobots**: motile, fully biological, self-constructing multicellular entities grown from a single adult human bronchial epithelial cell, without genomic editing, scaffolds, or manual sculpting. The load-bearing primitive is a **living construct in the latent morphospace of a wild-type genome**—not an organism (species-typical body plan), not an organoid (native-tissue recapitulation), and not a biohybrid robot. Adult somatic cells that spent decades as flat tracheal epithelium implement novel anatomies (polarized vs wholly ciliated; spherical vs ellipsoidal) and discrete motility types (circular, linear, curvilinear, eclectic) whose form–function mapping is statistically tight; fused “superbots” induce neural-scratch repair that is not inferable from tracheal default roles. This breaks **organism ≈ naturally evolved / genomically specified body plan**, and generalizes Xenobots (sculpted amphibian embryos) to self-assembled adult human cells.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** composite agent from non-agent parts and skin-as-organism heuristic (ch09); identity as transport across growth/split/reproduction rather than organism continuity (ch08); ε-boundary / wrong-object (ch07, ch01); successor as generative process (ch08); bearer “biological organism” (ch18, unread beyond grep). No xenobot/anthrobot/Levin/morphogenesis/body-plan hits in manuscript, App. B, field-agendas, or `metadata/concepts/`.
- **Overlap:** TSA already refuses to identify the alignment object with a labeled artifact or with material/organism continuity. Ch09’s thesis—an agent can be a dynamically coherent cluster whose parts need not themselves be agents—covers “tracheal cells jointly constitute a new bounded motile process.” Ch08 treats “organism continuity” as one identity criterion among others, and reproduction as an operator that can yield a new system rather than a copy.
- **Gap:** TSA’s biological examples still use **organism** as the familiar skin-bounded default. They do not name the morphogenetic split the paper operationalizes: same wild-type genome and cell type, novel living entity, discrete morphospace attractors, unexpected competence. “Composite” locates an optimizer across named artifacts; it does not say that a genome fails to uniquely specify a body plan, or that organoid ≠ biobot.

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** Real ontology, thin direct purchase on Claims 1–6. Useful as an empirical illustration that default labels (human, tracheal, organism) underdetermine the actual bounded process, and that successor-like construction can occur by microenvironment rather than genetic rewrite. Absorbing it into ch09/ch08 fails the hostile test: restating Anthrobots as “composite agency” or “identity transport” erases the body-plan non-uniqueness claim. Not a rival alignment decomposition; not missing a load-bearing TSA cut. Cite next to ch08–ch09 (and, if a biology row is added, beside TAME / kinematic self-reproduction) rather than rewriting those chapters.
- **Ontology-stickiness risk:** High for models trained on “organism = evolved body plan / genome.” TSA includes a nearby rename (composite / non-stationary identity) that will suck the source into ch09/ch08 without seeing morphogenetic latent space. Pre-2023 training also treats Xenobots as a frog-embryo curiosity; the adult-human self-construction result is easy to miss. TSA currently excludes this primitive by silence, not by argument.
- **Recommended action:** cite-in-crosswalk

## One-line finding

Anthrobots split wild-type human cells from species-typical organisms, yielding a self-assembled motile living construct TSA can cite as a composite/identity illustration but does not currently treat as a morphogenetic primitive.
