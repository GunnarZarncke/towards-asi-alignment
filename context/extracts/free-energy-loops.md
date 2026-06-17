# Extract: free_energy_loops.pdf

**Source PDF:** `context/free_energy_loops.pdf`
**Extract:** `context/extracts/free-energy-loops.md`
**Pages:** 8
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

Stratification of Free–Energy–Minimising Loops in the Vertebrate
Brain
Gunnar Zarncke
AE Studio
July 2025
Abstract
Biological agents appear to manage a portfolio of nested optimisation loops, each minimising
a distinct variational–free–energy term. We integrate recent literature into a single ledger, order
the loops by plausible evolutionary age, and expose an internal–external symmetry: for almost
every interoceptive (“inside–the–skin”) regulator there exists an exteroceptive twin that reshapes
the niche so that the corresponding sensory statistics become predictable. The taxonomy also
offers insights into a free-energy-based model of agency and phenomenal consciousness and
informs the design of safe artificial agents.
1
Introduction
Friston’s free–energy principle [5] predicts that any self–maintaining system will evolve mechanisms
that keep its sensory surprise low. Neuroscientific work has now mapped multiple such mechanisms
onto concrete circuits including ascending reticular pathways, cortico-thalamic loops, and descending
modulatory systems: Respiratory chemoreflexes [8], metabolic homeostasis [11], threat–response
columns [25], and so on. Yet the literature is fragmented and rarely ordered developmentally. We
synthesise the evidence into an ordered free-energy ledger (Tab. 1), emphasising (i) the distinct
free–energy term each loop targets; (ii) the pairwise internal/external bifurcation; and (iii) the
evolutionary trajectory from brainstem reflexes to neocortical abstractions.
All free-energy terms are expressed in the standard variational form F = Eq[ln q −ln p], where q
represents the approximate posterior and p the generative model, with specific instantiations derived
for each biological system.
2
Methods: Criteria for Loop Inclusion
A biological circuit was counted as a loop if it satisfied three criteria: (1) it closes a sensor–to–
actuator pathway through identifiable neural tissue; (2) interference with the pathway measurably
increases some entropy term (prediction error, Gibbs free energy, chrono–mismatch, etc.); (3) at
least one peer–reviewed article describes the loop in free–energy or closely allied control–theoretic
language.
3
Results: Ordered Ledger of Loops
Table 1 sorts loops from evolutionarily oldest (brainstem, present in most vertebrates) to most
recent (default–mode network, present in humans). Each row shows the internal register, its external
1

---

twin (when identified), the free–energy term minimised, dominant brain regions, and an anchoring
citation.
4
Canonical Lexicon
Symbol
Meaning
Example loop
|pCO2 −pCO∗
2|
Chemoreflex mismatch
Brain-stem breathing

$$
|\phiSCN −\philight| Circadian phase error
$$

SCN synchrony
H(threat)
Threat entropy
PAG defence
∆Gstrain
Tissue strain FE
Immune repair
\beta ∆I
Epistemic value
Curiosity loop
5
Free-Energy Terms: Biological Interpretations
Each loop in Tab. 1 targets a distinct free-energy term, derived from the general variational form
F = Eq[ln q −ln p]. Here we provide the mathematical formulation of each term:
5.1
Respiratory Control
Fresp = 1
2\gamma
pCOart
2
−pCO∗
2
2.
The respiratory system minimizes free energy over CO2 partial pressure distributions, where q
represents the current belief about pCO2 and p the generative model based on homeostatic setpoints.
This captures metabolic prediction error in chemoreceptor signaling.
5.2
Thermoregulation
Ftemp = Eq[ln q(Tcore) −ln p(Tcore|thermal comfort)]
Hypothalamic thermoregulation minimizes free energy over core temperature distributions. The
preoptic/anterior hypothalamus acts as a thermal controller, with prediction errors driving both
autonomic responses and behavioral thermoregulation.
5.3
Vestibular Balance
Forient = Eq[ln q(r, ˙r) −ln p(r, ˙r|gravity, motion)]
Vestibular systems minimize free energy over spatial orientation and motion estimates (r, ˙r).
This enables stable balance and spatial navigation by maintaining accurate beliefs about head
position and movement in gravitational and inertial reference frames.
5.4
Ocular Saccades
Fgaze = Eq[ln q(xgaze) −ln p(xgaze|visual salience)]
Saccadic eye movements minimize free energy over gaze direction xgaze. The superior colliculus
integrates sensory predictions to direct attention toward locations of high expected information
gain, reducing visual uncertainty.
2

---

5.5
Circadian Synchronization

$$
Fcircadian = Eq[ln q(\phiSCN) −ln p(\phiSCN|\philight)]
$$

$$
The suprachiasmatic nucleus (SCN) minimizes free energy over circadian phase \phiSCN, synchro-
$$

$$
nizing internal rhythms with external light-dark cycles \philight. This captures temporal prediction
$$

error between endogenous and environmental oscillators.
5.6
Metabolic Homeostasis
Fmetabolic = Eq[ln q(glucose, hormones) −ln p(glucose, hormones|energy demand)]
Metabolic regulation minimizes free energy over glucose levels and hormonal states. This includes
both interoceptive monitoring (insulin, leptin) and exteroceptive habitat assessment for resource
prediction.
5.7
Threat Detection
Fthreat = Eq[ln q(threat state) −ln p(threat state|environmental cues)]
The periaqueductal gray (PAG) system minimizes free energy over threat state distributions.
This enables rapid defensive responses by maintaining precise beliefs about environmental dangers
and appropriate behavioral responses.
5.8
Vascular Regulation
Fvascular = Eq[ln q(blood flow) −ln p(blood flow|metabolic demand)]
Vascular control loops minimize free energy over blood flow distributions, matching perfusion
to metabolic demand. This includes both local autoregulation and central control via brainstem
vasomotor centers.
5.9
Glial Homeostasis
Fglial = Eq[ln q(synaptic strength) −ln p(synaptic strength|activity patterns)]
Glial cells minimize free energy over synaptic strength distributions, pruning connections based
on activity patterns. This maintains neural network efficiency by removing unused synapses and
supporting active ones.
5.10
Morphological Repair
Frepair = Eq[ln q(tissue state) −ln p(tissue state|structural integrity)]
Immune and repair systems minimize free energy over tissue state distributions. This includes
both cellular damage detection and coordinated repair responses to maintain bodily integrity.
5.11
Precision and Timing
Ftiming = Eq[ln q(temporal predictions) −ln p(temporal predictions|sensorimotor context)]
Cerebellar circuits minimize free energy over temporal prediction distributions, enabling precise
motor control and sensory prediction timing. This reduces uncertainty in the temporal coordination
of behavior.
3

---

5.12
Reproductive Success
Freproduction = Eq[ln q(reproductive state) −ln p(reproductive state|mate availability, resources)]
The hypothalamo-pituitary-gonadal axis minimizes free energy over reproductive state distri-
butions. This balances mating effort against resource constraints and environmental conditions,
following optimal reproductive strategies.
5.13
Behavioral Valuation
Fvaluation = Eq[ln q(action values) −ln p(action values|reward context)]
Valuation systems minimize free energy over action-value distributions. This represents the
brain’s resource allocation problem: maintaining accurate beliefs about action outcomes to guide
optimal decision-making.
5.14
Epistemic Curiosity
Fcuriosity = Eq[ln q(world model) −ln p(world model|observations)]
Curiosity-driven systems minimize free energy over world model distributions by seeking in-
formation that reduces epistemic uncertainty. This drives exploration behavior that improves
environmental understanding.
5.15
Coalition Entropy
Fcoalition = Eq[ln q(social alliances) −ln p(social alliances|group dynamics)]
Social cognitive systems minimize free energy over coalition structure distributions.
This
enables prediction of group dynamics and social relationships, supporting cooperative behavior and
reputation management.
5.16
Cross-Species Validation
The evolutionary ordering in Tab. 1 makes testable predictions about loop presence across species:
• Loops 1–7 should be detectable in most vertebrates
• Loops 8–11 should emerge in mammals with developed social structures
• Loops 12–15 should be most developed in primates and cetaceans
This cross-species approach would validate both the evolutionary timeline and the universality
of free-energy minimization as an organizing principle.
6
Internal–External Symmetry
Columns two and three of Tab. 1 show that most interoceptive regulators possess an exteroceptive
counterpart. The pairing supports the hypothesis that agents not only keep their bodies in low–
surprise states but also shape their niches to make future sensation cheap to predict.
4

---

7
Implications for Agency and Consciousness
Higher loops (rows 13–15) rely on global broadcast and metacognitive tagging. Their success
presupposes the older loops but also enables flexible agency: valuation loops turn feelings into
plans, curiosity expands state space, and coalition loops amplify collective intelligence. Conscious
experience, on this account, is the subjective correlate of information made — and kept — globally
available; agency arises once valuation and efference cascade latch onto that data.
8
Implications for Alignment of Artificial Agents
Alignment of artificial agents to human (or any) goals is an unsolved problem [19, 15, 13]. This
structure of free–energy loops sheds light onto goal formation in biological agents that can be applied
to artificial agents:

### 1. Agents manage general classes of internal and external entropy. External entropy is often

overlooked in alignment research [3, 9].

### 2. It could be possible to identify corresponding loops and free–energy terms in artificial agents

[6, 20].

### 3. It could be possible to engineer artificial agents that manage internal and external entropy in

a way that is similar to biological agents and thus implicitly align closer with human goals
[14, 18].
9
Conclusion
Ordering free–energy loops by evolutionary age reveals a scaffold ascending from brainstem reflexes
to neocortical abstractions, each adding degrees of freedom for prediction error minimisation. A
dual emphasis on internal and external entropy suggests that safe artificial agents must account for
both sides: stabilise their internal variables and avoid uncontrolled niche manipulation.
The connection to the UAD framework transforms this descriptive taxonomy into an empirical
research program. By applying Markov blanket detection to neural or LLM time-series data,
researchers can try to validate the existence of each predicted loop and measure transparency
weights between loops that emerge from loop interactions. This represents a fundamental shift to
measurable science in understanding the architecture of biological agency. Our goal is detection of
loops in artificial agents for verification of compliant agent behavior and the design of compliant
loops in artificial agents.
10
Enhanced Canonical Lexicon for Free-Energy Loops
We adopt the following canonical lexicon for specifying free-energy loops clearly and consistently
across literature:
5

---

Symbol
Meaning
Biological Interpretation
|pCO2 −pCO∗
2|
Chemoreflex mismatch
Metabolic prediction error

$$
|\phiSCN −\philight| Circadian synchronization
$$

Temporal prediction error
|ovis −ˆocontext|
Metabolic homeostasis
Visual-contextual prediction mismatch
H(threat)
Threat entropy
Uncertainty about danger states
∆Gstrain
Morphological strain
Gibbs free energy of tissue damage
\sigma2
t
Timing variance
Temporal uncertainty
−log Ndesc
Reproductive efficiency
Logarithmic reproductive utility
E[c(a)]
Behavioral valuation
Expected cost minimization
\beta∆I
Epistemic curiosity
Information gain exploration
H(Cij)
Coalition entropy
Uncertainty in alliances
This lexicon unifies existing active-inference formulations [18] and explicitly connects each
free-energy loop with biological functions.
References
[1] Dora E Angelaki and Jean Laurens. The head direction cell network: attractor dynamics
underlying integrative computation. eLife, 11:e73266, 2022.
[2] Iain J Clarke and Jeremy T Smith. Hypothalamic control of reproduction by gonadotropin-
releasing hormone: recent advances. Nature Reviews Endocrinology, 18(9):573–589, 2022.
[3] Andrew Critch and David Krueger. Ai research considerations for human existential safety
(arches). arXiv preprint arXiv:2006.04948, 2020.
[4] Marc R Freeman and David H Rowitch. Evolving concepts of gliogenesis: a look way back and
ahead to the next 25 years. Neuron, 111(3):297–311, 2023.
[5] Karl Friston. The free-energy principle: a unified brain theory? Nature Reviews Neuroscience,
11(2):127–138, 2010.
[6] Karl Friston, Thomas Parr, Conor Heins, A. Aldo Faisal, Noor Mirza, Maxwell Ramstead,
Magnus Koudahl, Beren Millidge, Alexander Tschantz, Anil Seth, and Cesare Pezzato. Designing
efe agents: The free-energy principle and active inference. arXiv preprint arXiv:2211.06719,
2022.
[7] Matthias J Gruber et al. Post-learning hippocampal dynamics promote preferential retention
of rewarding events. Neuron, 110(16):2635–2646, 2022.
[8] Patrice G Guyenet and Douglas A Bayliss. Neural control of breathing and co2 homeostasis.
Nature Reviews Neuroscience, 16(7):367–378, 2015.
[9] Evan Hubinger, Chris van Merwijk, Vladimir Mikulik, Joar Skalse, and Scott Garrabrant.
Risks from learned optimization in advanced machine learning systems.
arXiv preprint
arXiv:1906.01820, 2019.
[10] Costantino Iadecola et al. Vascular cognitive impairment and dementia: Jacc scientific statement.
Journal of the American College of Cardiology, 81(16):1617–1641, 2023.
[11] Nuria Karraza-Samper et al. Metabolic coupling in the brain: neural-glial interactions in energy
homeostasis. Nature Neuroscience, 27(3):421–433, 2024.
6

---

[12] Tamar Koren et al. Insular cortex neurons encode and retrieve specific immune responses. Cell,
184(23):6103–6116, 2021.
[13] Machine Intelligence Research Institute. Ai alignment research guide. https://intelligence.
org/research-guide/, 2024.
[14] Beren Millidge, Alexander Tschantz, and Anil Seth. Deep active inference as variational policy
gradients. Journal of Mathematical Psychology, 96:102348, 2020.
[15] Richard Ngo.
The alignment problem from a deep learning perspective.
arXiv preprint
arXiv:2209.00626, 2022.
[16] Andrew P Patton and Michael H Hastings. The suprachiasmatic nucleus. Current Biology, 33
(15):R746–R750, 2023.
[17] Laurentiu S Popa and Timothy J Ebner. Cerebellum, predictions and errors. Frontiers in
Cellular Neuroscience, 12:524, 2018.
[18] Maxwell JD Ramstead et al. Bayesian mechanics. Neural Networks, 154:592–609, 2022.
[19] Stuart Russell. Human compatible: Artificial intelligence and the problem of control. 2019.
[20] Noor Sajid, Philip Ball, Thomas Parr, and Karl Friston. Active inference: Demystified and
compared. Neural Computation, 33(3):674–712, 2021.
[21] Martin Sarter et al.
Cholinergic genetics of visual attention: human and mouse choline
transporter capacity variants and attention. Biological Psychiatry, 93(4):331–339, 2023.
[22] Johanna Scholz et al. Right temporoparietal junction contributions to theory of mind in autism:
a developmental perspective. Developmental Cognitive Neuroscience, 61:101249, 2023.
[23] Chia-Li Tan et al. Warm-sensitive neurons that control body temperature. Nature, 532(7600):
586–590, 2016.
[24] Brian J White et al. Superior colliculus encodes visual saliency before the primary visual cortex.
Proceedings of the National Academy of Sciences, 119(12):e2121642119, 2022.
[25] Haofang Zhang et al. The contribution of periaqueductal gray to pain and defensive behaviors.
Nature Reviews Neuroscience, 24(10):597–610, 2023.
7

---

Age
Internal loop
External twin
Free–energy
term
Key regions (inter-
nal / external)
Ref.
1
Respiratory control
—
FCO2
Medullary
RTN,
phrenic nucleus
[8]
2
Thermoregulation
Microclimate selec-
tion
Ftemp
Hypothalamic PO/AH
/ PAG, motor cortex
[23]
3
Vestibular balance
Spatial navigation
Forient
Vestibular nuclei / en-
torhinal cortex
[1]
4
Ocular saccades
Visual attention
Fgaze
Superior
colliculus
/
frontal eye fields
[24]
5
Circadian synchro-
nization
Environmental
rhythm
synchro-
nization
Fcircadian
Suprachiasmatic
nu-
cleus (SCN) / retina,
pineal gland
[16]
6
Metabolic
home-
ostasis
Habitat–fit
(scene
preference)
Fmetabolic
Insula, hypothalamus /
PPA, retrosplenial
[11]
7
Threat
/
pain
(PAG)
Perimeter defence
Fthreat
Periaqueductal
gray,
amygdala / superior
colliculus
[25]
8
Vascular regulation
Resource
distribu-
tion
Fvascular
Brainstem vasomotor /
autonomic cortex
[10]
9
Glial homeostasis
Synaptic pruning
Fglial
Astrocytes, microglia /
PFC, hippocampus
[4]
10
Morphological
repair
Niche construction
Frepair
Insula, immune cortex
/ PPC, premotor
[12]
11
Precision / timing
Social/circadian
rhythm sync
Ftiming
Cerebellar cortex, infe-
rior olive / SCN
[17]
12
Reproductive physi-
ology
Cultural/memetic
reproduction
Freproduction
HPG axis,
BNST /
TPJ, Broca area
[2]
13
Valuation / agency
Resource foraging
Fvaluation
Ventral striatum, OFC
/ dlPFC, hippocampus
[21]
14
Curiosity
(epis-
temic)
Scientific
explo-
ration
Fcuriosity
Hippocampus, VTA /
frontoparietal
search
nets
[7]
15
Coalition entropy
Institutional reputa-
tion
Fcoalition
TPJ, mPFC / linguistic
cortex
[22]
Table 1: Free–energy loops ordered by evolutionary age (leftmost column). Dashes denote loops
with no clear exteroceptive twin. In the Key regions column, “/” separates internal loop regions
(left) from external loop regions (right). Abbreviations: Ref. = representative reference; RTN =
retrotrapezoid nucleus; PO/AH = preoptic/anterior hypothalamus; SCN = suprachiasmatic nucleus;
PPA = parahippocampal place area; PAG = periaqueductal gray; PFC = prefrontal cortex; PPC
= posterior parietal cortex; HPG = hypothalamo-pituitary-gonadal; BNST = bed nucleus of stria
terminalis; TPJ = temporoparietal junction; OFC = orbitofrontal cortex; dlPFC = dorsolateral
prefrontal cortex; VTA = ventral tegmental area; mPFC = medial prefrontal cortex.
8
