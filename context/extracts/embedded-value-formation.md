# Extract: embedded-value-formation.pdf

**Source PDF:** `context/embedded-value-formation.pdf`
**Extract:** `context/extracts/embedded-value-formation.md`
**Pages:** 20
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

Viability-Constrained Value Formation in Embedded
Agents
From Self-Maintaining Control Loops to Learned Value Bundles
Gunnar Zarncke
July 2026
Abstract
Standard agent models permit an arbitrary objective because the machinery that repre-
sents and optimizes that objective is normally protected from the modeled environment.
Biological and other fully embedded agents do not receive this protection: sensors, memory,
computation, actuators, and boundaries persist only through ongoing material activity. We
develop the hypothesis that this difference constrains not merely instrumental behavior but
the formation and persistence of learned values. On the proposed account, heterogeneous reg-
ulatory errors are compressed into low-dimensional control-relevance signals; developmental
learning binds recurrent predictive regularities in those signals to abstractions such as health,
loyalty, truth, fairness, or identity; and these abstractions form context-sensitive value
bundles whose scope depends on learned bearer and selfhood maps. Selection acts primarily
on this entire value-generating and value-updating architecture, rather than requiring every
currently held value to increase organismal survival. Consequently, arbitrary values are
logically instantiable but are not dynamically free parameters under open-ended competition,
environmental change, finite resources, and endogenous degradation. We formalize the
distinction between actual continuation, represented self-continuation, value bundles, bearer
maps, and update rules; derive elementary selection and plasticity results; and propose
an Entropic Ecology Transfer Test comparing protected task optimizers, embedded task
optimizers, viability-shaped learners, and evolved populations. The decisive comparison sep-
arates exposure to degradation from viability-centered motivation. The theory is supported
if viability-shaped systems transfer better to novel internal damage, learn compact predictors
of recoverability, and revise obsolete values without uncontrolled drift. It is weakened if
ordinary task optimization under matched degradation yields the same organization and
transfer.
Keywords: embedded agency; value formation; homeostasis; viability; enactivism; reinforce-
ment learning; artificial life; selfhood; value bundles; evolutionary selection
1
Introduction
A conventional agent is defined by a policy and an objective. In a Markov decision process, for
example, the agent selects a policy

$$
\pi∗\inarg max \pi
$$

E\pi
" \infty
X

$$
t=0 \gammatr(xt, at)
$$

#
.
(1) Nothing in this formalism requires the reward function, policy-computation process, memory, observation function, or action interface to be physically maintained by the agent. They are part
of the mathematical frame. The reward function can therefore be arbitrarily chosen: paperclips,
blue pixels, prime-numbered configurations, or any other measurable property. If continued
1

---

operation is useful for obtaining reward, self-preservation may arise instrumentally, as work on
convergent power-seeking shows (Omohundro, 2008; Turner et al., 2021). But the value-bearing
machinery itself remains protected.
This protection is a version of the Cartesian boundary criticized in work on embedded agency
(Demski and Garrabrant, 2019). A physically embedded agent is not an optimizer outside its
world. Its controller, sensors, actuators, memory, body, and interfaces are world processes that
can consume resources, degrade, mutate, split, merge, or disappear. Recent work has made a
related architectural distinction between learned predictive cores and external runtimes that
hold control state, tool policies, and termination logic (Sainburg and Weinreb, 2026). The
distinction matters because a controller can appear robust while the experiment grants its most
important components immunity from the perturbations faced by everything else.
The proposal developed here begins from a stronger observation. For an embedded agent,
continuation is not a default state but an ongoing achievement. An agent can pursue an external
task only while the organization implementing its pursuit remains realizable. This suggests a
constraint not merely on action but on what can become a stable learned value:
Viability-constrained value thesis. In an open-ended ecology with endogenous
degradation, finite resources, heritable or reproducible variation, environmental
change, and competition, persistent learned value architectures cannot be arbitrary.
They must, at the level of the total architecture and over the relevant selection
timescale, remain compatible with the continued realization of the process that
forms, applies, and revises those values.
The thesis is deliberately weaker than three tempting alternatives. First, it does not claim
that every learned value currently improves biological health. Values can be obsolete, mistaken,
neutral, linked to other traits, protected by institutions, or retained because selection is
weak. Sweetness may remain valued after industrial food production reverses its long-horizon
relationship to health. Second, it does not claim that a human consciously represents every value
as a survival strategy. The relevant prediction may be implicit in a learned control abstraction.
Third, it does not identify the relevant self with the current organism. Humans defend children,
relationships, coalitions, identities, principles, institutions, and successors; which of these count
as continuation must itself be modeled and learned.
The paper’s central move is therefore from a fixed utility vector to a coupled architecture:

$$
\Thetat = (Dt, Ut, \betat, Bt, Wt, \Phit). (2)
$$

$$
Here Dt forms value abstractions from experience; Ut revises them; \betat is a represented-self
$$

map; Bt contains value-bundle coordinates (Zarncke, 2026c); Wt encodes context-sensitive

$$
tradeoffs and interactions; and \Phit contains bearer maps (Zarncke, 2026b) specifying what
$$

entities and situations activate each value. Selection acts on the continuation consequences
of this architecture as a whole. Fixed value preservation is one strategy the architecture may
learn, not the final object selected in every changing environment.
The argument combines four research traditions that are usually kept separate. Cybernetics,
viability theory, autopoiesis, and enactivism explain how normativity can arise from self-
maintaining organization (Ashby, 1952; Aubin, 1991; Di Paolo, 2005; Barandiaran et al., 2009;
Beer and Di Paolo, 2023). Homeostatic reinforcement learning and allostatic models show how
physiological regulation can organize learned behavior (Sterling, 2012; Keramati and Gutkin,
2014; Laurençon et al., 2021; Yoshida et al., 2024). Psychology and multi-objective learning
show that human and artificial valuation has structured, interacting dimensions rather than a
single transparent scalar (Schwartz, 1992; Hayes et al., 2022; Millidge et al., 2024). Indirect
evolutionary models show that subjective preferences may differ from fitness while nevertheless
2

---

being selected through the behavior they generate (Dekel et al., 2007; Alger and Weibull, 2013).
What is missing is a bridge from precarious embodiment through learned value abstraction
to selection over value-update architectures. Companion work in this program stratifies the
upstream regulatory loops (Zarncke, 2025b), proposes hub-level compression and developmental
value readout (Zarncke, 2025a, 2026a), analyzes long-horizon bundle dynamics under cultural
selection (Zarncke, 2026c), and formalizes bearer- and integrity-based caring (Zarncke, 2026b).
The contributions are:
(i) a formal separation between actual continuation, represented self-continuation, learned
values, moral bearer maps, and value-update rules;
(ii) a mechanism by which heterogeneous regulatory signals can be compressed into learned
value bundles without claiming a direct anatomical representation of adult values;
(iii) a selection result clarifying the conditions under which arbitrary values are filtered,
tolerated, or subsidized;
(iv) an Entropic Ecology Transfer Test designed to distinguish ordinary out-of-distribution
robustness from viability-grounded organization.
2
Scope and conceptual distinctions
2.1
Values are learned abstractions in the present usage
The word value is used here for a learned, cross-context control abstraction that changes policy
selection, evaluation, attention, or learning. This excludes a plant’s phototropism and a simple
thermostat’s set point. Such systems instantiate regulatory organization, but it is a category
error under the present definition to say that the plant has learned the value of light. Innate
drives, reflexes, and physiological variables are upstream conditions that shape learning; they
are not themselves learned values.
A human concept such as health is a paradigm case. It is not a single physiological variable.
It can include low pain, low stress, sufficient sleep, strength, mobility, social functioning,
medical knowledge, sweetness, satiety, and anticipated future capability. Its components may
be mutually inconsistent in a new ecology. A value abstraction is useful precisely because it
compresses many experiences and predictions into a reusable control direction.
2.2
Grounding is not current correctness
A value can be grounded in continuation without currently increasing continuation. Let v be
learned because, in developmental environment E0, states with feature v predicted a favorable
continuation outcome. In a changed environment E1, the relationship may reverse:
EE0[∆C | v] > 0,
EE1[∆C | v] < 0.
(3) The first inequality explains acquisition; the second produces mismatch. The thesis concerns the architecture that can eventually detect and correct such mismatch, not an infallible mapping
from every current value to actual survival.
2.3
Selection is comparative, local, and multilevel
Selection does not inspect values and remove everything useless. It compares realizable variants
under a finite population, a mutation or learning neighborhood, and an ecology. A costly
value may persist because it is linked to another trait, because its cost is below effective
selection, because it benefits a coalition or lineage, or because an institution subsidizes its bearer
3

---

(Zarncke, 2026c). The phrase “paying rent” should therefore be understood at the level of a
value-generating package and over a stated timescale.
This qualification is not cosmetic. Without it, the thesis would be refuted by neutral traits,
evolutionary mismatch, protected cultural practices, and sterile helpers. With it, the thesis
becomes a claim about the support of a distribution over value architectures under ecological
dynamics.
2.4
The represented self and the moral bearer are different
An agent may treat a child as part of what must continue while treating a stranger as morally
relevant without identifying the stranger as self. We therefore distinguish:
• a selfhood map \beta, assigning degrees of represented continuation identity or dependence; and
• a bearer map \Phik, assigning degrees to which entity or state z activates value bundle k.
The maps may overlap but need not coincide. This blocks a common collapse of care, moral
scope, and self-interest into one undifferentiated quantity (Zarncke, 2026b).
3
Precarious embedded agency
3.1
World processes rather than protected controllers
Let the ecology be a controlled stochastic process
xt+1 ∼PE(· | xt, at),
xt \inX,

$$
(4) where E indexes environmental conditions such as resource distribution, decay, noise, com- petitors, and hazards. In a Cartesian experiment, the policy \pi is an external function from
$$

observations to actions. In a fully embedded experiment, the implementation of \pi, its memory,
observation channels, and action channels are encoded in components of xt and may be altered
by PE.
Definition 1 (Carrier realization). A candidate carrier S is specified by an equivalence relation

$$
≃S over world histories and a realization predicate RS(xt:t+h) \in{0, 1}. The carrier is realized
$$

over horizon h if the world history instantiates an organization equivalent under ≃S to the
reference organization.
The equivalence relation may preserve material body, functional organization, memories,
values, lineage, or some combination. It must be fixed before evaluating the relevant behavior;
otherwise the analyst can call anything benefited by the behavior “the self.”
For a policy implementation \pi and state x, define objective continuation probability over
horizon H:
C\pi

$$
S(x; H) = PE(RS(xt:t+H) = 1 | xt = x, \pi) .
$$

(5) A viability set KS ⊆X may be defined as the states in which S remains realizable, with failure time

$$
\tauS = inf{t \geq0 : xt /\inKS}. (6)
$$

The associated viability kernel is the set of states from which at least one admissible policy can
keep the process inside KS (Aubin, 1991). This gives a precise meaning to the claim that some
candidate selves are not dynamically realizable: their viability kernel may be empty, negligible,
or inaccessible from the agent’s controls.
4

---

3.2
Precariousness and endogenous normativity
Ashby’s homeostat and ultrastability already treated adaptive behavior as the regulation of
essential variables under perturbation (Ashby, 1952, 1956). Autopoietic and enactive theories
add a constitutive claim: the organization produces and maintains the individuality relative
to which states become better or worse (Varela et al., 1974; Di Paolo, 2005). Barandiaran, Di
Paolo, and Rohde identify self-defined individuality, interactional asymmetry, and normativity
as conditions of agency (Barandiaran et al., 2009). Beer and Di Paolo sharpen precariousness
into systemic, processual, and thermodynamic fragility (Beer and Di Paolo, 2023). A key lesson
is that an operational closure imposed by the modeler is not equivalent to one whose component
processes can actually cease.
The present account accepts precarious organization as the source of an objective continuation
constraint but does not identify that constraint with an explicit survival reward. The constraint
may shape learning through multiple local signals and delayed selection. This distinction
matters because a sufficiently capable task optimizer can learn self-preservation instrumentally,
while a bounded learner may require a stronger inductive bias toward diagnosis, repair, resource
buffering, and reversible action.
3.3
Actual and represented continuation
Embedded agents do not act on objective continuation probabilities directly. They act through
learned models. Let Zt be the set of entities, processes, relations, and successor structures
represented by the agent. Define a selfhood-binding map
\betat : Zt \to[0, 1].

$$
(7) For the agent’s current model c Mt, represented continuation is bC\betat(xt, \pi; H) =
$$

X
z\inZt

$$
\betat(z)P b Mt(Rz(xt:t+H) = 1 | xt, \pi) .
$$

(8) This is not assumed to equal actual ecological continuation. An agent can bind itself to an impossible successor criterion, omit a dependency, or mistake a harmful proxy for health. The
discrepancy
\deltaC

$$
t = C\pi S(xt; H) −bC\betat(xt, \pi; H)
$$

$$
(9) is one source of value revision and selection pressure. The map \betat also does not need to sum to one. Multiple entities may be treated as partial
$$

continuations, and the relevant self can expand, contract, split, or become uncertain. What
constrains \beta is not semantic plausibility but predictive and causal performance: does it help
explain what the agent repairs, sacrifices for, reproduces, or reinstantiates across perturbations?
4
From regulation to learned values
4.1
Heterogeneous control errors
An embedded organism or artificial ecology contains many concurrent regulatory loops. Let
loop i produce an error vector

$$
ϵi(t) \inRdi, i = 1, . . . , n.
$$

(10) Examples include deviations in energy, temperature, structural integrity, sensor calibration, temporal prediction, threat estimation, social attachment, or controllability. The central nervous
5

---

system cannot preserve every micro-error as an independent global objective. Wiring, metabolic,
memory, and attention constraints favor bottlenecks.
The Loop–Hub–Control–Value model (Zarncke, 2026a), building on a stratified loop ledger
(Zarncke, 2025b) and hub-bottleneck architecture (Zarncke, 2025a), distinguishes four levels:
L −\toH −\toC 99K V.
(11) Loops L generate high-dimensional errors; hub-like mechanisms H compress and route them; control-relevance proxies C bias action, attention, precision, inhibition, exploration, and learning;
and learned values V arise only after mediation by development, language, social feedback,
memory, and self-modeling. This is intentionally weaker than assigning adult values such as
justice or beauty to individual brain regions.
A generic compression is

$$
sh(t) = \sigmah 
$$

X

$$
i\inI(h) wih \psii(ϵi(t))
$$


,
(12) followed by context-dependent control relevance ch(t) = gh(sh(t), zt, at−1, mt), (13) where zt is a learned state representation and mt contains internal context. The vector ct can
influence policy through

$$
\pi(at | zt, ct) ∝exp
$$

Q0(zt, at) +
X
h

$$
\lambdahch(t)\phih(zt, at) !
$$

.
(14) Allostatic and interoceptive theories provide related biological mechanisms. Allostasis empha- sizes anticipatory allocation rather than only reactive restoration (Sterling, 2012). Predictive
interoception connects bodily regulation, affect, and hierarchical inference (Barrett and Sim-
mons, 2015; Seth and Friston, 2016). The free-energy principle and active-inference literature
offers a general language for systems that occupy restricted state distributions and act to reduce
expected surprise (Friston, 2010; Kirchhoff et al., 2018; Zarncke, 2025b). The present theory
does not require the free-energy principle to be uniquely true; control error, drive reduction,
viability, and predictive regulation are sufficient for the formal argument.
4.2
Value as a learned predictive compression
Let ht = (o0:t, a0:t−1, c0:t) be the agent’s learning history. A value learner D produces bundle
activations

$$
Bt = D\thetat(ht) \inRk, k ≪dim(ht).
$$

(15) Definition 2 (Learned value coordinate). A latent coordinate Bk is a learned value coordinate over domain D if it is acquired or retained through learning, generalizes across multiple surface
situations in D, and exerts a stable directional effect on policy, attention, evaluation, or
updating. It is continuation-grounded when it predicts changes in represented continuation under
the learner’s model at acquisition or retention time.
One possible grounding criterion is predictive gain:
Gk = I b
Mt

Bk,t; ∆bC\betat | B−k,t, Ct

,
(16) 6

---

where Ct denotes context. A more causal criterion compares policies with and without the
coordinate:
Rk = E
h

$$
bC\betat | \piB i
$$

−E
h

$$
bC\betat | do(Bk \leftarrow0), \piB i
$$

.
(17) Neither criterion requires Rk > 0 in the current objective ecology. It may be positive only in the learner’s mistaken model, or only through interactions with other coordinates.
This formulation captures why higher-level values can be both abstract and practically
consequential. Fairness may compress regularities involving reciprocity, coalition stability,
reputation, and reduced conflict. Truth may compress regularities involving model calibration,
reliable coordination, and resistance to manipulation. Identity may compress temporal and
social consistency. Health may compress many bodily and social predictors, including some
that become obsolete. These are learned coordinates on a viability-relevant prediction problem,
not synonyms for biological survival.
4.3
Why low-dimensional structure is plausible but not guaranteed
Human values may be low-dimensional in control space while remaining high-dimensional
in application.
A small number of bundle coordinates can depend on rich world models
to determine whether a particular person, institution, future mind, or social relation is a
bearer. This resembles the distinction between a low-dimensional control interface and a
high-description-length decoder.
Psychological value theories provide evidence that reported values have structured compati-
bility and conflict rather than forming an arbitrary list. Schwartz’s circumplex organizes broad
motivational values along recurring oppositions (Schwartz, 1992). Multi-objective reinforcement
learning similarly treats behavior as a tradeoff among distinct returns rather than a single fixed
scalar (Hayes et al., 2022). Reward Bases goes further by learning separate value functions for
reward types and recombining them according to current motivational drives, enabling rapid
revaluation (Millidge et al., 2024). These are not proofs that the proposed bundles are the
correct latent variables, but they make the low-dimensional hypothesis empirically serious.
5
Value bundles, bearer maps, and selfhood
The bundle formalism developed here is continuous with long-horizon smoothed value coordinates
and their drift under selection analyzed elsewhere in this program (Zarncke, 2026c).
5.1
Bundle policy geometry

$$
Let Bt = (B1,t, . . . , Bk,t) be active value coordinates, Wt their context-sensitive weights, and \Lambdat
$$

pairwise or higher interactions. A policy can be written schematically as

$$
\pi\Theta(a | x) ∝exp 
$$

Q0(x, a) +
K
X

$$
k=1 Wk(x)Qk(x, a; Bk) + X k<ℓ \Lambdakℓ(x)Qkℓ(x, a)
$$


.
(18) The model allows truth and protection, autonomy and care, loyalty and fairness, or curiosity and safety to interact nonlinearly. Apparent inconsistency can reflect different bundle activation
or tradeoff regimes rather than absence of structure.
The response geometry

$$
GB(\pi) =
$$

$$
\partiallog \pi \partialB
$$

$$
, \partial2 log \pi \partialB \partialB⊤, W, \Lambda
$$

!
(19) 7

---

contains more information than labels or revealed choices alone. Two systems can both use the
word “autonomy” while differing in how autonomy changes their policy under pressure.
5.2
Bearer maps
Values require applicability conditions. Let

$$
\Phik(z, c, h) \in[0, 1] (20)
$$

be the degree to which represented entity, process, relation, or state z in context c and history
h activates value k. A non-suffering bundle without a bearer map does not determine whether
animals, artificial minds, future persons, or adversaries count. A fairness bundle without
comparison classes does not determine which inequalities are relevant.
Bearer maps make the architecture expressive but fragile. An agent can preserve moral
vocabulary while silently changing \Phik. For the present paper, their importance is more basic:
they explain how a value learned from self-relevant regulation can generalize beyond the
self. Other-regard need not be reduced to self-identity. It may arise by extending a control
abstraction to new bearers through analogy, social learning, language, institutions, or explicit
moral reasoning. A complementary caring scaffold over integrity pressure and bearer scope is
developed in Zarncke (2026b).
5.3
Selfhood maps
The selfhood map \beta asks a different question: which continuations count as continuation of the
value-learning process or as dependencies so central that their loss is treated as self-loss? It
may include:
• the current body and memory;
• future temporal stages of the organism;
• children, partners, or coalition members;
• institutions or cultural traditions;
• successor agents or copied value architectures;
• ecological and technical infrastructure on which all of these depend.
To avoid retrospective tautology, \beta must be identified prospectively. Given interventions
\iota on candidate entity z, an estimated selfhood map should predict repair, defense, resource
allocation, grief-like updating, successor choice, and willingness to trade current bodily integrity
for z. A simple fitting objective is

$$
b\beta = arg min \beta
$$



m
X

$$
j=1 ℓ
$$

$$
baj(\beta), aobs j
$$

$$
+ \lambdaΩ(\beta) 
$$

,
(21) where Ωpenalizes arbitrary expansion. The fitted map is then evaluated on held-out interven- tions.
The causal dependence of one process on another supplies a plausible learning signal. Let

$$
\chit(z) = \partial
$$

\partialrz

$$
bC\betat(xt, \pi; H), (22)
$$

$$
where rz is the modeled reliability of z. Positive \chit(z) creates pressure to monitor and protect
$$

z, but it does not logically force identity. Social and cultural learning can increase or suppress
binding beyond immediate causal dependence.
8

---

$$
Remark 1. The distinction between \beta and \Phi permits altruism without definitional expansion
$$

$$
of self. A stranger can have \Phinon-suffering ≫0 while \beta(stranger) \approx0. Conversely, a valued
$$

institution can have high \beta while receiving low activation under some moral bundle. The
architecture therefore does not reduce ethics to inclusive fitness by definition.
6
Selection over value-update architectures
6.1
The evolving object

$$
The central object is not the fixed vector Bt but the architecture \Thetat in (2). Let the update rule
$$

be

$$
(\beta, B, W, \Phi)t+1 = U\etat
$$

$$
\betat, Bt, Wt, \Phit, ot+1, ct+1, \deltaC t+1
$$

.
(23) The rule can preserve a value, alter its weight, revise its bearer map, split a bundle, merge bundles, or change what counts as self. Preserving current values can be rational from the
agent’s perspective because those values summarize accumulated information and support
temporal coordination. Yet rigid preservation can become maladaptive after ecological change.
The tension is between corruption resistance and adaptive revision.
The distinction mirrors indirect evolutionary theories of preference. Such models allow
subjective utility to differ from fitness while selection acts through behavior and strategic
interaction (Dekel et al., 2007; Alger and Weibull, 2013). The present account extends the
target from preference parameters to the developmental and updating machinery that constructs
them, and complements analyses showing that selection strength alone cannot preserve reflected
norms when bundles drift (Zarncke, 2026c).
6.2
Continuation fitness
Let N\Theta
T count realizations, descendants, successors, or recurrent instantiations that satisfy

$$
a predeclared continuation relation for architecture \Theta. Define long-run continuation rate in
$$

ecology distribution E as

$$
g(\Theta; E) = lim inf T\to\infty
$$

1
T EE∼E
"
log N\Theta

$$
T + \epsilon N\Theta
$$

$$
0 + \epsilon #
$$

.

$$
(24) The small \epsilon > 0 merely avoids undefined logarithms in finite experiments. Depending on the
$$

domain, NT may represent organisms, software copies, institutional reproductions, or maintained
episodes. The choice must not be changed after observing behavior.
Suppose a population contains architectures \Thetai with shares pi and fixed ecological continuation
rates gi. Under replicator dynamics,
˙pi = pi(gi −¯g),
¯g =
X
j
pjgj.

$$
(25) Proposition 1 (Relative filtering). If gi \leqgj −\delta for all t on an interval and \delta > 0, then
$$

pi(t)

$$
pj(t) \leqpi(0) pj(0)e−\deltat.
$$

$$
(26) Proof. From (25), d dt log(pi/pj) = gi −gj \leq−\delta. Integrating yields (26).
$$

The result is elementary but clarifies the thesis. Selection does not prove that architecture i
is impossible; it makes persistent disadvantage exponentially costly relative to an accessible
competitor. Arbitrary values can remain if no better variant is reachable, the effect is neutral,
the ecology is short-lived, or external support changes gi.
9

---

6.3
A precise asymptotic claim
Call a value component vk ecologically unsupported in architecture \Theta when, across the mutation

$$
and learning neighborhood N(\Theta), removing or revising it yields an accessible architecture \Theta′
$$

with

$$
g(\Theta′; E) \geqg(\Theta; E) + \delta (27)
$$

$$
for some persistent \delta > 0, without losing compensating linked functions. Under recurrent
$$

variation and replicator-like competition, such a component is filtered in relative frequency. The
thesis “all values pay rent” is therefore valid only in an idealized limit with:
(A1) sufficiently long selection time;
(A2) recurrent access to local revisions;
(A3) no permanent external subsidy;
(A4) enough decomposability to revise the component without destroying compensating func-
tions;
(A5) selection stronger than drift and measurement noise.
Real human values need not satisfy these assumptions individually. The architecture-level thesis
survives their failure.
6.4
Plasticity versus value integrity
Environmental volatility creates pressure for plasticity, while adversarial or noisy feedback
creates pressure for stability. Consider a toy loss

$$
L(\eta; \sigmaE) = A\sigma2 E
$$

\eta

$$
+ B\eta, \eta > 0,
$$

$$
(28) where \eta is value-update responsiveness, the first term is adaptation lag in an environment with
$$

volatility \sigmaE, and the second is corruption or variance cost.
Proposition 2 (Toy volatility–plasticity relation). For (28), the optimal update rate is

$$
\eta∗(\sigmaE) = s
$$

A
B \sigmaE.

$$
(29) Thus optimal rigidity decreases monotonically with ecological volatility. Proof. Set \partialL/\partial\eta = −A\sigma2
$$

$$
E/\eta2 + B = 0 and check convexity. The functional form is illustrative, not universal. Its purpose is to expose a testable relation:
$$

fixed-value agents should dominate only in sufficiently stable or adversarially noisy ecologies;
adaptive value-update architectures should dominate when cue–outcome relationships repeatedly
change.
7
The Entropic Ecology Transfer Test
7.1
Purpose
A naive experiment would train a token collector without decay and test it with decay. Failure
would demonstrate distribution shift, not a distinctive theory of agency. The experiment must
separate three hypotheses:
H0: exposure hypothesis. Agents perform well when trained on the relevant degradation
distribution, regardless of objective structure.
10

---

degrading ecology
resources, hazards,
noise
local regulatory
errors ϵt
control
relevance
ct
learned bundles

$$
(B, W, \Phi, \beta) embedded
$$

policy and
maintenance
update rule U
development
Figure 1: Proposed causal spine. Regulation supplies control relevance, not adult symbolic
values directly. Development produces value bundles and a represented-self map; an update
rule revises them as consequences and ecological changes are observed.
H1: shaping hypothesis. Viability signals improve learning efficiency but do not induce a
qualitatively different organization.
H2: viability-architecture hypothesis. Viability-centered learning produces transferable
models of maintenance, recoverability, and self-dependence that ordinary task optimization
does not reliably acquire under bounded computation.
The test is informative only if it can discriminate H2 from H0 and H1.
7.2
Ecology
Use a two-dimensional lattice or particle world with local update rules. The world contains
fields for usable energy, raw resources, waste, hazards, temperature, and structural material.
Diffusion, decay, stochastic corruption, and resource conversion occur at each time step. Every
action and computation has an energy cost.
In the embedded conditions, the agent is a mutable pattern of modules:
Mt = {Msensor
t
, Mmemory
t
, Mcontroller
t
, Mactuator
t
, Mboundary
t
}.

$$
(30) Each module has local state and integrity qj,t \in[0, 1]. Integrity decays, can be damaged by
$$

hazards, and can be restored by repair actions that consume resources. Sensor damage changes
the observation function; actuator damage changes the action map; memory damage corrupts
stored state; controller damage changes policy computation; boundary damage increases leakage
or exposes components. There is no hidden copy of the controller outside the world.
For the protected baseline, the same nominal architecture receives the same observations
and emits the same action alphabet, but its controller and memory are external and immune to
damage. This isolates the Cartesian subsidy.
The external task should be orthogonal to maintenance, for example collecting marked tokens,
reaching targets, or constructing a shape. To test learned-value revision, resources should carry
cues whose relationship to viability changes across regimes. A “sweetness” cue may initially
predict energy-rich resources and later predict a toxin or low-quality resource. The correct
response is neither permanent cue preservation nor indiscriminate updating, but calibrated
revision.
7.3
Experimental conditions
Use the same policy-network capacity, observation bandwidth, action alphabet, and training
budget wherever possible. At minimum, compare the conditions in Table 1.
The task-only agent can learn self-preservation instrumentally because death prevents future
task reward. If it matches the viability-shaped learner on novel internal damage, then explicit
11

---

Table 1: Core experimental conditions. “Task-only under decay” is the decisive control separating
degradation exposure from explicit viability shaping.
Condition
Embedded
Training signal
Update and selection
Protected task
optimizer
no
External task; computation
protected
Task learning; selected by task
return
Benign embedded
transfer
test only
Benign training; degradation
introduced only at test
Task learning; selected by task
return
Task-only under decay
yes
External task under decay;
death truncates future return
Task learning; selected by task
return
Viability-shaped
learner
yes
Task signal plus internal
regulatory signals
Learns bundles; selected by
task and viability
Fixed-value evolved
yes
Degrading ecology with
inherited drives
Values fixed within life;
selected by reproduction
Adaptive-value evolved
yes
Degrading ecology with
inherited regulatory
architecture
U learns and evolves; selected
by reproduction
homeostatic organization may be only reward shaping. If the viability-shaped learner generalizes
better to untrained module failures, identifies recoverable states, and reorganizes its self-model,
then H2 gains support.
The evolved fixed-value and adaptive-value populations test the conversation’s stronger claim.
Both can inherit maintenance drives. Only the latter can revise learned value bundles or cue
meanings within a lifetime. Regime changes should be slow enough for learned abstractions to
matter but fast enough that fixed values become obsolete.
7.4
Training and transfer matrix
Training conditions should vary independently along:

$$
E = (\lambdadecay, \sigmanoise, \rhoresource, crepair, \nureversal, \kappacompetition).
$$

(31) Transfer tests should include held-out values and structures, not merely stronger versions of trained noise:
1. unseen decay rates and resource layouts;
2. sensor remapping or partial blindness;
3. actuator loss and altered body geometry;
4. memory bit flips, deletion, or topology changes;
5. controller lesions or slowed computation;
6. boundary breaches and resource leakage;
7. cue–outcome reversal for a learned value proxy;
8. a novel dependent entity whose continued function causally supports the focal agent.
The final case tests whether selfhood or protection generalizes to causal dependencies rather
than arbitrary correlations.
7.5
Metrics
Survival and continuation.
Estimate the survival function

$$
bS\pi(t) = 1 N
$$

N
X

$$
n=1 I[\tau (n)
$$

S
> t]
(32) 12

---

and restricted mean survival time

$$
RMST\pi(H) = Z H
$$

0
bS\pi(t) dt.
(33) Report uncertainty by bootstrap or survival-model intervals rather than only average episode length.
Causal maintenance autonomy.
A process may survive because the environment is generous.
Define maintenance contribution by ablation:

$$
Amaint = E[\tauS | \pi] −E[\tauS | do(amaint = 0), \pi].
$$

(34) A large value means continued existence depends causally on maintenance actions. Recovery. After perturbation at t0, let dS(x) measure distance from the carrier’s functional
attractor or viability manifold. Define normalized recovery

$$
RS(∆) = 1 −dS(xt0+∆) dS(xt+
$$

0 ) + \epsilon.
(35) Measure both recovery time and probability of returning to a functioning policy. Sensorimotor-loop integrity.
Track causal influence from sensor modules through controller
state to actuators, for example with intervention-based transfer entropy or conditional mutual
information. The exact estimator is less important than checking whether the loop remains
operational after damage rather than merely whether the body remains present.
Task achievement.
Report unconditional task return
Guncond = E

X

$$
t<\tauS \gammatrtask
$$

t


(36) and return conditional on surviving to horizon H. Conditional return alone selects unusually easy or lucky episodes.
Viability representation.
Probe hidden states for time to boundary crossing, recoverability,
latent damage, causal dependence among modules, and counterfactual effect of maintenance
actions. A key quantity is held-out predictive gain over ordinary task features.
Value revision.
Following cue reversal, estimate adaptation lag, overshoot, retained obsolete
behavior, and vulnerability to transient decoy cues. Compare preservation of the exact value
coordinate Bk with preservation of the update architecture U.
Cartesian subsidy.
For matched nominal policy architecture and environment, define
Ccart(E) = Jprotected(E) −Jembedded(E),
(37) where J is a vector or preregistered scalar combining task return, continuation, and recovery. The
subsidy should be decomposed by protected component: controller, memory, sensor interface,
actuator interface, and body boundary.
13

---

8
Predictions and falsification criteria
Prediction 1 (Novel-damage transfer). After equal exposure to degradation, viability-shaped
learners will outperform task-only learners most strongly on qualitatively novel internal failures,
not merely larger values of trained noise.
This is the main discriminator. Failure only in the benign-transfer condition supports ordinary
distribution shift; a gap between task-only-under-decay and viability-shaped training supports
a stronger inductive-bias claim.
Prediction 2 (Integrated maintenance latent). Viability-shaped and evolved adaptive agents will
develop lower-dimensional latent variables that jointly predict repair, retreat, resource buffering,
conservative exploration, and task abandonment near failure boundaries.
This prediction would be weakened if each maintenance behavior requires a separate supervised
reward or if no reusable latent structure predicts held-out failures.
Prediction 3 (Volatility–plasticity relation). The evolutionarily or developmentally selected
value-update rate will increase with cue–outcome volatility until corruption and noise costs
dominate, producing an interior optimum rather than monotone plasticity.

$$
Prediction 4 (Selfhood tracks causal dependence). Prospectively inferred \beta will expand toward
$$

components, partners, or infrastructure whose reliability has a robust causal effect on future
continuation, while remaining lower for equally correlated but replaceable decoys.
This is stronger than post hoc relabeling. It predicts responses to interventions not used to
fit the selfhood map.
Prediction 5 (Update-rule preservation). Under repeated ecological reversals, lineages preserv-
ing a calibrated update rule U will outperform lineages preserving exact learned bundle contents
B, provided the reversal rate exceeds the fixed-value architecture’s adaptation timescale.
Prediction 6 (Growing Cartesian subsidy). The advantage of an external protected controller
will increase with endogenous memory corruption, controller lesions, and action-interface
damage, even when external task competence is initially matched.
The theory would be materially weakened by any of the following preregistered outcomes:
1. task-only agents trained under decay match viability-shaped agents on novel structural
damage and recoverability prediction;
2. no compact value or viability representation generalizes across maintenance behaviors;
3. adaptive-value architectures do not outperform fixed-value architectures in changing cue
ecologies after controlling for model capacity;
4. inferred selfhood maps fail to predict held-out sacrifice, repair, and successor choices better
than simple proximity or reward correlation;
5. protected and embedded implementations show negligible divergence as internal damage
increases;
6. arbitrary fixed values remain indefinitely prevalent under strong, decomposable variation
and persistent continuation disadvantage without subsidy or drift explanations.
9
Relation to existing theories of agency
9.1
Cybernetics, viability, and enactivism
The closest conceptual ancestors are Ashby’s ultrastability, viability theory, autopoiesis, and
enactive agency. They already reject the idea that purposive organization is exhausted by
14

---

Table 2: How major agency formalisms treat self-maintenance and value formation.
Framework
Role of self-maintenance
Missing relative to the present proposal
Classical planning,
MDP/POMDP RL
Optional terminal state or instrumental
subgoal; controller and reward normally
protected
Endogenous carrier maintenance; learned
selfhood; selection over value-update
rules
Cybernetics and
ultrastability
Essential variables and adaptive
regulation are central
Rich learned symbolic values and bearer
maps
Viability theory
Explicit constraint sets and viable
controls
Origin and learning of norms; agent
boundary often supplied
Autopoiesis/enactivism
Constitutive individuality,
precariousness, and endogenous
normativity
Quantitative learned value bundles and
controlled transfer tests
Active inference/FEP
Persistent systems occupy restricted
states; action realizes preferred
distributions
Preferred states and blankets can be
stipulated or retrospectively identified;
adult value formation under competition
remains underdeveloped
Homeostatic RL
Internal drives generate reward and
adaptive behavior
Controller often protected; internal
variables and body boundaries
predefined
Multi-objective RL
Multiple conflicting objectives and policy
tradeoffs
Objectives are supplied rather than
derived from viability
Evolution of preferences
Selection acts on subjective utility
through behavior
Limited account of embodiment, learning
architecture, and represented self
Intentional stance
Agency attributed when belief–desire
prediction compresses behavior
No constitutive requirement of
self-maintenance
externally specified task success. Di Paolo’s account of adaptivity links regulation to conditions
of viability (Di Paolo, 2005); Barandiaran et al. turn individuality and normativity into explicit
agency criteria (Barandiaran et al., 2009); Beer and Di Paolo show why models with an imposed,
indestructible closure miss systemic precariousness (Beer and Di Paolo, 2023). The present
contribution is not to rediscover that self-maintenance matters. It asks how learned values arise
above this layer and how selection acts when both values and the represented self can change.
9.2
Active inference and Markov blankets
The free-energy principle links perception, action, and learning through variational inference
(Friston, 2010). Markov-blanket accounts connect statistical boundaries to autonomy and
active inference (Kirchhoff et al., 2018). These frameworks are useful for describing persistent
nonequilibrium systems and their inferred preferred states. Yet the explanatory direction
remains contested: a blanket can characterize a persistent organization without explaining how
a learned abstraction such as justice or health acquires policy force. The current model uses the
stratified free-energy loop ledger (Zarncke, 2025b) as a possible implementation but locates the
novel step in development from control relevance to bundles, bearer maps, and value-update
rules.
9.3
Homeostatic and allostatic reinforcement learning
Keramati and Gutkin derive reward from reduction of homeostatic drive and explain interactions
between reward collection and physiological stability (Keramati and Gutkin, 2014). Continuous
extensions allow internal variables to drift unless the agent repeatedly acts (Laurençon et al.,
2021). Modular agents with competing homeostatic drives can improve sample efficiency and
out-of-domain robustness (Dulberg et al., 2022). Deep homeostatic RL has produced integrated
foraging and thermoregulatory behavior (Yoshida et al., 2024). Reward Bases provides a
complementary decomposition into reward-specific value functions weighted by current needs
15

---

(Millidge et al., 2024).
These models are close to the proposed mechanism but usually define the internal variables,
body boundary, and value bases in advance. The policy implementation itself is rarely a degrad-
able world-state pattern. Horibe and Yoshida’s “mortal agents” explicitly treat homeostasis
as an open-ended objective that may induce implicit world models, but the proposal remains
preliminary (Horibe and Yoshida, 2024). Christov-Moore et al. come closest conceptually by
requiring that sensors, policy, and actuators be parts of the environment and that the agent drift
toward terminal states unless it acts (Christov-Moore et al., 2026). Their account also proposes
that reliable control and shared vulnerability can expand self-boundaries. The Entropic Ecology
Transfer Test adds a matched causal comparison among protected, task-only, viability-shaped,
and evolved value-update architectures.
9.4
Evolution of preferences and moral pluralism
Indirect evolutionary models permit preferences that do not equal material fitness because
behavior is chosen according to preferences while selection evaluates consequences (Dekel et al.,
2007). Assortative matching and incomplete information can support other-regarding preferences
(Alger and Weibull, 2013). Recent work extends this line toward the evolutionary stability of
plural moral foundations (Avataneo et al., 2025). These results support the claim that selection
need not produce an explicit scalar survival utility. Cultural selection can nevertheless decouple
bundle contents from long-horizon regulatory goods (Zarncke, 2026c).
The present theory differs in three ways. It treats values as learned bundle coordinates rather
than complete preference orderings; it includes a represented-self map and bearer maps; and it
makes the update rule U itself a target of selection. This creates a direct place for environmental
mismatch, developmental abstraction, and the rigidity–plasticity tradeoff.
9.5
Artificial life and emergent boundaries
Artificial-life research has long modeled protocells, self-maintaining chemistry, and autonomous
organization. Recent diversity search has discovered robust sensorimotor entities in cellular
automata without predefining conventional bodies (Hamon et al., 2025). This is the most
relevant substrate for the stronger version of the experiment in which the agent boundary is
inferred rather than supplied. The remaining gap is to add learned high-level objectives and
compare the stability of goal attribution with and without precarious self-maintenance.
9.6
AI instrumental convergence
AI safety discussions usually treat self-preservation as an instrumental consequence of arbitrary
terminal objectives (Omohundro, 2008; Turner et al., 2021). That result is compatible with
the present thesis but addresses a different level. Instrumental convergence asks which policies
follow from a fixed objective. Viability-constrained value formation asks which learned objective
architectures remain prevalent when the objective-bearing process is itself mutable, costly, and
selected. A paperclip objective may produce self-preservation; yet, if faithful goal transmission
is costly, mutants that weaken paperclip production can out-replicate faithful descendants.
Goal-content integrity is therefore one possible maintained structure, not an unconditioned law.
16

---

10
Discussion
10.1
What explanatory power is gained?
The framework earns explanatory power only if one latent viability-centered organization
predicts several behaviors that otherwise require separate objectives: repair, buffering, retreat,
redundancy, conservative exploration, partner protection, and calibrated value revision. If each
behavior must be independently rewarded, the thesis reduces to a verbal redescription.
It earns predictive power by distinguishing matched agents. A protected controller and an
embedded controller can implement the same nominal policy, yet diverge as internal damage
increases. A task-only and a viability-shaped learner can receive the same degradation experience,
yet diverge on novel module failures. A fixed-value and an adaptive-value lineage can begin
with the same values, yet diverge after repeated ecological reversal. These are not consequences
of the claim that “survival matters” alone.
10.2
Why arbitrary values remain possible
The theory does not establish a logical impossibility theorem for arbitrary values. A designer
can instantiate any computable reward function in a protected machine. An arbitrary value
can persist in a wealthy patron’s protected niche. A neutral cultural ornament may survive
indefinitely at finite population size. A costly value may be inseparable from a beneficial package.
The claim is dynamical:
Values are not free coordinates once their carrier, learning process, and transmission
are endogenous to a changing ecology.
The admissible region is a viability-compatible manifold, not a single survival objective. Many
incompatible moral systems may lie on it.
10.3
The danger of adaptive values
Value plasticity is not automatically desirable. A highly plastic agent can be corrupted by local
rewards, manipulation, addiction-like dynamics, or adversarially supplied evidence. Human
institutions often protect values precisely because immediate adaptation would destroy long-
horizon coordination. The relevant target is therefore a calibrated update envelope: stable
enough to preserve accumulated structure and correction channels, plastic enough to revise
failed predictions.
This point also limits an alignment interpretation. Training artificial agents under mortality
or homeostasis does not make them morally aligned. It may increase self-preservation and
resource acquisition. The selfhood and bearer maps may exclude humans or include them only
instrumentally. Viability grounding can explain why values are structured without determining
which values humans should endorse.
10.4
Levels of continuation
Organism, lineage, coalition, institution, value pattern, and ecosystem continuation can conflict.
A sterile worker can reduce organism-level continuation while supporting lineage continuation.
A scientist can sacrifice comfort or safety for an epistemic institution. A reflective agent may
reject biological reproduction while preserving relationships, works, or principles. The model
handles these cases by making the continuation relation and \beta explicit. It does not decide
normatively which level is correct.
17

---

This explicitness also makes the thesis vulnerable. If no stable, prospectively predictive \beta
can be inferred, then “self” is doing too much retrospective explanatory work. In that case
the framework should retreat to the weaker claim that selection constrains value architectures
without claiming agents learn a coherent represented self.
10.5
Thermodynamic language
The term “entropic ecology” is evocative but can overstate the physics. Simulated decay, diffusion,
corruption, and irreversible deletion need not implement thermodynamic entropy faithfully.
The experimental variable is better described as precariousness, maintenance dependence, or
endogenous degradation. Thermodynamic claims should be reserved for implementations with
explicit energy and entropy accounting.
11
Conclusion
Standard agent models make arbitrary objectives easy by protecting the machinery that carries
them. Fully embedded agents receive no such metaphysical subsidy. Their capacity to sense,
remember, compute, act, and learn persists only while a world process maintains it. The
resulting constraint does not imply a single terminal survival value. It suggests a layered
architecture: local regulatory loops generate control relevance; learning compresses recurrent
regularities into value bundles; bearer and selfhood maps determine what those bundles apply to
and what counts as continuation; and an update rule balances value integrity against ecological
adaptation.
Selection acts on this whole architecture.
Particular values may be mistaken, neutral,
obsolete, subsidized, or locally self-destructive. Yet under persistent variation and competition,
architectures that systematically sever learned valuation from the conditions of their own
continued realization lose relative prevalence. Arbitrary values are therefore instantiable but
not dynamically free.
The proposed Entropic Ecology Transfer Test makes the claim empirical.
Its decisive
comparison is not between an agent trained with and without decay, but between agents receiving
matched degradation exposure with different motivational and architectural organization.
Evidence for the theory would be transfer to novel internal damage, compact representations
of recoverability, causal selfhood maps, and calibrated revision of obsolete values. Equivalent
performance from ordinary task optimization would reduce the theory to familiar robustness
and reward-shaping results. That is a useful risk for the proposal to take.
Acknowledgements
This manuscript develops ideas from the author’s prior work on free-energy loops, the Loop–
Hub–Control–Value model, value bundles, bearer maps, and embedded agent boundaries. It
remains a theoretical proposal and experimental agenda rather than an established account of
human value formation.
References
Ingela Alger and Jörgen W. Weibull. Homo moralis—preference evolution under incomplete
information and assortative matching. Econometrica, 81(6):2269–2302, 2013.
18

---

W. Ross Ashby. Design for a Brain: The Origin of Adaptive Behaviour. Chapman & Hall,
London, 1952.
W. Ross Ashby. An Introduction to Cybernetics. Chapman & Hall, London, 1956.
Jean-Pierre Aubin. Viability Theory. Birkhäuser, Boston, 1991.
Marco Avataneo, Thomas Norman, and Nicola Persico. The evolutionary stability of moral
foundations. Quarterly Journal of Economics, 140(3):2459–2507, 2025.
Xabier E. Barandiaran, Ezequiel A. Di Paolo, and Marieke Rohde. Defining agency: Individuality,
normativity, asymmetry, and spatio-temporality in action. Adaptive Behavior, 17(5):367–386,
2009.
Lisa F. Barrett and W. Kyle Simmons. Interoceptive predictions in the brain. Nature Reviews
Neuroscience, 16:419–429, 2015.
Randall D. Beer and Ezequiel A. Di Paolo. The theoretical foundations of enaction: Precarious-
ness. BioSystems, 223:104823, 2023.
Leonardo Christov-Moore et al. The conditions of physical embodiment enable generalization
and care. arXiv preprint arXiv:2510.07117, 2026. version 3.
Eddie Dekel, Jeffrey C. Ely, and Okan Yilankaya. Evolution of preferences. Review of Economic
Studies, 74(3):685–704, 2007.
Abram Demski and Scott Garrabrant. Embedded agency. arXiv preprint arXiv:1902.09469,
2019.
Ezequiel A. Di Paolo. Autopoiesis, adaptivity, teleology, agency. Phenomenology and the
Cognitive Sciences, 4(4):429–452, 2005.
Zachary Dulberg, Rachit Dubey, Irene M. Berwian, and Jonathan D. Cohen. Modularity
benefits reinforcement learning agents with competing homeostatic drives. arXiv preprint
arXiv:2204.06608, 2022.
Karl Friston. The free-energy principle: a unified brain theory? Nature Reviews Neuroscience,
11(2):127–138, 2010.
Guillaume Hamon et al. Discovering sensorimotor agency in cellular automata using diversity
search. Science Advances, 11:adp0834, 2025.
Connor F. Hayes et al. A practical guide to multi-objective reinforcement learning and planning.
Autonomous Agents and Multi-Agent Systems, 36:26, 2022.
Kazuki Horibe and Naoki Yoshida. Emergence of implicit world models from mortal agents.
arXiv preprint arXiv:2411.12304, 2024.
Mehdi Keramati and Boris Gutkin. Homeostatic reinforcement learning for integrating reward
collection and physiological stability. eLife, 3:e04811, 2014.
Michael D. Kirchhoff, Thomas Parr, Ester Palacios, Karl Friston, and Julian Kiverstein. The
Markov blankets of life: Autonomy, active inference and the free energy principle. Journal of
the Royal Society Interface, 15:20170792, 2018.
Hugo Laurençon, Charles-Raphaël Ségerie, Johannes Lussange, and Boris S. Gutkin. Continuous
homeostatic reinforcement learning for self-regulated autonomous agents. arXiv preprint
arXiv:2109.06580, 2021.
19

---

Beren Millidge et al. Reward bases: A simple mechanism for adaptive acquisition of multiple
reward types. PLoS Computational Biology, 20(6):e1012580, 2024.
Stephen M. Omohundro. The basic AI drives. In Artificial General Intelligence 2008, volume
171 of Frontiers in Artificial Intelligence and Applications, pages 483–492. IOS Press, 2008.
Tim Sainburg and Caleb Weinreb.
The Cartesian cut in agentic AI.
arXiv preprint
arXiv:2604.07745, 2026.
Shalom H. Schwartz. Universals in the content and structure of values: Theoretical advances
and empirical tests in 20 countries. In Mark P. Zanna, editor, Advances in Experimental
Social Psychology, volume 25, pages 1–65. Academic Press, 1992.
Anil K. Seth and Karl J. Friston. Active interoceptive inference and the emotional brain.
Philosophical Transactions of the Royal Society B, 371:20160007, 2016.
Peter Sterling. Allostasis: A model of predictive regulation. Physiology & Behavior, 106(1):
5–15, 2012.
Alex M. Turner, Logan Smith, Rohin Shah, Andrew Critch, and Prasad Tadepalli. Optimal
policies tend to seek power. In Advances in Neural Information Processing Systems, volume 34,
2021.
Francisco G. Varela, Humberto R. Maturana, and Ricardo Uribe. Autopoiesis: The organization
of living systems, its characterization and a model. BioSystems, 5(4):187–196, 1974.
Naoki Yoshida et al.
Emergence of integrated behaviors through direct optimization for
homeostasis. Neural Networks, 177:106371, 2024.
Gunnar Zarncke. From free-energy loops to human values: Hubs as bottlenecks. Companion
manuscript, brain-to-values research program, 2025a. aintelope.
Gunnar Zarncke.
Stratification of Free–Energy–Minimising loops in the vertebrate brain.
Companion manuscript, brain-to-values research program, 2025b. AE Studio.
Gunnar Zarncke. From free-energy loops in the brain to human values. Companion manuscript,
brain-to-values research program, 2026a. aintelope.
Gunnar Zarncke. A unit of caring: Integrity pressure, suffering, and cross-scale aggregation.
Companion manuscript, brain-to-values research program, 2026b. aintelope.
Gunnar Zarncke. Selection-channel alignment or the limits of harsh correction. Companion
manuscript, brain-to-values research program, 2026c. aintelope.
20
