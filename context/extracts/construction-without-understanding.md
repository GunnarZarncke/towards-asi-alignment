# Extract: construction_without_understanding.pdf

**Source PDF:** `context/construction_without_understanding.pdf`
**Extract:** `context/extracts/construction-without-understanding.md`
**Pages:** 9
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

Construction Without Understanding:
A UAD–B-IQ Account of Reproduction, Successor-Building, and
Reflection
Draft note
May 26, 2026
Abstract
An agent can be able to reproduce, instantiate, or build copies without explicitly knowing
how its own construction works. This is not an anomaly but a general feature of constructors:
reproductive competence may be carried by an inherited or scaffolded construction process rather
than by a self-transparent model inside the reproducing agent. In the vocabulary of Unsupervised
Agent Discovery (UAD), reproduction can be mediated by a construction channel whose control
information is high even when the agent’s internal model of the construction mechanism is
weak. Reflection becomes useful only when additional internal modelling increases expected
successor quality, robustness, or verification by more than it costs in memory, delay, experiment,
coordination, and self-distortion.
We formalize this distinction using UAD boundaries, B-
IQ, construction complexity, verification entropy, and reflection value. The resulting picture
reconciles von Neumann construction, biological reproduction, scaffolded development, semantic
information, and successor-agent construction: copying can be cheap without understanding;
improvement is where understanding earns its keep.
1
Core claim
The central distinction is between performed construction information and accessible reflective
construction knowledge. A cell may reliably construct a daughter cell while possessing no explicit
model of embryology or molecular biology in any cognitively accessible sense. A shell script may
instantiate a large language model without representing the architecture. A society may reproduce
an institution, ritual, legal form, or educational pipeline without understanding which parts are
causally essential.
In UAD terms, the ability to produce a successor is not the same as having an internal model
slot that predicts and controls the causal microstructure of successor construction. The agent may
have a high-control construction channel,
I(Abuild
X
; Yt+∆) ≫0,

$$
(1) but low reflective construction knowledge, I(M\theta
$$

$$
X; \thetaY | SX, AX, IX \ M\theta X) \approx0,
$$

$$
(2) where Y is the successor, \thetaY denotes construction-relevant degrees of freedom, and M\theta
$$

X \subsetIX is an
internal model slice of X that would count, by UAD inter-agent/inter-process modelling tests, as a
representation of the construction mechanism.
The slogan is therefore:
1

---

Reproduction requires sufficient control over a constructor; improvement requires useful
information about the constructor.
2
UAD preliminaries
UAD discovers candidate agents from raw dynamical traces by locating subsets C whose internal
variables IC, sensory variables SC, active variables AC, and external variables EC approximately
satisfy a Markov-blanket conditional-independence condition,
I(IC
t+1; EC
t+1 | SC
t , AC

$$
t ) \leq\epsilon. (3)
$$

Memory localization tests whether some internal variable m \subsetIC carries unique lagged predictive
information,
∆m(k) = I(mt−k; IC
t+1 | SC
t , AC
t , IC
t \ {m}).
(4) Inter-agent modelling analogously tests whether X contains a memory/model slot predictive of Y ’s
actions,
∆m,Y (k) = I(mX
t−k; AY
t | SX
t , AX
t , IX
t \ {m}).
(5) Goal inference treats the observed trajectory as evidence for an objective, reward, or free-energy
functional. For this note, write the inferred objective of agent X as
GX = arg max
G

$$
P(\tauX | G, E, CX)P(G), (6)
$$

where CX summarizes capacity, embodiment, and environmental constraints. This is deliberately
extensional: GX is a trajectory-scoring functional inferred from behavior, not a semantic goal-
statement.
B-IQ measures competence as predictive and control information discounted by memory and
surprise costs,
B-IQX = IX

$$
pred + \alphaIX ctrl −\betaH(IX) −\gammaSX,
$$

(7) with IX pred = I(IX t ; SX
t+1),
IX
ctrl = I(AX
t ; EX
t+1),
SX = E[−log P(SX
t+1 | IX
t )].
(8) The physical envelope is bounded by sensory and actuator channels in the low memory/surprise regime,
B-IQX ≲CX

$$
sens + \alphaCX act. (9)
$$

3
Constructors and copies

$$
Let X be a current agent, Y a successor/copy, and \Pi a construction process. \Pi may include
$$

molecular machinery, developmental scaffolding, a compiler, a factory, a reproductive body, a social
institution, a cloud API, a training pipeline, or a universal constructor. The transition is
(X, \Pi, E) −\toY.

$$
(10) Let \thetaY describe construction-relevant parameters of Y : morphology, genome, weights, architecture,
$$

initial memory, training environment, legal structure, ritual form, or local task-policy.
The missing construction information is

$$
Kmiss(Y | X, \Pi, E) = K(\thetaY | X, \Pi, E), (11)
$$

2

---

where K may be read as Kolmogorov, MDL, engineering-specification, or search complexity measured
in nats. If \Pi already contains most of the constructor, then
Kmiss ≪K(\thetaY ).
(12) This is the cell case. The cell need not know molecular developmental biology; the construction process already embodies the relevant causal organization.
A construction feasibility condition is
Z Tbuild
0
˙
B-IQ
build

$$
X+\Pi(t) dt \geqKmiss + Kwrite + Kerror, (13)
$$

$$
where Kwrite is the control information needed to inscribe or instantiate \thetaY , and Kerror is redundancy/error-
$$

correction margin. The effective builder is usually X + \Pi, not X alone.
4
Knowing what to build versus being able to build
Separate design identification from instantiation:
Z T
0
˙Idesign

$$
pred (t) dt \geqKid, (14)
$$

Z T
0
˙Ibuild

$$
ctrl (t) dt \geqKwrite. (15)
$$

The first inequality says the agent has enough prediction/model information to identify a suitable
construction target. The second says it has enough causal leverage to realize it. Copying can satisfy
the second without satisfying the first. Reflective improvement generally requires both.
This gives four regimes:
High construction control
Low construction control
High construction model
engineering, medicine, AI design
reflective impotence
Low construction model
reproduction, copying, ritual replication
neither knowing nor building
The biologically common regime is high construction control with low explicit model. The
technologically dangerous and powerful regime is high construction control with high construction
model.
5
Accessible understanding
The word “knowing” should not be cashed out as mere mutual information somewhere in the
physical system. DNA has information relevant to development; a polymerase has construction
specificity; a cell has mechanistic organization. But the claim at issue concerns accessible reflective
knowledge: internal state that can be used flexibly to predict, modify, and improve construction.
Define construction-understanding of X with respect to Y as

$$
UX(Y ) = I(M\theta X; \thetaY | SX, AX, IX \ M\theta
$$

X),
(16) 3

---

with an actionability correction,
Uact

$$
X (Y ) = I(M\theta X; \thetaY | · · · ) · I(Amodify
$$

X

$$
; Yt+∆| M\theta X)
$$

H(Amodify
X
) + ϵ
.
(17) This distinguishes latent causal structure from usable knowledge. A genome may contain construction-
relevant information, while the agent-level reflective subsystem has little Uact
X
over developmental
mechanisms.
6
The Conant–Ashby point, correctly localized
Conant and Ashby’s good-regulator theorem suggests that every good regulator must contain a
model of the system it regulates. This does not imply that every good reproducer must explicitly
understand its own construction. The model may be:

$$
1. distributed in the constructor \Pi rather than in the agent’s reflective subsystem;
$$

2. implicit in evolved biochemical dynamics rather than explicit in semantic representations;
3. stored in a template or instruction tape rather than inferred online;
4. located in a higher-level scaffold, such as a body, ecology, institution, or toolchain.
Thus good regulation requires modelling somewhere in the closed regulatory loop. It does not
require introspective availability to the focal UAD agent.
7
Reflection as meta-construction control
Reflection is the allocation of B-IQ to modelling, evaluating, and modifying the construction process.
Let P0(Y ) be the default successor distribution produced by inherited construction machinery, and
Pr(Y ) the successor distribution after reflection and intervention. Reflection is worthwhile iff
∆Jref = EY ∼Pr[J(Y )] −EY ∼P0[J(Y )] −Cref > 0.

$$
(18) A B-IQ decomposition is ˙ B-IQref = ˙Iref pred + \alpha ˙Iref
$$

ctrl −\beta ˙H(Iref) −\gamma ˙Sref −˙\Psiref.

$$
(19) The value of reflection is bounded by the useful construction information it can produce: ∆Jref \leq\lambdaJ min
$$

$$
H(\thetarel), Z T
$$

0
˙
B-IQref(t) dt

−Cref,

$$
(20) where \lambdaJ is marginal successor-value per useful construction nat and \thetarel are the construction
$$

variables whose knowledge would change action.
Unpacking cost,
Cref = Ccompute + Cmemory + Cexperiment + Cdelay + Ccoord + Cerror + Cself−distortion.
(21) The last term matters. Reflection can create memetic parasites, proxy fixation, credential loops,
reproductive anxiety, benchmark gaming, or institutional self-protection.
The marginal stopping condition is

$$
\lambdaJ(t) ˙Iconstruct(t) \leq˙Cref(t). (22)
$$

At that point, further reflection is overthinking, not improvement.
4

---

8
Search framing
If construction improvement is search over interventions a \inA, and a blind intervention succeeds

$$
with probability \pi0, then expected trial cost is approximately
$$

ctrial
\pi0
.

$$
(23) If reflection raises the success probability to \pir, reflection is worthwhile when
$$

Cref < ctrial
 1
\pi0
−1
\pir

.
(24) This is often the cleanest bound. Reflection has high value when blind search is expensive, reflective
modelling substantially increases hit rate, and intervention handles exist.
9
Successor construction and copying
For successor-agent construction, define an acceptability set for predecessor X:

$$
ΩX(∆X) = n \theta : E\tau∼M\theta[GX(\tau)] \geqV base
$$

X
+ ∆X
o
.

$$
(25) For two predecessors A, B, the mutually acceptable successor region is ΩAB = ΩA \capΩB.
$$

$$
(26) The construction problem is simply find and instantiate \thetaM \inΩAB. (27)
$$

The feasibility bound is
Z Tbuild
0
˙
B-IQ
build

$$
A+B+\Pi(t) dt \geqKmiss + Ksearch + KA verify + KB
$$

verify + Ktransfer + Kerror.
(28) Copying is the special case where Kmiss and Ksearch are small because \Pi already contains a template.
Novel reflective successor engineering is the case where these terms dominate.
10
Verification before behavior
Existing agents can be evaluated from trajectories.
A not-yet-existing successor lacks a long
trajectory, so predecessors must infer acceptability from plan, architecture, proof, construction

$$
process, copy relation, or tests. Let ZX = 1 iff M \inΩX. If the prior is PX(ZX = 1) = \piX and X
$$

requires posterior failure probability at most \deltaX, then the required log Bayes factor is
KX

$$
verify ≳log (1 −\deltaX)(1 −\piX) \deltaX\piX
$$

.

$$
(29) Copying and shared checkpoints raise \piX and lower verification cost. Opaque novel construction
$$

lowers \piX and raises it.
5

---

11
Parasites and cultural reproduction
Culture is a mixed reservoir of useful information and memetic parasites. A cultural item m can
improve host prediction/control,
∆B-IQX(m) > 0,
(30) or reproduce by controlling attention, identity, status, and obligation while imposing negative host
value,
Rmem(m) > 1,
∆B-IQX(m) < 0.
(31) Reflection over reproduction can itself be captured by such items. A culture may reproduce rituals,
institutions, or successor-building habits without knowing which pieces are load-bearing. Reflective
science is valuable partly because it converts inherited copy-processes into tested construction
handles; it is costly because it introduces new semantic/control channels through which parasites
can enter.
12
Empirical UAD signatures
A system exhibits construction without understanding when the following pattern is detected:
I(Abuild
X
; Yt+∆) ≫0,

$$
(32) I(M\theta
$$

$$
X; \thetaY | SX, AX, IX \ M\theta X) \approx0,
$$

$$
(33) I(Amodify X ; ∆B-IQY | M\theta
$$

X) \approx0.

$$
(34) It exhibits reflective successor improvement when I(M\theta
$$

$$
X; \thetaY | · · · ) > 0, (35)
$$

I(Amodify
X

$$
; ∆B-IQY | M\theta X) > 0,
$$

(36) E[J(Y ) | reflection] −E[J(Y ) | copy] > Cref. (37) The key observational distinction is whether internal model variables causally improve successor
outcomes beyond what the inherited constructor already does.
13
Examples
Cell division.
The cell has high construction control because inherited biochemical machinery
copies and partitions components. It need not contain explicit reflective developmental knowledge.
Reflection-like knowledge appears only in organisms or cultures that model and intervene in
reproduction, e.g. medicine, nutrition, IVF, genetic screening, and childcare.
Universal constructors.
Von Neumann separates a constructor from a description tape. The
tape need not understand the constructor; the constructor executes the tape. This architecture
cleanly separates copyable specification from construction dynamics.
Software deployment.
A script can instantiate a model checkpoint. The script has construction
control but little model-understanding. A research team that understands architecture, training
data, evals, and deployment risks has higher reflective construction knowledge.
6

---

Institutions.
A society can reproduce courts, schools, bureaucracies, churches, or laboratories
through imitation and ritual.
It may not know which mechanisms cause their useful effects.
Institutional science attempts to raise Uact
X
but pays coordination and memetic costs.
Successor agents.
Digital copies are plausible when templates, checkpoints, and build metadata
lower Kmiss and Kverify. Novel successors require large reflection-relevant B-IQ and robust verification
before long behavioral traces exist.
14
Relation to prior work
Von Neumann’s theory of self-reproducing automata provides the canonical constructor/description
split. Eigen’s error threshold formalizes limits on heredity when copying error overwhelms se-
lectable information. Autopoiesis emphasizes self-producing networks, but often blurs reflective
knowledge with organizational closure. Griesemer’s reproducer and scaffolded-development ac-
counts are especially close to the present framing because they reject a pure formal-copy view
and emphasize material continuity and developmental scaffolding. Maynard Smith and Szathm´ary
locate major evolutionary transitions in changes to how information is stored and transmitted.
Conant–Ashby explains why regulation requires modelling, but UAD localizes where the model may
reside. Kolchinsky–Wolpert’s semantic information links information to viability, while UAD/B-IQ
distinguishes viability-relevant construction information from agent-accessible reflective control.
Krakauer et al.’s information theory of individuality and Biehl–Virgo’s POMDP interpretation
program are close relatives in treating agency and individuality as inferable from dynamics rather
than assumed ontology.
15
Conclusion
The ability to reproduce or build copies is not equivalent to understanding the construction mecha-
nism. In UAD terms, reproduction may be high-control but low-reflection: Abuild
X
reliably routes

$$
through an inherited constructor \Pi, while no internal model slice M\theta
$$

X gives flexible predictive/control
access to the construction variables. Reflection becomes valuable only where it changes the successor
distribution enough to pay for its costs. This yields a compact principle:
copy when Kmiss is already compressed by \Pi;

$$
reflect when \lambdaJ∆Iconstruct > Cref. (38)
$$

The same distinction applies to cells, software, institutions, cultures, and artificial successor agents.
Copying is the cheap inheritance of construction. Reflection is the costly attempt to make construc-
tion steerable.
References
[1] G. Zarncke, “Foundations of Unsupervised Agent Discovery in Raw Dynamical Systems,” AE
Studio technical report, 2025.
[2] G. Zarncke, “Bitwise Intelligence: A Blanket–Information Measure of Competence,” AE Studio
technical report, 2025.
[3] G. Zarncke, “Attractor Basins of Cooperation, Privacy, and Parasite Persistence,” AE Studio
technical report, 2025.
7

---

[4] G. Zarncke, “A Formalization of Acausal Trade on Top of Unsupervised Agent Discovery,” AE
Studio technical report, 2025.
[5] M. Biehl and N. Virgo, “Interpreting systems as solving POMDPs: a step towards a formal
understanding of agency,” arXiv:2209.01619v2, 2025.
[6] J. von Neumann, Theory of Self-Reproducing Automata, edited and completed by A. W. Burks.
Urbana: University of Illinois Press, 1966.
[7] A. W. Burks, “Von Neumann’s self-reproducing automata,” in A. W. Burks, ed., Essays on
Cellular Automata. Urbana: University of Illinois Press, 1969.
[8] U. Pesavento, “An implementation of von Neumann’s self-reproducing machine,” Artificial Life,
vol. 2, no. 4, pp. 337–354, 1995.
[9] M. Eigen, “Selforganization of matter and the evolution of biological macromolecules,” Natur-
wissenschaften, vol. 58, pp. 465–523, 1971. doi:10.1007/BF00623322.
[10] H. R. Maturana and F. J. Varela, Autopoiesis and Cognition: The Realization of the Living.
Dordrecht: Reidel, 1980.
[11] E. Szathm´ary and J. Maynard Smith, “The major evolutionary transitions,” Nature, vol. 374,
pp. 227–232, 1995. doi:10.1038/374227a0.
[12] J. Maynard Smith and E. Szathm´ary, The Major Transitions in Evolution. Oxford: Oxford
University Press, 1995.
[13] J. R. Griesemer, “Reproduction and the reduction of genetics,” in P. Beurton, R. Falk, and
H.-J. Rheinberger, eds., The Concept of the Gene in Development and Evolution. Cambridge:
Cambridge University Press, pp. 240–285, 2000.
[14] J. R. Griesemer, “Reproduction in complex life cycles: toward a developmental reaction norms
perspective,” Philosophy of Science, vol. 83, no. 5, pp. 803–815, 2016.
[15] J. W. Szostak, D. P. Bartel, and P. L. Luisi, “Synthesizing life,” Nature, vol. 409, pp. 387–390,
2001. doi:10.1038/35053176.
[16] W. Hordijk and M. Steel, “Autocatalytic sets and the origin of life,” Entropy, vol. 12, no. 7, pp.
1733–1742, 2010.
[17] R. C. Conant and W. R. Ashby, “Every good regulator of a system must be a model of that
system,” International Journal of Systems Science, vol. 1, no. 2, pp. 89–97, 1970.
[18] A. Kolchinsky and D. H. Wolpert, “Semantic information, autonomous agency and non-
equilibrium statistical physics,” Interface Focus, vol. 8, no. 6, 20180041, 2018.
[19] D. Krakauer, N. Bertschinger, E. Olbrich, N. Ay, and J. C. Flack, “The information theory of
individuality,” Theory in Biosciences, vol. 139, pp. 209–223, 2020.
[20] N. Bertschinger, E. Olbrich, N. Ay, and J. Jost, “Information and closure in systems theory,”
in Explorations in the Complexity of Possible Life, 2008.
[21] K. Friston, “The free-energy principle: a unified brain theory?” Nature Reviews Neuroscience,
vol. 11, pp. 127–138, 2010.
8

---

[22] L. P. Kaelbling, M. L. Littman, and A. R. Cassandra, “Planning and acting in partially
observable stochastic domains,” Artificial Intelligence, vol. 101, no. 1–2, pp. 99–134, 1998.
[23] L. Orseau, S. M. McGill, and S. Legg, “Agents and devices: a relative definition of agency,”
arXiv:1805.12387, 2018.
[24] Z. Kenton, R. Kumar, S. Farquhar, J. Richens, M. MacDermott, and T. Everitt, “Discovering
agents,” arXiv:2208.08345, 2022.
9
