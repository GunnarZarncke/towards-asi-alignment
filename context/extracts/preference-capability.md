# Extract: preference-capability.pdf

**Source PDF:** `context/preference-capability.pdf`
**Extract:** `context/extracts/preference-capability.md`
**Pages:** 2
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

Preference–Conditioned Capability: From B–IQ to Goal–Realizing
LLM Agent Loops
Gunnar Zarncke
AE Studio
August 22, 2025
Abstract
Large–language models (LLMs) excel at raw prediction, but deployed agent loops require
competence that is conditioned on what the agent wants. Building on Unsupervised Agent
Discovery (UAD) and the Bitwise Intelligence (B–IQ) metric, we formalize preference–conditioned
prediction and control and derive a companion measure B-IQwant. We show how to infer wants
as prior preferences over observations in an active–inference lens, then evaluate systems via
alignment ratios rpred and rctrl that compare value–conditioned to raw channels. We argue
that natural selection drives these ratios high in biological agents, while contemporary LLM
training leaves them low. We propose training and evaluation protocols for LLM agent loops
that directly raise Iwant
pred and Iwant
ctrl , and we connect to related work in Inverse RL, RLHF/DPO,
control–as–inference, world–model RL, and active inference.1
1
Introduction
Distinguishing predicting P from preferring P is central to alignment discussions.
The UAD
framework discovers agents as Markov–blanket partitions in raw dynamics and exposes separate
information flows for prediction and control [Zarncke, 2025a]. B–IQ adds a task–agnostic competence
functional combining predictive and control mutual information with cost terms [Zarncke, 2025b].
Yet both quantities are raw channels: they measure total prediction and control, not necessarily
directed at the agent’s goals.
This paper introduces a preference–conditioned refinement of these channels and shows how, for
LLM agent loops, we can (i) infer
”wants
” as prior preferences over future observations and (ii) measure competence at realizing those wants.
The result sharpens why LLMs, though strong at Ipred, often underperform at Iwant
pred and Iwant
ctrl
compared to biological agents.
Contributions

### 1. Define preference–conditioned channels Iwant

pred and Iwant
ctrl
and the competence score B-IQwant.

### 2. Derive inverse–active–inference estimators that recover wants as linear–feature priors over

observations from LLM agent trajectories.

### 3. Propose alignment ratios rpred, rctrl and an evaluation protocol for humans vs. LLM agents.

1Information quantities are in nats unless noted.
1

---

### 4. Discuss training interventions that raise the preference–conditioned channels and relate to CIRL,

RLHF/DPO, ReAct/Toolformer/WebGPT, SayCan/PaLM–E, Dreamer, control–as–inference,
and active inference.
2
Background: UAD and B–IQ
UAD. Given raw variables {Xk(t)}, UAD clusters an agent C when the blanket test holds
I(IC
t+1; EC
t+1 | SC
t , AC

$$
t ) \approx0, then localizes memory by lagged mutual information and infers goals via
$$

an information–theoretic Lagrangian [Zarncke, 2025a]. UAD also formalizes inter–agent coupling
and a cooperativity index that generalizes Hamilton’s rule [Zarncke, 2025a,c].
B–IQ. The baseline competence metric is

$$
B-IQ = Ipred + Ictrl −\beta H(I) −\gamma S, (1)
$$

with Ipred = I(It; St+1), Ictrl = I(At; Et+1), memory cost H(I), and residual surprise S =
E[−log P(St+1 | It)] [Zarncke, 2025b].
Physical bounds follow from sensor/actuator channel
capacities.
3
Preference–Conditioned Channels
Let an agent’s “wants” be prior preferences over next observations, encoded as

$$
log Ppref(S′) ∝\psi⊤\phi(S′), (2)
$$

$$
with features \phi(·) (e.g., pass/fail, constraint violations, reward proxies, human–approval signals)
$$

and weights \psi to be inferred.
Value–conditioned prediction
projects the predictive channel onto want–relevant sensory
subspaces:
Iwant
pred
= I
It; S′
\psi

,

$$
(3) where S′[\psi] indexes the sufficient statistics of \phi(S′). Value–conditioned control
$$

similarly restricts control to the preferred externals:
Iwant
ctrl
= I
At; E′
\psi

.
(4) Preference–conditioned competence is then B-IQwant = Iwant pred + Iwant
ctrl

$$
−\beta H(I) −\gamma S, (5)
$$

with alignment ratios
rpred :=
Iwant
pred
Ipred
,
rctrl := Iwant
ctrl
Ictrl
.
(6) 2
