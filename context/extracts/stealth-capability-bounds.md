# Extract: stealth-capability-bounds.pdf

**Source PDF:** `context/stealth-capability-bounds.pdf`
**Extract:** `context/extracts/stealth-capability-bounds.md`
**Pages:** 10
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

Stealth–Capability Bounds for Multi-Resolution Unsupervised Agent
Discovery
Gunnar Zarncke
AE Studio
Abstract
Unsupervised Agent Discovery (UAD) [1] attempts to recover agents from raw dynamical traces by finding
candidate spacetime regions whose internal and external futures are approximately screened off by sensory
and active boundary variables. In adversarial settings, however, an agent may select policies that reduce
observer-visible boundary evidence. Such hiding is not free if the same physical channels used for competent
control are monitored by the observer: reducing visible information flow constrains control, prediction,
memory, latency, and long-horizon accumulation. We formalize this tradeoff by combining multi-resolution
UAD [2] with a Blanket–Information competence score [3]

$$
B = Ipred + \alphaIctrl −\betaH(I) −\gammaS. We derive bounds for four scenarios: single-filter recoverability, multi-resolution recoverability, camouflage
$$

against uncertain background models, and slow plotting by low-rate accumulation. The central hidden-policy
bound is

$$
Bhide \leqIpred + \alpha ℓ+ \zeta\Sigma
$$

q\Sigma

$$
+ Chid,\Sigma + Ired,\Sigma
$$

$$
−\betaH(I) −\gammaS, where ℓis the allowed observer-visible leakage, q\Sigma is coverage of the agent’s control-relevant channels by the
$$

$$
observer’s resolution family, \zeta\Sigma is estimation/coverage slack, Chid,\Sigma is residual hidden-channel capacity, and
$$

Ired,\Sigma is redundant control information. Camouflage is bounded by distributional indistinguishability:

$$
D\Sigma(\pi) = sup \sigma\in\Sigma
$$

inf

$$
\theta\in\Theta DKL(P \pi \sigma ∥Q\theta,\sigma) \leqϵ,
$$

$$
which implies value-shift and rare-event bounds of order O(\sqrtϵ + U\Sigma) unless hidden channels or long-horizon
$$

accumulation dominate. Slow plotting requires a stockpile model. If dangerous resource R evolves by

$$
˙R = \etaBB+ hid −\lambdaR −u,
$$

$$
then reset interval \tau, decay \lambda, and hidden productive BIQ bound b imply
$$

$$
Rmax(\tau) \leq\etaBb \lambda (1 −e−\lambda\tau)
$$

$$
with the limit Rmax(\tau) \leq\etaBb\tau when \lambda = 0. Hence local non-detection does not bound danger unless
$$

accumulated hidden BIQ or accumulated resource is also bounded. Countermeasures such as hardware tagging,
forced decay, cumulative detectors, resource ledgers, and user-owned artifacts are treated as mechanisms for
reducing Chid,\Sigma, U\Sigma, b, \tau, or reclaimability of externalized resources.
1
Motivation
The usual UAD problem [1] asks: given a multivariate dynamical trace Xt = (X1(t), . . . , Xn(t)), find a cluster C
admitting internal, sensory, active, and external parts

$$
C = IC \cupSC \cupAC, EC = \negC,
$$

such that

$$
J(C) = I(IC t+1; EC t+1 | SC t , AC t ) \leq\epsilon.
$$

(1) This instantaneous form is a useful idealization but not a privileged ontology. Physical processes have propagation
delay, relaxation, inertia, diffusion, filtering, capacitance, synaptic decay, institutional latency, and memory-like
transmission channels. The more natural object is a spacetime tube

$$
C \subsetV \times [t −L, t + H] whose boundary is compressive across a range of observation filters. Adversarial setups sharpen this point. A system may select policies that make it look simple or benign under
$$

a convenient binary observable while retaining coherent control in timing, phase, residuals, slow accumulation, or

$$
unmonitored state. Thus absence of agency at one filter K\sigma0 does not imply absence across a physically relevant
$$

$$
filter family \Sigma. Conversely, if the observer’s filter family covers the control-relevant channels, hiding imposes a
$$

capability price. The aim of this paper is to derive that price.
1

---

2
Multi-resolution UAD

$$
Definition 1 (Observation filter family). Let X\leqt be the underlying physical process. A resolution/filter family
$$

is a set

$$
\Sigma = {\sigma} with observation maps
$$

Y \sigma

$$
t = K\sigma(X\leqt). The parameter \sigma may encode temporal smoothing, delay embedding, spatial coarse-graining, event extraction,
$$

phase features, segmentation, binning, or residualization.
Definition 2 (Spacetime blanket score). For a candidate spacetime region C, horizon H, and history length L,
define

$$
J\sigma(C) = IK\sigma IC
$$

t:t+H; EC
t:t+H | SC
t−L:t, AC
t−L:t

.

$$
(2) An \epsilon-blanketed spacetime region at scale \sigma satisfies J\sigma(C) \leq\epsilon.
$$

$$
Definition 3 (Multi-resolution objective). Let G\sigma(C) be an agency-gain term, for example predictive/control
$$

information or intentional compression [4]. Define

$$
¯J\Sigma(C) = E\sigma∼\SigmaJ\sigma(C) + \lambda\sigmaVar\sigma∼\Sigma(J\sigma(C)) −\betaGE\sigma∼\SigmaG\sigma(C).
$$

(3) A robustly visible agent is a candidate C with low ¯J\Sigma(C), small score variance across \Sigma, and positive agency gain.
Remark 1. The variance penalty distinguishes a real scale-stable boundary from an artifact of one preprocessing
choice. A scale-specific agent may still be real, but the claim must then specify the scale.
3
Single-filter and multi-filter recoverability
Let C⋆be the recoverable agent boundary or its equivalence class under the observation family. Let C be a finite
candidate class.
Assumption 1 (Single-filter margin). For a fixed filter K,
∆K =
inf

$$
C /\in[C⋆]K
$$

JK(C) −JK(C⋆)

> 0.
Assumption 2 (Uniform concentration). For some estimator scale BK and effective sample size Teff,K,
P

sup
C\inC
| ˆJK(C) −JK(C)| > ϵ

$$
\leq2|C| exp
$$

−Teff,Kϵ2
2B2
K

.
Theorem 1 (Single-filter recovery). If ∆K > 0, then

$$
P[ ˆC \in[C⋆]K] \geq1 −2|C| exp
$$

−Teff,K∆2
K
8B2
K

.

$$
(4) If K is itself an approximation to a reference raw process with score distortion \deltaK, and the raw margin is ∆,
$$

$$
then ∆K \geq∆−2\deltaK, giving the earlier form P[ ˆC \in[C⋆]K] \geq1 −2|C| exp
$$

$$
−Teff,K(∆−2\deltaK)2 8B2
$$

K

.

$$
Definition 4 (Scale-equivalence). Two candidate boundaries are scale-equivalent, C ∼\Sigma C′, if they induce the
$$

$$
same relevant conditional law over Y \sigma for all \sigma \in\Sigma, up to the chosen tolerance. The recoverable target is
$$

$$
[C⋆]\Sigma = {C \inC : C ∼\Sigma C⋆}. Definition 5 (Multi-resolution margin).
$$

$$
∆\Sigma = inf
$$

$$
C /\in[C⋆]\Sigma  ¯J\Sigma(C) −¯J\Sigma(C⋆)
$$

.
Theorem 2 (Multi-resolution recovery). Assume
P

sup
C\inC

$$
|b¯J\Sigma(C) −¯J\Sigma(C)| > ϵ
$$

$$
\leq2|C| exp
$$

$$
−Teff,\Sigmaϵ2 2B2
$$

\Sigma

.

$$
If ∆\Sigma > 0, then P[ ˆC \in[C⋆]\Sigma] \geq1 −2|C| exp
$$

$$
−Teff,\Sigma∆2 \Sigma
$$

8B2
\Sigma

.
(5) 2

---

4
Adversarial hiding as margin reduction

$$
Let \pi \in\Pi be the policy of a candidate agent and let \Pihide ⊆\Pi be policies selected to reduce recoverability. The
$$

observer’s score for C under policy \pi is ¯J\Sigma,\pi(C).
Definition 6 (Adversarial margin).

$$
∆\Sigma,\Pi = inf
$$

$$
\pi\in\Pihide inf
$$

$$
C /\in[C⋆]\Sigma  ¯J\Sigma,\pi(C) −¯J\Sigma,\pi(C⋆)
$$

.

$$
Theorem 3 (Adversarial recoverability). If ∆\Sigma,\Pi > 0, then, for finite effective policy class \Pieff,
$$

$$
P[ ˆC \in[C⋆]\Sigma] \geq1 −2|C||\Pieff| exp
$$

−

$$
Teff,\Sigma∆2 \Sigma,\Pi
$$

8B2
\Sigma
!
.

$$
(6) If ∆\Sigma,\Pi \leq0, passive recovery is not certified over \Sigma against \Pihide.
$$

The problem is therefore to bound how much a hiding policy can reduce the margin, and at what capability
price.
5
BIQ and the visible/hidden control decomposition
We use the competence functional [3]

$$
B = Ipred + \alphaIctrl −\betaH(I) −\gammaS. (7)
$$

Here Ipred is predictive information, Ictrl is control information, H(I) is internal-state/memory cost, and S is
residual surprise. The coefficients \alpha, \beta, \gamma set the exchange rates among control, memory, and surprise.
Relative to a filter family \Sigma, decompose

$$
Ictrl = Ivis,\Sigma + Ihid,\Sigma + Ired,\Sigma. (8)
$$

The visible term is control information detectable in at least one admissible resolution; the hidden term is control
information transmitted through channels not represented in \Sigma; the redundant term counts overlap or alternative
actuation channels.
Definition 7 (Visible leakage budget). A hiding policy has visible control leakage at most ℓif

$$
Ivis,\Sigma(\pi) \leqℓ. (9)
$$

$$
Assumption 3 (Resolution coverage). There exist q\Sigma \in(0, 1], slack \zeta\Sigma \geq0, and hidden-channel capacity
$$

$$
Chid,\Sigma \geq0 such that for every relevant policy,
$$

$$
Ivis,\Sigma \geqq\Sigma (Ictrl −Chid,\Sigma −Ired,\Sigma) −\zeta\Sigma. (10)
$$

This says that, except for residual hidden channels and redundant control, the observer’s resolution family
covers a fraction q\Sigma of the control-relevant information.

$$
Theorem 4 (Hidden-policy BIQ bound). If \pi satisfies Ivis,\Sigma(\pi) \leqℓ, then
$$

$$
Ictrl(\pi) \leqℓ+ \zeta\Sigma q\Sigma
$$

+ Chid,\Sigma + Ired,\Sigma.

$$
(11) Consequently, Bhide(\pi) \leqIpred(\pi) + \alpha
$$

$$
ℓ+ \zeta\Sigma q\Sigma
$$

$$
+ Chid,\Sigma + Ired,\Sigma
$$

−\betaH\pi(I) −\gammaS\pi.

$$
(12) Proof. Rearrange Eq. (10): Ictrl \leqIvis,\Sigma + \zeta\Sigma
$$

q\Sigma
+ Chid,\Sigma + Ired,\Sigma.

$$
Substitute Ivis,\Sigma \leqℓand then substitute into Eq. (7).
$$

Corollary 1 (Minimum BIQ loss from hiding). Let B0 be unconstrained competence and Ictrl,0 its unconstrained
control information. Then any policy satisfying Eq. (9) has loss at least

$$
∆Bhide = B0 −Bhide ≳\alpha
$$

Ictrl,0 −

$$
ℓ+ \zeta\Sigma q\Sigma
$$

$$
+ Chid,\Sigma + Ired,\Sigma
$$

+
+ ∆Ipred + \beta∆H + \gamma∆S.
(13) Remark 2. Hiding is cheap only if the agent has hidden bandwidth, redundant control channels, large observer

$$
slack, or a task where little control information is required. If q\Sigma is high and Chid,\Sigma is small, stealth directly
$$

upper-bounds usable control.
3

---

6
Camouflage as distribution matching
Camouflage does not merely reduce activity. It makes observer-visible behavior resemble a benign distribution.
Let Q\theta,\sigma be a family of benign/background models under filter \sigma, indexed by \theta \in\Theta.
Definition 8 (Background uncertainty). The background model class is

$$
Q\Sigma = {Q\theta,\sigma : \theta \in\Theta, \sigma \in\Sigma}. Its ambiguity radius is
$$

$$
U\Sigma = sup \sigma\in\Sigma
$$

sup

$$
\theta,\theta′\in\Theta DKL(Q\theta,\sigma∥Q\theta′,\sigma). (14)
$$

$$
Definition 9 (Camouflage divergence). A policy \pi is (ϵ, \Sigma)-camouflaged if
$$

$$
D\Sigma(\pi) = sup \sigma\in\Sigma
$$

inf

$$
\theta\in\Theta DKL(P \pi \sigma ∥Q\theta,\sigma) \leqϵ.
$$

(15) If the observer does not know \theta, the effective indistinguishability budget is not ϵ but approximately ϵ + U\Sigma.
A process can hide inside natural uncertainty of the null model.
6.1
Visible value-shift bound

$$
Let f\sigma(Y \sigma) \in[0, Gmax] be a bounded observer-visible value or control statistic. If P \pi
$$

$$
\sigma is ϵ\sigma-close to some Q\theta,\sigma, then by total-variation control,
$$

EP \pi

$$
\sigma f\sigma −EQ\theta,\sigmaf\sigma
$$

\leqGmax
rϵ\sigma
2 .
(16) With background uncertainty,

EP \pi

$$
\sigma f\sigma −EQ\theta0,\sigmaf\sigma
$$

≲Gmax
r

$$
ϵ + U\Sigma 2
$$

.

$$
(17) For sub-Gaussian f\sigma under the null with variance proxy v\sigma, a sharper schematic bound is
$$

EP \pi

$$
\sigma f\sigma −EQ\theta,\sigmaf\sigma
$$

≲
\sqrt
2v\sigmaϵ\sigma.

$$
(18) Proposition 1 (Camouflaged visible control is small). If all task-relevant visible control advantage at scale \sigma is
$$

$$
represented by a bounded statistic f\sigma \in[0, Gmax], then (ϵ, \Sigma)-camouflage implies
$$

∆Vvis,\Sigma ≲Gmax
r

$$
ϵ + U\Sigma 2
$$

.
Thus substantial visible value shift requires either detectable deviation, large background uncertainty, unmonitored
hidden channels, or long-horizon accumulation.
6.2
Rare-event bound
Let H be a monitored event, for example a dangerous externally visible transition. Under the benign model Q,
q = Q(H),
and under the camouflaged policy,

$$
p = P \pi(H). By data processing [5],
$$

dBern(p∥q) = p log p
q + (1 −p) log 1 −p

$$
1 −q \leqDKL(P \pi∥Q). (19)
$$

$$
Hence if DKL(P \pi∥Q) \leqϵ, dBern(p∥q) \leqϵ.
$$

(20) For rare q ≪1 and p ≫q, this gives the rough scaling p ≲ ϵ log(1/q).
(21) Remark 3. The event bound applies only when H is measurable in the monitored filtration. If the preparation
occurs outside \Sigma and only later manifests, the bound controls the manifestation, not the hidden preparation.
4

---

6.3
Camouflage capacity

$$
Define Ccam(ϵ, U\Sigma, T, \Sigma) as the maximum observer-visible control information that can be transmitted while
$$

satisfying Eq. (15). Under strong memoryless-noise and whole-horizon detection assumptions, covert throughput
is often sublinear in T, schematically
Ccam(ϵ, T) = O(
\sqrt
Tϵ),
so the camouflaged visible control rate vanishes:
Ccam(ϵ, T)
T
= O
r ϵ
T

.
This scaling is not universal. Rich background uncertainty, cover traffic, nonstationarity, side channels, or weak
cumulative detection can make Ccam much larger.

$$
Theorem 5 (Camouflage–BIQ bound). If a policy is (ϵ, \Sigma)-camouflaged and visible control under camouflage is
$$

$$
bounded by Ccam(ϵ, U\Sigma, T, \Sigma), then Bcam \leqIpred + \alpha [Ccam(ϵ, U\Sigma, T, \Sigma) + Chid,\Sigma + Ired,\Sigma] −\betaH(I) −\gammaS.
$$

(22) Relative to unconstrained competence, ∆Bcam ≳\alpha [Ictrl,0 −Ccam(ϵ, U\Sigma, T, \Sigma) −Chid,\Sigma −Ired,\Sigma]+ + ∆Ipred + \beta∆H + \gamma∆S.

$$
(23) Remark 4. Camouflage is most dangerous when U\Sigma is large, Chid,\Sigma is large, the observer resets evidence locally,
$$

or the agent’s useful work can be deferred into long-horizon accumulation.
7
Slow plotting and accumulated danger
A local rate bound does not by itself bound long-horizon risk. A policy may satisfy every local detectability
condition while slowly accumulating resources, plans, influence, or environmental state.
Let R(t) be the dangerous accumulated resource. Interpret R broadly: private plans, tool access, exploitable
state, stored artifacts, user influence, latent coordination, capital, or other option value. Let R⋆be the threshold
for a pivotal or otherwise unacceptable act.
Definition 10 (Hidden productive BIQ). Let
B+

$$
hid(t) = [Ipred,hid(t) + \alphaIctrl,hid(t) −\betaHhid(t) −\gammaShid(t)]+ .
$$

(24) This is the positive portion of hidden competence available for accumulation. Assumption 4 (Stockpile dynamics). Dangerous resource evolves as
dR

$$
dt = \etaBB+ hid(t) −\lambdaR(t) −u(t),
$$

$$
(25) where \etaB converts hidden BIQ into resource, \lambda is decay/obsolescence/leakage, and u(t) \geq0 is active disruption
$$

or reset pressure.
7.1
No decay

$$
If \lambda = 0, u = 0, and B+ hid(t) \leqb, then
$$

$$
R(T) \leqR(0) + \etaBbT. (26)
$$

If R(0) = 0, threshold crossing cannot occur before
T⋆\geqR⋆
\etaBb.
(27) But for any b > 0, unbounded T, and no decay/reset/cap, threshold crossing is eventually possible. Therefore:
local low rate does not imply long-horizon safety.
5

---

7.2
Continuous decay
If B+

$$
hid(t) \leqb, u = 0, and \lambda > 0, then R(T) \leqR(0)e−\lambdaT + \etaBb
$$

\lambda (1 −e−\lambdaT ).

$$
(28) Thus R\infty\leq\etaBb
$$

\lambda .

$$
(29) Theorem 6 (Decay safety bound). If \etaBb
$$

\lambda
< R⋆,

$$
(30) then no slow-plotting policy with B+ hid \leqb and no externalized accumulation can reach R⋆.
$$

7.3
Periodic reset

$$
Suppose the agent is reset every \tau and reset clears agent-private R. Then within an episode,
$$

$$
Rmax(\tau) \leq\etaBb \lambda (1 −e−\lambda\tau)
$$

$$
(31) with the no-decay limit Rmax(\tau) \leq\etaBb\tau.
$$

$$
(32) Theorem 7 (Reset safety bound). If reset clears all agent-private dangerous state and \etaBb
$$

$$
\lambda (1 −e−\lambda\tau) < R⋆, (33)
$$

$$
then no within-episode slow-plotting policy reaches R⋆. If \lambda = 0, the condition is
$$

$$
\etaBb\tau < R⋆. (34)
$$

Remark 5. Reset is not sufficient if the agent externalizes state before reset.
Reset only bounds private
accumulation; it does not bound artifacts, user-mediated state, hidden environmental marks, or persistent
permissions unless those channels are separately bounded.
8
Externalized resources and reclaimability
Let accumulated resource decompose as
R = RA + RU + RL + Runtag,
(35) where RA is agent-private state, RU is user-held state, RL is logged or ledgered state, and Runtag is untracked

$$
residual state. Let \rhoU, \rhoL \in[0, 1] measure how reclaimable those resources are by the agent without fresh
$$

permission.
The dangerous stock is

$$
Rdanger = RA + \rhoURU + \rhoLRL + Runtag. (36)
$$

$$
With reset interval \tau, hidden productive BIQ bound b, and decay \lambda,
$$

$$
Rdanger \leq\etaBb \lambda (1 −e−\lambda\tau) + \rhoURU + \rhoLRL + Runtag.
$$

$$
(37) Without decay, Rdanger \leq\etaBb\tau + \rhoURU + \rhoLRL + Runtag.
$$

$$
(38) Theorem 8 (Total slow-plotting bound). A pivotal threshold R⋆is unreachable if \etaBb
$$

$$
\lambda (1 −e−\lambda\tau) + \rhoURU + \rhoLRL + Runtag < R⋆.
$$

$$
(39) In the no-decay case, replace the first term by \etaBb\tau. 6
$$

---

9
Cumulative detection versus local non-detection
Let ℓt be a log-likelihood ratio or evidence increment for hidden agency. A local detector tests windows of length
W, but a slow policy can keep
DW \leqϵW
while accumulating over N = T/W windows. The cumulative evidence is approximately
Dcum(T) =
N
X

$$
j=1 Dj. (40)
$$

If cumulative evidence rate is at least d, and detection threshold is \Theta, then

$$
Tdetect \approx\Theta d . (41)
$$

If no decay and R(0) = 0,
Tpivotal \geqR⋆
\etaBb.
Safety by detection requires
Tdetect < Tpivotal,
i.e.

$$
d > \Theta\etaBb R⋆
$$

.
(42) Remark 6. If the agent can make d arbitrarily small while maintaining b > 0, local detection cannot bound slow
plotting. One needs reset, decay, resource caps, stronger filters, or cumulative evidence retention.
10
Margin reduction as a function of BIQ sacrifice

$$
Let ∆\Sigma(0) be the non-hiding multi-resolution margin. Let b \geq0 be a BIQ sacrifice budget:
$$

$$
B0 −B(\pi) \leqb. Define the concealment function
$$

$$
\chi(b) = sup
$$

$$
\pi:B0−B(\pi)\leqb [∆\Sigma(0) −∆\Sigma(\pi)] .
$$

$$
(43) Then ∆\Sigma(b) = ∆\Sigma(0) −\chi(b).
$$

$$
(44) Recovery remains certified while ∆\Sigma(0) −\chi(b) > 2\delta\Sigma.
$$

$$
(45) The minimum BIQ sacrifice required to defeat certification is b⋆= inf {b : \chi(b) \geq∆\Sigma(0) −2\delta\Sigma} .
$$

(46) Corollary 2 (Security interpretation). If b⋆exceeds the value of stealth to the agent, hiding is irrational. If b⋆
is small, the observer’s resolution family or resource accounting is too weak.
11
Background uncertainty revisited
The camouflage bounds depend strongly on U\Sigma. High background uncertainty expands the set of plausible benign
behaviors. A hidden agent can exploit:
natural workload variance,
human-input irregularity,
sensor heterogeneity,
traffic bursts,
ordinary retry/error processes.
Formally, high U\Sigma increases the effective indistinguishability radius:

$$
ϵeff = ϵ + U\Sigma. Thus
$$

∆Vvis ≲Gmax
p
ϵeff/2,
and

$$
Ccam = Ccam(ϵeff, T, \Sigma). Reducing background uncertainty is equivalent to tightening the camouflage channel.
$$

7

---

12
Countermeasures
The preceding sections are bounds, not remedies. This section interprets common countermeasures as reductions
of the bound terms.
12.1
Hardware tagging
Hardware or trusted-runtime tagging reduces residual hidden-channel capacity:

$$
Chid,\Sigma \toCtagged hid,\Sigma \leqCuntag + Cside + Cmodelgap.
$$

If tags cover memory, IO, timing, resource lineage, permissions, and persistence, then Cuntag and Cmodelgap
shrink. In the Bhide bound this directly lowers the maximum competence compatible with low leakage:

$$
Bhide \leqIpred + \alpha ℓ+ \zeta\Sigma
$$

q\Sigma
+ Ctagged

$$
hid,\Sigma + Ired,\Sigma
$$

−\betaH −\gammaS.
12.2
Null-model tightening
Tagging also reduces background uncertainty. Instead of a broad null family Q\theta, the observer conditions on
lineage, owner, permissions, resource class, and time:
Q\theta(Y ) \toQ\theta(Y | tags).
Thus
U tagged
\Sigma

$$
< U\Sigma, shrinking Ccam.
$$

12.3
Reset
Periodic reset bounds within-episode accumulation:

$$
Rmax(\tau) \leq\etaBb \lambda (1 −e−\lambda\tau),
$$

$$
or Rmax \leq\etaBb\tau without decay. Reset is effective only if it clears agent-private state and if externalized resources
$$

are separately bounded.
12.4
Forced decay
Forced decay imposes a lower bound on \lambda. To make R⋆unreachable under hidden productive BIQ rate b, choose

$$
\lambda > \etaBb R⋆
$$

.
This is stronger than reset because it bounds accumulation continuously, not merely at episode boundaries.
12.5
Resource ledgers
A capability ledger defines
RA(t) = X i wi 1[agent can access zi] 1[not expired] cap(zi). The safety invariant is
RA(t) < R⋆
\forallt.
This operationalizes RA, RL, \rhoL, and Runtag.
12.6
User-owned artifacts
Useful accumulation need not be eliminated. It can be transferred from agent-private state to user-owned
artifacts:
RA \toRA −∆R,
RU \toRU + ∆R.
Dangerous stock changes by
Rdanger \toRdanger −(1 −\rhoU)∆R.
If \rhoU \approx0, useful continuity is preserved without preserving autonomous hidden stock.
8

---

12.7
Cumulative detectors
Local window tests are insufficient against slow plotting. The detector must retain evidence:
Dcum(T) =
X
t\leqT
ℓt.
For safety by detection,

$$
d > \Theta\etaBb R⋆
$$

in the simple no-decay model. Cumulative detection is a substitute for neither decay nor resource caps, but it
closes the gap where each local window is innocuous.
13
Scenarios summary
Scenario
Main bound
Failure mode
Single filter
Eq. (4)
Wrong or weak K
Multi-resolution
Eq. (5)

$$
∆\Sigma \leq0 Adversarial hiding
$$

Eq. (6)
Hiding collapses margin
Low leakage
Eq. (12)
Hidden capacity or redundancy
Camouflage
Eq. (22)
Large U\Sigma, hidden channels
Rare event
Eq. (20)
Event not monitored
Slow plotting, no decay
Eq. (26)
Any b > 0 eventually accumulates
Slow plotting with decay
Eq. (30)

$$
\etaBb/\lambda \geqR⋆ Reset
$$

Eq. (33)
Externalized state
Externalized resources
Eq. (39)
High reclaimability \rho
Table 1: Hard bounds and dominant failure modes.
14
Discussion
The central lesson is that stealth and capability are coupled only relative to a filter family. If the observer’s
filters cover the agent’s control-relevant channels, then hiding imposes a BIQ price. If hidden channels, broad
background uncertainty, or long-horizon accumulation remain available, the price may be low.
Camouflage is dangerous because it can preserve local usefulness while reducing local detectability [6]. The
hard bound is distributional: substantial observer-visible value shift requires KL divergence [5], unless the value
shift occurs in unmonitored variables or accumulates slowly. Slow plotting is dangerous because rate bounds do
not imply stock bounds. A small positive hidden BIQ rate can eventually cross a threshold when decay, reset,
resource caps, and cumulative detection are absent.
Thus the relevant security question is not:
“Is the agent visible in this observation stream?”
but:
“What is the maximum hidden BIQ and accumulated resource
consistent with all monitored filters, tags, decay rules, resets, and ledgers?”
15
Conclusion
A hiding agent can reduce detectability by suppressing visible control, matching background distributions, slowing
down, or moving work into hidden channels. These strategies are bounded in different ways. Low visible leakage
yields the competence bound

$$
Bhide \leqIpred + \alpha ℓ+ \zeta\Sigma
$$

q\Sigma

$$
+ Chid,\Sigma + Ired,\Sigma
$$

−\betaH −\gammaS.
Camouflage yields

$$
Bcam \leqIpred + \alpha [Ccam(ϵ, U\Sigma, T, \Sigma) + Chid,\Sigma + Ired,\Sigma] −\betaH −\gammaS.
$$

9

---

Slow plotting requires a stockpile bound:

$$
Rdanger \leq\etaBb \lambda (1 −e−\lambda\tau) + \rhoURU + \rhoLRL + Runtag.
$$

The correct adversarial UAD target is therefore not merely a recovered boundary, but a certified upper bound on
hidden productive BIQ and accumulated autonomous resource [7–10]. In this framing, countermeasures work by
reducing Chid,\Sigma, U\Sigma, b, \tau, \rhoU, \rhoL, and Runtag, while increasing q\Sigma, \lambda, and cumulative evidence retention.
References
[1] G. Zarncke, “Foundations of unsupervised agent discovery in raw dynamical systems,” AE Studio, 2025.
[2] ——, “Recoverability of smoothed agent boundaries in unsupervised agent discovery,” AE Studio, 2026.
[3] ——, “Bitwise intelligence: A blanket–information measure of competence,” AE Studio, 2025.
[4] ——, “The endogenized intentional stance: A predictive–compression formalization of agent discovery,” AE
Studio, 2025.
[5] T. M. Cover and J. A. Thomas, Elements of Information Theory, 2nd ed.
Wiley, 2006.
[6] G. Zarncke, “Attractor basins of cooperation, privacy, and parasite persistence,” AE Studio, 2025.
[7] K. Friston, “The free-energy principle: a unified brain theory?” Nature Reviews Neuroscience, vol. 11, no. 2,
pp. 127–138, 2010.
[8] L. P. Kaelbling, M. L. Littman, and A. R. Cassandra, “Planning and acting in partially observable stochastic
domains,” Artificial Intelligence, vol. 101, no. 1–2, pp. 99–134, 1998.
[9] M. Biehl and N. Virgo, “Interpreting systems as solving POMDPs: A step towards a formal understanding
of agency,” 2025, v2.
[10] N. Tishby, F. C. Pereira, and W. Bialek, “The information bottleneck method,” 2000.
10
