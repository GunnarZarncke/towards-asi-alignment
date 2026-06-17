# Extract: loop-hub-value-model.pdf

**Source PDF:** `context/loop-hub-value-model.pdf`
**Extract:** `context/extracts/loop-hub-value-model.md`
**Pages:** 5
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

From Free–Energy Loops to Human Values: Hubs as Bottlenecks
Gunnar Zarncke
AE Studio
July 2025
Abstract
Zarncke [2025] catalogued fifteen free–energy–minimising loops in the vertebrate brain. Each
loop closes a prediction–error feedback and projects into one or more neuromodulatory or salience
“hubs” that broadcast precision weights. Here we introduce the loop–hub–value (LHV) model: an
architectural proposal in which a small set of hubs transforms high–dimensional error vectors
into low–bandwidth scalars that are then read out as human value tags. We (i) formalise the

$$
two transfer steps (loop \tohub and hub \tovalue); (ii) compile an empirical mapping between
$$

hubs and intrinsic values, drawing on Zarncke [1]; and (iii) outline falsifiable predictions. Details
of agent implementation and learning dynamics will appear in Part III.
1
Motivation
Biological agents cannot transmit every prediction error upstream; long–range bandwidth is con-
strained by wiring and metabolic costs. Evolution appears to have solved this with hub bottlenecks:
mid–brain nuclei and limbic structures that compress multidimensional errors into one or two slow
neuromodulatory signals. Cortex, basal ganglia and cerebellum decode those signals as values that
steer policy selection.
2
Formal Skeleton of the LHV Model
Error compression.

$$
Each loop i produces an error vector ϵi(t) \inRdi. A hub h receives a
$$

weighted sum over incoming loops

$$
sh(t) = \sigma  X
$$

$$
i\inI(h) wih ∥ϵi(t)∥p
$$

,

$$
(1) where \sigma is a saturating non–linearity and wih are learned transfer weights. Value tagging. A cortical decoder D maps hub signals to symbolic values V = {v1, . . . , vm} via
$$

P
vk | {sh}h
 = softmaxk

$$
\betak + X
$$

h
\alphakh sh
,

$$
(2) with \alphakh contextually gated by attention and task set. 3
$$

Empirical Hub–Value Map
Table 1 lists the hubs, the principal loops that feed them, and representative intrinsic values from
Zarncke [1].
1

---

Hub
Dominant upstream loops
Example intrinsic values
Periaqueductal Gray (PAG)
Threatpain; Pavlovian threat loop
Protection, Non–suffering, Freedom
Ventral Tegmental Area (VTA)
Curiosity; Valuation regret
Learning, Diversity, Legacy
Locus Coeruleus (LC)
Precisiontiming
Achievement
Nucleus Accumbens (NAcc)
Valuationagency
Happiness
Orbitofrontal Cortex (OFC)
Policy–regret valuation
Appraisal, Hedonics
Hypothalamus
Metabolic; Steroidal timing
Longevity, Caring
HPG axis
Steroidal timing
Reputation
Insula
Metabolic; Morphological repair
Fairness, Purity
Anterior Cingulate Cortex (ACC)
Coalition entropy
Justice, Respect
Amygdala
Pavlovian threat tagging
Virtue
Septal Nuclei
Reproductive physiology
Loyalty
Superior Colliculus
Perimeter defence
Nature, Truth
Primary Visual Cortex
Scene novelty†
Beauty
Table 1: Hub–value correspondences. †The scene novelty loop is hypothesised and will be formalised
in Part III.
4
Orphaned Hubs and Candidate Loops
Although most neuromodulatory hubs receive direct input from an identified free–energy loop, three
sub-hubs in Table 1—orbitofrontal cortex (OFC), hypothalamo–pituitary–gonadal (HPG) axis, and
amygdala—currently lack a first-pass loop in the evolutionary ledger. We treat them as bottleneck
refinements: second-stage processors that reshape upstream error signals onto slower or more
specialised control channels. Below we sketch their provisional computations and outline candidate
loops to be formalised in future work.
4.1
Orbitofrontal Cortex (OFC)
The OFC integrates multi-modal evidence with predicted outcomes to compute a policy–regret
signal: the squared discrepancy
E
(Q −Q)2
between the best attainable action value Q and the executed value Q. This counterfactual loop acts
on a timescale of hundreds of milliseconds to seconds, refining valuation updates supplied by ventral
striatum and VTA.
4.2
Hypothalamo–Pituitary–Gonadal (HPG) Axis
The HPG axis implements neuroendocrine control over fertility and life-history trade-offs. We posit
a distinct steroidal timing loop that minimises a deviation term

Ssteroid −ˆS

,
where Ssteroid denotes circulating gonadal hormones and ˆS an energy- or age-adjusted set-point.
Feedback operates over hours to months, providing a slow but powerful prior on reproductive
strategy.
4.3
Amygdala
Beyond rapid nocifensive processing in the periaqueductal loop, the basolateral–central amygdala
complex assigns socio-emotional salience. We hypothesise a social appraisal loop that reduces entropy
2

---

over affective threat states,
H
threataff
,
capturing mid-latency fear conditioning and norm-violation detection.
5
Predictions

### 1. Disrupting a hub (e.g., chemogenetically) should simultaneously perturb all values anchored

to that hub, even if upstream loops remain intact.

### 2. Task contexts that enlarge ∥ϵi∥will modulate subjective value ratings in proportion to wih.

### 3. Agents endowed with an LHV bottleneck should yield more interpretable preference shifts

than agents using flat reward summation when hub weights are perturbed.
6
Related Research
6.1
Loop–Through–Hub Circuitry
Weiller et al. [2] identify a dual–loop motif in human cortex where dorsal (sequencing) and ventral
(conceptual) streams converge on frontal and posterior hubs, forming a closed circuit. Expanding this,
Weiller et al. [3] describe a meta–loop in which lateral (external) and medial (internal) dual–loops
interact via cross–hub projections, furnishing a substrate for integrating needs and demands.
Lyu et al. [4] provide causal evidence: effective–connectivity analyses reveal a recurrent loop
between dorsal and ventral precuneus subdivisions that modulates DMN and fronto–parietal networks
as tasks change. These findings validate the LHV claim that prediction–error messages funnel
through hubs before influencing global policy.
6.2
Hub–Level Precision Weighting
Predictive–coding theory posits that precision (gain) of error signals is regulated by key hubs.
Thalamic work by Kanai and Friston [5] highlights the pulvinar as a relay that encodes sensory
reliability and synchronises relevant cortices, implementing precision control. Human fMRI by
Hauser et al. [6] shows unsigned prediction–error signals in dorsal ACC and superior frontal cortex
are precision–weighted in a dopamine–dependent manner, underscoring cortical hubs in error salience
modulation.
6.3
Internal Value–External Information Integration
The salience network, centred on anterior insula and dorsal ACC, mediates switching between
internal and external modes [7]. Malfunctions yield aberrant salience attribution, reinforcing its
valuational gating role. Complementarily, fronto–striatal loops through ventral striatum and OFC
relay dopaminergic reward–prediction signals, aligning instrumental value with ongoing cognition
[8].
6.4
Error Compression Across Hierarchies
Predictive coding expects iterative suppression of redundant errors at each level. White–matter
tractography reveals structural bottlenecks where converging fibres concentrate information flow [3].
3

---

Combined with neuromodulator–driven precision control, these bottlenecks plausibly compress the
high–dimensional error space into the low–bandwidth hub scalars central to LHV.
References
[1] Gunnar Zarncke. Stratification of free–energy–minimising loops in the vertebrate brain. Com-
panion manuscript, brain-to-values research program, AE Studio, 2025.
[2] Cornelius Weiller, Jana H. Hoffmann, Lennart R. Baillet, and Arthur Johannes. Two converging
cortical processing streams constitute the dual–loop model of higher cognition. NeuroImage,
255:119190, 2022.
[3] Cornelius Weiller, Jana H. Hoffmann, and Arthur Johannes. The meta–loop: a dual–loop fusion
of lateral and medial brain networks underpins internal–external integration. Cerebral Cortex,
35(4):2112–2128, 2025.
[4] Dian Lyu, Yi Chen, Changzhen Zhang, and Jiahui Han. A causal loop within the precuneus
integrates default–mode and executive networks. Journal of Neuroscience, 41(45):9497–9511,
2021.
[5] Ryota Kanai and Karl J. Friston. A neurobiological perspective on predictive coding and
Bayesian inference. Royal Society Open Science, 2:150293, 2015.
[6] Tobias U. Hauser, Vasilisa Skvortsova, Camilla Donn, Michael Maier, and Raymond J. Dolan.
Precision–weighted prediction errors in the human dopamine system. Molecular Psychiatry,
23(3):599–608, 2018.
[7] Vinod Menon. The salience network, dopaminergic precision signals, and psychosis. Biological
Psychiatry, 93(4):e1–e12, 2023.
[8] Xiangning Li, Helen B. Everitt, and John P. O’Doherty. Mapping cortico–basal ganglia–thalamic
loops: implications for reward learning. Nature, 599(7884):351–356, 2021.
4

---

Superior Colliculus
Periaqueductal Gray
Ventral Tegmental Area
Locus Coeruleus
Nucleus Accumbens
Dorsal Raphe Nucleus
Hypothalamus
Amygdala
Anterior Cingulate Cortex
Insula
Septal Nuclei
Primary Visual Cortex
fractal visuals evoke
nature affinity
Nature
errors may spur
truth-seeking
Truth
low error states
may create unity
Spirituality
escape circuits motivate
freedom
Freedom
homeostasis underpins comfort
Non-suffering
threat response drives
defense
Protection
dopamine tags surprise
events
Learning
low discount may
foster identity
Legacy
novelty-seeking encourages variety
Diversity
norepinephrine may signal
mastery
Achievement
opioids encode basic
need fulfillment
Happiness
serotonin rewards basic
needs
Pleasure
vital sensing drives
survival value
Longevity
social bonding signals
status
Reputation
oxytocin circuits foster
nurturing
Caring
acceptance learning may
shape morality
Virtue
hierarchy detection may
inform respect
Respect
inequity distress flags
violations
Justice
inequity signals underpin
fairness
Fairness
disgust reflex grounds
purity
Purity
attachment bonds build
loyalty
Loyalty
visual symmetry triggers
beauty
Beauty
Hub-centric brain value mapping
Figure 1: Hub-centric brain–value mapping. Neuromodulatory and salience hubs (inner ring) project
intrinsic value tags (outer ring), compiled from Zarncke [1].
5
