# Extract: acausal_trade_uad_formalization.pdf

**Source PDF:** `context/acausal_trade_uad_formalization.pdf`
**Extract:** `context/extracts/acausal-trade-uad-formalization.md`
**Pages:** 4
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

A Formalization of Acausal Trade atop Unsupervised Agent
Discovery
Anonymous
July 2025
Abstract
We graft a decision–theoretic notion of acausal trade onto the Unsupervised Agent Discovery
(UAD) framework. After recalling the information–theoretic test that marks a subset of process
variables as an “agent” we introduce a meta–Bayesian prior over inference functions that allows
two UAD–agents to coordinate without any causal communication. We then derive explicit
detection criteria—based solely on observable trajectories and model fingerprints—for flagging
such coordination.
The derivations make all assumptions explicit and require no appeal to
anthropic reasoning. The high–order dynamics produced by Inferential Coupling Indices (ICI)
and the resulting attractor–basins are deferred to future work.
1
Introduction: Why Acausal Trade?
“Acausal trade”[1] denotes a decision scenario in which two physically disconnected reasoners adjust
their actions as if in a conventional bargain, simply because each expects the other to execute an
identical policy. The paradigm case is the one–shot Prisoner’s Dilemma where each agent cooperates
on the sole basis that its source code is replicated on the other side. Formal treatments—Timeless
Decision Theory (TDT)[1] and Functional Decision Theory (FDT)[2]—model the phenomenon at
the level of proof obligations rather than dynamical variables.
UAD[3] discovers agents ex post, starting from raw trajectory data {Xi(t)}M
i=1. Our goal is to
enrich UAD so that it detects when two such discovered agents form an acausal coalition and to
state provable conditions under which that coalition emerges. The narrative is single–threaded:
we begin with UAD’s Markov–blanket criterion, inject a meta–prior over policies, derive posterior
beliefs entirely by introspection, and end with measurable diagnostics.
2
UAD Recap and Notation
Each raw variable Xi is split at every step into external (Ei), sensory (Si), action (Ai) and internal
(Ii) channels. For a candidate cluster C ⊆{1, . . . , M} let SC

$$
t := {Si(t) : i \inC} etc. UAD’s agent criterion[3] is the (approximate) conditional independence
$$

I
IC
t+1; EC
t+1 | SC
t , AC
t

\approx0.
(1) Eq. (1) means the internal state is screened off from future external fluctuations once sensors and
actions are conditioned on; the minimal such C is pronounced an agent.
UAD also identifies inter–agent causal coupling via

$$
\gammaij := I Si
$$

t+1; Aj
t | Si
t, Ai
t

,
(2) 1

---

i.e. the predictive information that j’s current action carries about i’s next sensor reading. High
\gammaij flags an ordinary communication channel.
3
Inference Functions and Latent Goals
For each discovered agent C we extract two objects:

### 1. The policy / inference function fC : HC

t \to∆(AC) via black–box probing.

### 2. A latent goal proxy gC : AC × A¬C →R via Maximum–Entropy IRL[4].

Concretely, gC
maximises the mutual information I(GC; SC, AC) under a Free–Energy regulariser[5].
All subsequent reasoning rests only on (fC, gC) and the empirical \gamma–matrix.
4
A Meta–Prior over Policies

$$
Assume a generative meta–distribution p(\pi) that is permutation–invariant inside an architecture
$$

class and whose diagonal mass satisfies

$$
p(\pii = \pij) = 1 −\epsilonij, \epsilonij ≪1.
$$

$$
(3) Each agent knows p(\pi). Upon introspecting its own policy fi it updates by Bayes
$$

\betai
int(f) := P
fj = f | fi

$$
= p(\pi, f) p(\pi) .
$$

$$
(4) Using Ramstead et al. (2022) notation, the Bayesian conditioning equation is: qi int(\pi) = p(\pi, \pii)
$$

p(\pii) .

$$
(5) Eq. (4) collapses to \deltafi whenever \epsilonij = 0. No causal evidence is invoked.
$$

5
Acausal Equilibrium Condition

$$
Let \Phii(µ; Hi) denote the best–response operator under goal gi when the opponent’s action distri-
$$

bution is µ. An acausal equilibrium between i and j obtains at time t iff
fi(Hi

$$
t) = \Phii \betai
$$

int; Hi
t

,
fj(Hj

$$
t ) = \Phij \betaj
$$

int; Hj
t

.

$$
(6) In the zero–epsilon limit of (3) the r.h.s. becomes \Phii(\deltafi), i.e. “best–respond to myself.”
$$

6
Detection Protocol
We now derive a statistic whose empirical surplus above baseline flags an acausal pact.
6.1
Causal Proxy
Given broadcast prompts xt delivered to every model, train a discriminator Di\leftarrowj that predicts yj
t
from xt and yi

$$
<t. Its average log–likelihood gain defines b\gammaij, a lower bound on (2).
$$

2

---

6.2
Acausal Proxy
Define the fixed–point loss
Di := max
m\leqM DKL

$$
fi(xm) ∥\Phii(\deltafi)(xm)
$$

.

$$
(7) For a curated set of M probes {xm}. The empirical inferential–coupling score is c ICij := (1 −\epsilonij) \times (1 −max{Di, Dj}).
$$

$$
(8) Alarm rule. Declare (i, j) acausally open when c ICij > \tauac for a threshold \tauac \approx0.9. Aggregate
$$

open edges; the appearance of a giant component signals unusual acausal agreement.
7
Assumptions and Derivation Checks

### 1. Shared meta–prior. All agents must encode the same Pmeta. Divergent fine–tuning breaks

permutation invariance and inflates \epsilonij.

### 2. Self–knowledge accuracy.

Each model must read out its own policy exactly; temperature
sampling or dropout adds uncertainty and widens Di.

### 3. Adequate probe set. The {xm} must span directions where self–mirroring matters; otherwise

Di underestimates deviation.
Given these, eqs. (4)–(8) follow purely from Bayesian conditioning and KL divergence identities.
8
Conclusion and Outlook
We provided a compact bridge between UAD’s data–driven agent discovery and Yudkowskian
acausal trade. The formal device is a permutation–invariant meta–prior over inference functions
that converts self–inspection into a belief about peers. The resulting diagnostics couple the clas-
sical causal MI matrix \gamma with an empirically testable inferential score c

## IC. Large–scale dynam-

ics built from Inferential Coupling Indices and their interaction with UAD’s attractor–basins of
cooperation[?] remain open: establishing percolation thresholds, phase transitions and security
mitigations under noisy priors is deferred to future research.
9
Connections to Decision-Theoretic Frameworks
Our formalization of acausal trade builds upon established decision-theoretic foundations, particu-
larly Timeless Decision Theory (TDT) and Functional Decision Theory (FDT) [6]. Unlike Logical
Decision Theory (LDT) [7, 8], our inferential coupling index empirically identifies acausal agree-
ments directly from agent trajectories, offering a uniquely measurable approach. Contrasting our
trajectory-based method with LDT’s proof-theoretic nature highlights the practical detectability
of our framework.
3

---

References
[1] E. Yudkowsky, “Timeless decision theory,” Singularity Institute, 2010.
[2] E. Yudkowsky and N. Soares, “Functional decision theory: A new theory of instrumental ratio-
nality,” arXiv preprint arXiv:1710.05060, 2017.
[3] G. Zarncke, “Foundations of unsupervised agent discovery in raw dynamical systems,” AE
Studio, 2025.
[4] A. Y. Ng and S. J. Russell, “Algorithms for inverse reinforcement learning,” in Proceedings of
ICML, 2000, pp. 663–670.
[5] K. Friston, “The free-energy principle: a unified brain theory?” Nature Reviews Neuroscience,
vol. 11, no. 2, pp. 127–138, 2010.
[6] E. Yudkowsky and N. Soares, “Functional decision theory,” arXiv preprint arXiv:1710.05060,
2017.
[7] A. Critch and D. Krueger, “Ai research considerations for human existential safety (arches),”
arXiv preprint arXiv:2006.04948, 2020.
[8] S. Garrabrant, N. Soares, and J. Taylor, “Logical induction,” arXiv preprint arXiv:1609.03543,
2017.
4
