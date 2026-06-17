# Extract: lhcv-model-v2.pdf

**Source PDF:** `context/lhcv-model-v2.pdf`
**Extract:** `context/extracts/lhcv-model-v2.md`
**Pages:** 6
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

From Free-Energy Loops in the Brain to Human Values
Gunnar Zarncke, aintelope
May 20, 2026
Abstract
Zarncke [8] catalogues fifteen free-energy-minimising loops in the vertebrate brain, ordered
by evolutionary age in a companion ledger. Each loop closes a prediction-error feedback and
projects into one or more neuromodulatory or salience “hubs” that broadcast precision weights.
Here we introduce a loop-hub-control-value (LHCV) model: an architectural proposal in which a
small set of hubs transforms high-dimensional error vectors into low-bandwidth scalars, which
function as control relevance proxies and are read out, through development and context, as

$$
human value tags. We (i) formalise three transfer steps, loop \tohub, hub \tocontrol relevance
$$

proxy, and control relevance proxy 99K value readout; (ii) compile an empirical mapping between
hubs, control relevance proxies, and typical value readouts, drawing on the stratified ledger; and
(iii) outline falsifiable predictions.
1
Architecture
Biological agents cannot transmit every prediction error upstream; long-range bandwidth is con-
strained by wiring and metabolic costs. Evolution addresses this with hub bottlenecks: mid-brain
nuclei and limbic structures that compress high-dimensional loop errors into slow neuromodulatory
scalars. The upstream loop inventory follows the stratified free-energy ledger of Zarncke [8]; LHCV
specifies how those loop errors are bottlenecked, control-relevant, and eventually read out as values.
In the loop–hub–control–value (LHCV) model, those scalars serve two roles at different timescales.
Immediately, they act as control relevance proxies that steer policy—modulating attention, precision,
learning rate, exploration, inhibition, and action priors. Developmentally, overlapping proxy histories
are decoded—via language, social feedback, memory, and self-model—into stabilized human value
readouts.
The architecture is a four-stage pipeline:

$$
L \toH \toC 99K V, where L denotes free-energy loops, H denotes hub bottlenecks, C denotes control relevance proxies,
$$

and V denotes learned value readouts. The dashed arrow marks contextual mediation, not a direct
anatomical projection.
2
Formal Skeleton of the LHCV Model
We now instantiate each step.
Error compression. Each loop i in the stratified ledger [8] produces an error vector ϵi(t) \inRdi.
A hub h receives a weighted sum over incoming loops

$$
sh(t) = \sigma 
$$

X

$$
i\inI(h) wih∥ϵi(t)∥p
$$


,
(1) 1

---

Free-energy
loops
Hub
bottlenecks
Control relevance
proxies
Value
readouts
The dashed step is mediated by envi-
ronment, development, social feedback,
language, memory, and self-modeling.
Figure 1: The LHCV pipeline: free-energy loops compress through hub bottlenecks into control
relevance proxies, which are read out as human values under developmental and environmental
mediation.
where \sigma is a saturating non-linearity and wih are learned transfer weights.
Control relevance proxies. Hub scalars map to control relevance proxies,
ch(t) = gh
sh(t), zt, at
,
(2) where zt is the current learned state and at denotes the current action context. A control relevance
proxy is a compressed signal about where control is needed, valuable, or failing: threat, damage,
uncertainty, metabolic deficit, social exclusion, caregiver need, opportunity, or policy regret. These
proxies can modulate attention, precision, memory writing, exploration, inhibition, learning rate,
and action priors.
One simple policy-level readout is

$$
\pi(at | zt, ct) ∝exp
$$

$$
Q\theta(zt, at) + X
$$

h

$$
\lambdahch(t) \phih(zt, at) !
$$

,

$$
(3) where \phih selects the action features affected by proxy h and \lambdah controls the strength of the
$$

corresponding policy bias.
Value readout. A cortical and social decoder D maps hub-shaped control histories into
symbolic values V = {v1, . . . , vm} via
P (vk | {ch}h, et) = softmaxk

$$
\betak + X
$$

h

$$
\alphakh(et)ch !
$$

,

$$
(4) where et summarizes the environment-mediated developmental context: learned concepts, social feedback, language, memory, and self-modeling. The coefficients \alphakh are contextually gated by
$$

attention and task set. This is the formal location of the dashed C 99K V step.
Interpretive note. The LHCV model therefore does not claim that “PAG represents protection”
or “ACC represents justice.” It claims that nocifensive, conflict, salience, and precision signals make
protection-like, justice-like, care-like, and truth-like abstractions easier to learn and stabilize in
ordinary developmental environments.
3
Empirical Hub-Control-Value Map
Table 1 lists the hubs, the principal loops that feed them, the primary control relevance proxies,
and typical downstream value readouts. The table should be read as a hypothesis generator. The
value column is downstream and mediated; the control relevance proxy column is the more direct
biological claim.
2

---

Hub
Dominant
upstream
loops
Primary control relevance
proxy
Typical value readouts
Periaqueductal
Gray
(PAG)
Threat-pain;
Pavlovian
threat loop
Nocifensive urgency, defensive
inhibition, protection pressure
Protection, non-suffering, bodily
safety
Ventral Tegmental Area
(VTA)
Curiosity;
valuation re-
gret
Exploration, novelty,
reward-prediction update
Learning, curiosity, discovery,
diversity
Locus Coeruleus (LC)
Precision-timing
Arousal, uncertainty, precision,
task urgency
Achievement, vigilance,
responsibility
Nucleus
Accumbens
(NAcc)
Valuation-agency
Approach, appetitive salience,
agency-contingent reward
Happiness, motivation, agency
Orbitofrontal
Cortex
(OFC)
Policy-regret valuation
Counterfactual value, regret,
expected outcome
Appraisal, prudence, hedonics
Hypothalamus
Metabolic; steroidal tim-
ing
Metabolic, thermoregulatory,
and caregiving regulation
Longevity, care, nurturance
HPG axis
Steroidal timing
Reproductive timing, mating
effort, status-sensitive endocrine
allocation
Reputation, mating, life-history
strategy
Insula
Metabolic; morphological
repair
Interoceptive error, disgust,
boundary salience
Purity, fairness, self-protection
Anterior Cingulate Cor-
tex (ACC)
Coalition entropy
Conflict, effort, social pain,
coalition error
Justice, respect, duty
Amygdala
Pavlovian threat tagging
Affective threat, social salience,
fear conditioning
Danger, trust, virtue/vice tags
Septal Nuclei
Reproductive physiology
Bonding, affiliative reward,
social soothing
Loyalty, affiliation
Superior Colliculus
Perimeter defence
Orienting, vigilance, defensive
spatial prioritization
Situational awareness, nature,
truth-like orientation
Primary Visual Cortex
Habitat-fit
(scene
preference)†
Scene novelty, aesthetic salience,
perceptual compression gain
Beauty
Table 1: Hub-control-value correspondences.
†External twin of metabolic homeostasis in the
stratified ledger [8]. Value readouts are not claimed to be directly represented in hubs; they are
learned downstream from control relevance proxies under environmental and social mediation.
4
Orphaned Hubs and Candidate Loops
Although most neuromodulatory hubs receive direct input from an identified free-energy loop in the
stratified ledger [8], three sub-hubs in Table 1–orbitofrontal cortex (OFC), hypothalamo-pituitary-
gonadal (HPG) axis, and amygdala–lack a dedicated first-pass hub projection in the present map.
We treat them as bottleneck refinements: second-stage processors that reshape upstream error
signals onto slower or more specialised control relevance proxies. Below we sketch their provisional
computations and outline candidate loops formalised in 8.
4.1
Orbitofrontal Cortex (OFC)
The OFC integrates multi-modal evidence with predicted outcomes to compute a policy-regret
signal: the squared discrepancy
E
h
(Q⋆−Q)2i
between the best attainable action value Q⋆and the executed value Q. This counterfactual loop
acts on a timescale of hundreds of milliseconds to seconds, refining valuation updates supplied by
ventral striatum and VTA.
3

---

4.2
Hypothalamo-Pituitary-Gonadal (HPG) Axis
The HPG axis implements neuroendocrine control over fertility and life-history trade-offs. We posit
a distinct steroidal timing loop that minimises a deviation term

Ssteroid −ˆS

,
where Ssteroid denotes circulating gonadal hormones and ˆS an energy- or age-adjusted set-point.
Feedback operates over hours to months, providing a slow but powerful prior on reproductive
strategy.
4.3
Amygdala
Beyond rapid nocifensive processing in the periaqueductal loop, the basolateral-central amygdala
complex assigns socio-emotional salience. We hypothesise a social appraisal loop that reduces
entropy over affective threat states,
H (threataff) ,
capturing mid-latency fear conditioning and norm-violation detection.
5
Predictions
Because control and value occupy different layers, LHCV yields distinct falsifiers for each:

### 1. Disrupting a hub should first perturb salience, attention, action priors, learning rates, inhibition

patterns, and exploration tendencies. Value reports should shift downstream when the relevant
learned value concepts depend on those control relevance proxies.

### 2. Task contexts that enlarge ∥ϵi∥will modulate control relevance proxies in proportion to wih, and

will modulate subjective value ratings only where the corresponding value decoder depends on
those proxies.

### 3. Agents endowed with an LHCV bottleneck should yield more interpretable policy and preference

shifts than agents using flat reward summation when hub or proxy weights are perturbed.

### 4. The H→C effect should be more anatomically immediate and cross-context stable than the

C99KV effect. Developmental history, language, and social environment should explain substantial
variance in the value readout from the same control relevance proxy.
6
Related Research
6.1
Loop-Through-Hub Circuitry
Weiller et al. [6] identify a dual-loop motif in human cortex where dorsal (sequencing) and ventral
(conceptual) streams converge on frontal and posterior hubs, forming a closed circuit. Expanding this,
Weiller et al. [7] describe a meta-loop in which lateral (external) and medial (internal) dual-loops
interact via cross-hub projections, furnishing a substrate for integrating needs and demands.
Lyu et al. [4] provide causal evidence: effective-connectivity analyses reveal a recurrent loop
between dorsal and ventral precuneus subdivisions that modulates DMN and fronto-parietal networks
as tasks change. These findings validate the LHCV claim that prediction-error messages funnel
through hubs before influencing global policy.
4

---

6.2
Hub-Level Precision Weighting
Predictive-coding theory posits that precision (gain) of error signals is regulated by key hubs.
Thalamic work by Kanai and Friston [2] highlights the pulvinar as a relay that encodes sensory
reliability and synchronises relevant cortices, implementing precision control. Human fMRI by
Hauser et al. [1] shows unsigned prediction-error signals in dorsal ACC and superior frontal cortex
are precision-weighted in a dopamine-dependent manner, underscoring cortical hubs in error salience
modulation.
6.3
Internal Control-External Information Integration
The salience network, centred on anterior insula and dorsal ACC, mediates switching between
internal and external modes [5]. Malfunctions yield aberrant salience attribution, reinforcing its
control-allocation role. Complementarily, fronto-striatal loops through ventral striatum and OFC
relay dopaminergic reward-prediction signals, aligning instrumental control with ongoing cognition
[3].
6.4
Error Compression Across Hierarchies
Predictive coding expects iterative suppression of redundant errors at each level. White-matter
tractography reveals structural bottlenecks where converging fibres concentrate information flow [7].
Combined with neuromodulator-driven precision control, these bottlenecks plausibly compress the
high-dimensional error space into the low-bandwidth hub scalars central to LHCV.
References
[1] Tobias U. Hauser, Vasilisa Skvortsova, Camilla Donn, Michael Maier, and Raymond J. Dolan.
Precision-weighted prediction errors in the human dopamine system. Molecular Psychiatry, 23
(3):599–608, 2018.
[2] Ryota Kanai and Karl J. Friston. A neurobiological perspective on predictive coding and
Bayesian inference. Royal Society Open Science, 2:150293, 2015.
[3] Xiangning Li, Helen B. Everitt, and John P. O’Doherty. Mapping cortico-basal ganglia-thalamic
loops: implications for reward learning. Nature, 599(7884):351–356, 2021.
[4] Dian Lyu, Yi Chen, Changzhen Zhang, and Jiahui Han. A causal loop within the precuneus
integrates default-mode and executive networks. Journal of Neuroscience, 41(45):9497–9511,
2021.
[5] Vinod Menon. The salience network, dopaminergic precision signals, and psychosis. Biological
Psychiatry, 93(4):e1–e12, 2023.
[6] Cornelius Weiller, Jana H. Hoffmann, Lennart R. Baillet, and Arthur Johannes. Two converging
cortical processing streams constitute the dual-loop model of higher cognition. NeuroImage, 255:
119190, 2022.
[7] Cornelius Weiller, Jana H. Hoffmann, and Arthur Johannes. The meta-loop: a dual-loop fusion
of lateral and medial brain networks underpins internal-external integration. Cerebral Cortex,
35(4):2112–2128, 2025.
5

---

[8] Gunnar Zarncke. Stratification of Free–Energy–Minimising loops in the vertebrate brain. Com-
panion manuscript, brain-to-values research program, 2025. AE Studio.
6
