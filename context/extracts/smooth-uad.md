# Extract: smooth-uad.pdf

**Source PDF:** `context/smooth-uad.pdf`
**Extract:** `context/extracts/smooth-uad.md`
**Pages:** 8
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

Recoverability of Smoothed Agent Boundaries in Unsupervised Agent
Discovery
Gunnar Zarncke
AE Studio
Abstract
Unsupervised Agent Discovery (UAD) [1] identifies candidate agents in raw dynamical systems by searching
for approximately Markov-blanketed clusters whose internal and external futures are conditionally independent
given sensory and active boundary variables. In realistic measurement regimes, however, the available
observables are rarely raw. Neural calcium imaging, low-frequency behavioral logging, spatially averaged
sensors, segmentation pipelines, and economic or organizational aggregates all impose temporal smoothing,
variable mixing, coarse-graining, and measurement noise. This paper gives a compact recoverability theory

$$
for such settings. We model the measured process as an observation-channel transform Yt = K(Xt−r:t) + \etat
$$

$$
of an underlying dynamical process Xt. We show that an \epsilon-blanket is recoverable only up to the equivalence
$$

class induced by K, and derive a finite-sample lower bound of the form

$$
P[ ˆC \in[C⋆]K] \geq1 −2|C| exp
$$

$$
−Teff(∆−2\deltaK)2 8B2
$$

,

$$
where C⋆is the true agent, ∆is its blanket-separation margin, \deltaK is observation-channel distortion, Teff is
$$

autocorrelation-adjusted effective sample size, and B controls estimator scale. We then report a minimal
finite-state-machine experiment with known internal state, known sensor/action channels, noisy environment,
and distractor variables. Temporal smoothing mainly reduces Teff and inflates apparent memory; variable
smoothing directly increases \deltaK and can destroy identifiability by mixing internal and external variables.
Empirically, the bound is conservative but directionally correct: recovery remains high until the margin is
eaten by smoothing distortion or effective sample size collapses.
1
Problem
UAD [1] begins with timestamped variables
Xt = (X1(t), . . . , Xn(t))
and seeks clusters C ⊆{1, . . . , n} admitting a partition

$$
C = IC \cupSC \cupAC such that internal and external futures are screened off by sensory and active boundary variables:
$$

JX(C) := IX(IC
t+1; EC
t+1 | SC
t , AC

$$
t ) \leq\epsilon. (1)
$$

Here EC denotes variables outside C. A perfect blanket would have JX(C) = 0, but realistic systems require

$$
\epsilon-blankets: finite data, overlapping controllers, hidden variables, and measurement noise make exact conditional
$$

independence implausible.
The difficulty considered here is sharper. In empirical settings, UAD rarely observes Xt directly. It observes

$$
Yt = K(Xt−r:t) + \etat, (2)
$$

where K may smooth over time, mix variables, coarse-grain states, apply segmentation, or impose a calcium-
imaging kernel. Thus UAD estimates
JY (C) = IY (IC
t+1; EC
t+1 | SC
t , AC
t ),
not JX(C). The question is therefore not whether smoothing adds ordinary noise. It changes the graphical
object being discovered.
The target guarantee has the shape:
if an agent is present and its sensors/actions are known up to smoothing K,
then it is recovered with likelihood p.
The central claim of this paper is that such a guarantee is possible only for the K-equivalence class of the agent,
not generally for its exact raw boundary.
1

---

2
Observation-channel equivalence
Definition 1 (UAD blanket score). For a candidate cluster C, define the raw and observed blanket violations
JX(C) = IX(IC
t+1; EC
t+1 | SC
t , AC
t ),
JK(C) = JY (C).
The UAD estimator returns
ˆC \inarg min
C\inC
ˆJK(C),
where C is a finite candidate class.

$$
Definition 2 (K-equivalence). Two clusters C, C′ \inC are observationally equivalent under K, written C ∼K C′,
$$

if they induce the same conditional distribution over the observed process relevant to the blanket test:
P(Y C

$$
t+1, Y \negC t+1, Y SC
$$

t
, Y AC
t
) = P(Y C′

$$
t+1, Y \negC′ t+1 , Y SC′
$$

t
, Y AC′
t
),
up to the chosen coarse-graining and candidate representation. The recoverable target is

$$
[C⋆]K = {C \inC : C ∼K C⋆}. Remark 1. If K is invertible on the variables and timescales relevant to the blanket, then [C⋆]K can collapse
$$

to the exact raw cluster. If K is many-to-one, only the induced coarse-grained boundary can be recovered. If K
mixes internal and external variables strongly enough, two different raw agent structures can induce the same
observed process; no unsupervised method can distinguish them without extra assumptions or interventions.
3
Recoverability theorem
Let C⋆be the true agent cluster or true recoverable coarse-grained cluster.
Assumption 1 (Approximate blanket).

$$
JX(C⋆) \leq\epsilon0. Assumption 2 (Separation margin). There is a margin ∆> 0 such that every non-equivalent candidate has
$$

larger raw blanket violation:
inf

$$
C /\in[C⋆]K [JX(C) −JX(C⋆)] \geq∆. (3)
$$

Assumption 3 (Observation distortion). The observation channel perturbs blanket scores by at most
sup
C\inC

$$
|JK(C) −JX(C)| \leq\deltaK. (4)
$$

We decompose

$$
\deltaK = \deltatime + \deltavar + \deltacoarse + \deltanoise. Assumption 4 (Uniform concentration). For some estimator scale B > 0, effective sample size Teff, and all
$$

ϵ > 0,
P

sup
C\inC
| ˆJK(C) −JK(C)| > ϵ

$$
\leq2|C| exp
$$

−Teffϵ2
2B2

.

$$
(5) Theorem 1 (Finite-sample recovery under smoothing). If ∆> 2\deltaK,
$$

then

$$
P[ ˆC \in[C⋆]K] \geq1 −2|C| exp
$$

$$
−Teff(∆−2\deltaK)2 8B2
$$

.

$$
(6) If ∆\leq2\deltaK, the bound gives no nontrivial recovery guarantee.
$$

$$
Proof. For C /\in[C⋆]K, Assumptions 3 and 4 imply
$$

$$
JK(C) −JK(C⋆) \geqJX(C) −JX(C⋆) −2\deltaK \geq∆−2\deltaK.
$$

Thus the observed population score has positive separation

$$
gK := ∆−2\deltaK > 0. 2
$$

---

If
sup
C\inC
| ˆJK(C) −JK(C)| < gK/2,

$$
then for every C /\in[C⋆]K, ˆJK(C) −ˆJK(C⋆) \geqgK −2(gK/2) = 0,
$$

so no non-equivalent candidate beats the true equivalence class. Applying the concentration bound with ϵ = gK/2
yields Eq. (6).
Remark 2 (The bound is intentionally conservative). The theorem protects against the worst candidate in C,
the worst score perturbation under K, and the worst estimator deviation. Empirical recovery can remain high

$$
even when ∆−2\deltaK < 0, but in that regime recovery is not guaranteed by the available margin argument.
$$

4
Temporal smoothing
Consider a temporal observation channel
Yt =
r
X

$$
ℓ=0 hℓXt−ℓ+ \etat.
$$

(7) Even if Xt is Markov of order m, Yt need not be Markov of order m. Smoothing stores information from the
past in the present observable. Thus a first-order blanket test can falsely report residual coupling:
I(Y I
t+1; Y E
t+1 | Y S
t , Y A
t ) > 0
because the conditioning set omits latent filter state.
The standard repair is delay embedding:
¯Yt = (Yt, Yt−1, . . . , Yt−L).
A sufficient condition is approximate delay sufficiency:

$$
I(Xt+1; X<t−L | ¯Yt) \leq\deltadelay. (8)
$$

For finite-memory dynamics and finite-memory filters, one expects L ≳r + m. If this holds,

$$
\deltatime ≲\deltadelay + \deltadeconv, where \deltadeconv captures non-invertible loss in the temporal kernel. Temporal smoothing also reduces effective sample size. For an approximately stationary scalar trace with
$$

autocorrelation \rhok,
Teff \approx
T
1 + 2 P

$$
k\geq1 \rhok .
$$

$$
(9) Thus temporal smoothing harms recovery through two channels: \deltaK ↑,
$$

Teff ↓.
Conceptually, it inflates apparent memory, blurs causal ordering, and makes fast sensorimotor blankets less
visible. But it may improve recovery of slow behavioral-state agents by suppressing irrelevant high-frequency
noise.
Corollary 1 (Temporal smoothing). Under delay sufficiency and weak temporal information loss, recovery
remains likely if

$$
∆> 2(\deltadelay + \deltadeconv + \deltanoise) + 2ϵest(Teff),
$$

where
ϵest(Teff) = O

B
s

$$
log |C| + log(1/\alpha) Teff
$$


.
3

---

5
Variable smoothing
Variable smoothing has the form

$$
Yt = MXt + \etat. (10)
$$

Let the true partition be ordered as (I, S, A, E). Decompose
M =




MI
0
0
0
0
MS
0
0
0
0
MA
0
0
0
0
ME



+ R,
where R contains cross-boundary leakage. If R = 0, variable smoothing only coarse-grains within the relevant
parts. Recovery of a coarse-grained blanket can still be possible. If R ̸= 0, internal variables may contain
external information and external variables may contain internal information. Then the observed conditional
independence relation is not the raw one.
In smooth sub-Gaussian or Gaussian regimes, a schematic perturbation estimate is

$$
\deltavar = O ∥R∥2
$$

\sigma2
min

,
where \sigmamin is the smallest singular value of the within-block observation map relevant to the blanket variables.
This expression should not be read as universal; it gives the correct qualitative dependence. Cross-boundary
mixing is dangerous when it is large relative to within-boundary signal strength.
Corollary 2 (Variable smoothing). If M is approximately block-diagonal relative to the true blanket partition
and the within-block maps preserve the sufficient sensory/action variables, UAD can recover the corresponding
coarse-grained blanket. If R is large enough that

$$
\deltavar \geq∆/2, no margin-based recovery guarantee is available.
$$

6
Agenthood beyond boundaryhood
A low conditional-mutual-information boundary is not sufficient for agency. Rocks, vortices, and stable chemical
aggregates can have boundaries [2]. UAD-style agent discovery therefore benefits from coupling blanketness to
predictive and control information [3]. A generic competence score is

$$
B(C) = I(IC t ; SC t+1) + I(AC t ; EC t+1) −\betaH(IC
$$

$$
t ) −\gammaSC, where SC = E[−log P(SC
$$

t+1 | IC
t )] is residual sensory surprise. One may instead use an intentional-compression
score [4]

$$
∆LC = Lintentional(C) −Lmechanistic(C) −\lambdaDL(rC).
$$

The mature recovery objective is not simply
arg min
C J(C),
but something like
arg min
C [J(C) −\lambdaBB(C) −\lambdaL∆LC] .
The same theorem applies with J replaced by any score F that has a separation margin and a smoothing
perturbation bound.
7
Minimal FSM experiment
We tested the bound on a controlled binary finite-state system with known agent structure. The latent process
contains
Xt = (It, St, At, Et, Dt),
where It is the true internal FSM state, St is the known sensor, At is the known action, Et is the environment,
and Dt is an environment-correlated distractor. The transition structure is

$$
St = Et \oplus\xiS t ,
$$

$$
At = It \oplusSt, 4
$$

---

$$
It+1 = It \oplusSt, Et+1 = At \oplus\xiE
$$

t ,

$$
Dt+1 = Et+1 \oplus\xiD t .
$$

The true recoverable internal candidate is I. Competing candidates are E and D. Recovery succeeds when
ˆC = arg
min

$$
C\in{I,E,D} ˆI(Ct+1; EC
$$

t+1 | St, At)
equals I.
The raw margin was estimated from a long reference run:
∆\approx0.240447.
We then evaluated two observation-channel families.
Temporal smoothing.

$$
Yt = (1 −\alpha)Xt + \alphaYt−1 + \etat. The smoothing parameter \alpha \in[0, 1) controls low-pass memory.
$$

Variable smoothing.

$$
Yt = M\lambdaXt + \etat, where \lambda controls cross-boundary leakage between internal and external variables.
$$

For each smoothing setting, the experiment estimated:

$$
\deltaK \approx max
$$

$$
C\in{I,E,D} |JK(C) −JX(C)|, Teff \approx
$$

T
1 + 2 P

$$
k\geq1 \rhok ,
$$

and the lower bound
pbound = max

0, 1 −2|C| exp

$$
−Teff(∆−2\deltaK)2 8B2
$$

.
The empirical recovery probability pemp was estimated over repeated trials.
8
Results
Type
Strength
\deltaK

$$
∆−2\deltaK Teff
$$

pbound
pemp
Temporal
0.000
0.000
0.240
2431 0.999 1.000 Temporal 0.200
0.001
0.239
1649 0.987 1.000 Temporal 0.400
0.073
0.095
1047 0.000 1.000 Temporal 0.600
0.057
0.127
631 0.000 1.000 Temporal 0.800
0.047
0.147
300 0.000 1.000 Temporal 0.920
0.139
-0.038
125 0.000 1.000 Temporal 0.985
0.195
-0.150
45
0.000
0.983
Temporal
0.995
0.227
-0.214
29
0.000
0.683
Variable
0.000
0.000
0.240
2435 0.999 1.000 Variable 0.050
0.000
0.240
2346 0.999 1.000 Variable 0.100
0.000
0.240
2189 0.998 1.000 Variable 0.150
0.000
0.240
2140 0.998 1.000 Variable 0.200
0.012
0.217
2039 0.988 1.000 Variable 0.250
0.128
-0.016
1961 0.000 1.000 Variable 0.300
0.298
-0.355
1889 0.000 1.000 Variable 0.400
0.320
-0.399
1799 0.000 0.783 Table 1: Finite-sample recovery under temporal and variable smoothing. The bound is a lower bound and

$$
becomes vacuous when ∆−2\deltaK \leq0. Empirical recovery may remain high beyond the guaranteed regime.
$$

5

---

Placeholder for Figure 1
Temporal smoothing: empirical recovery probability and theoretical lower bound versus
smoothing strength \alpha.

$$
Expected pattern: Teff collapses as \alpha \to1; empirical recovery remains high until extreme
$$

low-pass smoothing.
Figure 1: Temporal smoothing mainly harms recovery by increasing autocorrelation and reducing effective
sample size, with eventual margin collapse at extreme smoothing.
Placeholder for Figure 2
Variable smoothing: empirical recovery probability and theoretical lower bound versus
cross-boundary mixing strength \lambda.
Expected pattern: recovery remains strong while leakage is weak; strong cross-boundary
mixing makes candidate scores nearly indistinguishable.

$$
Figure 2: Variable smoothing directly attacks identifiability by increasing \deltaK, rather than merely reducing
$$

effective sample size.
9
Interpretation
The experiment supports four claims.
First, the margin term is the right conceptual object. When

$$
∆−2\deltaK > 0, the bound can be nontrivial and recovery is robust. When
$$

$$
∆−2\deltaK \leq0, the bound becomes silent. This does not imply empirical failure; it means the theorem no longer certifies success.
$$

Second, temporal smoothing is usually less structurally destructive than cross-variable smoothing. It mainly
modifies time scale:
Teff ↓,
apparent memory ↑,
causal timing resolution ↓.
An FSM whose relevant dynamics survive low-pass filtering can still be recovered, but fast blankets disappear
first.
Third, variable smoothing can destroy the target itself. Once internal and external variables are strongly
mixed, the observed process may no longer contain enough information to decide which raw variable was the
internal state. In the experiment, strong variable smoothing pushed
J(I) \approxJ(E) \approxJ(D), which is precisely the finite-candidate version of observational non-identifiability.
Fourth, the bound is conservative. At several smoothing values the lower bound is zero while empirical
recovery remains one. This is expected because the proof uses the worst-case uniform deviation and worst-case
score perturbation. Its role is certification, not prediction of the exact recovery curve.
6

---

10
Implications for smoothed biological observables
In calcium imaging, population calcium traces are not raw neural activity. They are temporally convolved,
spatially mixed, segmented, motion-corrected, and often postprocessed [5,6]:

$$
Yt = KsegKspatialKcalciumXt + \etat. The theory predicts:
$$

temporal calcium kernel \Rightarrowinflated apparent memory and slower inferred agency,
spatial/segmentation mixing \Rightarrowover-merged variables and shifted boundaries.
Thus UAD on calcium data should generally be interpreted as recovering coarse behavioral-state or neural-
population blankets, not spike-level agent boundaries, unless the result is stable under delay embedding,
deconvolution, segmentation perturbations, and cross-neuron leakage controls.
11
Practical recovery protocol
A practical smoothed-UAD protocol should not run UAD on one preprocessed trace and declare the resulting
cluster an agent. It should construct a family of observation channels:

$$
{K\sigma}\sigma\in\Sigma, including different temporal lags, deconvolution strengths, bin widths, masks, and leakage controls, then estimate
$$

C⋆= arg min
C E\sigma\in\SigmaJK\sigma(C) + \lambda Var\sigma(JK\sigma(C)).
A credible recovered agent is one whose boundary is stable under moderate perturbations of the observation
channel. A boundary that appears only at one smoothing scale is more plausibly a filter artifact.
The empirical diagnostic is:
b∆K =
min

$$
C /\in[ ˆ C]K
$$

ˆJK(C) −ˆJK( ˆC).
Recovery is credible when
b∆K ≫2b\deltaK + 2bϵest.
It is fragile when this inequality fails.
12
Conclusion
The recoverability of agents under smoothed observables is governed by a simple ratio:
recoverability ∼blanket separation margin −observation distortion
estimation noise
.
Temporal smoothing primarily creates hidden filter memory and reduces effective sample size. Variable smoothing
changes the observable ontology and can eliminate identifiability. The finite-sample theorem formalizes this by
requiring

$$
∆> 2\deltaK and then giving an explicit lower bound on recovery probability. The FSM experiment confirms the predicted
$$

qualitative structure: recovery is robust under weak smoothing, certification disappears when smoothing eats
the margin, and empirical failure appears when extreme smoothing collapses candidate distinctions.
The appropriate claim is therefore not:
“UAD recovers the true raw agent despite smoothing.”
The correct claim is:
“UAD can recover the K-observable equivalence class of an agent
when the blanket margin exceeds observation distortion and finite-sample error.”
This distinction is especially important for biological and social data, where the measurement process is often a
large part of the apparent system dynamics [7–9].
7

---

References
[1] G. Zarncke, “Foundations of unsupervised agent discovery in raw dynamical systems,” AE Studio, 2025.
[2] M. D. Kirchhoff, T. Parr, E. Palacios, K. Friston, and J. Kiverstein, “The markov blankets of life: autonomy,
active inference and the free energy principle,” Journal of the Royal Society Interface, vol. 15, no. 138, p.
20170792, 2018.
[3] G. Zarncke, “Bitwise intelligence: A blanket–information measure of competence,” AE Studio, 2025.
[4] ——, “The endogenized intentional stance: A predictive–compression formalization of agent discovery,” AE
Studio, 2025.
[5] K. Friston, “The free-energy principle: a unified brain theory?” Nature Reviews Neuroscience, vol. 11, no. 2,
pp. 127–138, 2010.
[6] L. P. Kaelbling, M. L. Littman, and A. R. Cassandra, “Planning and acting in partially observable stochastic
domains,” Artificial Intelligence, vol. 101, no. 1–2, pp. 99–134, 1998.
[7] R. C. Conant and W. R. Ashby, “Every good regulator of a system must be a model of that system,”
International Journal of Systems Science, vol. 1, no. 2, pp. 89–97, 1970.
[8] M. Biehl and N. Virgo, “Interpreting systems as solving POMDPs: A step towards a formal understanding
of agency,” 2025, v2.
[9] N. Tishby, F. C. Pereira, and W. Bialek, “The information bottleneck method,” 2000.
8
