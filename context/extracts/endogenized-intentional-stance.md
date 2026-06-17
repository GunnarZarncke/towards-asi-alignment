# Extract: endogenized-intentional-stance.pdf

**Source PDF:** `context/endogenized-intentional-stance.pdf`
**Extract:** `context/extracts/endogenized-intentional-stance.md`
**Pages:** 4
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

The Endogenized Intentional Stance:
A Predictive–Compression Formalization of Agent
Discovery
Author Name
AE Studio
author@aestudio.org
November 2025
Abstract
We formalize an Endogenized Intentional Stance (EIS): a behavioral–informational pro-
cedure for discovering agents and goals directly from raw observation streams without pre-
specified entities or sensors. EIS extends the pragmatic–predictive view of Dennett (1987)
and recent stochastic formalizations (McGregor et al., 2025) by replacing the assumption
of a given world model with a learned latent dynamics that simultaneously grounds envi-
ronment, action, and purpose. Agency emerges where a soft-optimal (goal-rational) prior
over latent interventions reduces description length relative to a purely mechanistic base-
line.
Intentionality thus becomes an empirical, compression-based property of dynamics
rather than an anthropomorphic stance. We derive sufficient conditions for intentional gain,
outline a hierarchical aggregation scheme, and connect the resulting constructs to known
information-theoretic quantities: predictive mutual information, control entropy, and value
gradients under bounded rationality.
1
Introduction
Attributing beliefs and desires to a system can dramatically simplify behavioral prediction.
Dennett’s intentional stance treats such attributions as modeling conveniences, vindicated when
they increase predictive success at low cognitive cost. McGregor et al. (2025) showed that any
stochastic process may, in principle, admit a normative–epistemic interpretation.
Yet both
perspectives presuppose a world model defining what could be believed or desired. We here
remove that presupposition: given only an observation sequence {ot}T
t=1, we ask where goal-
directed explanations yield better compression than purely mechanistic ones. The resulting
procedure endogenizes world, agent, and goal in a single generative model.
2
Predictive world modeling
Let \theta parameterize a predictive latent dynamics

$$
p\theta(o1:T , z1:T ) = Y
$$

t

$$
p\theta(ot | zt) p\theta(zt | zt−1), (1)
$$

with hidden variables zt \inRd learned by maximizing

$$
L0(\theta, \phi) = X
$$

t

$$
Eq\phi(zt|o\leqt)[log p\theta(ot | zt)] −\beta DKL(q\phi∥p\theta).
$$

No partition into sensors, actuators, or entities is assumed.
1

---

3
Intentional prior and compression gain

$$
We augment (1) with discrete latent impulses at \inA acting as candidate interventions in z:
$$

p(o, z, a) =
Y
t
p(ot | zt) p(zt+1 | zt, at) p(at).

$$
(2) The intentional stance introduces a soft-optimal prior p\beta(at | zt) ∝exp[\beta r\psi(zt, at)],
$$

$$
(3) where r\psi is a learned reward density and \beta > 0 an inverse-temperature. This converts the
$$

purely generative dynamics into a bounded-rational control process.
Let LI denote the log evidence of the intentional model and LM that of a baseline with
uniform p(at). The intentional gain

$$
∆L = LI −LM −\lambda DL(r\psi) (4)
$$

measures the code-length reduction due to goal-directed explanation. A subsystem C is declared
intentional when ∆LC > 0, signifying that rationality assumptions compress its trajectory.
4
Emergent entities
We seek subsets of latent coordinates C ⊆z for which ∆LC is maximized subject to sparse
coupling with the remainder. Operationally, we minimize
J (C) = I(z′
C; z′

$$
\negC | aC) −\alpha ∆LC, (5)
$$

where I(·; · | ·) is conditional mutual information.
Local minima define dynamically quasi-
autonomous modules whose behavior is efficiently summarized by (3). These modules constitute
endogenously discovered agents.
5
Hierarchical aggregation
Given intentional modules {Ci} with latent values z(i)
t , construct an abstract state ¯zt = f({z(i)
t })
and abstract actions ¯at = g({a(i)
t }). Reapplying (3) in the compressed space yields higher-level

$$
intentional priors p\beta(¯at | ¯zt) ∝exp[\beta ¯r(¯zt, ¯at)]. Hierarchies thus emerge recursively where joint
$$

intentional gain exceeds the sum of constituent gains. This realizes Dennett’s multi-level stance:
agents within agents, unified by shared compression criteria.
6
Cooperative structure
For modules i, j define an empirical cooperativity index

$$
\kappaij = ∆V (i)(do(a(j))) cost(i)
$$

,

$$
(6) where ∆V (i) is the change in expected cumulative reward V (i)(z) = E[P t r(i) \psi (zt, at)] under
$$

$$
counterfactual manipulation of a(j). Edges with \kappaij > 1 define cooperative clusters; \kappaij < 0
$$

indicates competition. These relations permit percolation analyses analogous to those used in
evolutionary models of cooperation (Hamilton, 1964).
2

---

7
Relation to information principles
The intentional prior (3) connects to known information-theoretic quantities: let Ipred = I(zt; zt+1)
and Ictrl = I(at; zt+1). Expected log evidence decomposes as

$$
E[log p(o)] \approxIpred + Ictrl −\betaH(zt) −\gammaS, (7)
$$

$$
with S = −E[log p(ot+1 | zt)] the residual surprise and coefficients (\beta, \gamma) reflecting memory and
$$

uncertainty costs (Friston, 2010; Tishby et al., 2000). Hence intentional gain (4) corresponds
to an information-bottleneck advantage achieved by positing latent goals.
8
Determinacy and uniqueness
Following McGregor et al. (2025), multiple normative–epistemic interpretations can coexist for
stochastic processes. EIS refines this by assigning quantitative preference
P(interpretation) ∝exp[∆L],
so that interpretations form an energy landscape whose minima represent the simplest ra-
tionalizations. Deterministic subsystems yield unique minima; chaotic or noisy ones support
degenerate stances.
9
Discussion
EIS reinterprets Dennett’s intentional stance as a model-selection principle.
Whereas clas-
sic formulations required an observer’s external world model, EIS internalizes it by train-
ing a predictive generative model directly from data.
Intentionality becomes an empirical
regularity—regions of the dynamics for which rational-goal assumptions save bits. This ex-
tends bounded-rational control to settings lacking predefined agents or utilities, aligning with
information-theoretic frameworks of adaptation (Friston et al., 2010; Tishby et al., 2000) and
with normative–epistemic mappings in stochastic processes (McGregor et al., 2025).
10
Conclusion
The Endogenized Intentional Stance provides a unified, data-driven criterion for the emergence
of agency and purpose. An observer need not know what is sensed or controlled; the system’s
own predictive structure reveals where such attributions improve compression. Hierarchies and
cooperation follow naturally from additivity of intentional gain. This formulation renders the
intentional stance measurable, bridging philosophical pragmatism and information physics.
References
[1] D. C. Dennett. The Intentional Stance. MIT Press, 1987.
[2] K. Friston. The free-energy principle: a unified brain theory? Nature Reviews Neuroscience,
11(2):127–138, 2010.
[3] W. D. Hamilton. The genetical evolution of social behaviour. Journal of Theoretical Biology,
7(1):1–16, 1964.
[4] N. Tishby,
F. C. Pereira,
and W. Bialek.
The information bottleneck method.
arXiv:physics/0004057, 2000.
3

---

[5] S. McGregor, et al. Formalising the intentional stance I: Attributing goals and beliefs to
stochastic processes. arXiv:2405.16490v2, 2025.
4
