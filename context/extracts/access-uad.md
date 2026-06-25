# Extract: access-uad.pdf

**Source PDF:** `context/access-uad.pdf`
**Extract:** `context/extracts/access-uad.md`
**Pages:** 11
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

Handles Before Interventions:
Access-Model UAD and the Embedded Semantics of
Agency Tests
Gunnar Zarncke
AE Studio
June 24, 2026
Abstract
Unsupervised Agent Discovery (UAD) [1] is usually stated as if the observer receives
variables, partitions them into internal, sensory, active, and external components, and then
applies conditional-independence or control-information tests. This paper argues that this
picture is too shallow for real systems.
In laboratories, software audits, social systems,
biological assays, recommender platforms, and human interaction, neither “intervention”
nor “interface” is primitive. What the observer has are handles: embedded access points
through which the system may be observed or operated upon. A handle has observational
semantics, operational semantics, cost, latency, reversibility, spillover, and uncertain uptake.
Causal graph interventions such as do(Xi = x) [2] are idealizations of rare depth-zero cases.
We introduce an access-model formulation of UAD in which the data are generated through
observation kernels and operation kernels. Agent loops, interfaces, and interventions are then
inferred jointly. The resulting Bayesian/regularized objective draws on blanket-information
competence scoring [3] and treats agency as posterior mass over handle-mediated control-
loop hypotheses, not as a label on a raw time series. We prove an impossibility result: no
method can distinguish agent structures that are equivalent under the available access model.
We then give a margin-style recovery bound for finite candidate classes, an intervention-value
criterion based on expected information gain over agent-loop posteriors, and a sparse layer-
wise regularization scheme that encourages interpretable causal roles at every scale while
allowing full agency only at selected coarse-grained bottlenecks. The framework explains
why algorithmic feeds and advertising systems can manipulate humans while hiding agency:
users see content handles but lack access to objective, ranking, telemetry, and policy-update
handles. Interface forcing is therefore not merely convenience; it is access-channel design.
1
Motivation
UAD begins from an appealing mathematical fantasy. There is a dynamical system
Xt = (X1(t), . . . , Xn(t)),
and one seeks a subset C ⊆{1, . . . , n} with an internal–sensory–active–external decomposition

$$
C = IC \cupSC \cupAC, EC = {1, . . . , n} \ C,
$$

such that
J(C) := I
IC
t+1; EC
t+1 | SC
t , AC
t

\approx0.
(1) The test says: conditional on sensory and active boundary variables, internal and external futures are approximately screened off.
This is a useful formal target. But it hides a prior ontological assumption: the observer has
already been given the right variables at the right scale and knows enough of the interface to
1

---

call some variables sensory and some active. Likewise, when we say “intervene on Xi”, we often
implicitly assume the Pearlean ideal [2]
do(Xi = x),
as if the observer could surgically set one coordinate of the system. Real systems rarely offer
such access. A chemical perturbation changes many pathways. A prompt changes a distribution
over latent computations. A platform audit flag changes incentives, ranking policies, and future
strategic behavior. A social request is interpreted by another agent with its own beliefs. Even
a laboratory apparatus has uptake, delay, measurement error, spillover, and constraints.
Thus the primitive of intervention-capable UAD should not be a variable. It should be a
handle.
A handle is an access point with observational and/or operational semantics.
The
observer does not perform do(Xi = x); the observer applies an operation u through a handle h,
producing a stochastic change in future observations:

$$
u@h ⇝P(Yt+1:t+H | Y\leqt, u, h). The question becomes: given an access model, what agent loops are identifiable, and which
$$

handle-operations should be used to test them?
2
Worlds, Observations, and Handles

$$
Let (Xt)t\geq0 be an unobserved world process with state space X. The observer does not see Xt
$$

directly. Instead, observations arrive through a set of handles.
Definition 1 (Observation handle). An observation handle is a tuple

$$
hY = (Yh, Kh, ℓh, \sigmah, ch), where Yh is the handle’s observation space,
$$

$$
Kh : X \times X −\to∆(Yh) is an observation kernel possibly depending on current and recent world states, ℓh is latency, \sigmah
$$

is an uncertainty or resolution descriptor, and ch is the cost of using the handle. The observed
datum is
Y h
t ∼Kh(· | Xt−ℓh:t).
Definition 2 (Operation handle). An operation handle is a tuple

$$
hU = (Uh, \Gammah, \rhoh, \chih, ch), where Uh is a space of available operations,
$$

$$
\Gammah : X \times Uh \to∆(X) is an operation kernel, \rhoh is reversibility, \chih describes constraints or legality, and ch : Uh \toR\geq0
$$

is operation cost. Applying operation u \inUh at time t induces

$$
Xt+1 ∼\Gammah(· | Xt, u) or, more generally, a finite-horizon kernel
$$

$$
Xt+1:t+H ∼\GammaH h (· | X\leqt, u).
$$

2

---

Definition 3 (Access model). An access model is

$$
A = (HY , HU, K, \Gamma, Cost, Risk, C), where HY is a family of observation handles, HU a family of operation handles, K = {Kh}h\inHY ,
$$

$$
\Gamma = {\Gammah}h\inHU , Cost and Risk assign costs and risks to handle-use, and C encodes constraints
$$

on allowable observations and operations.
The data available to UAD are therefore not merely X1:T but
DT = {(hY
t , yt), (hU
t , ut), contextt}T

$$
t=1, together with partial knowledge or priors over K and \Gamma.
$$

Remark 1. The passive time-series case is recovered by taking HU = ∅and a single observation

$$
handle hY with Yt = Xt+\etat. The classical UAD setting [1,4,5] is therefore a special, high-access,
$$

low-embedding case.
3
From Variables to Handles
In classical causal notation [2], intervention is represented as graph surgery:
P(X−i | do(Xi = x)).
The handle view replaces this with an operation kernel:

$$
P(Yt+1:t+H | D\leqt, u, h). The relationship between the two is approximate and itself inferential.
$$

Definition 4 (Effective target distribution). For operation u through handle h, define the
effective target posterior

$$
\tauh,u(i) := P(Xi is directly affected by (h, u) | D) .
$$

The spillover posterior is
ςh,u(j) := P(Xj is indirectly affected by (h, u) | D) .
An ideal intervention is one with concentrated \tau and low ς:

$$
H(\tauh,u) \approx0, ∥ςh,u∥1 −max
$$

i
\tauh,u(i) \approx0.
Most real interventions have broad target and spillover distributions.
Definition 5 (Intervention depth). The depth of an operation u@h relative to a hypothesized
target variable Xi is the minimal causal path length, in the observer’s current structural poste-
rior, from the operation event Ut = (h, u) to Xi. Depth zero corresponds to do(Xi = x). Depth
one corresponds to a known actuator on Xi. Depth two or greater corresponds to mediated
perturbations through apparatus, environment, norms, incentives, language, or other agents.
The depth notion is not intended as a fixed graph invariant. It is posterior and access-
relative:
P(depth(u@h, Xi) = d | D).
3

---

4
Interfaces as Coupling Surfaces
A sensor/action interface is not generally a set of raw variables. It is a stable coupling surface,
often constructed by an observer.
Let C be a candidate system and E its complement at some representation level. A candidate
interface Q is a handle-mediated representation of coupling between C and E.
Definition 6 (Candidate interface). A candidate interface for C is

$$
Q = (QS, QA, KQ, \GammaQ), where QS are candidate sensory handles/channels, QA candidate active handles/channels, KQ
$$

describes how interface observations are produced, and \GammaQ describes how interface operations or
outputs affect the world.
The interface should approximately screen off internal and external futures:
JQ(C) := I(Ct+1; Et+1 | Qt)
small.
(2) For directed sensor/action roles, define the asymmetric information scores RS(Q; C) = I(Et; QS t | Ct) + I(QS
t ; Ct+1 | Ct),
(3) RA(Q; C) = I(Ct; QA t | Et) + I(QA t ; Et+1 | Et). (4)
These are not sufficient for agency, but they localize candidate inbound and outbound channels.
Definition 7 (Handle interface score). For candidate C and interface Q, define

$$
I(C, Q) = −JQ(C) + \alphaSRS(Q; C) + \alphaARA(Q; C) −\lambdaQ DL(Q) + µQ Manip(Q).
$$

(5) Here Manip(Q) measures whether available operation handles can selectively affect or read the interface:
Manip(Q) = max

$$
h,u I(u; Qt+1:t+H | D\leqt, h). Remark 2. Interface forcing is the deliberate construction of a high-I(C, Q) access channel.
$$

An API, laboratory assay, telemetry schema, randomized audit interface, or standardized social
probe is not merely a measurement. It changes the access model and may change the system.
5
Agent-Loop Hypotheses
An agent-loop hypothesis is a structured explanation of a candidate bounded process as a
stateful control system.
Definition 8 (Agent-loop hypothesis). An agent-loop hypothesis is

$$
Ω= (C, Q, B, G, \pi, V, \Theta), where C is a candidate boundary, Q = (QS, QA) a candidate interface, Bt a latent belief or
$$

$$
information state, Gt a latent goal/preference/viability state, \pi a policy, V a viability or objective
$$

functional, and \Theta additional parameters. The model class induced by Ωpredicts observations
and responses by

$$
Bt+1 ∼U\Theta(Bt, QS t+1, QA
$$

t ),

$$
(6) Gt+1 ∼R\Theta(Gt, Bt, Qt),
$$

$$
(7) QA t ∼\pi\Theta(· | Bt, Gt),
$$

$$
(8) Yt+1 ∼P\Theta(· | Bt+1, Gt+1, QA
$$

t , Et).
(9) The latent variables Bt and Gt need not be internal physical states. They are explanatory coordinates under which behavior compresses and interventions become predictable.
4

---

6
Bayesian Access-Model UAD
The full posterior should include both agent-loop hypotheses and access semantics:
P(Ω, K, \Gamma, Q | DT ).
This is the core object. It replaces both “detect an agent in a time series” and “intervene on a
variable”.
Definition 9 (Access-model posterior). Given priors over access semantics and loop hypotheses,
P(Ω, K, \Gamma, Q | DT ) ∝P(DT | Ω, K, \Gamma, Q)P(Ω| Q)P(Q | K, \Gamma)P(K, \Gamma).
(10) To make this computationally tractable, use an energy parameterization: P(Ω, Q | DT ) ∝exp[−E(Ω, Q; DT )].
A generic energy is

$$
E(Ω, Q; DT ) = \lambdaJJQ(C) −\lambdaCIctrl(Ω) −\lambdaP Rpersist(Ω)
$$

$$
−\lambdaBRbelief(Ω) −\lambdaV Rviability(Ω) −\lambdaL∆LEIS(Ω)
$$

$$
−\lambdaM Manip(Q) + \kappaΩDL(Ω) + \kappaQ DL(Q) + \kappaA DL(K, \Gamma). (11)
$$

where ∆LEIS is the intentional compression gain [6].
The terms have the following intended meanings:
Ictrl(Ω) = I(QA
t ; Et+1:t+H | Et, QS
t ),

$$
(12) Rpersist(Ω) = I(Gt; Gt+k) −\etaGH(Gt),
$$

$$
(13) Rbelief(Ω) = I(QA
$$

t ; Bt | Et, Gt),

$$
(14) Rviability(Ω) = E[∆Vt:t+H | \piΩ] −E[∆Vt:t+H | \pinull],
$$

$$
(15) ∆LEIS(Ω) = log P(DT | Mbelief/goal, Ω) −log P(DT | Mnull, Q) −\lambdaint DL(Mbelief/goal).
$$

(16) Remark 3. The non-agentic baseline should not be an unconstrained universal predictor. A powerful predictor can absorb agentic regularities without representing agent loops. Instead, the
null family should consist of constrained causal topologies: passive dynamics, reactive dynamics,
scripted dynamics, field dynamics, and habitual dynamics without intervention-sensitive goals.
7
Null Models as Restricted Topologies
Let
M = {MA, M1
0 , . . . , Mk
0 },
where MA is an agent-loop model and Mi
0 are restricted alternatives.
The posterior agent
probability is
P(MA | D) =
P(D | MA)P(MA)
P(D | MA)P(MA) + P
i P(D | Mi
0)P(Mi
0).
(17) Useful nulls include: Mpassive 0 :

$$
Xt+1 = F(Xt) + \etat, (18)
$$

Mreactive
0
:
QA
t = f(QS

$$
t ) + \etat, (19)
$$

Mscript
0
:
QA

$$
t = f(t, context) + \etat, (20)
$$

Mfield
0
:

$$
Xt+1 = Fglobal(Xt) + \etat, (21)
$$

Mhabit
0
:
QA
t = f(QS
\leqt, QA

$$
<t) + \etat, (22)
$$

where none includes a persistent goal variable that remains stable under changed means and
predicts counterfactual policy adaptation.
5

---

8
Layered Role Regularization
It is too strong to require agentic structure at every representation layer. Low-level features
may be pixels, tokens, molecules, or local dynamical modes. They need not be agentic. But
they should become locally understandable.
Let a representation learner produce layers
Z0
t = Xt,
Zℓ
t = fℓ

$$
\theta(Zℓ−1 \leqt ).
$$

At each layer ℓ, introduce soft role masks
mℓ
C, mℓ
Q, mℓ
E, mℓ
B, mℓ
G \in[0, 1]dℓ.
Use role regularization at all layers:
Rℓ

$$
role = \rho1Rℓ persistence + \rho2Rℓ
$$

$$
locality + \rho3Rℓ separability + \rho4Rℓ
$$

$$
causal−handle −\rho5Rℓ degenerate. (23)
$$

But introduce sparse agent-loop gates
aℓ

$$
C \in{0, 1} and apply the full agent score only when aℓ
$$

C = 1:
L = Lpred −
X
ℓ
\lambdaroleRℓ
role −
X
ℓ,C
q(aℓ

$$
C = 1)\lambdaagentRℓ agent(C) + \tau
$$

X
ℓ,C
DKL

q(aℓ
C) ∥p(aℓ
C)

.
(24) The prior p(aℓ C = 1) is sparse. Most regions at most layers are not agents. Definition 10 (Agentic structure prior). For a layer ℓand candidate C,
p(Ωℓ
C) ∝exp

Rℓ

$$
agent(C) −\kappa DL(Ωℓ C)
$$

.
Thus agentic regularization is the log prior over latent loop structures.
9
Coarse-Graining and Hierarchical Agency
Representation layers are not necessarily ontological layers.
Hierarchy should therefore be
searched over coarse-graining operators

$$
K\sigma,\tau : X1:T \toZ\sigma,\tau 1:T ,
$$

$$
where \sigma denotes variable/spatial aggregation and \tau temporal aggregation. Define
$$

$$
ScaleAgent(C) = E\sigma,\tau [Ragent(C; K\sigma,\tau)] −\lambdavar Var\sigma,\tau [Ragent(C; K\sigma,\tau)] .
$$

(25) A hierarchical agent is a stable basin in scale-space, not merely an activation in a neural-network
layer.
10
Identifiability Under Access Models
The access model determines what can be known.
Definition 11 (Access equivalence). Two agent-loop hypotheses Ωand Ω′ are equivalent under
access model A, written Ω∼A Ω′, if for every admissible observation and operation policy \nu
over handles,

$$
PΩ(D\nu T | A) = PΩ′(D\nu
$$

T | A)
\forallT.
The recoverable target is the equivalence class
[Ω]A = {Ω′ : Ω′ ∼A Ω}.
6

---

Theorem 1 (Access-model impossibility). If Ω∼A Ω′, then no UAD procedure whose inputs
are restricted to data generated through A can distinguish Ωfrom Ω′ with probability better than
chance under all priors assigning equal mass to Ωand Ω′.
Proof. By access equivalence, every admissible data-generating distribution is identical under
Ωand Ω′. Hence the likelihood ratio is identically one:
P(DT | Ω, A)
P(DT | Ω′, A) = 1.
With equal prior mass, posterior odds remain one for all T and all admissible operation policies.
Any decision rule must therefore have symmetric error.
Remark 4. This theorem is the handle-level analogue of observation-channel non-identifiability.
If the access model hides the objective, policy update, telemetry, or actuator channels of a
platform, then user-level observations may not distinguish an optimizing recommender from a
non-agentic content stream with matching distribution.
11
Finite Candidate Recovery
Let O be a finite class of candidate loop/interface hypotheses. Let SA(Ω) be a population score,
for example the negative energy in Eq. (11), and bSA(Ω) its empirical estimate.
Assumption 1 (True recoverable class). There is a true access-equivalence class [Ω⋆]A.

$$
Assumption 2 (Access margin). For all Ω/\in[Ω⋆]A,
$$

$$
SA(Ω⋆) −SA(Ω) \geq∆A > 0. Assumption 3 (Access distortion). The implemented handles and estimated kernels distort the
$$

ideal access score by at most
sup
Ω\inO
|S b

$$
A(Ω) −SA(Ω)| \leq\deltaA. Assumption 4 (Uniform concentration). For all ϵ > 0,
$$

P

sup
Ω\inO
|bS b
A(Ω) −S b
A(Ω)| > ϵ

$$
\leq2|O| exp
$$

−Teffϵ2
2B2

.
Theorem 2 (Handle-recovery bound). Let
bΩ\inarg max
Ω\inO
bS b
A(Ω).
If

$$
∆A > 2\deltaA, then
$$

P
h

$$
bΩ\in[Ω⋆]A i
$$

$$
\geq1 −2|O| exp
$$

$$
−Teff(∆A −2\deltaA)2 8B2
$$

.

$$
Proof. For any Ω/\in[Ω⋆]A, S b
$$

A(Ω⋆) −S b

$$
A(Ω) \geqSA(Ω⋆) −SA(Ω) −2\deltaA \geq∆A −2\deltaA. If empirical deviation is less than (∆A −2\deltaA)/2 uniformly, no non-equivalent candidate can
$$

beat the true class. Apply the concentration assumption with this value.
7

---

12
Intervention Selection as Handle-Operation Planning
Given posterior

$$
P(Ω, K, \Gamma, Q | D), a test is not an abstract do(Xi = x) but a handle-operation pair (h, u). Its value is expected
$$

posterior contraction.

$$
Definition 12 (Expected information gain of a handle-operation). For u \inUh,
$$

EIG(h, u) = Ey′∼P(·|D,h,u)

DKL
P(Ω| D, h, u, y′) ∥P(Ω| D)

.

$$
(26) The recommended test is (h⋆, u⋆) = arg max h,u [EIG(h, u) −\lambdac Cost(h, u) −\lambdar Risk(h, u) −\lambda\chi1{(h, u) /\inC}] .
$$

(27) Proposition 1 (Diagnostic separation form). Suppose two hypotheses Ω1, Ω2 dominate the posterior. Let
ph,u
i
(y′) = P(y′ | Ωi, D, h, u).
Then, up to posterior weights, EIG(h, u) is increasing in the predictive separation
DKL(ph,u
1 ∥ph,u
2 ) + DKL(ph,u
2 ∥ph,u
1 ).
Thus good interventions are handle-operations for which competing loop hypotheses make dif-
ferent downstream predictions.
13
Agency Tests as Handle Tests
The usual intuitive agency tests become precise only when indexed by handles. Table 1 gives
the translation.
Suspected
struc-
ture
Handle operation
Diagnostic contrast
Sensor
channel
QS
hide, delay, corrupt, amplify input
handle
behavior tracks information rather than
world state
Action
channel
QA
block, attenuate, reroute output
handle
environmental control collapses or compen-
sates
Goal/resource G
move,
remove,
revalue resource
handle
means change while latent target persists
Belief state B
false cue, occlusion, asymmetric
information
action follows belief rather than actual state
Policy \pi
change cost,
risk,
payoff,
time
pressure
action trades off costs approximately coher-
ently
Boundary C
separate, perturb, damage, con-
strain coupling
repair, compensation, or loss of autonomy
Communication
cut, corrupt, delay signal handle
coordination degrades predictably
Model
of
other
agent
alter partner behavior or apparent
belief
anticipation, teaching, deception, or adap-
tation
Self-maintenance
resource stress, load, disruption
actions preserve viability variables
Table 1: Agency tests rephrased as embedded handle operations.
8

---

14
Language as a High-Bandwidth Handle
Language is special because it makes latent control variables queryable. A non-linguistic ob-
server sees trajectories:
QS
t , QA
t , QS
t+1, QA
t+1, . . .
and must infer Bt, Gt, \pi. A linguistic system emits public symbols that purport to describe
these latents:

$$
Bt 7\to⌜Bt⌝, Gt 7\to⌜Gt⌝,
$$

\pit 7\to⌜\pit⌝.
This does not guarantee truth.
In adversarial settings, self-reports may be strategic.
But
language changes the access model by adding handles:
hask,
hchallenge,
hexplain,
hcommit,
hcounterfactual.
These handles can generate high expected information gain when the system is cooperative or
only weakly adversarial.
15
Algorithmic Feeds as Hidden Agent Loops
An algorithmic feed illustrates handle failure. A user observes:
content item \toreaction \tonext content item.
But the relevant loop is closer to:
platform objective \toranking policy \touser-state perturbation \totelemetry \topolicy update.
The user lacks handles for:
Gplatform,
QA
ranking,
QS
telemetry,
\piupdate,
auction and advertiser constraints.
Thus user-level observations can be explained as local content variation even when a distributed
optimization loop is acting on the user. Agency is hidden not because the loop is weak, but
because the access model is poor.
A meaningful audit interface would expose at least:
candidate set,
ranking action,
objective contribution,
targeting features,
measured response,
policy update.

$$
Such an interface changes K and \Gamma, increasing the recoverable margin ∆A and shrinking access-
$$

equivalence classes.
16
Data Contracts
Access-model UAD requires different claims for different data tiers.
Definition 13 (Tiered data contract). Tier 1: Passive access:
D = (Y1:T , K).
The system can generate candidate loops but cannot make strong causal claims.
Tier 2: Manipulable access:

$$
D = (Y1:T , K, HU, \Gamma, Cost, Risk). The system can recommend handle-operations and update loop posteriors from their
$$

outcomes.
9

---

Tier 3: Interface-exposed access:
D = (QS
t , QA
t , Rt, updatet, Yt+1)T
t=1. The system can audit a largely exposed control loop. The same mathematical model can operate at all tiers, but the strength of conclusions
differs:
passive discovery < causal testing < loop auditing.
17
Practical Algorithm

### 1. Fit access model. Estimate or encode observation kernels Kh, operation kernels Γh, costs,

risks, legal constraints, and handle semantics.

### 2. Learn representations. Produce multi-scale representations Zσ,τ through coarse-graining,

prediction, and event segmentation.

### 3. Propose candidates. Use amortized heads to propose

q\phi(C, Q, B, G, \pi, M | D).

### 4. Score candidates. Evaluate explicit UAD/EIS/B-IQ-style energies [1,3,6]:

JQ(C),
Ictrl,
Rpersist,
Rbelief,
∆LEIS,
DL .

### 5. Infer posterior. Approximate

P(Ω, Q, K, \Gamma | D) by variational inference, MCMC, sequential Monte Carlo, or energy-based reranking. 6. Select test. Choose (h, u) maximizing Eq. (27).

### 7. Update. Observe outcome y′ and update posterior. Stop when posterior mass over agent-

loop equivalence classes is sufficiently concentrated or when further tests are too costly.
18
Discussion
The handle approach changes the ontology of intervention-capable UAD. It says: do not start
with variables and interventions. Start with access. Variables, interfaces, interventions, and
intentions are all high-level abstractions over embedded dynamics.
This has several consequences.
First, agency claims become conditional:
“agentic under access model A”.
No method can recover distinctions erased by A.
Second, intervention suggestion becomes scientifically meaningful only when operation se-
mantics are modeled. A recommendation such as “perturb variable Xi” is often ill-posed. A
recommendation such as “use handle h with operation u because hypotheses Ω1 and Ω2 predict
different outcomes” is well-formed.
Third, interface forcing is access-channel design. It may improve identifiability, but it may
also distort the system. The correct question is whether the forced interface is faithful enough
for the target agency claim.
10

---

Fourth, layer-wise regularization should be weakened. Lower layers should be regularized
toward stable, local, separable, and manipulable roles. Full agent-loop regularization should be
sparse and scale-selective.
Fifth, adversarial systems break naive EIS [6, 7]. If a system optimizes its outputs to im-
itate the sufficient statistics of agency while hiding its loop, behavioral compression alone is
insufficient. One needs handle diversity, hidden tests, costly perturbations, or enforced audit
interfaces.
19
Conclusion
Intervention, interface, and intention are all compressed names for deep embedded stacks.
Causal graphs make intervention look primitive; real systems provide handles.
Intentional
explanations make goals look primitive; real agents expose or hide them through behavior, lan-
guage, and interface structure. UAD [1] should therefore be formulated relative to an access
model:

$$
A = (HY , HU, K, \Gamma, Cost, Risk, C). Given A, the target of discovery is not an agent simpliciter but a posterior over handle-mediated
$$

loop hypotheses:
P(C, Q, B, G, \pi, K, \Gamma | D).
The recoverable object is an access-equivalence class. The appropriate test is not do(Xi = x)
but a handle-operation chosen by expected information gain. The practical path is therefore:

$$
access modeling \torole-regularized representation learning
$$

\tosparse agent-loop inference \tohandle-based experimental design.
This makes UAD less elegant but more real. It also explains why hidden optimization systems
such as algorithmic feeds are hard for humans to perceive: they act through the handles we see
while hiding the handles that would reveal the agent loop.
References
[1] G. Zarncke, “Foundations of unsupervised agent discovery in raw dynamical systems,” AE
Studio, 2025.
[2] J. Pearl, Causality: Models, Reasoning, and Inference, 2nd ed. Cambridge University Press,
2009.
[3] G. Zarncke, “Bitwise intelligence: A blanket–information measure of competence,” AE Stu-
dio, 2025.
[4] R. C. Conant and W. R. Ashby, “Every good regulator of a system must be a model of that
system,” International Journal of Systems Science, vol. 1, no. 2, pp. 89–97, 1970.
[5] M. D. Kirchhoff, T. Parr, E. Palacios, K. Friston, and J. Kiverstein, “The markov blankets of
life: autonomy, active inference and the free energy principle,” Journal of the Royal Society
Interface, vol. 15, no. 138, p. 20170792, 2018.
[6] G. Zarncke, “The endogenized intentional stance: A predictive–compression formalization
of agent discovery,” AE Studio, 2025.
[7] D. C. Dennett, The Intentional Stance.
Cambridge, MA: MIT Press, 1987.
11
