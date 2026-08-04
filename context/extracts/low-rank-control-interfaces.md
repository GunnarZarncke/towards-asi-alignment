# Extract: low-rank-control-interfaces.pdf

**Source PDF:** `context/low-rank-control-interfaces.pdf`
**Extract:** `context/extracts/low-rank-control-interfaces.md`
**Pages:** 21
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

Low-Rank Control Interfaces in Multiscale
Competency Architectures
A Causal Criterion for Coordination Across Scales
Gunnar Zarncke
July 2026
Abstract
Biological systems coordinate competent subsystems across scales without specifying
every lower-level action. Cells repair tissues, tissues restore anatomy, and organisms regulate
physiology despite perturbations that alter the microscopic implementation. Michael Levin
describes this organization as a multiscale competency architecture. We study one candidate
mechanism of cross-scale composition: a restricted control interface through which few
independent command directions preserve most of the viability obtainable by unrestricted
lower-level control.
The proposal is deliberately narrower than the claim that biological systems compress
information. We define a low-rank control interface by its contribution to finite-horizon
viability under a specified disturbance family. Two quantities suffice: a normalized viability-
retention curve RT (r; ∆), comparing the best rank-r interface with null and unrestricted-

$$
control baselines, and the minimal viability-preserving rank r\epsilon,T (∆). We connect these
$$

quantities to viability theory, feedback refinement relations, bisimulation, structural causal
models, and low-rank approximation.
Three formal results carry the argument. First, bidirectional feedback refinement makes
viability at a coarse scale equivalent to viability of the corresponding concrete states,
giving a precise condition under which a higher-level controller can ignore lower-level detail.
Second, for a locally linear disturbance-correction problem, the optimal rank-r interface
is determined by the leading singular directions of the whitened interventional response,
and the neglected singular-value tail yields an explicit upper bound on viability loss. Third,
observational data cannot identify causal interface rank: structural causal models with
identical observational distributions can have arbitrary different interventional ranks. We
operationalize the framework for bacterial chemotaxis and planarian morphogenesis, and
use muscle synergies as a negative control where observational low dimensionality does not
establish a low-rank controller. The framework may eventually shed light on human values
by separating the semantic complexity of learned value content from the dimensionality of
the channels through which it changes policy.
1
Introduction
A multicellular organism contains an enormous number of degrees of freedom, yet successful
regulation rarely resembles centralized micromanagement. A wound does not issue a complete
cell-by-cell construction plan. A nervous system does not normally command each motor unit
independently. A bacterial chemotaxis circuit does not represent every environmental molecule
at the motor. Across such cases, lower-level components absorb variation while a smaller set of
signals changes the larger-scale outcome.
This pattern is easy to overstate. Every interface discards detail, and almost every scientific
model reduces dimension. It would therefore be nearly vacuous to say that biological organization
relies on compression or bottlenecks. The substantive question is narrower:
1

---

Can a small number of independent intervention directions preserve a larger-scale
competency across perturbations, relative to what could be achieved with unrestricted
lower-level control?
This question is naturally situated inside Levin’s multiscale competency architecture (MCA)
framework Fields and Levin (2022); Levin (2023). MCA emphasizes that biological components
at many scales exhibit regulative plasticity: they pursue preferred regions in metabolic, physio-
logical, morphological, and behavioral problem spaces despite perturbations. The present paper
does not attempt to replace or subsume that program. It isolates one possible mechanism by
which competencies at adjacent scales compose.
The historical structural precursor is Simon’s near decomposability Simon (1962). In a
nearly decomposable system, within-module interactions dominate on short timescales, while
slower aggregate variables mediate interactions among modules. Near decomposability explains
why cross-scale variables may exist. It does not by itself show that a few such variables preserve
adaptive function under intervention.
Friston’s Markov-blanket framework supplies a related account of statistical boundaries
Friston (2010); Kirchhoff et al. (2018). A blanket identifies variables through which internal and
external states are conditionally coupled. A blanket may be large, and conditional independence
does not imply that a small set of intervention directions controls the system’s viable behavior.
Boundaries and low-rank control therefore answer different questions.
Pearl’s structural causal models (SCMs) supply the required distinction between observing
a variable and changing it Pearl (2009, 2010). An observationally predictive latent may be a
downstream readout, a common-cause proxy, or a mechanically induced correlation. A control
interface must be evaluated under interventions. This point matters especially in motor-control
and representation-learning settings, where low-dimensional observational structure is common
but causally ambiguous.
The mathematical center of the paper is viability theory Aubin (1991); Aubin et al. (2011).
A competency is represented operationally by a constraint or target set that the system can
remain in, return to, or reach despite disturbances. This does not imply that every biological
goal is literally a fixed set. It provides a standard and checkable approximation for a specified
experiment.
The paper makes four contributions.

### 1. It defines a rank-dependent viability-retention curve with explicit null and unrestricted-control

baselines.

### 2. It derives three results connecting multiscale control to feedback refinement, low-rank

interventional response, and causal non-identifiability.

### 3. It gives a common experimental protocol for bacterial chemotaxis, planarian morphogenesis,

and motor coordination.

### 4. It distinguishes the low rank of a control channel from low description length of the compe-

tencies or values implemented behind that channel.
The claim is conditional and falsifiable. Some multiscale competencies may require dis-
tributed, high-rank control. Others may use several context-dependent interfaces rather than
one stable interface. A system can also appear low-dimensional only because the experiment
explores a narrow task family. The proposed quantities are designed to expose these failures
rather than redescribe them as successes.
2
Conceptual and Technical Positioning
2.1
Levin: multiscale competency architectures
Fields and Levin characterize cognition in terms of navigation through problem spaces toward
preferred regions, allowing comparison across very different embodiments Fields and Levin
2

---

(2022). Levin further argues that development and regeneration exploit competent materials
whose local capabilities can be harnessed by evolution rather than constructed from passive
parts Levin (2023). The resulting MCA contains nested competencies: molecular networks
regulate chemical states, cells regulate cellular states, tissues regulate anatomy, and organisms
regulate behavior.
The central engineering advantage is delegation. A higher scale can specify a target or error
without specifying the lower-scale trajectory that realizes it. Lower-level competencies fill in
implementation detail, compensate for damage, and reuse existing physiological machinery.
We formalize this delegation with three standard objects:
MCA term
Control-theoretic counterpart used here
Preferred region or goal state
Target set, safe set, or terminal set K
Regulative plasticity
Viability or robust controlled invariance under a distur-
bance class
Cross-scale control interface
Restricted command space and a refinement map to
lower-level controls
Lower-level competency
Controller that realizes abstract commands while ab-
sorbing within-fiber disturbances
Problem space
State or output space in which success constraints are
defined
This translation is intentionally partial. MCA includes learning, goal plasticity, scale changes,
and the formation of new problem spaces. The current paper treats the simpler question of
preserving a specified competency over a specified horizon.
2.2
Simon: near decomposability
Simon observed that many complex systems are hierarchically organized and nearly decompos-
able: interactions within subsystems are stronger or faster than interactions between subsystems
Simon (1962). After fast local transients decay, aggregate variables can describe slower cross-
module dynamics. The proposal here can be viewed as an interventional strengthening of that
observation.
Near decomposability gives a timescale and coupling condition under which a coarse state
may be predictive. A low-rank control interface additionally requires that a restricted command
space preserve the relevant viability. The implication is one-way:

$$
near decomposability ̸\Rightarrowlow-rank viability-preserving control,
$$

but near decomposability can make such control possible by allowing local dynamics to
settle inside fibers of a coarse description.
2.3
Friston: boundaries and sufficient statistics
Markov blankets partition variables into internal, external, sensory, and active sets so that
internal and external states become conditionally independent given the blanket Friston (2010);
Kirchhoff et al. (2018). This is useful for locating candidate boundaries and candidate channels.
It does not determine whether the active states have low intervention rank, nor whether
interventions through them preserve a larger-scale competency.
A blanket is therefore best treated as a search-space restriction.
Once a boundary is
identified, the present framework asks how the viable behavior of the bounded system changes
when the available active-state interventions are restricted to a rank-r command family.
3

---

This distinction also clarifies the relation to unsupervised agent discovery (UAD), which
searches raw dynamics for approximate blanket-like boundaries Zarncke (2025b). UAD can
propose where an adaptive unit and its boundary might be. Low-rank control-interface discovery
asks which interventions through that boundary preserve the unit’s competency.
2.4
Pearl: intervention rather than association
For an SCM, the quantity
P(Y | Z = z)
describes an observational conditional, whereas
P(Y | do(Z = z))
describes the distribution after replacing the structural equation for Z by the assignment Z = z
Pearl (2009, 2010). The difference is not cosmetic. A low-dimensional Z may predict Y because
it is caused by Y , because both share a cause, or because task mechanics constrain them jointly.
Only the interventional distribution can establish that Z is a control channel.
Pearl’s machinery is used here at two levels. First, the response of a candidate interface
is defined interventionally. Second, the non-identifiability theorem in Section 4.3 shows that
observational data alone cannot identify causal interface rank, even with infinite samples and
exact knowledge of the joint distribution.
3
Formal Setting
3.1
Controlled dynamics and viability
Let a discrete-time controlled system be

$$
\Sigma = (X, U, W, F), where X is the state space, U the admissible control set, W the disturbance set, and
$$

xt+1 \inF(xt, ut, wt).
Set-valued dynamics allow uncertainty, unmodeled lower-level detail, and nondeterministic
responses. A deterministic system is the special case in which F is single-valued.
Let K ⊆X encode the competency-relevant constraint. For homeostasis, K may be a
physiological safe range. For regeneration, it may be the set of trajectories that terminate in
an admissible anatomy. For chemotaxis, it may be a position-energy region or a minimum
nutrient-acquisition condition.
For worst-case disturbances, the finite-horizon viability kernel is
Viab\Sigma

$$
T (K) = n x0 \inK : \exists\pi, \forallw0:T−1 \inW T , xt \inK for all 0 \leqt \leqT
$$

o
.
(1) The infinite-horizon kernel is obtained by requiring the condition for all T. This is the standard
viability-theoretic notion: the largest subset from which some admissible feedback can satisfy
the constraints Aubin (1991); Aubin et al. (2011).

$$
Biological experiments more often estimate a probability than a worst-case set. Let \rho0 be a
$$

distribution over initial states and let \nu∆be a disturbance distribution indexed by severity ∆.
For a controller class \Pi, define

$$
ST (\Pi; ∆) = sup \pi\in\Pi
$$

$$
P\rho0,\nu∆,\pi [xt \inK for all 0 \leqt \leqT] . (2)
$$

This is a stochastic finite-horizon viability probability.
The disturbance index ∆can be
experimentally concrete: ligand noise amplitude, fraction of cells ablated, duration of gap-
junction blockade, or external force magnitude.
4

---

3.2
Control interfaces
A rank-r interface consists of a command space Vr ⊆Rr and a refinement map
\alphar : X \times Vr \toU.

$$
A higher-level controller chooses vt \inVr; the refinement map converts it into lower-level
$$

$$
actuation ut = \alphar(xt, vt). Dependence on xt allows the lower level to implement the same
$$

abstract command differently in different microstates.
The rank is the dimension of the independent command space. For smooth nonlinear

$$
interfaces, this is replaced locally by the maximal differential rank of v 7\to\alphar(x, v) on the
$$

operating region. This uses standard input dimension rather than a new checklist of interface
properties.

$$
Let \Pir(\alphar) be the set of concrete controllers implementable through interface \alphar. We
$$

distinguish three baselines:

$$
• \Pifull: the unrestricted lower-level controller class;
$$

• \Pinull: a fixed, absent, scrambled, or ablated interface baseline;
• \Pir: the best allowed rank-r interface/controller class under the experimental protocol.
The phrase “best rank-r” is relative to a specified search space. In a synthetic model,
all rank-r linear subspaces may be optimized. In a biological experiment, the search may be
restricted to combinations of known channels, stimulation patterns, or independently addressable
modes.
3.3
The viability-retention curve
Define
Sfull

$$
T (∆) = ST (\Pifull; ∆), Snull
$$

T

$$
(∆) = ST (\Pinull; ∆), and
$$

S⋆
T (r; ∆) = sup
\alphar
ST (\Pir(\alphar); ∆).
Assuming Sfull
T (∆) > Snull
T
(∆), define the normalized viability retention
RT (r; ∆) = S⋆
T (r; ∆) −Snull
T
(∆)
Sfull
T (∆) −Snull
T
(∆) .
(3) When the interface search space is nested in r, RT (r; ∆) is nondecreasing and lies in [0, 1]. The normalization makes different systems comparable without pretending that a chemotactic
success probability and a regeneration probability have the same natural unit.
The corresponding minimal viability-preserving rank is

$$
r\epsilon,T (∆) = min {r : RT (r; ∆) \geq1 −\epsilon} . (4)
$$

Equations (3) and (4) are the only new measurement definitions required by the paper.
Other quantities, such as recovery time or perturbation tolerance, enter by changing T or ∆
and inspecting the same curve.

$$
Remark 1. A low value of r\epsilon,T (∆) does not imply that the controlled competency has low
$$

$$
description length. The refinement map \alphar, the lower-level dynamics, and the target set may be
$$

extremely complex. A small command alphabet can select among complex, already learned or
evolved behaviors.
5

---

4
Three Formal Results
4.1
Result I: viability preservation under feedback refinement
Abstraction-based control studies when a controller synthesized on a coarse model can be refined
into a controller for a detailed plant. Feedback refinement relations provide a standard sufficient
condition Reissig et al. (2017); bisimulation provides a stronger two-way behavioral equivalence
that preserves reachability and temporal properties Pappas (2003); Tabuada (2009). We state
the viability consequence in a form adapted to MCA.
Let the concrete system be

$$
\Sigma = (X, U, F) and the abstract system
$$

$$
¯\Sigma = ( ¯X, ¯U, ¯F), where uncertainty and disturbance have been absorbed into set-valued transitions. Let Q ⊆
$$

X \times ¯X relate concrete to abstract states. For a set A ⊆¯X, write

$$
Q−1(A) = {x \inX : \exists¯x \inA, (x, ¯x) \inQ}. A relation Q is a feedback refinement relation from \Sigma to ¯\Sigma if every abstract input enabled at
$$

a related abstract state can be refined into a concrete input such that every concrete successor
remains related to an allowed abstract successor. This is the control-compatible version of a
simulation relation Reissig et al. (2017).
Proposition 1 (One-way viability preservation). Let Q be a feedback refinement relation from

$$
\Sigma to ¯\Sigma. Let ¯K ⊆¯X and let K = Q−1( ¯K). Then for every horizon T,
$$

Q−1
Viab
¯\Sigma
T ( ¯K)

⊆Viab\Sigma
T (K).

$$
(5) If the inverse relation Q−1 is also a feedback refinement relation, then Q−1 Viab ¯\Sigma
$$

T ( ¯K)

$$
= Viab\Sigma T (K).
$$

$$
(6) Proof. Take x0 \inQ−1(Viab
$$

¯\Sigma

$$
T ( ¯K)). There exists a related ¯x0 \inViab
$$

¯\Sigma
T ( ¯K) and an abstract
feedback policy that keeps every abstract trajectory in ¯K for T steps.
By the feedback
refinement property, each abstract action can be refined to a concrete action whose possible
successors are related to possible abstract successors. Induction on t yields a concrete trajectory
related at every step to an abstract trajectory in ¯K, hence contained in K = Q−1( ¯K). This
proves the inclusion. Applying the same argument to Q−1 gives the reverse inclusion under
bidirectional refinement.
Interpretation.
Equation (6) is a precise version of cross-scale delegation. When the abstract
and concrete dynamics are control-equivalent for the safety specification, a higher-level controller
loses no viability by ignoring distinctions within the fibers of Q. The lower-level system can
vary or repair itself inside a fiber without changing the higher-level policy.
The result connects three literatures without replacing them:
Simon’s coarse aggregate + Levin’s lower-level competency
+ feedback refinement/bisimulation \Rightarrowpreserved viability.
One-way refinement is more realistic than exact equivalence. It certifies that an abstract
controller is safe when refined, but it may be conservative: the concrete system can possess
viable strategies absent from the abstraction. Empirically, the gap between the two sides of (5)
measures how much lower-level competency the coarse interface fails to expose.
6

---

4.2
Result II: optimal local rank and a viability bound
The global computation of viability kernels is difficult. Around a target manifold or operating
point, however, an intervention experiment often supplies a local response matrix. We derive a
baseline connecting its singular spectrum to the best rank-r interface.
Suppose a disturbance creates a corrective demand d \inRm. An unrestricted controller could
apply u = d. The competency-relevant output error after applying u is locally
e = G(d −u),

$$
(7) where G \inRq\timesm is the interventional response from residual lower-level error to the macro-
$$

$$
outcome. Let d have mean zero and covariance \Sigma ≻0. A rank-r linear interface applies
$$

u = Pd,
where P is a rank-r projector in the whitened demand coordinates.
Let

$$
M = G\Sigma1/2 have singular values
$$

$$
\sigma1 \geq\sigma2 \geq· · · \geq\sigmas \geq0. Theorem 1 (Best rank-r local interface). Among rank-r orthogonal projections in whitened
$$

demand coordinates, the minimum expected squared macro-error is
min
rank(P)=r E∥e∥2

$$
2 = X
$$

i>r
\sigma2
i (M).

$$
(8) An optimum projects onto the leading r right singular vectors of M. Proof. Write d = \Sigma1/2z with E[zz⊤] = I. For a projector ˜P in whitened coordinates,
$$

e = M(I −˜P)z.
Therefore
E∥e∥2
2 = ∥M(I −˜P)∥2
F .
The Eckart–Young–Mirsky theorem implies that the best rank-r approximation to M in
Frobenius norm retains its leading r singular directions, leaving squared error equal to the tail
sum in (8) Eckart and Young (1936); Mirsky (1960).
Suppose local viability requires ∥e∥2 < m, where m is the distance to the nearest competency-
violating boundary in the chosen output metric.
Corollary 1 (Finite-horizon one-step viability bound). For the optimal rank-r interface,

$$
P(∥e∥2 \geqm) \leq P
$$

$$
i>r \sigma2 i (M)
$$

m2
.

$$
(9) Hence P(∥e∥2 < m) \geq1 −
$$

P

$$
i>r \sigma2 i (M)
$$

m2
.
(10) Proof. Apply Markov’s inequality to the nonnegative random variable ∥e∥2 2 and substitute Theorem 1.
7

---

The bound is conservative, but it pays rent in three ways.
First, it gives an experimentally calculable baseline. Estimate G by randomized interventions,

$$
estimate \Sigma from the disturbance ensemble, and measure the local margin m. The singular-value
$$

tail then predicts how many independent interface directions should suffice.
Second, it distinguishes low-rank control response from low-dimensional observations. The
SVD is applied to an interventional response matrix, not to passive trajectories.
Third, it yields a falsification test. If the empirical RT (r; ∆) is much lower than the local
bound predicts, then nonlinearities, state dependence, temporal effects, or unobserved bypasses
matter. If it is much higher, lower-level feedback may be absorbing disturbances that the local
open-loop response treats as residual error.
Relation to controllability and model reduction.
The result is related to output con-
trollability, controllability Gramians, balanced truncation, and input-output model reduction
Moore (1981); Antoulas (2005). It is not equivalent to full-state controllability. A system can
require many directions to reach arbitrary microstates while requiring few directions to keep a
macro-output inside a viable set. The relevant spectrum is therefore the response of competency
variables to interventions, not the rank of the full controllability matrix.
4.3
Result III: causal rank is not observationally identifiable
We now show that even exact knowledge of the observational distribution cannot determine
whether a predictive low-dimensional variable is a control interface.

$$
Theorem 2 (Observational non-identifiability of interface rank). For any matrix A \inRq\timesk,
$$

there exist two SCMs with identical observational distributions over (Z, Y ) but interventional
response ranks rank(A) and 0, respectively.

$$
Proof. Let H \inRk and \epsilon \inRq be independent random variables. Consider
$$

M1 :
Z := H,

$$
Y := AZ + \epsilon, and
$$

M2 :
Z := H,

$$
Y := AH + \epsilon. Observationally Z = H, so both models induce exactly the same joint distribution:
$$

$$
Y = AZ + \epsilon. Under intervention, however,
$$

$$
E[Y | do(Z = z)] = Az + E[\epsilon] in M1, whose derivative with respect to z has rank rank(A). In M2, intervening on Z leaves
$$

H unchanged, so

$$
E[Y | do(Z = z)] = AE[H] + E[\epsilon], which is independent of z and has rank 0.
$$

Corollary 2. No statistic computed solely from the observational joint distribution P(Z, Y ),
including mutual information, predictive sufficiency, principal-component rank, or representation
dimension, can identify the causal rank of Z \toY without additional causal assumptions or
interventions.
8

---

This result is elementary but consequential. It rules out a common shortcut: observing that
many downstream variables covary with a low-dimensional latent does not establish that the
system coordinates through that latent. The same data can arise when the latent is a passive
readout of a hidden common cause.
Pearlian causal assumptions can sometimes identify intervention effects from observational
data, for example through back-door or front-door criteria Pearl (2009). In the biological cases
emphasized here, direct perturbation is often more credible because the candidate interface is
experimentally manipulable. Where interventions are limited, causal identifiability assumptions
should be stated as part of the result, not hidden inside a representation-learning method.
5
Measurement Protocol
The common empirical object is the curve
RT (r; ∆).
A measurement protocol should make each symbol concrete before data collection.
5.1
Step 1: specify the competency set and horizon
Choose K and T so that success is externally checkable. Examples include:
• remaining inside a nutrient-rich spatial region for T minutes;
• regenerating one anterior and one posterior pole by a fixed day;
• keeping endpoint force or gait stability inside a tolerance tube for T seconds.
A target should not be selected only because the candidate interface predicts it well. It
should be justified independently as a competency-relevant outcome.
5.2
Step 2: define a disturbance family
Specify \nu∆, including the intervention timing and a scalar severity index. The same system
may be low-rank for one disturbance family and high-rank for another. This dependence is not
a nuisance. It is part of the claim.
Useful disturbance families vary one axis at a time initially:
• sensory noise or gradient reversals;
• cell deletion, tissue cuts, or transient channel blockade;
• forces, loads, or actuator failures.
5.3
Step 3: establish null and full baselines
The null baseline should remove or scramble the candidate control channel while preserving
as much unrelated function as possible. The full baseline should expose all experimentally
available independent control directions, not an imagined omnipotent controller.
This makes the normalization in (3) empirically checkable. It also prevents a weak rank-r
interface from looking impressive merely because the task is easy without control.
5.4
Step 4: construct nested interface families
For each r, construct a nested family of independently controllable modes. Depending on the
system, these may be:
• biochemical concentrations or pulse modes;
• spatial voltage eigenmodes or optogenetic stimulation patterns;
• neural stimulation components or muscle-command modes.
9

---

Whenever possible, randomize interventions within the allowed family and estimate the
interventional response matrix G. The leading singular directions from Theorem 1 provide
a baseline ordering. A nonlinear controller can then be compared against this local linear
benchmark.
5.5
Step 5: estimate retention and rank
Estimate Snull
T
, S⋆
T (r), and Sfull
T
with binomial or survival-model uncertainty intervals. Report

$$
the full RT (r; ∆) curve rather than only r\epsilon,T . A sharp elbow supports a compact interface; a
$$

gradual curve indicates distributed control; crossings across ∆indicate context-dependent rank.
The primary comparisons are:
RT (r; ∆)
against

$$
RT (0; ∆) = 0 and RT (rfull; ∆) = 1, and r\epsilon,T (∆)
$$

across disturbance severities and systems.
No additional case-specific score is necessary.
6
Canonical Cases
6.1
Bacterial chemotaxis: a minimal control-interface case
The Escherichia coli chemotaxis system maps temporally varying receptor occupancy into
run-and-tumble behavior. Receptor methylation supports adaptation, the kinase pathway
changes the concentration of phosphorylated CheY, and CheY-P binds the flagellar motor
switch to alter clockwise versus counterclockwise rotation Clausznitzer et al. (2010); Yuan
et al. (2012); Tu (2013). The pathway is attractive as a minimal case because the molecular
components, perturbations, and motor output are experimentally accessible.
6.1.1
Candidate abstraction
A useful hierarchy is:

$$
ligand and receptor microstate −\toCheY-P concentration −\tomotor bias
$$

−\tospatial nutrient acquisition.
At the motor-switch level, CheY-P is approximately a scalar broadcast variable. This yields
a concrete upper bound of one on the instantaneous command dimension for changing motor
bias under a fixed receptor and motor context. It does not establish that the entire chemotactic
competency has rank one. Receptor adaptation, multiple motors, motor-level adaptation, and
cell-state dependence may add independent directions or state variables Yuan et al. (2012).
6.1.2
Common estimand
Let K be the set of trajectories that keep the cell above a specified nutrient-acquisition or energy
threshold for T. Let ∆index gradient noise, reversal frequency, or background-concentration
variation.
The baselines are experimentally direct:
• Null: CheY absent, nonphosphorylatable, clamped, or scrambled so that ligand changes no
longer modulate motor bias.
• Rank one: a controlled CheY-P trajectory, or an optogenetic/chemical proxy that supplies
one scalar time-varying command.
10

---

• Full: all independently accessible pathway interventions, including receptor, kinase, adapta-
tion, and motor-level control.
The central measurement is
RT (1; ∆).
If it remains near one across a wide disturbance range, the scalar CheY-P channel preserves most
experimentally available chemotactic viability. If retention falls under changing backgrounds
while a higher-rank controller restores performance, the system is low-rank only locally.
6.1.3
Checkable baseline
The local response from CheY-P to motor bias is steep and experimentally measured, while
motor adaptation shifts the response curve as the steady-state CheY-P level changes Yuan
et al. (2012). This supplies a direct test of the local linear theorem: estimate the interventional
response around several operating points and ask whether a single direction predicts viability
retention. The known operating-point dependence is expected to break a globally fixed linear
interface, providing a useful nontrivial baseline rather than a guaranteed success.
6.2
Planarian bioelectric morphogenesis: the central multiscale case
Planarian regeneration is a clearer instance of MCA because lower-level cells reconstruct large-
scale anatomy after cutting. Bioelectric states generated by ion channels, pumps, and gap
junctions participate in anterior-posterior patterning and anatomical memory Levin (2014);
Durant et al. (2017). Transient perturbation of endogenous bioelectric networks can produce
persistent changes in the anatomy to which later fragments regenerate.
Durant and colleagues reported that brief gap-junction perturbation produced a stable
mixture of normal and two-headed regenerates; morphologically normal treated animals retained
a cryptic altered regenerative state, and later amputations reproduced the altered outcome ratio
even after the original treatment was absent Durant et al. (2017). Experimental reversal of the
bioelectric state restored wild-type regeneration. This is strong evidence that a manipulable
physiological state lies upstream of a complex anatomical outcome. It is not yet evidence that
the full interface has low rank.
6.2.1
Candidate abstraction
Let x include cellular voltage, gap-junction state, gene expression, neoblast state, and local
geometry. Let the macrostate y = h(x) describe regenerative polarity and head number. The
higher-level target set is
¯KWT = {one anterior head and one posterior tail}.
The concrete target set is its preimage under h.
The MCA interpretation is that lower-level cellular competencies implement a coarse
anatomical target despite large changes in cell identity and position. Proposition 1 gives the
exact idealization: if anatomical states and cellular states are related by a feedback refinement
relation, a controller defined over anatomy can be safely refined into cellular dynamics.
6.2.2
Common estimand
Let ∆index cut geometry, removed tissue fraction, pharmacological perturbation duration,
or targeted cell ablation. Define success at horizon T as regeneration into the chosen target
morphology.
11

---

Construct spatially controlled voltage modes, gap-junction perturbation modes, or combina-
tions of ion-channel interventions. Then estimate
RT (r; ∆)
for nested mode families.
The baselines are:
• Null: sham stimulation or a perturbation that destroys the instructive spatial relation while
matching exposure.
• Rank r: the best r independently controlled bioelectric modes.
• Full: the full experimentally addressable stimulation basis, possibly combined with known
pharmacological channel controls.
The 2017 result already supplies a checkable one-direction intervention effect: a transient
manipulation changes the long-run distribution over anatomical attractors, and a reverse
intervention resets it Durant et al. (2017). It therefore establishes causal leverage and persistence.
It does not provide r\epsilon,T , because the study did not compare nested control bases against a
full-control baseline. The proposed experiment converts the qualitative “bioelectric code” claim
into a rank-retention curve.
6.2.3
Decisive outcomes
Three patterns would discriminate hypotheses.

### 1. A sharp elbow at small r, stable across cut geometries, would support a low-rank anatomical

control interface.

### 2. A low rank for simple anterior-posterior polarity but a rising rank for head shape, organ

placement, and scaling would support task-relative hierarchy rather than a single anatomical
code.

### 3. A high rank with no stable modes across perturbations would suggest distributed morpho-

genetic control, even though individual bioelectric interventions remain powerful.
The framework therefore supports Levin’s program whether the low-rank hypothesis succeeds
or fails: it measures how much anatomical competency is delegated through a compact interface
rather than presuming that it is.
6.3
Muscle synergies: a negative control for forced mappings
Muscle activity often lies near a low-dimensional subspace, motivating the hypothesis that the
nervous system controls groups of muscles through reusable synergies Bizzi and Cheung (2013).
This appears, at first, to be an ideal example of a low-rank control interface.
Kutch and Valero-Cuevas showed why that inference is unsafe Kutch and Valero-Cuevas
(2012). Musculoskeletal geometry and task constraints can produce low-dimensional electromyo-
graphic patterns even when muscles receive independent commands. The observed rank may
therefore reflect the feasible output manifold rather than the controller’s input dimension.
This case directly instantiates Theorem 2. Passive recordings cannot distinguish a neural
low-rank controller from a high-rank controller acting through low-dimensional biomechanics.
6.3.1
Common estimand
Let K be a task-level tolerance tube for endpoint force, posture, or gait. Let ∆index external
force or actuator impairment. Compare:
• Null: stimulation or command patterns uncorrelated with task-relevant modes;
• Rank r: direct stimulation of r independently calibrated neural or muscular command
modes;
• Full: independently addressable stimulation of the available muscles or motor pools.
12

---

Table 1: Common quantities and evidence status.
Case
Competency set
K
Candidate
interface
Known causal
fact
Missing rank
test
E. coli
chemotaxis
Nutrient
acquisition or
spatial retention
CheY-P and
pathway modes
CheY-P
intervention
changes motor
bias; adaptation
changes operating
point
Nested pathway
modes versus full
accessible control
Planarian
regeneration
Target morphology
after cut
Spatial bioelectric
and gap-junction
modes
Transient
perturbation
persistently
changes
anatomical
outcome
distribution;
reversal can reset
Nested spatial
modes across cut
and damage
families
Motor
coordination
Force, posture, or
gait tolerance
Neural or
muscle-command
modes
Stimulation can
evoke structured
patterns, but
passive low rank
has mechanical
alternatives
Direct rank-r
command
interventions
versus
independent-
control baseline
Only interventional estimates of
RT (r; ∆)
can establish whether few command modes preserve task viability. PCA or nonnegative matrix
factorization of EMG can propose candidate modes but cannot supply the causal conclusion.
As a negative control, muscle coordination sets a demanding standard for the other cases.
A candidate interface should not be accepted merely because a low-dimensional factor predicts
the macro-outcome. The same nested intervention protocol must outperform both null and
mechanically induced observational baselines.
7
Cross-Case Comparison
Table 1 summarizes what is currently established and what remains to be measured. The table
intentionally avoids assigning speculative numerical ranks.
The same two reported objects apply to all three:
RT (r; ∆)
and
r\epsilon,T (∆).
This provides three useful comparisons.
Within-system comparison.
Does the required rank increase with perturbation severity?
A control interface that appears scalar in a narrow operating regime may recruit additional
modes under damage.
Across-task comparison.
Does the same interface preserve multiple competencies? Shared
low-rank control predicts correlated failures and common-mode leverage; task-specific interfaces
predict different rank curves.
13

---

Against an observational baseline.
How does interventional rank compare with the rank
obtained from PCA, factor analysis, or latent-state models? A lower observational rank than
interventional rank indicates compression without control. A lower interventional rank than
observational rank indicates that many observed states can be steered through few commands
because lower-level feedback supplies the detail.
8
Why Low-Rank Interfaces Might Emerge
The framework defines and measures a property. It does not by itself explain why the property
should be common. Several mechanisms make it plausible.
8.1
Timescale separation
In nearly decomposable systems, fast local dynamics relax before slow cross-module dynamics
change substantially Simon (1962). A higher-level controller can then act on aggregate variables
while local controllers stabilize the omitted dimensions. Formally, timescale separation makes
approximate feedback refinement more plausible because many microstates inside a coarse fiber
have similar future coarse behavior.
8.2
Evolvability and reuse
If evolution can alter a small command interface while reusing competent lower-level machinery,
large phenotypic changes require fewer coordinated genetic modifications. This does not mean
that the resulting phenotype is simple. It means that the mapping from high-level signal to
lower-level response has already been built and can be reused Levin (2023).
8.3
Communication and energetic constraints
Long-range broadcast is costly. Compact control signals can coordinate distributed subsystems
without transmitting their full local states. Neuromodulators, hormones, and bioelectric fields
are plausible implementations, but the physical narrowness of a broadcast channel does not

$$
guarantee low r\epsilon,T . Context-dependent receptor states can effectively increase the dimension of
$$

the interface.
8.4
Credit assignment
A shared control channel can carry outcome-relevant error or precision signals to many local
learning systems. This may accelerate adaptation while leaving semantic content distributed.
The loop-hub-value proposal applies a related idea to neuromodulatory control of human
motivation Zarncke (2025a). The present framework supplies a way to test the architectural
part of that proposal without assuming a one-to-one mapping between hubs and value concepts.
8.5
Why high-rank control may persist
Low rank also creates common-mode vulnerabilities.
A pathogen, tumor, or adversarial
intervention that captures a central interface can redirect many downstream processes at once.
Redundant or distributed control can be selected precisely because it is harder to capture. The
empirical prediction is not that rank is always small, but that rank reflects a tradeoff among
evolvability, communication cost, robustness to ordinary variation, and robustness to interface
corruption.
14

---

9
Applications Beyond the Canonical Cases
9.1
Motivational control and human values
Human values are semantically rich, learned, culturally shaped, and internally inconsistent.
None of this determines the dimensionality of the control channels through which motivational
state changes policy.
Suppose a high-dimensional learned world model and concept system is modulated by a
smaller family of affective, neuromodulatory, or self-referential control signals. Then value
content may have high description length even if policy changes lie on a low-rank intervention
manifold. Conversely, finding a small preference direction in a trained model does not show that
the represented concept of goodness is simple; the direction may rely on distributed semantic
machinery.
The relevant experiment is therefore not PCA over value judgments alone. It is a rank-
retention experiment:
1. specify a family of value-relevant policy competencies;
2. perturb candidate motivational channels in independently controlled combinations;
3. measure whether a small r reproduces the policy changes obtainable through the full accessible
intervention set;
4. test stability across contexts, development, reflection, and distribution shift.
This will not solve value learning. It may shed light on human values by separating two
questions that are often conflated:
How complex is what humans value?
versus
How many control directions change policy?
A low value of r\epsilon,T would make motivational control more identifiable and manipulable, but
also more vulnerable to common-mode capture. A high value would weaken simple hub-based
value models and make stable value inference harder. The low-dimensional value-learning
argument should therefore be treated as an application hypothesis rather than evidence for the
general framework Zarncke (2026).
9.2
Conscious access and self-models
Global-workspace and metacognitive theories propose that only a restricted subset of neural
states becomes jointly available for report, planning, and reflection. A limited bandwidth is not
by itself a low-rank control interface. The stronger claim would be that interventions on a small
set of workspace or self-model directions reproduce most changes in globally coordinated policy.
The same retention protocol can be used, with competency sets defined by cross-modal
report, sequential planning, or ownership attribution. These applications require ethically and
technically difficult interventions, so they are secondary to the biological systems above.
9.3
AI correction channels
AI systems are often trained through architecturally narrow feedback channels: scalar rewards,
preference labels, constitutions, critique messages, or gradient updates. Their nominal interface
dimension is easy to count, but nominal narrowness does not imply continued control. A capable
system may learn internal routes that make behavior insensitive to the correction channel.
For an AI system, define K as a set of correction-responsive policy constraints and ∆as
capability growth or distribution shift. Then
RT (r; ∆)
15

---

measures how much of the policy correction obtainable through the full training or editing
stack remains available through a restricted channel. A decline with ∆would indicate loss of
cross-scale control even if the interface still exists syntactically.
10
Failure Modes and Scope Conditions
10.1
Task-relative rank
The rank is always indexed by K, T, and ∆. A scalar interface may preserve one coarse
competency while destroying another. Calling a system “low-rank” without these indices is
incomplete.
10.2
Nonlinearity and mode switching
A nonlinear system may use different low-rank interfaces in different regions, while the union
has high rank. Reporting only a local Jacobian spectrum can conceal switching. The empirical
retention curve should therefore be measured across operating points.
10.3
Redundancy
Multiple interfaces may each preserve viability. Ablating one can leave performance unchanged,
not because it is irrelevant but because another channel compensates. The optimization in
S⋆
T (r; ∆) naturally allows alternative interfaces, but causal attribution to a particular biological
channel requires combinatorial interventions.
10.4
Changing target sets
Development and learning can alter the competency itself. Viability theory assumes a specified
constraint set. For target plasticity, one must enlarge the state to include target parameters or
compare rank curves before and after target change.
10.5
Intervention damage
Manipulating a candidate interface may damage lower-level machinery, violating the assumption
that only the command variable changed. Sham interventions and multiple implementation meth-
ods are necessary. Pearl’s do-operator describes an ideal intervention; biological interventions
only approximate it.
10.6
Search-space dependence
The “best rank-r” interface can be found exactly only in small synthetic systems or restricted
linear families. Biological studies estimate a candidate-relative rank. The paper’s notation
should not be read as claiming global optimization when the experimental basis is limited.
10.7
Adversarial adaptation
A system can respond to the measurement process or route control around monitored channels.
This is especially relevant for AI and social systems. Rank measured under a passive disturbance
family may fail under strategic pressure.
16

---

11
A Minimal Synthetic Benchmark
Before applying the protocol to biological data, a benchmark should separate three properties
that passive representation learning often conflates:
1. observational dimension;
2. causal response rank;
3. viability-preserving rank.
Consider a 20-dimensional microstate
xt+1 = Axt + But + Ewt
with a two-dimensional macrostate
yt = Cxt
and competency set

$$
K = {x : ∥Cx∥\infty\leq1}. Choose A so that 18 fiber directions are stable and rapidly contracting, while the two macro
$$

directions are unstable without control. Let B have full state-controllability rank 20, but let
only two singular directions of the interventional map to y have appreciable gain.
The benchmark has an analytic expectation:
• full-state controllability remains high-rank;

$$
• the best viability-preserving interface has r\epsilon,T = 2 over the designed disturbance range;
$$

• PCA rank can be made arbitrarily large by adding high-variance stable fiber noise;
• a common-cause latent can be added to create a low-dimensional observational predictor
with zero interventional rank, as in Theorem 2.
Four methods should be compared:

### 1. PCA or nonlinear latent dimension;

2. information-bottleneck prediction;

### 3. Markov-blanket or UAD boundary discovery;

4. randomized interventional estimation of G, followed by rank-r viability evaluation.
The intended result is not that intervention always wins. The benchmark identifies which
question each method answers. PCA describes variance; information bottlenecks describe
predictive compression; blanket methods describe conditional boundaries; the present method
estimates restricted causal control of viability.
12
Research Program
A focused program can proceed in three stages.
12.1
Stage I: formal and synthetic

### 1. Generalize Theorem 1 from one-step linear response to finite-horizon stochastic systems

using output-reachability Gramians.

### 2. Quantify approximate rather than exact feedback refinement and derive bounds on viability-

kernel mismatch.

### 3. Release synthetic benchmarks where observational rank, causal rank, and viability rank vary

independently.
12.2
Stage II: tractable biological systems

### 1. Estimate RT (1; ∆) for CheY-P control across chemotactic operating regimes.

### 2. Construct nested spatial bioelectric stimulation bases for planarian regeneration.

17

---

### 3. Use motor-control experiments as a negative-control domain in which mechanical and neural

low rank must be separated.
12.3
Stage III: cognition and alignment
Only after the measurement protocol succeeds on systems with known interventions should
it be applied to motivational control, conscious access, self-models, and AI correction. These
domains have richer semantics and worse causal access. Their importance is not a reason to
relax the evidential standard.
13
Discussion
The paper began with the concern that “low-dimensional bottleneck” may merely restate
compression and interfaces. The viability formulation identifies what would make the claim
substantive.
A low-rank control interface is not just a small representation. It is a restricted command
space that preserves most of the competency available through a richer controller, under a
stated disturbance family. The comparison against null and full baselines makes the claim
quantitative. The dependence on K, T, and ∆prevents a local or task-specific result from
silently becoming a universal one.
The conceptual stack is deliberately asymmetrical.
• Levin supplies the target phenomenon: competencies compose across biological scales.
• Simon supplies the structural reason coarse interfaces can exist: near decomposability and
timescale separation.
• Friston supplies a related method for locating statistical boundaries through which coupling
occurs.
• Pearl supplies the distinction between predictive summaries and causes.
• Aubin and control-abstraction theory supply the formal criterion: preservation of
viability under restricted and refined control.
This positioning is supportive rather than competitive. The framework does not claim that
MCA is “really” viability theory, that Markov blankets are low-rank interfaces, or that all
biological intelligence reduces to a single control principle. It offers a measurable subquestion
within the broader agenda.
The strongest current biological evidence concerns causal leverage, not low rank. Chemo-
taxis contains a scalar motor-control signal, but its global competency is context-dependent.
Bioelectric interventions can rewrite regenerative anatomy, but the number of independent
modes required for near-complete control is unknown. Muscle synergies show why passive
low-dimensionality cannot settle the issue.
The central empirical unknown is therefore not whether compact signals exist. They plainly
do. It is the shape of
RT (r; ∆).
A steep curve would show that lower-level competencies absorb most variation behind a compact
interface. A shallow curve would show that control remains distributed. A curve that changes
sharply with ∆would show that low rank is a feature of ordinary operation but not of repair
under severe damage.
This distinction also changes the alignment interpretation. A low-rank motivational or
correction interface could make value influence easier to infer and reproduce. It would simulta-
neously create a concentrated failure mode. An interface can be a handle for alignment and an
attack surface for misalignment. The framework measures the concentration before deciding
whether it is desirable.
18

---

14
Conclusion
Multiscale competency architectures pose a concrete composition problem: how can a larger-
scale system preserve a target while delegating implementation to competent lower-level parts?
We proposed that some such systems use low-rank control interfaces, defined not by generic
compression but by retained viability under restricted intervention.
The paper introduced one retention curve,
RT (r; ∆),
and one derived quantity,
r\epsilon,T (∆).
It connected exact preservation of viability to feedback refinement and bisimulation, derived a
singular-value baseline and viability-loss bound for local linear response, and proved that causal
interface rank is not identifiable from observations alone.
Bacterial chemotaxis and planarian regeneration provide strong candidate systems. Muscle
synergies provide a warning against forced mappings. The next step is not another broad
analogy. It is to estimate nested rank-retention curves under controlled perturbations. If small
ranks preserve viability across cases and disturbance regimes, low-rank control interfaces will
constitute a genuine recurring mechanism of multiscale competency. If they do not, the same
experiments will identify where biological coordination remains irreducibly distributed.
A
Deterministic and Stochastic Viability
For deterministic worst-case analysis, the success indicator in (2) can be replaced by the robust
condition
inf

$$
w0:T −1\inW T 1{xt \inK, 0 \leqt \leqT}. Then ST is either zero or one for a fixed initial state, and the useful aggregate is the probability
$$

mass or volume of the viability kernel:

$$
VT (\Pi) = \rho0
$$

Viab\Pi
T (K)

.
The same null/full normalization gives

$$
RT (r) = VT (\Pir) −VT (\Pinull) VT (\Pifull) −VT (\Pinull).
$$

This version is appropriate for gridded synthetic systems and formal reachability tools.
B
Approximate Refinement
Exact feedback refinement is strong. Let an abstract safety controller keep abstract trajectories
at least distance m from the boundary of ¯K. Suppose the concrete-to-abstract simulation error

$$
is bounded by \delta < m in the output metric over horizon T. Then the refined concrete controller
$$

$$
remains inside the \delta-expansion of the abstract trajectory and therefore inside ¯K. This standard
$$

robustness-margin argument converts approximate bisimulation or approximate refinement
bounds into safety certificates Tabuada (2009).
For MCA applications, the quantity of interest is not only the approximation error but its
dependence on perturbation severity:

$$
\delta = \delta(∆). A lower-level competency is effective when \delta(∆) remains below the macro-level margin without
$$

requiring an increase in command rank.
19

---

C
Estimating the Interventional Response Matrix

$$
Let z \inRr parameterize a candidate stimulation basis and let y \inRq be a vector of competency-
$$

relevant outcomes. Around operating point (z0, c), define

$$
G(c) = \partial \partialz E [Y | do(Z = z), C = c]
$$

z=z0 . A randomized local design estimates columns of G by finite differences. For nonlinear systems,
repeat across contexts c, operating points, and disturbance levels.

$$
The singular values of G(c)\Sigma1/2(c) should be reported with bootstrap intervals. A stable
$$

low-rank interface predicts that leading singular subspaces align across contexts. Principal
angles between the estimated subspaces provide a standard comparison; no new stability score
is required.
D
Relation to Information Bottlenecks
The information-bottleneck method seeks a representation Z that compresses X while preserving
information about Y , often through an objective of the form

$$
I(X; Z) −\betaI(Z; Y ) Tishby et al. (2000). This is an observational or predictive criterion unless the data and graphical
$$

assumptions identify interventions.
A control interface can be information-rich but low-rank, for example when a scalar time
series has high temporal precision. It can also be information-poor but high-rank if many binary
actuators each provide one independent direction. The relation between information rate and
control rank is therefore empirical rather than definitional.
References
Athanasios C. Antoulas. Approximation of Large-Scale Dynamical Systems. SIAM, 2005.
Jean-Pierre Aubin. Viability Theory. Birkhäuser, 1991.
Jean-Pierre Aubin, Alexandre M. Bayen, and Patrick Saint-Pierre. Viability Theory: New
Directions. Springer, 2011.
Emilio Bizzi and Vincent C. K. Cheung. The neural origin of muscle synergies. Frontiers in
Computational Neuroscience, 7:51, 2013.
Damien Clausznitzer, Olga Oleksiuk, Lutz Løvdok, Victor Sourjik, and Robert G. Endres.
Chemotactic response and adaptation dynamics in Escherichia coli. PLoS Computational
Biology, 6(5):e1000784, 2010.
Fallon Durant, Junji Morokuma, Chris Fields, Katherine Williams, Dany S. Adams, and Michael
Levin. Long-term, stochastic editing of regenerative anatomy via targeting endogenous
bioelectric gradients. Biophysical Journal, 112(10):2231–2243, 2017.
Carl Eckart and G. Young.
The approximation of one matrix by another of lower rank.
Psychometrika, 1:211–218, 1936.
Chris Fields and Michael Levin. Competency in navigating arbitrary spaces as an invariant for
analyzing cognition in diverse embodiments. Entropy, 24(6):819, 2022.
20

---

Karl Friston. The free-energy principle: A unified brain theory? Nature Reviews Neuroscience,
11(2):127–138, 2010.
Michael D. Kirchhoff, Thomas Parr, Ester Palacios, Karl Friston, and Julian Kiverstein. The
Markov blankets of life: Autonomy, active inference and the free energy principle. Journal of
the Royal Society Interface, 15:20170792, 2018.
Jason J. Kutch and Francisco J. Valero-Cuevas. Challenges and new approaches to proving the
existence of muscle synergies of neural origin. PLoS Computational Biology, 8(5):e1002434,
2012.
Michael Levin. Molecular bioelectricity: How endogenous voltage potentials control cell behavior
and instruct pattern regulation in vivo. Molecular Biology of the Cell, 25(24):3835–3850,
2014.
Michael Levin. Darwin’s agential materials: Evolutionary implications of multiscale competency
in developmental biology. Cellular and Molecular Life Sciences, 80:142, 2023.
L. Mirsky. Symmetric gauge functions and unitarily invariant norms. Quarterly Journal of
Mathematics, 11:50–59, 1960.
Bruce C. Moore. Principal component analysis in linear systems: Controllability, observability,
and model reduction. IEEE Transactions on Automatic Control, 26(1):17–32, 1981.
George J. Pappas. Bisimilar linear systems. Automatica, 39(12):2035–2047, 2003.
Judea Pearl. Causality: Models, Reasoning, and Inference. Cambridge University Press, 2
edition, 2009.
Judea Pearl. An introduction to causal inference. The International Journal of Biostatistics, 6
(2):Article 7, 2010.
Gunter Reissig, Alexander Weber, and Matthias Rungger. Feedback refinement relations for the
synthesis of symbolic controllers. IEEE Transactions on Automatic Control, 62(4):1781–1796,
2017.
Herbert A. Simon. The architecture of complexity. Proceedings of the American Philosophical
Society, 106(6):467–482, 1962.
Paulo Tabuada. Verification and Control of Hybrid Systems: A Symbolic Approach. Springer,
2009.
Naftali Tishby, Fernando C. Pereira, and William Bialek. The information bottleneck method.
arXiv:physics/0004057, 2000.
Yuhai Tu. Quantitative modeling of bacterial chemotaxis: Signal amplification and accurate
adaptation. Annual Review of Biophysics, 42:337–359, 2013.
Jun Yuan, Robert W. Branch, Basarab G. Hosu, and Howard C. Berg. Adaptation at the
output of the chemotaxis signalling pathway. Nature, 484:233–236, 2012.
Gunnar Zarncke. From free-energy loops to human values: A hub-centric precision model.
Technical report, Technical manuscript, 2025a.
Gunnar Zarncke. Foundations of unsupervised agent discovery in raw dynamical systems.
Technical report, Technical manuscript, 2025b.
Gunnar Zarncke. Value learning needs a low-dimensional bottleneck. LessWrong, 2026.
21
