# Extract: uad_literature_review.pdf

**Source PDF:** `context/uad_literature_review.pdf`
**Extract:** `context/extracts/uad-literature-review.md`
**Pages:** 7
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

Prior and Related Work on Unsupervised Agent Discovery
Gunnar Zarncke (aintelope)
May 2026
1
Framing the Problem
Unsupervised Agent Discovery (UAD) sits at the intersection of several literatures that have
mostly developed separately: formal definitions of agency, Markov blankets and active inference,
information-theoretic autonomy, biological individuality, inverse reinforcement learning, predictive-
state modeling, object-centric representation learning, and multi-agent interaction analysis. Its
distinctive ambition is not merely to score an already given system as more or less agentic, nor
to infer a reward function for an already given agent, but to infer from raw or weakly structured
dynamical data which subsystems should count as agents, where their boundaries lie, what internal
variables carry memory, what objective-like regularities govern behavior, and how subsystems model
or influence one another [30].
This scope is broader than most existing approaches. Classical reinforcement learning and
inverse reinforcement learning usually assume an agent, state space, action space, and reward-feature
ontology [3, 22, 31]. Active-inference and Markov-blanket approaches supply powerful language for
organism-environment separation, but often begin with a system boundary already specified or with
strong assumptions about stationarity and conditional independence [10, 15, 24]. Object-centric
learning discovers entities, but entities are not necessarily agents [14, 21]. Multi-agent trajectory
analysis detects interaction, but influence is not the same as goal-directed agency [4, 20, 26].
2
Formal Agency and Interpretation
One line of work defines when a system should be interpreted as an agent. Dennett’s intentional
stance gives the classical philosophical starting point: a system is treated as an agent when ascribing
beliefs and desires improves prediction [9]. Orseau, McGill, and Legg formalize a related distinction
between agents and devices by comparing behavioral hypotheses [23]. Their framework gives a
relative probabilistic notion of agency, but it does not solve the UAD problem because the behavioral
interface and candidate system are already given.
Biehl and Virgo provide a closer formal bridge by asking under what conditions a physical
system can be interpreted as solving a POMDP [7]. Their interpretation map from physical states
to belief states, coupled to an optimality condition over actions and rewards, is directly relevant
to UAD’s goal-inference layer. The limitation is scope: this asks whether a given system can be
1

---

interpreted as an agent, while UAD asks how to discover the candidate system and boundary in the
first place.
Kenton et al.’s causal treatment of agency is one of the closest direct predecessors [13]. It proposes
an algorithmic route to agent discovery from data by testing policy sensitivity to interventions
that alter action consequences. This moves beyond interpretation toward discovery, but it does not
provide a full raw-trace pipeline for boundary, memory, latent goal, and inter-agent model discovery
in one integrated system.
3
Markov Blankets, Active Inference, and Boundary Discovery
The Markov-blanket literature supplies a natural mathematical substrate for UAD’s boundary-
discovery step. In Bayesian networks, a Markov blanket separates a variable set from the rest
of the graph. In active inference and Free Energy Principle work, Markov blankets formalize
organism-environment separation by asserting conditional independence of internal and external
states given sensory and active states [8, 10, 15, 24].
This body of work is foundational for UAD because it links boundary, inference, action, and
self-organization. However, many FEP applications assume the boundary, whereas UAD treats it
as an inference target. A second issue is exactness: real systems rarely exhibit perfect blankets.
Approximate blankets are more realistic, especially for hierarchical and social systems with porous
boundaries.
Recent work on dynamic Markov blanket detection for macroscopic objects is close to the UAD
boundary problem [5]. These approaches infer object-like macrovariables and boundary variables
from microdynamics. However, object discovery is not yet agent discovery: an object may be
dynamically coherent without memory, policy, control channels, or objective-like behavior.
4
Information-Theoretic Agency and Autonomy
Another major literature defines agency-like properties via information-theoretic quantities. Em-
powerment captures potential control from actions to future sensations [16]. Predictive information
captures temporal structure and modelability [6]. Transfer entropy and Granger causality quantify
directed dependence [4, 26]. Related work on semantic information and integrated information
addresses meaningful organization and system-level integration [1, 17].
These tools map naturally onto UAD components. Boundary discovery uses conditional inde-
pendence or conditional mutual information; memory discovery uses lagged predictive information;
control uses action-to-environment information flow; and inter-agent modeling uses cross-predictive
structure in internal variables. The B-IQ proposal combines predictive information, control informa-
tion, memory cost, and residual surprise into one competence measure [29].
The caution is over-interpretation. Directed influence is not agency by itself [20]. UAD therefore
needs a composite criterion over boundary, memory, action, and objective-like regularity rather than
2

---

any single information-theoretic statistic.
5
Biological Individuality and Autopoiesis
Biological individuality work is relevant because organisms are paradigmatic agents with boundaries
that are neither arbitrary nor always sharp.
The information theory of individuality frames
individuals as dynamically coherent units with informational closure and persistence across scales
[18]. This helps avoid a simplistic skin-boundary model and supports multiscale agency analysis.
The limitation is algorithmic: much of this literature is conceptual, evolutionary, or comparative
rather than a direct inference pipeline from raw time series to discovered boundaries, memories, and
goals.
6
Predictive State Representations and Memory Discovery
UAD’s memory-localization step connects strongly to predictive state representations and compu-
tational mechanics. PSRs define state through predictions over future observations rather than
hidden ontological variables [19]. Computational mechanics defines causal states as equivalence
classes of histories with identical predictive consequences [27].
This aligns with UAD’s view that memory variables should carry unique predictive information
about future dynamics conditional on boundary variables. The remaining gap is that PSR and
causal-state methods recover predictive structure of a process, not necessarily agentic structure with
explicit action boundary, control channel, and objective-like dynamics.
7
Goal Inference, IRL, and Ontology Import
Inverse reinforcement learning is the obvious precursor for UAD’s goal-inference layer. Classical IRL
asks which reward would render observed behavior approximately optimal [22]; maximum-entropy
IRL provides a stochastic generalization that avoids assuming perfect optimality [31]; and modern
surveys catalog extensions and open limits [3].
The main UAD challenge is ontology import. Standard IRL assumes an agent, state space,
action space, and feature representation. UAD instead treats part of this ontology as latent: which
variables count as internal state, sensory input, action, and objective-relevant outcomes is itself
inferred.
8
Object-Centric and Agent-Centric Representation Learning
Object-centric learning is relevant because agent discovery from raw observations often starts with
entity discovery. Slot Attention and related structured world-model approaches provide practical
decomposition of high-dimensional observations into persistent factors [11, 14, 21].
3

---

However, object-centric learning usually stops short of agency. It can separate entities without
identifying controlled actors, policy structure, memory variables, or objective-like dynamics. Newer
agent-centric approaches such as Variational Agent Discovery move closer to UAD’s empirical setting
but still do not supply a full boundary-memory-goal-interaction stack [2].
9
Multi-Agent Interaction and Social Structure Discovery
Multi-agent systems research contributes tools for interaction, coordination, communication, and
role analysis. Directed-information methods identify influence [4, 20, 26]. Multi-agent IRL and
trajectory models handle interacting decision-makers, but usually with prespecified agents and
interfaces [3].
UAD’s inter-agent modeling criterion is stricter: whether memory-like internal variables in one
discovered subsystem predict another subsystem’s actions, conditional on local sensory and active
states. This shifts from interaction detection to inferred internal modeling.
Related cooperation literatures are relevant but assume predefined agents [12, 28]. UAD-style
cooperation analysis instead treats agent identity and coupling structure as inferred objects.
10
Synthesis: Where UAD Appears Novel
Prior work contains many pieces of UAD but usually not one integrated inference pipeline. Formal
agency work clarifies interpretability [7, 9, 23]. Markov-blanket and active-inference work clarifies
boundary dynamics [8, 10, 15, 24]. Information theory quantifies control, prediction, and influence
[6, 16, 26]. IRL handles reward inference [22, 31]. PSR and computational mechanics recover
predictive state [19, 27]. Representation learning supports raw perceptual decomposition [11, 14, 21].
The novel claim of UAD is the integration: discover boundary, then memory, then objective-like
regularities, then inter-agent modeling and cooperation, from raw or weakly structured traces
[29, 30]. The strongest near-neighbors each solve only part of this stack [5, 7, 13, 25].
References
[1] Larissa Albantakis, Luis S. Barbosa, Graham Findlay, Mattia Grasso, Andrew M. Haun,
William Marshall, William G. P. Mayner, and Giulio Tononi. Integrated information theory 4.0:
Formulating the properties of phenomenal existence in physical terms. PLOS Computational
Biology, 19(3):e1011465, 2023. doi: 10.1371/journal.pcbi.1011465.
[2] Anonymous. Variational agent discovery. OpenReview submission, 2025.
[3] Saurabh Arora and Prashant Doshi. A survey of inverse reinforcement learning: Challenges,
methods and progress. Artificial Intelligence, 297:103500, 2021. doi: 10.1016/j.artint.2021.
103500.
4

---

[4] Lionel Barnett, Adam B. Barrett, and Anil K. Seth. Granger causality and transfer entropy
are equivalent for gaussian variables. Physical Review Letters, 103(23):238701, 2009. doi:
10.1103/PhysRevLett.103.238701.
[5] Jacob Beck and Maxwell J. D. Ramstead. Dynamic markov blanket detection, 2025.
[6] William Bialek, Ilya Nemenman, and Naftali Tishby. Predictability, complexity, and learning.
Neural Computation, 13(11):2409–2463, 2001. doi: 10.1162/089976601753195969.
[7] Max Biehl and Nathaniel Virgo. Interpreting systems as solving POMDPs: A step towards a
formal understanding of agency, 2022.
[8] Lancelot Da Costa, Karl Friston, Conor Heins, and Grigorios A. Pavliotis. Bayesian mechanics
for stationary processes, 2021.
[9] Daniel C. Dennett. True believers: The intentional strategy and why it works. In A. F.
Heath, editor, Scientific Explanation: Papers Based on Herbert Spencer Lectures, pages 53–75.
Clarendon Press, Oxford, 1981.
[10] Karl Friston. The free-energy principle: A unified brain theory? Nature Reviews Neuroscience,
11(2):127–138, 2010. doi: 10.1038/nrn2787.
[11] Anirudh Goyal, Alex Lamb, Jordan Hoffmann, Shagun Sodhani, Sergey Levine, Yoshua Bengio,
and Bernhard Schölkopf. Recurrent independent mechanisms. In International Conference on
Learning Representations, 2021.
[12] W. D. Hamilton. The genetical evolution of social behaviour. Journal of Theoretical Biology, 7
(1):1–16, 1964. doi: 10.1016/0022-5193(64)90038-4.
[13] Zachary Kenton, Rohin Kumar, Sebastian Farquhar, Jonathan Richens, Matt MacDermott,
and Tom Everitt. Discovering agents, 2022.
[14] Thomas Kipf, Elise van der Pol, and Max Welling. Contrastive learning of structured world
models. In International Conference on Learning Representations, 2020.
[15] Michael D. Kirchhoff, Thomas Parr, Ester Palacios, Karl Friston, and Julian Kiverstein. The
markov blankets of life: Autonomy, active inference and the free energy principle. Journal of
the Royal Society Interface, 15(138):20170792, 2018. doi: 10.1098/rsif.2017.0792.
[16] Alexander S. Klyubin, Daniel Polani, and Chrystopher L. Nehaniv. Empowerment: A universal
agent-centric measure of control.
In Proceedings of the IEEE Congress on Evolutionary
Computation, pages 128–135, 2005. doi: 10.1109/CEC.2005.1554676.
[17] Artemy Kolchinsky and David H. Wolpert. Semantic information, autonomous agency and non-
equilibrium statistical physics. Interface Focus, 8(6):20180041, 2018. doi: 10.1098/rsfs.2018.0041.
5

---

[18] David C. Krakauer, Nils Bertschinger, Eckehard Olbrich, Jessica C. Flack, and Nihat Ay.
The information theory of individuality. Theory in Biosciences, 139(2):209–223, 2020. doi:
10.1007/s12064-020-00313-7.
[19] Michael L. Littman, Richard S. Sutton, and Satinder Singh. Predictive representations of state.
In Advances in Neural Information Processing Systems 14, pages 1555–1561, 2001.
[20] Joseph T. Lizier and Mikhail Prokopenko. Differentiating information transfer and causal effect.
European Physical Journal B, 73(4):605–615, 2010. doi: 10.1140/epjb/e2010-00034-5.
[21] Francesco Locatello, Dirk Weissenborn, Thomas Unterthiner, Aravindh Mahendran, Georg
Heigold, Jakob Uszkoreit, Alexey Dosovitskiy, and Thomas Kipf. Object-centric learning with
slot attention. In Advances in Neural Information Processing Systems 33, 2020.
[22] Andrew Y. Ng and Stuart J. Russell.
Algorithms for inverse reinforcement learning.
In
Proceedings of the Seventeenth International Conference on Machine Learning, pages 663–670,
2000.
[23] Laurent Orseau, Stephen M. McGill, and Shane Legg. Agents and devices: A relative definition
of agency, 2018.
[24] Thomas Parr, Lancelot Da Costa, and Karl Friston. Markov blankets, information geometry
and stochastic thermodynamics. Philosophical Transactions of the Royal Society A, 378(2164):
20190159, 2020. doi: 10.1098/rsta.2019.0159.
[25] Fernando E. Rosas, Pedro A. M. Mediano, Henrik J. Jensen, Anil K. Seth, Adam B. Barrett,
Robin L. Carhart-Harris, and Daniel Bor. Reconciling emergence: An information-theoretic
approach to identify causal emergence in multivariate data. PLOS Computational Biology, 16
(12):e1008289, 2020. doi: 10.1371/journal.pcbi.1008289.
[26] Thomas Schreiber. Measuring information transfer. Physical Review Letters, 85(2):461–464,
2000. doi: 10.1103/PhysRevLett.85.461.
[27] Cosma Rohilla Shalizi and James P. Crutchfield. Computational mechanics: Pattern and
prediction, structure and simplicity. Journal of Statistical Physics, 104(3–4):817–879, 2001. doi:
10.1023/A:1010388907793.
[28] Anita Williams Woolley, Christopher F. Chabris, Alex Pentland, Nada Hashmi, and Thomas W.
Malone. Evidence for a collective intelligence factor in the performance of human groups.
Science, 330(6004):686–688, 2010. doi: 10.1126/science.1193147.
[29] Gunnar Zarncke. Bitwise intelligence: A blanket-information measure of competence. Technical
report, AE Studio, 2025.
[30] Gunnar Zarncke. Foundations of unsupervised agent discovery in raw dynamical systems.
Technical report, AE Studio, 2025.
6

---

[31] Brian D. Ziebart, Andrew L. Maas, J. Andrew Bagnell, and Anind K. Dey. Maximum entropy
inverse reinforcement learning. In Proceedings of the Twenty-Third AAAI Conference on
Artificial Intelligence, pages 1433–1438, 2008.
7
