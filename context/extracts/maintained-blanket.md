# Extract: maintained-blanket.pdf

**Source PDF:** `context/maintained-blanket.pdf`
**Extract:** `context/extracts/maintained-blanket.md`
**Pages:** 10
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

Discovering Maintained Agent Boundaries
Gunnar Zarncke
September 11, 2026
Abstract
Unsupervised Agent Discovery (UAD) [1] identifies candidate agents in raw dynamical
data by searching for approximate Markov blankets [2,3]: partitions into internal, sensory,
active, and external variables, i.e., a causal boundary. But it misses a second property of real
agents: A real agent boundary is not only a place where conditional independence holds. It is
a boundary that a real system must continually maintain against entropic degradation. Cells
repair membranes, organisms regulate temperature and ion gradients, companies maintain
accounting and legal identity, and software services maintain authentication, schema validity,
tests, monitoring, and rollback procedures.
We therefore extend UAD from boundary
discovery to maintained-boundary discovery. The central observable is not a latent distance
to a theorist-specified viable manifold, but a time-local boundary damage functional built from
measurable leakage, volatility, and boundary-disorder proxies. We define observational repair
as mean reversion of this damage after high-damage episodes, and action-mediated repair as
conditional information from candidate action variables to later damage reduction. A minimal
synthetic experiment compares an active boundary-repairing agent, a passive mean-reverting
boundary-like system, and a decaying boundary. Plain UAD detects approximate separation,
but cannot distinguish accidental or passive stability from maintained stability. The repair
extension adds a second axis: whether boundary damage reliably decreases after degradation.
Without interventions, active and passive repair remain only weakly distinguishable. This is
not a failure of the extension but an identifiability theorem in miniature: passive observation
can reveal maintained boundary-like dynamics, but not establish causal repair agency without
handles.
1
Introduction
A Markov blanket is a conditional-independence structure. In the active-inference and UAD
setting [4], a candidate agent is represented by a partition of observed variables into internal
states It, sensory states St, active states At, and external states Et. The idealized blanket
condition says that, once the sensory and active interface is known, the internal and external
futures are conditionally independent:
I(It+1; Et+1 | St, At) = 0.
(1) Real systems do not satisfy this exactly. They leak. The operational UAD criterion therefore relaxes the condition to

$$
I(It+1; Et+1 | St, At) \leq\epsilon. (2)
$$

This is already useful. It turns agency from an assumed label into an empirically testable
structure in a time series.
But it is incomplete. A purely causal blanket may exist only accidentally. It may be a
transient statistical shadow, or a passive equilibrium, or a boundary that exists for a few time
steps before entropy dissolves it. A soap bubble, a rock surface, a legal shell corporation, a
cell membrane, and a production service may all generate approximate separation in some
observational regime. Yet they differ in whether the boundary is maintained.
1

---

The missing condition is anti-entropic. A real agent boundary is not just a separator. It is a
controlled, resource-consuming, self-stabilizing interface. The boundary is part of the process by
which the agent continues to exist.
This paper formalizes that upgrade.
The key move is to avoid defining repair by reference to a hidden “true” viable boundary
manifold. Such a manifold is usually not observable from raw traces. Instead, we define boundary
damage using observable predictive consequences. A candidate boundary is damaged when
leakage rises, boundary variables become volatile or unpredictable, or local boundary dynamics
drift. A maintained boundary is one whose damage mean-reverts after high-damage episodes.
An agentic maintained boundary is one where candidate action variables predict later damage
reduction.
The paper contributes four pieces:
(i) a distinction between approximate causal blankets and maintained blankets;
(ii) an observable boundary-damage functional that avoids latent viable-manifold assumptions;
(iii) a repair-discovery statistic based on post-damage mean reversion and optional action-
mediated repair information;
(iv) a minimal synthetic experiment comparing active repair, passive repair, and boundary
decay.
The resulting method is deliberately conservative. It does not solve causal identification
from passive data. It instead separates what passive observation can support from what requires
interventions.
2
From causal blankets to maintained blankets
2.1
Plain UAD

$$
Let X1:T \inRT\timesn be a multivariate trace. A candidate boundary B is a partition
$$

B = (I, S, A, E),
(3) where I are candidate internal variables, S are candidate sensory variables, A are candidate active variables, and E are the remaining external variables.
Plain UAD [1] evaluates the blanket violation
LB = I(It+1; Et+1 | St, At).

$$
(4) A low value means that the interface (St, At) screens off internal and external futures. The candidate boundary is then an approximate \epsilon-blanket if
$$

$$
LB \leq\epsilon. (5)
$$

This is a separation test. It is not yet a viability test. It is also not a competence test:
blanket-information scores such as B-IQ measure prediction and control [5], not whether the
boundary itself is restored after damage.
2

---

2.2
Why separation is insufficient
Suppose a candidate partition satisfies Eq. 4 during an observation window. Several different
mechanisms can produce this:
(a) Accidental separation. The relevant variables are temporarily uncorrelated.
(b) Passive separation. Physical relaxation makes the boundary stable without controlled
repair.
(c) Externally imposed separation. Some outside process maintains the boundary.
(d) Homeostatic separation. The system contains feedback loops that restore the boundary
after perturbation.
(e) Agentic separation. The system allocates resources and actions to preserve the boundary
while pursuing other objectives.
Plain UAD does not distinguish these cases. It only sees the low conditional dependence.
But agents are not merely things with boundaries. They are things whose boundaries survive
because energy, control, and representation are continually spent on preserving them.
This suggests the stronger criterion [6]:
agent boundary = approximate separation + boundary maintenance.
(6) 3 The latent repair-capacity ideal It is useful to first state the ideal notion, then remove its unobservable parts.
Let D⋆
B(t) be the true boundary-damage state of candidate boundary B at time t. This
could include membrane tears, access-control failures, schema inconsistencies, resource depletion,
uncontrolled permeability, and other domain-specific degradation variables.
Given a perturbation class ∆, a policy class \PiK with resource budget K, and a recovery
horizon \tau, define latent repair capacity:
C⋆
repair(B) = sup

$$
\pi\in\PiK inf
$$

$$
\delta\in∆ E [D⋆
$$

B(t) −D⋆

$$
B(t + \tau) | do(\deltaBt), \pi] \tau
$$

.
(7) The uncontrolled entropic degradation rate is G⋆ entropy(B) = E D⋆

$$
B(t + \tau) −D⋆ B(t)
$$

\tau

$$
| \pi = \pipassive
$$

.
(8) The ideal viability condition is C⋆ repair(B) > G⋆ entropy(B).
(9) Equivalently, the repair margin m⋆ B = C⋆ repair(B) −G⋆
entropy(B)
(10) must be positive over the relevant perturbation class. This is conceptually right but empirically dangerous. It moves the problem into D⋆
B and the
viable boundary manifold. In real raw observational traces we do not usually observe either. If
we define them by hand, the method becomes circular.
Therefore we replace D⋆
B with an observable surrogate.
3

---

4
Observable boundary damage
Definition 1 (Observable boundary damage). Given a candidate partition B = (I, S, A, E),
define observable boundary damage as
DB(t) = wLbLB(t) + wV bVB(t) + wR bRB(t),
(11) where: bLB(t) = bIW (Iu+1; Eu+1 | Su, Au)t u=t−W , (12)
bVB(t) = H(Bt+1 | Bt),

$$
(13) bRB(t) = DKL (bp(Bt+1:t+h | Bt) ∥bp(Bt:t+h−1 | Bt−1)) . (14)
$$

The first term measures rolling blanket leakage.
The second term measures boundary
unpredictability. The third term measures local drift in boundary dynamics. All three are
observable from traces, modulo estimator limitations.
In minimal simulations we may include a directly observed boundary-integrity proxy qt, such
as membrane damage, authentication failure rate, or schema violation rate:
DB(t) = wLbLB(t) + wQqt + wV bVB(t).
(15) This does not change the conceptual status of the method. It merely uses a measured damage sensor when available. In real systems the choice of proxy is part of the audit design.
5
Repair discovery without interventions
5.1
Mean reversion of damage

$$
Let q\alpha(DB) be the empirical \alpha-quantile of boundary damage. Define high-damage times:
$$

$$
H\alpha = {t : DB(t) > q\alpha(DB)}. (16)
$$

$$
Definition 2 (Observational repair score). The observational repair score at horizon \tau is
$$

$$
RB(\tau, \alpha) = Et\inH\alpha DB(t) −DB(t + \tau)
$$

\tau

.
(17) If RB > 0, then high boundary damage tends to be followed by lower boundary damage. This is mean reversion of damage. It is observable and does not require handles.
But it is not yet causal repair. Passive physical relaxation can also generate RB > 0.
5.2
Action-mediated observational repair
A stronger observational statistic asks whether candidate active variables predict later damage
reduction beyond current damage and internal state:
Cact

$$
repair(B) = I (At; −∆\tauDB(t) | St, It, DB(t)) ,
$$

$$
(18) where ∆\tauDB(t) = DB(t + \tau) −DB(t).
$$

(19) This is not a causal effect. It is an action-channel repair signature. The causal claim would require interventions [7]:

$$
E[DB(t + \tau) | do(At = a)] ̸= E[DB(t + \tau)].
$$

(20) In this paper we explicitly do not assume access to such handles. 4

---

5.3
Maintained-boundary criterion
A candidate boundary is an observationally maintained approximate blanket when:

$$
¯LB \leq\epsilon, (21)
$$

$$
RB(\tau, \alpha) > r0. (22)
$$

It is an observationally action-mediated maintained blanket when additionally:
Cact
repair(B) > c0.
(23) This yields the taxonomy in Table 1. Type Observable condition Interpretation
Accidental blanket
low ¯LB only
separation appears but may not persist
Passive boundary
low ¯LB, RB > 0
damage mean-reverts, possibly by physics
Maintained
bound-
ary
low ¯LB, robust RB > 0
boundary-like process restores itself observa-
tionally
Action-mediated
boundary
above plus Cact
repair > 0
candidate actions predict repair
Interventionally
re-
paired boundary

$$
repair persists under do(\deltaB) tests
$$

causal repair established
Table 1: Boundary taxonomy. Passive observation can reach the first four rows only weakly.
The final row requires handles or interventions.
6
Minimal experiment
6.1
Purpose
The experiment asks whether the repair extension detects a distinction missed by plain UAD.
The aim is not to prove causal agency. The aim is to show that approximate separation and
boundary maintenance are different empirical axes.
6.2
Systems
We simulate three systems.
Active repair agent.
The agent has internal state It, sensory state St, action At, external
hazard Et, and boundary damage Qt. External hazard increases damage. When sensory variables
indicate damage, internal state activates a repair policy. The repair action reduces damage but
consumes resources. High damage increases leakage between internal and external variables.
Passive mean-reverter.
The system has boundary-like damage dynamics, but damage relaxes
passively toward a baseline. It contains no meaningful repair policy. Its action-like variable is
either noise or a correlate of the same dynamics. This is the crucial anti-example: a passive
system can look repaired from observational traces.
Decaying boundary.
The system starts with a boundary-like structure but lacks sufficient
repair. Damage tends to accumulate. Leakage rises and recovery after high-damage episodes is
weak.
5

---

6.3
Trace variables
Each simulated system produces a time series containing variables of the following form:
Xt = (It, St, At, Et, Qt, . . .).
(24) The synthetic ground-truth partition is supplied to the scoring procedure: B = (I, S, A, E). (25)
This isolates the repair-scoring question from the separate clustering problem. A full UAD
pipeline would first infer B from raw variables, then apply the maintained-boundary extension.
6.4
Estimators
All information quantities are estimated by discretization into bins. Conditional mutual infor-
mation is estimated by empirical plug-in counts:
bI(X; Y | Z) =
X
x,y,z
ˆp(x, y, z) log
ˆp(x, y | z)
ˆp(x | z)ˆp(y | z).
(26) For the minimal experiment this is sufficient. It is not recommended as the final estimator for high-dimensional systems. More realistic variants should use k-NN CMI, classifier-based
conditional dependence tests, or neural density-ratio estimators.
The damage functional used in the implementation is:
DB(t) = bLB,W (t) + 0.45Qt + 0.05|Qt −Qt−1|.
(27) Here bLB,W (t) is a rolling leakage estimate, Qt is the observed damage proxy, and |Qt −Qt−1| is
boundary volatility.

$$
The repair score uses \alpha = 0.8 and a fixed recovery horizon \tau:
$$

RB = E

$$
DB(t) −DB(t + \tau) \tau
$$

| DB(t) > q0.8

.

$$
(28) The action-repair score is estimated as a discretized conditional mutual information: bCact repair = bI (At; 1{DB(t + \tau) < DB(t)} | DB(t)) .
$$

(29) The implementation uses a simplified conditioning set for sample-size stability. This statistic is
included as a weak observational hint, not as causal evidence.
7
Results
Table 2 reports one representative run.
7.1
Interpretation
The active repair agent has the lowest mean damage and lowest plain UAD leakage. This is
expected: its repair policy keeps boundary damage low, and low damage reduces internal-external
leakage.
The passive mean-reverter has worse mean damage and worse leakage than the active repair
agent, but it has high damage reversion. This is the intended counterexample. Passive relaxation
can imitate repair under observational scoring. Therefore RB > 0 is not evidence of active
agency by itself.
6

---

Candidate
Plain UAD
leakage
Mean
damage
High-damage
reversion
Uncond.
reversion
Action-repair
CMI
Active repair agent
0.1048
0.2981
0.0071
-0.0003
0.0405
Passive mean-reverter
0.1257
0.5873
0.0082
0.0004
0.0374
Decaying boundary
0.1625
0.6565
0.0049
-0.0023
0.0238
Table 2: Minimal maintained-boundary experiment. Plain UAD leakage measures approximate
separation. High-damage reversion measures observational repair. Action-repair CMI is a weak
passive-data hint and should not be read causally.
The decaying boundary has the highest leakage, high damage, and weaker high-damage
reversion. It is still not completely monotone because stochastic episodes can temporarily reduce
damage, but it lacks the stable maintenance signature of the first two systems.
The action-repair CMI is highest for the active repair agent, slightly lower for the passive
mean-reverter, and lowest for the decaying boundary. This is directionally suggestive but not
decisive. In passive data, an action-like variable can correlate with restoration because both are
driven by hidden state, hazard cycles, or the damage process itself.
8
What the experiment shows
The experiment supports three narrow claims.
Claim 1 (Plain UAD is a separation test, not a viability test). A low value of I(It+1; Et+1 | St, At)
can identify an approximate causal boundary, but it does not determine whether the boundary is
actively maintained, passively stable, externally imposed, or transient.
Claim 2 (Repair is observable as damage mean reversion). Given an observable boundary-damage
functional DB(t), passive traces can reveal whether high-damage episodes tend to be followed by
recovery. This is a genuine additional empirical axis beyond plain leakage.
Claim 3 (Active repair is not identifiable from passive traces alone). Without interventions or
handles, action-mediated repair scores can suggest active maintenance but cannot distinguish it
reliably from passive mean reversion or common-cause correlation.
The third claim is as important as the first two. The extension does not make causal
agency magically observable. It clarifies the boundary between observational evidence and
interventionally grounded evidence.
9
Discussion
9.1
Why not use distance to a viable manifold?
A natural first formulation defines boundary damage as distance from a viable boundary manifold:
d(Bt, MB).
(30) This is mathematically attractive but empirically suspect. In raw observational settings, MB is usually unavailable. If the researcher defines it by domain intuition, the agent-discovery
procedure inherits the researcher’s ontology. That defeats the purpose of unsupervised discovery.
The observable damage formulation avoids this by using predictive consequences:
DB(t) = leakage + volatility + drift + available damage proxies.
(31) This is less metaphysically satisfying but more operationally honest. 7

---

9.2
Boundary maintenance as anti-entropic control
A maintained boundary is a local violation of passive decay, paid for by resources. Cells pump ions
and repair membranes. Animals regulate temperature and immune boundaries. Organizations
maintain membership, roles, accounting, access control, and legal identity. Software services
maintain dependency versions, schemas, certificates, credentials, tests, alerts, and rollback paths.
This suggests that boundary maintenance is not an optional supplement to agency. It is
one of the physical signatures of agency. An agent that cannot maintain its boundary becomes
environment, debris, or substrate for another process.
Formally, the maintained-boundary view adds a second inequality to the ordinary blanket
condition:

$$
I(It+1; Et+1 | St, At) \leq\epsilon, (32)
$$

$$
RB(\tau, \alpha) > r0. (33)
$$

In intervention-rich settings, one should replace the second inequality with a causal repair
condition:

$$
E[DB(t + \tau) | do(\deltaBt), \picandidate] < E[DB(t + \tau) | do(\deltaBt), \piablated].
$$

(34) 9.3 Relation to agent discovery UAD asks: where is the approximate boundary [1]? Maintained-boundary UAD asks: which approximate boundaries are restored after degrada-
tion?
B-IQ and related scores ask: how much predictive/control competence does that boundary
carry [5]?
Handle-based UAD [8] asks: which approximate boundaries resist or compensate when
perturbed?
These form a natural ladder:
separation \toobservational recovery \toaction-predictive recovery \tointerventional repair.
(35) The first two can be attempted from ordinary traces. The last two require stronger assump- tions, better variables, or actual perturbations.
10
Failure modes
Passive relaxation.
A soap bubble, elastic membrane, or stable physical equilibrium may
show high RB without agency. This is why repair mean reversion is not sufficient.
Hidden common causes.
An unobserved variable may drive both action-like variables and
later damage reduction. Then Cact
repair is inflated.
Bad damage proxies.
If DB uses the wrong observables, it may measure environmental
fluctuations rather than boundary degradation.
Estimator artifacts.
Discretized CMI is biased in finite samples, especially with many
conditioning states. Rolling estimates can induce apparent damage oscillations.
Over-smoothing.
If traces are temporally smoothed, repair may look slower, leakage may be
underestimated, and active correction may be blurred into passive mean reversion [9].
8

---

Adaptive hiding.
An adversarial agent may repair only below the observation resolution, or
may preserve the functional boundary while making the statistical boundary appear passive [10].
11
Implications for future work
The next step is not to make the observational score more elaborate. The next step is to add
handles. A handle is an interventionable variable or interface through which the candidate
boundary can be perturbed. With handles, repair capacity can be measured by recovery under
controlled disturbance:
Rdo

$$
B (\delta, \tau) = E [DB(t) −DB(t + \tau) | do(\deltaBt)] /\tau.
$$

$$
(36) One can then test ablations: ∆Rdo B = Rdo B (\piintact) −Rdo
$$

B (\piablated).
(37) This is the proper causal version of repair discovery. For practical systems, relevant handles include:
• perturbing access-control state in a sandbox;
• injecting schema drift into a service boundary;
• degrading communication channels between modules;
• varying environmental hazards in simulation;
• ablating candidate repair variables;
• measuring recovery time, leakage, and resource expenditure.
12
Conclusion
An approximate Markov blanket is not yet a real agent boundary. It is a conditional-independence
pattern. Real agent boundaries are maintained against entropy. They persist because some
process spends resources to keep leakage, volatility, and drift within viable ranges.
This paper proposed an observable extension of UAD [1,11] that adds boundary repair to
boundary separation. The extension avoids a hidden viable-manifold term by defining damage
through observable predictive consequences. In a minimal synthetic experiment, plain UAD
measures approximate separation, while the repair score detects whether high-damage episodes
tend to recover. The experiment also shows the central limitation: passive mean reversion can
imitate repair. Therefore passive data can support a maintained-boundary hypothesis, but not
establish active repair agency.
The resulting lesson is simple:
Agency discovery should not only ask where the boundary is. It should ask what
keeps the boundary from falling apart.
References
[1] G. Zarncke, “Foundations of unsupervised agent discovery in raw dynamical systems,” AE
Studio, 2025.
[2] K. Friston, “The free-energy principle: a unified brain theory?” Nature Reviews Neuro-
science, vol. 11, no. 2, pp. 127–138, 2010.
9

---

[3] M. D. Kirchhoff, T. Parr, E. Palacios, K. Friston, and J. Kiverstein, “The markov blankets
of life: autonomy, active inference and the free energy principle,” Journal of the Royal
Society Interface, vol. 15, no. 138, p. 20170792, 2018.
[4] M. J. Ramstead et al., “Bayesian mechanics,” Neural Networks, vol. 154, pp. 592–609, 2022.
[5] G. Zarncke, “Bitwise intelligence: A blanket–information measure of competence,” AE
Studio, 2025.
[6] R. C. Conant and W. R. Ashby, “Every good regulator of a system must be a model of
that system,” International Journal of Systems Science, vol. 1, no. 2, pp. 89–97, 1970.
[7] J. Pearl, Causality: Models, Reasoning, and Inference, 2nd ed.
Cambridge University
Press, 2009.
[8] G. Zarncke, “Handles before interventions: Access-model UAD and the embedded semantics
of agency tests,” AE Studio, 2025.
[9] ——, “Recoverability of smoothed agent boundaries in unsupervised agent discovery,” AE
Studio, 2026.
[10] ——, “Stealth–capability bounds for multi-resolution unsupervised agent discovery,” AE
Studio, 2026.
[11] N. Tishby, F. C. Pereira, and W. Bialek, “The information bottleneck method,” 2000.
10
