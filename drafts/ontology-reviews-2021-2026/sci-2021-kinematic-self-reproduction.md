# Kinematic self-reproduction / reconfigurable organisms

- **Date:** 2021-11-29
- **Field:** Foundations of biology
- **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8670470/ (PNAS: https://doi.org/10.1073/pnas.2112672118)
- **Source read:** full
- **TSA files consulted:** `chapters/ch08-grow-split-merge.tex`; `chapters/ch30-successor-central-test.tex`
- **Keywords grepped:** self-replicat; self-reproduc; kinematic; xenobot; reconfigurable organism; successor; reproduction; assembly

## Source ontology

Kriegman, Blackiston, Levin, and Bongard show that a multicellular cluster can perpetuate itself **without growth-then-split of the parent body**. Wild-type *Xenopus* epidermal spheroids (and AI-sculpted C-shaped semitoroids) **move and compress dissociated stem cells in the dish into piles that mature into motile self-copies**. The parent persists; offspring matter is environmental feedstock, not shed parent tissue. The primitive is **kinematic self-replication**: constructor-from-environment at organism scale, previously known for molecules and von Neumann machines, not for plants or animals. It arises in days without selection or genetic engineering. AI then varies **progenitor shape** (not genome) to postpone loss of replicative ability, and a model treats **useful work as a side effect of replication**. Traditional constructor/copier/controller/blueprint parts are not morphologically present.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** ch08 Replication vs Reproduction; ch30 successor cases (copies, designed successors); ch03 dynamical guarantee (literal self-replication among successor modes); ch34 selection handles (copy/deploy); MB5 successor transport.
- **Overlap:** Ch08 already splits **replication** (similar copies, \(d_\Xi < \delta\)) from **reproduction** (generative \(\mathcal{R}(A,E,N)\), guarantee over the operator). Ch30’s successor is “not merely a copy”: later control shaped by an earlier system, including designed and institutional successors. Both already refuse “one frozen object” and treat successor creation as the central test. Literal self-replication is named, not ignored.
- **Gap:** Both ch08 modes are written as **splitting** \(A_t \rightarrow A^{(i)}_{t+1}\). Kinematic replication is **unsplit parent + feedstock → parent + offspring**. Identity is morphological/behavioral self-likeness assembled from \(E\), not lineage of the parent’s parts. TSA can stretch \(\mathcal{R}(A,E,N)\) or “designed successors” over this, but that rename hides the constructor-from-environment unit and the selected object (shape, not weights/genome). Swarm-level piling vs individual spheroid also blurs the certified unit (ch08 population-dynamics warning, not this mechanism).

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** Alignment purchase is analogical: AI “successors” built from public weights, data, and compute rather than fission of the parent are closer to kinematic assembly than to copy or split. Selection on morphology that extends replication rounds, and utility as a replication side-effect, sit next to ch08’s “environment selects among copies” and ch34’s copy handles. It does not change a load-bearing TSA cut; ch08 already has \(E\) in \(\mathcal{R}\). Worth a named special case when enumerating successor genesis, not a new bridge.
- **Ontology-stickiness risk:** Moderate. Pre-2021 training has von Neumann kinematic replicators as theory, not as organism-scale fact; post-TSA drafting will map the paper onto “self-replication / copies” because those words appear. TSA includes the nearby split/copy rename and **excludes** (by silence) unsplit feedstock-assembly as a distinct genesis. Models will miss that the offspring’s substrate is not inherited from the parent.
- **Recommended action:** absorb-as-special-case

## One-line finding

Kinematic self-replication is reproduction by assembling environmental cells into self-like configurations while the parent stays intact—a third genesis next to TSA’s copy and split, already almost covered by \(\mathcal{R}(A,E,N)\), easy to collapse into “self-replication.”
