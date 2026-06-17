# Extract: attractor-basins.pdf

**Source PDF:** `context/attractor-basins.pdf`
**Extract:** `context/extracts/attractor-basins.md`
**Pages:** 2
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

Attractor Basins of Cooperation, Privacy, and
Parasite Persistence:
Applications of Foundations of Unsupervised Agent
Discovery in Raw Dynamical Systems
Gunnar Zarncke
AE Studio
Date: July 23, 2025
Abstract—Extending Unsupervised Agent Discovery (UAD), we

$$
derive analytic conditions under which transparency (\gamma > 0)
$$

percolates into global cooperation, under which strategic opacity
(\gamma
<
0) preserves privacy, and under which high-entropy
“parasites” evade host detection. Key results: (i) a configuration-

$$
model percolation threshold \phic = \langled\rangle/(\langled2\rangle−\langled\rangle) bounds the
$$

size of the cooperative attractor; (ii) host capacity Ccrit
X
=

$$
H(AY )−\lambdaY H(IY )/\beta sets parasite-persistence; (iii) hierarchical
$$

$$
links with \kappaiH < 1 generate privacy islands despite dense peer
$$

cooperation in closed-form expressions.

## I. RECAP: BLANKET DISCOVERY AND TRANSPARENCY

WEIGHT
Given raw variables Xi(t), Unsupervised Agent Discovery
clusters a subset C when
I(IC
t+1; EC
t+1 | SC
t , AC

$$
t ) \approx0, yielding sensory S, active A, internal I, external E. Each agent
$$

i endows every neighbour j with a signed transparency weight

$$
\gammaij = \partial
$$

$$
\partialI(M j; Aj)
$$

$$
−Eq[−log P(Si | Ii)] −\lambdaH(Ii)
$$

I=I∗
ij
,
positive for cooperation, negative for opacity.

## II. PAIRWISE COOPERATIVITY INDEX

For ordered pair (i, j) define

$$
\kappaij = bij pij \rhoij cij
$$

,
with b=benefit per bit shared, p=repeat-interaction probability,

$$
\rho=payoff correlation, c=marginal cost. Edge j \toi is ”open”
$$

$$
if \kappaij > 1. p(si
$$

t | xi
t, aj

$$
t; \gammaij) ∝exp[−\gammaij d(si t, aj
$$

t)].
0We build directly on the blanket– and information-theoretic framework of
L. et al. (2025), hereafter “UAD.”

## III. PERCOLATION THEOREM: GLOBAL ATTRACTOR OF

COOPERATION
Let G be a configuration model with degree distribution

$$
P(d) and bond-probability \phi = Pr(\kappaij > 1). Theorem. A
$$

$$
giant cooperative component of size \Theta(N) exists iff
$$

$$
\phi > \phic = \langled\rangle
$$

\langled2\rangle−\langled\rangle.

$$
If \phi \leq\phic all cooperative clusters satisfy |C| \leqO(log N).
$$

Consequently the “attractor basin of cooperation” contains a
fraction

$$
S(\phi) = 1 −G0 u(\phi)
$$

,
u = G1

$$
1 −\phi + \phi u
$$

,
with G0, G1 the standard generating functions of P(d).

## IV. PARASITE-PERSISTENCE CRITERION

A hostile agent Y with action entropy H(AY ) persists
inside host X when

$$
CX < H(AY ) −\lambdaY H(IY ) \beta
$$

,
where CX bounds host modelling entropy and \beta rewards
resource extraction. Noise \eta lowers effective capacity to
CX −\eta; adversarial camouflage raises the RHS, enlarging the
persistence region.

## V. PRIVACY ISLANDS IN HIERARCHIES

For individual i versus hierarchy H we typically have

$$
\kappaiH < 1. Optimal policy sets \gammaiH < 0, driving I(M H; Si)\to
$$

### 0. If a fraction ψ of vertical edges satisfy κiH < 1, the network

decomposes into:

$$
1) a giant peer-cooperative component (if \phi > \phic),
$$

2) disjoint “privacy islands” disconnected from H by
closed bonds.
Regulatory or cryptographic measures reduce piH or raise ciH,
expanding \psi and thus the privacy basin.

---

## VI. MIXED AND CONTEXTUAL TRANSPARENCY

$$
Each agent holds a context-dependent \gammaij(t). Define state
$$

Cij(t) tracking reciprocity; update rule

$$
\gammaij(t + 1) = (
$$

$$
+\gamma0, \kappaij(t) >1,
$$

$$
−\gamma0, \kappaij(t) <1.
$$

Dynamic bond-percolation analysis shows that if the time-

$$
average ¯\phiij = Prt(\kappaij(t) > 1) exceeds \phic the cooperative
$$

giant persists in expectation; otherwise cooperation fragments
intermittently.

## VII. DISCUSSION

The blanket-based disclosure cost rewrites classic Hamil-
ton/Trivers intuitions in measurable bits: transparency wins

$$
when \phi > \phic; privacy becomes rational when vertical \kappa < 1;
$$

parasites survive whenever host capacity falls below an en-
tropy threshold. These results hold for directed, weighted,
or hierarchically nested networks and clarify why higher-
complexity organisms (larger CX) enjoy lower parasite loads
yet still value privacy against asymmetric principals.

## VIII. CONCLUSION

By marrying UAD with percolation and capacity bounds,
we give closed-form conditions for the size of cooperative,
private, and parasitic attractors in any large dynamical sys-
tem—biological, social, or artificial.

## IX. COMPARATIVE LITERATURE ON COOPERATION AND

PARASITE DYNAMICS
Prior studies on cooperation percolation have addressed
binary cooperation-defection edges [1]. Our work significantly
extends these by introducing continuous transparency weights
derived from mutual information, thus offering a finer-grained
analytical perspective. Related empirical findings on parasite-
host co-evolution [2] strengthen our theoretical results, pro-
viding biological evidence for entropy-based thresholds of
parasite persistence. Additionally, the collective intelligence
factor [3] supports our percolation thresholds empirically in
human groups, confirming transitions in group effectiveness
as communication bandwidth varies.
REFERENCES
[1] Y. Yang et al., “Cooperation percolation in spatial evolutionary games,”
EPL (Europhysics Letters), vol. 124, no. 4, p. 48001, 2018.
[2] C. Bonneaud and B. Longdon, “Coevolutionary theory of hosts and
parasites,” Proceedings of the Royal Society B, vol. 289, no. 1987, p.
20211987, 2022.
[3] A. W. Woolley, C. F. Chabris, A. Pentland, N. Hashmi, and T. W. Malone,
“Evidence for a collective intelligence factor in the performance of human
groups,” Science, vol. 330, no. 6004, pp. 686–688, 2010.
