# Extract: bitwise_iq.pdf

**Source PDF:** `context/bitwise_iq.pdf`
**Extract:** `context/extracts/bitwise-iq.md`
**Pages:** 6
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

Bitwise Intelligence:
A Blanket–Information Measure of Competence
Gunnar Zarncke
AE Studio
Abstract—We introduce B-IQ, a task-agnostic competence
metric grounded in the information flows across an agent’s
Markov blanket. B-IQ combines predictive and control mutual
information and discounts memory cost and residual surprise.
We derive physical bounds, show how B-IQ aggregates hierar-
chically, and provide empirical anchors spanning ants, human
societies, and large-language-model (LLM) services. Efficiency

$$
(\eta)—the rate at which additional B-IQ converts into relative
$$

growth—varies by 15 orders of magnitude across anchors. A
tentative U-shaped scaling with system size appears, though the
pattern may reflect sampling bias or hidden confounds.

## I. BLANKET PRELIMINARIES (UAD)

For any agent X discovered via Unsupervised Agent Dis-
covery (UAD) [?], variables factor as Markov blankets: IX
t \to
AX
t
\toSX
t+1, SX
t
\toIX
t+1, with externals EX
t . The UAD
framework identifies coherent agents by locating boundaries
where I(IX
t+1; EX
t+1 | SX
t , AX

$$
t ) \approx0, ensuring conditional independence across the Markov blanket. We define the core information-theoretic quantities:
$$

Ipred = I(It; St+1),
Ictrl = I(At; Et+1),
S = E[−log P(St+1 | It)],
H(It)
= entropy of It.

$$
(1) II. DEFINITION OF B-IQ Per time step (nat s−1): B-IQ = Ipred + Ictrl −\betaH(x) −\gammaS.
$$

$$
(2) A. Coefficient Choices \alpha, \beta, \gamma
$$

The competence functional (Sec. II)

$$
B−IQ = Ipred + \alpha Ictrl −\beta H(It) −\gamma S contains three dimensionless weights; we adopt the following
$$

canonical values.

$$
1) Control weight \alpha = 1. Adding one nat to the causal
$$

channel Ictrl reduces expected variational free-energy by
exactly one nat when the actuator is noise-free. Setting

$$
\alpha = 1 therefore places prediction and control on the
$$

same natural information scale.

$$
2) Surprise penalty \gamma =
$$

### 1. Residual surprise S

=
−log P(St+1 | It) already measures free-energy (in

$$
nats). A unit penalty \gamma = 1 is thus the least-assumption
$$

choice.

$$
3) Memory cost \beta ≪1. Sustaining one stored bit for
$$

$$
one second costs at minimum kT ln 2 \approx3 \times 10−21 J
$$

(Landauer, 300 K). A single cortical spike dissipates

$$
∼2 \times 10−13 J, eight orders higher. We therefore assign
$$

$$
a small constant \beta \approx10−3 (brains) or 10−4 (modern
$$

DRAM), reflecting the marginal energetic burden of
memory relative to functional gain.
These choices are physically motivated yet remain tunable;
Sec. VIII-E quantifies downstream sensitivity.

$$
For this study we use \alpha = \gamma = 1, \beta ≪1 (memory cost
$$

minor for biological brains).

## III. PHYSICAL ENVELOPE

With input channel capacity Csens and actuator capacity
Cact:

$$
0 \leqIpred \leqmin
$$

Csens, H(St+1)

,

$$
0 \leqIctrl \leqCact, 0 \leqH(It) \leqCrt
$$

mem \leq
P
kT ln 2,

$$
H(St+1) −Csens \leqS \leqH(St+1). (3)
$$

Substituting gives1
−\betaCrt

$$
mem −\gammaH(St+1) \leqB−IQ \leqCsens + \alphaCact. (4)
$$

## IV. EFFICIENCY η

Following ABC, for two agents A, H competing for share
w:
˙wA
wA
−˙wH
wH

$$
= \eta B−IQA −B−IQH
$$

,

$$
(5) so wA/wH =(wA/wH)0 exp[\eta ∆B t]. Empirical \eta is extracted
$$

as g/∆B where g is observed growth differential.

## V. MULTI-AGENT COOPERATIVITY INDEX

Building on UAD and attractor basin theory [?], [?], we
characterize when agents benefit from transparency versus
opacity in their information disclosure. For agents i and j,
cooperation emerges when the cooperativity index exceeds
unity:

$$
\kappaij = bij · pij · ϱij cij
$$

> 1,
(6) where: • bij: marginal benefit to agent i per bit of information disclosed by agent j • pij: probability that j’s cooperative action reaches i’s
sensory channel
1Derivation mirrors ABC Eq. (6); see also [?] for predictive information
bounds.

---

• ϱij: strategic correlation between agents (normalized mu-
tual information I(M j; Aj)/H(Aj))
• cij: marginal cost to agent j per bit of cooperative
disclosure
This generalizes Hamilton’s rule to information-theoretic
settings where relatedness is measured by predictive corre-
lation rather than genetic similarity.
A. Transparency Weight
Each agent i assigns a transparency weight \gammaij to neighbor
j:

$$
\gammaij = \partial
$$

$$
\partialI(M j; Aj)
$$

$$
−Eq[−log P(Si | Ii)] −\lambdaH(Ii)
$$

, (7)

$$
positive for cooperation (\kappaij > 1), negative for strategic
$$

$$
opacity (\kappaij < 1). B. Percolation of Cooperation
$$

In networks with degree distribution P(d) and bond prob-

$$
ability \phi = Pr(\kappaij > 1), a giant cooperative component
$$

emerges when:

$$
\phi > \phic = \langled\rangle
$$

\langled2\rangle−\langled\rangle.
(8) This percolation threshold determines whether cooperation spreads globally or remains fragmented in small clusters.

## VI. EMPIRICAL ANCHORS

Table I summarises initial anchors with ∆B estimated from
published IO rates and g from longitudinal studies.
TABLE I
REPRESENTATIVE B-IQ ANCHORS (NAT S−1)
System
∆B
g (s−1)
\eta
Ant species

$$
1 \times 104 7\times10−8
$$

$$
7\times10−12 Fire-ant colony
$$

$$
7\times107 5.7\times10−7
$$

$$
8\times10−15 GitHub Copilot
$$

$$
5\times102 2.3\times10−4
$$

$$
4.6\times10−7 Kiva warehouse
$$

$$
1\times109 2.2\times10−8
$$

$$
2\times10−17 Large US firms
$$

$$
2\times1012 9.5\times10−10
$$

$$
5\times10−22 A. Hierarchical Scaling Anchors
$$

Beyond single-agent measurements, we examine hierarchi-
cal systems across two domains: AI architectures and hu-
man organizations. Table II presents efficiency measurements
across system scales.
*Hierarchical Trend*: Both AI and human systems exhibit
U-shaped efficiency curves, with peak efficiency at small
scales (N < 102), minimum efficiency at intermediate scales
(103–104), and partial recovery at large scales (N > 105) due
to institutional coordination.
TABLE II
HIERARCHICAL B-IQ SCALING ANCHORS
System
Scale (N)
∆B
\eta
AI Hierarchies
Microservice guild
101–102
∼103
10−9
Kubernetes cluster
103–104
∼106
10−14
Multi-tenant platform
105–106
∼109
10−16
Global AI society
107–108
∼1012
10−15
Human Hierarchies
Individual
1

$$
3 \times 105 –
$$

Bands/tribes
101–102
∼106
10−11
Chiefdoms
103–104
∼108
10−17
Nation-states
105–108
∼1011
10−14
B. System-Specific Derivations

$$
1) Ant Species: B-IQ Estimate: ∆B \approx104 nat/s. Seidl
$$

& Wehner (2008) demonstrate ants integrate visual, proprio-
ceptive, and efference copy signals for navigation. Dauzere-
Peres & Wystrach (2024) show ants process multiple sensory
modalities simultaneously for robust path planning. While
these papers don’t specify bit rates, we estimate individual
ant sensory bandwidth ∼103 bit/s based on processing visual
landmarks, chemical gradients, and tactile cues at ∼10 Hz
with ∼10 bits/channel across ∼10 channels. Motor output
∼102 bit/s for movement direction, speed, and pheromone
release patterns. Colony coordination [?] adds ∼101 nat/s
per individual through collective information processing. For
∼103 individuals: total B-IQ \approx104 nat/s.

$$
Efficiency: Growth rate g \approx7\times10−8 s−1 from reproductive
$$

$$
success data over seasonal cycles [?]. Efficiency \eta = g/∆B \approx
$$

7 \times 10−12.
2) Fire-Ant Colonies: B-IQ Estimate: ∆B \approx7\times107 nat/s.
Tschinkel [?]. documents fire ant territories ranging from small
colonies to extensive foraging networks with complex under-
ground tunnel systems extending ¿15m from nests. The study
shows territory area positively correlates with colony size
and forager population, but doesn’t provide specific colony
sizes. We estimate large colonies at N ∼105 based on the
described territorial scope and foraging complexity. Individual
ant B-IQ ∼102 nat/s, but coordination overhead reduces
effective per-capita contribution. Non-linear scaling due to
communication bottlenecks and foraging territory constraints:
total B-IQ ∝N 0.7 \approx7 \times 107 nat/s.
Efficiency: Tschinkel [?]. describes seasonal variations in
colony growth with spring decline due to sexual production
and fall recovery through worker production, but provides no

$$
quantitative growth rates. We estimate g \approx5.7 \times 10−7 s−1
$$

assuming annual territorial expansion cycles of ∼20% based

$$
on the described seasonal dynamics: g \approxln(1.2)/(365\times24\times
$$

$$
3600) \approx5.7 \times 10−7 s−1. Efficiency \eta = g/∆B \approx8 \times 10−15.
$$

3) GitHub Copilot: B-IQ Estimate: ∆B \approx5 \times 102 nat/s.
Miller & Buschman [?]. establish working memory capacity

$$
of 4\pm1 items with processing limitations due to oscillatory
$$

brain rhythms. Individual programming session: developer
sensory input (screen) ∼106 bit/s, but focused attention
is limited by working memory to ∼4 simultaneous items.

---

Assuming each programming concept requires ∼25 bits of
information and updates occur at ∼1 Hz: effective bandwidth

$$
\approx4 \times 25 \times 1 \approx102 bit/s [?]. Copilot suggestions add ∼102
$$

nat/s predictive information about code completion patterns,
effectively augmenting human cognitive bandwidth.
Efficiency: Peng et al. [?] report 55.8% faster task comple-
tion in controlled trials. Converting to instantaneous growth
rate: if development time decreases by factor f = 0.558, this

$$
implies a time advantage ratio of 1/(1−f) = 1/0.442 \approx2.26.
$$

$$
For tasks completed in characteristic time \tau ∼1 hour, the
$$

$$
growth rate is g = ln(2.26)/\tau \approx0.82/3600 \approx2.3 \times 10−4
$$

s−1. Additional studies [?], [?], [?] report 30-50% time savings
across various coding tasks. Using the conservative 55.8% fig-

$$
ure: g \approx2.3\times10−4 s−1. Efficiency \eta = g/∆B \approx4.6\times10−7.
$$

4) Kiva Warehouse: B-IQ Estimate: ∆B \approx109 nat/s.
Fleet of ∼103 robots, each with sensor bandwidth ∼106
bit/s (LiDAR, cameras), actuator capacity ∼104 bit/s (motion
control) [?]. Central coordination system processes ∼109 nat/s
for optimization and routing. Robots achieve 2-3x productivity
gains over manual picking through goods-to-person paradigm.

$$
Efficiency: Operational efficiency gain g \approx2.2 \times 10−8 s−1
$$

from throughput improvements vs traditional warehouses [?].
Pick rates of 600+ lines/hour vs 100-180 lines/hour manual

$$
operations. Efficiency \eta = g/∆B \approx2 \times 10−17.
$$

$$
5) Large US Firms: B-IQ Estimate: ∆B \approx2 \times 1012
$$

nat/s. Enterprise with ∼105 employees, each contributing
∼107 nat/s effective information processing (accounting for
coordination overhead). Information systems, databases, and
communication infrastructure scale total capacity to ∼1012
nat/s. Large firms show systematic productivity advantages
over smaller firms across industries [?], [?].
Efficiency: Canadian data [?], [?] show large firms (¿500
employees) achieve 2-3x higher labor productivity than small
firms (¡100 employees). Assuming similar US patterns and
annual productivity advantage of ∼3%, we estimate growth

$$
differential g \approxln(1.03)/(365 \times 24 \times 3600) \approx9.5 \times 10−10
$$

s−1 between large and small firms. This reflects economies
of scale in human capital, technology adoption, and market

$$
access. Efficiency \eta = g/∆B \approx5 \times 10−22. 6) Microservice Guilds: B-IQ Estimate: ∆B \approx103 nat/s.
$$

Small cluster (N = 10–102) of stateless services. Each service
processes ∼102 requests/s with ∼10 bit/request metadata.
Limited coordination overhead due to loose coupling: total B-
IQ \approxN \times 101 \approx103 nat/s.

$$
Efficiency: Development velocity metric \eta \approx10−9 from
$$

deployment frequency improvements.
7) Kubernetes Clusters: B-IQ Estimate: ∆B \approx106 nat/s.
Medium-scale orchestration (N = 103–104 pods). Container
scheduling, service discovery, and resource management re-
quire significant coordination overhead. Orchestration plane
processes ∼106 events/s, each carrying ∼1 nat of scheduling
information.

$$
Efficiency: Operational efficiency \eta \approx10−14 reflecting
$$

coordination overhead costs.

$$
8) Multi-Tenant Platforms: B-IQ Estimate: ∆B \approx109
$$

nat/s. Large-scale cloud platform (N = 105–106 instances).
Service mesh and load balancing enable higher coordination
efficiency. Per-instance B-IQ ∼103 nat/s with coordination
factor \rho \approx0.1.
Efficiency: Platform economies of scale yield \eta \approx10−16.
9) Global AI Society: B-IQ Estimate: ∆B \approx1012 nat/s.
Internet-scale AI coordination (N = 107–108 devices). IoT
sensors, robotic actuators, and distributed AI services. Theo-
retical maximum limited by physical communication latencies
and coordination protocols.

$$
Efficiency: Projected efficiency \eta \approx10−15 assuming opti-
$$

mal coordination infrastructure.

$$
10) Human Individual: B-IQ Estimate: ∆B \approx3 \times 105
$$

nat/s. Miller & Buschman [?] establish working memory
capacity of 4\pm1 items constrained by oscillatory brain rhythms.
Human cortex has ∼1011 neurons firing at ∼10 Hz,
yielding theoretical capacity ∼1012 bit/s. However, conscious
processing is severely limited: only ∼4 items can be held

$$
simultaneously, updated at ∼10 Hz with ∼16 bits/item (216 \approx
$$

$$
65,000 concepts), giving effective bandwidth \approx4\times10\times16 \approx
$$

$$
6\times102 bit/s for conscious thought. For goal-directed behavior
$$

involving subconscious processing, we estimate ∼105 nat/s

$$
[?]. Miller (1956) originally suggested 7\pm2 items, but modern
$$

estimates favor ∼4.
Efficiency: Individual baseline—no growth differential
computed.

$$
11) Bands/Tribes: B-IQ Estimate: ∆B \approx106 nat/s. Small
$$

social group (N = 10–102) with high trust and direct commu-
nication. Minimal coordination overhead due to kin networks.

$$
Total B-IQ \approxN \times 3 \times 105/102 \approx106 nat/s accounting for
$$

information sharing benefits.
Efficiency: Social cooperation benefits yield \eta \approx10−11.

$$
12) Chiefdoms: B-IQ Estimate: ∆B \approx108 nat/s. Mid-
$$

scale society (N = 103–104) with hierarchical organization.
Coordination overhead increases due to status competition and
reduced trust. Effective per-capita B-IQ drops to ∼104 nat/s.
Efficiency: Organizational friction yields minimum effi-
ciency \eta \approx10−17.
13) Nation-States: B-IQ Estimate: ∆B \approx1011 nat/s.
Large-scale society (N = 105–108) with institutional infras-
tructure. Legal systems, markets, and communication networks
enable coordination recovery. Per-capita effective B-IQ ∼103
nat/s due to institutional overhead.
Efficiency: Institutional coordination yields \eta \approx10−14.
14) GPT-4 Inference: Current B-IQ: ∼108 nat/s. Trans-
former model processing ∼103 tokens/s during inference
[?], each token carrying ∼105 bits of semantic information.
Attention mechanisms and feed-forward layers compress and
transform this to ∼108 nat/s effective information processing.
Performance varies significantly with inference framework,
with TensorRT-LLM achieving highest throughput [?].
Theoretical Max: ∼1013 nat/s. Hardware substrate (GPUs)
capable of ∼1015 operations/s, but model architecture and
memory bandwidth limit effective B-IQ to ∼1013 nat/s.
Network latency becomes critical bottleneck for distributed
inference.

---

Utilization: Current systems achieve ∼10−5 of theoretical
maximum, limited by model inefficiencies and coordination
overhead [?].
15) Human Expert: Current B-IQ: ∼106 nat/s. Expert-
level performance in focused domains (medicine, chess, pro-
gramming) extends beyond the basic 4-item working memory
limit [?] through chunking and domain-specific pattern recog-
nition. Experts process complex patterns as single chunks,
effectively increasing functional capacity from ∼102 bit/s
(novice) to ∼106 nat/s through practiced access to long-term
memory structures and automated pattern recognition.
Theoretical Max: ∼1011 nat/s. Full cortical capacity with
optimal information integration across all brain regions.
Utilization: Experts achieve ∼10−5 utilization through
focused attention and domain knowledge.
16) Warehouse Robotics: Current B-IQ: ∼109 nat/s.
Modern automated warehouse with ∼103 robots, each pro-
cessing ∼106 bit/s sensory input and ∼104 bit/s motor
control. Central coordination system adds ∼109 nat/s for
optimization and routing.
Theoretical Max: ∼1013 nat/s. Physical limits from sensor
bandwidth (∼1012 bit/s aggregate) and actuator capacity (∼
1011 bit/s) across the facility.
Utilization: Current systems achieve ∼10−4 efficiency due
to conservative control algorithms and safety margins.
17) National Economy: Current B-IQ: ∼1011 nat/s.
GDP-scale information processing across ∼108 economic
agents, financial networks, supply chains, and government
institutions. Each agent contributes ∼103 nat/s effective
economic decision-making capacity.
Theoretical Max: ∼1015 nat/s. Theoretical limit if all com-
munication channels, computing infrastructure, and human
cognitive capacity were optimally coordinated for economic
information processing.
Utilization: National economies achieve ∼10−4 efficiency
due to market inefficiencies, institutional friction, and coordi-
nation problems.

## VII. HIERARCHICAL AGGREGATION

$$
A multi-layer agent stack {B(k)} with actuator weight \omegak =
$$

C(k)
act/ P
j C(j)
act obeys
B−IQhier =
X
k
\omegak
h
I(k)

$$
pred +\alphaI(k) ctrl −\betaH(I(k))−\gammaS(k)i
$$

. (9)

$$
When coordination lifts \rho and amortises cost, the top-level
$$

B-IQ asymptotically approaches the sensor/actuator ceiling
(Sec. III).

## VIII. SCALING PATTERN

A. Scaling Ansatz
We model efficiency scaling using power laws for system
parameters. For an N-unit system, assume:
b(N) ∝N a,
p(N) ∝N −b,

$$
\rho(N) \approx 1
$$

$$
1 + e−\kappa(N−N0) , c(N) ∝N c,
$$

∆B(N) ∝N B1 (per-unit B1).

$$
(10) Then efficiency scales as: \eta(N) =
$$

g

$$
∆B(N) ∝b(N)p(N)\rho(N) c(N)N B1
$$

∝N a−b−c−1\rho(N).
(11) B. AI Hierarchy Scaling Table III details scaling regimes across AI system layers: TABLE III AI HIERARCHY SCALING PARAMETERS
Layer
Scale (N)
Exponent regime
Microservice guild
10–102
a = 0, b = 1, c = 0.5
Kubernetes cluster
103–104
\rho rising
Multi-tenant platform
105–106

$$
\rho \to1 Global AI society
$$

107–108
c amortized

$$
Initial drop (N < N0): \eta ∼N −2.5 plummets as microser-
$$

vices fragment.

$$
Rebound (N ≳N0 \approx104): \rho \to1 and if a−c−1 > 0 (e.g.,
$$

c \approx0.5), then \eta ∝N −1.5 or flattens, recovering efficiency.
Ceiling: Sensor/actuator channels saturate at Csens, Cact,
capping b and c.

## C. Human Hierarchy Scaling

Table IV presents scaling across human organizational lay-
ers:
TABLE IV
HUMAN HIERARCHY SCALING PARAMETERS
Layer
Scale (N)
Exponent regime
Individual
1
–
Bands/tribes
101–102

$$
a \approx0.5, b \approx1, c \approx1 Chiefdoms
$$

103–104
\rho dips
Nation-states
105–108

$$
\rho \to1 Small scale: \eta ∼N −2.5 but high \rho softens drop (N < 102).
$$

$$
Mid scale: Chiefdoms see minimal bp\rho/c, yielding lowest
$$

\eta.
Macro scale (N > 105): Legal/institutional scaffolding
drives \rho \to1 and amortizes c, so \eta ∝N −1.5 or better.
D. Universal Scaling Principles
Both AI and human hierarchies exhibit:

### 1. Fragmentation penalty: Small-scale systems achieve

high per-bit efficiency only up to threshold N0.

### 2. Mid-range collapse: Without coordination technology,

$$
overheads c and low p, \rho cause \eta to drop by orders of
$$

magnitude.

### 3. Institutional rebound: Once rules/protocols bind many

$$
units (N > N0), p and \rho rise while c is shared, partially
$$

restoring \eta.

---

### 4. Convergent ceilings: Both hierarchies approach the same

physical IO limits (Csens, Cact), giving comparable ultimate
competence bounds (∼1013–1014 nat s−1).

$$
E. Sensitivity to \alpha, \beta, \gamma Using the anchors of Table I we test how varying the coef-
$$

$$
ficients shifts B−IQ and the derived efficiency \eta = g/∆B.
$$

• Control
scaling

$$
(\alpha). Across anchors Ictrl/Ipred \in
$$

$$
[0.02, 0.3]. Replacing \alpha = 1 by \alpha \in[0.5, 2] alters B−IQ
$$

by < 20% (humans) and < 5% (LLMs, firms); efficiency

$$
brackets in Sec. VI shift by \leq0.2 decades.
$$

$$
• Surprise scaling (\gamma). Observed S/Ipred \leq0.2. Choosing
$$

$$
\gamma \in[0.5, 2] therefore perturbs total B-IQ by at most
$$

\pm20%, leaving the rank order of agents unchanged.

$$
• Memory penalty (\beta). If \beta were raised from 10−3
$$

to 1, the B-IQ of silicon megaclusters (dominated by
H(I)) would fall two orders, possibly dropping below hu-
man–society levels. All qualitative statements in §III–VIII

$$
remain valid provided \beta < 10−2; above that threshold
$$

memory cost becomes decisive and large-memory agents
lose their advantage.

$$
Summary: For physically grounded settings \alpha = \gamma =
$$

$$
1, \beta ≪1, uncertainty in the weights modifies numerical B-
$$

IQ values by ≲0.3 orders—small relative to the 10–15-order

$$
span seen in the empirical \eta distribution. The tentative U-
$$

shape in efficiency is therefore unlikely to be an artefact of
coefficient choice, though it may still reflect sampling bias or
hidden covariates.

## IX. ABSOLUTE LIMITS AND CURRENT POSITION

A. Theoretical Ceilings
Physical constraints impose hard bounds on achievable B-
IQ:

$$
B-IQmax = Csens + \alphaCact −\betaCrt mem −\gammaSmin
$$

$$
\leqCsens + Cact (for \beta, \gammaSmin ≪Csens)
$$

(12) For concrete systems: • 10 MW datacenter: Optical fiber ingress ∼1012 bit/s, robotic actuators ∼1011 bit/s, yielding B-IQmax ∼1014
nat/s.

$$
• Human cortex: Neural bandwidth ∼1012 spike/s \times 1
$$

bit/spike \approx1011 nat/s.
• Global internet: Aggregate bandwidth ∼1015 bit/s, but
coordination overhead limits effective B-IQ to ∼1012
nat/s.
B. Distance from Limits
Current systems operate far below theoretical maxima:
Key findings: 1. Massive headroom: Even advanced sys-
tems utilize < 10−3 of their theoretical capacity. 2. Co-

$$
ordination bottleneck: Large systems are limited by \rho(N)
$$

rather than raw processing power. 3. Efficiency opportunity:
Orders of magnitude improvement possible through better
coordination protocols.
TABLE V
DISTANCE FROM THEORETICAL LIMITS
System
Current B-IQ
Theoretical Max
Utilization
GPT-4 inference
∼108
∼1013
∼10−5
Human expert
∼106
∼1011
∼10−5
Warehouse robotics
∼109
∼1013
∼10−4
National economy
∼1011
∼1015
∼10−4

## C. Scaling Trajectories

Extrapolating current trends:
• AI systems: Following N −1.5 scaling, global AI society
(N ∼108) could achieve \eta ∼10−15 with \rho \to1.
• Human institutions: Nation-states approach ∼10−14
efficiency ceiling, limited by communication latency.
• Hybrid systems: AI-human collaboration may overcome
individual limitations, potentially reaching \eta ∼10−12.

## X. DISCUSSION

Hierarchical universality. The U-shaped efficiency scaling
observed across both AI and human hierarchies suggests
fundamental constraints on information processing at differ-
ent organizational scales. The mid-range efficiency minimum
around N ∼103–104 appears to be a universal coordination
bottleneck where systems are too large for direct commu-
nication but too small for effective institutional structures.
Notably, this pattern may help explain why empires and
large organizations often experience internal collapse: As they
grow beyond optimal coordination scales, efficiency drops
precipitously, making them vulnerable to smaller, more agile
competitors or internal fragmentation.
Physical bounds and headroom. Current systems operate
3–5 orders of magnitude below their theoretical limits. Even
a 10 MW datacenter, saturating both optical ingress and

$$
robotic egress, tops out near 1014 nat s−1—roughly 500\times a
$$

whole human cortex. This massive headroom suggests that
competence growth is limited by coordination protocols rather
than raw computational capacity.
Efficiency patterns. Biological micro-agents convert com-

$$
petence into fitness at \eta ∼10−12–10−14; current industrial
$$

systems sit many orders lower, suggesting large slack. The
efficiency rebound at macro scales (N > 105) in both AI
and human systems indicates that institutional scaffolding can
partially overcome coordination overhead, though never fully
recovering small-scale efficiency.
Convergent ceilings. Both AI and human hierarchies ap-
proach similar ultimate competence bounds (∼1013–1014 nat
s−1), suggesting that environment complexity and coordina-
tion infrastructure, rather than substrate differences, determine
system-level intelligence limits.
Implications for AI development. The analysis suggests
that building larger AI systems without addressing coordina-

$$
tion efficiency (\rho(N)) may yield diminishing returns. Focus
$$

should shift from raw model scaling to developing better proto-
cols for multi-agent coordination and information sharing. The

---

$$
cooperativity index \kappaij (Sec. V) provides a quantitative frame-
$$

work for optimizing transparency versus privacy in multi-
agent AI systems, with percolation thresholds determining
when cooperative behaviors spread globally versus remaining
localized.
Caveats. Anchors use heterogeneous proxies; memory costs
\betaH(I) are approximated; sensor entropy estimates are coarse.
The observed U-shape may reflect sampling bias across dif-
ferent temporal and spatial scales. Larger datasets with more
uniform measurement protocols are needed to confirm these
scaling patterns.
Future work. We intend to develop a common mea-
surement protocol for B-IQ across diverse systems. Current
estimates rely on heterogeneous methodologies, making direct
comparisons difficult. Standardized approaches for measuring
information processing capacity, growth rates, and efficiency
would enable more robust cross-system analysis and better
validation of the proposed scaling laws.

## XI. CONCLUSION

B-IQ provides a principled, language-free gauge of agent
competence derivable from blanket statistics. Preliminary an-
chors span 15 orders of efficiency, hinting that coordination
overhead—not raw information processing—dominates large-
scale performance. Further empirical work is required to
confirm or refute the tentative U-shape in \eta(N).

## XII. COMPARATIVE COMPETENCE METRICS AND

SCALING LAWS
B-IQ complements other competence measures such as
Integrated Information Theory (IIT 4.0) [?] and semantic
information measures [?]. Unlike IIT, which emphasizes in-
tegrated consciousness, B-IQ explicitly quantifies predictive
and control information flows across agent Markov blankets.
Furthermore, neural network scaling laws [?] provide empir-
ical evidence for diminishing returns in performance gains
as computational resources grow, corroborating our efficiency
scaling results. Empirical studies on collective intelligence [?]
further substantiate our observed U-shaped efficiency scaling
across organizational scales.
REFERENCES
[1] G. Zarncke, “Foundations of unsupervised agent discovery in raw
dynamical systems,” AE Studio, 2025.
[2] N. Tishby, F. C. Pereira, and W. Bialek, “The information bottleneck
method,” 2000.
[3] G. Zarncke, “Attractor basins of cooperation, privacy, and parasite
persistence,” AE Studio, 2025.
[4] D. M. Gordon, “Movement, encounter rate, and collective behavior in
ant colonies,” Annals of the Entomological Society of America, vol. 114,
no. 5, pp. 541–546, 2020.
[5] W. R. Tschinkel, “The organization of foraging in the fire ant, solenopsis
invicta,” Journal of Insect Science, vol. 11, no. 26, 2011.
[6] E. K. Miller and T. J. Buschman, “Working memory capacity: Limits
on the bandwidth of cognition,” Daedalus, vol. 144, no. 1, pp. 112–122,
2015.
[7] L. Albantakis et al., “Integrated information theory 4.0,” PLOS Compu-
tational Biology, vol. 19, no. 3, 2023.
[8] A. Kolchinsky and D. H. Wolpert, “Semantic information,” Entropy,
vol. 20, no. 11, 2018.
[9] J. Kaplan et al., “Scaling laws for neural language models,” arXiv
preprint arXiv:2001.08361, 2020.
[10] A. W. Woolley, C. F. Chabris, A. Pentland, N. Hashmi, and T. W.
Malone, “Evidence for a collective intelligence factor in the performance
of human groups,” Science, vol. 330, no. 6004, pp. 686–688, 2010.
