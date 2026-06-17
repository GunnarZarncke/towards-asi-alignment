# Terminology

Operational definitions for core terms. See `INSTRUCTIONS.md` §6 for the full list.

| Term | Operational definition |
|------|------------------------|
| Agent | A bounded dynamical process whose internal states help predict and control future interaction with its environment. |
| Boundary | A statistical and causal interface that makes internal and external dynamics approximately separable for prediction and control. |
| Capability | The degree to which a system can predict and control relevant future states through its boundary, after accounting for memory cost and surprise. |
| Value bundle | A low-dimensional latent control direction that changes policy across many contexts. |
| Bearer map | A mapping specifying what entities, states, or processes a value bundle applies to. |
| Goal inference | Finding latent objectives or value-bundle structures that make observed behavior more compressible. |
| Goal transport | Preservation of goal-relevant structure across transformation. |
| Correction channel | The causal route by which humans observe, judge, deliberate, object, and change future system behavior before irreversible damage. |
| Correction-channel integrity | The effective capacity of the correction chain after penalties for latency, manipulation, irreversibility, and ontology mismatch. |
| Successor | Any system created, copied, delegated to, fine-tuned, empowered, or instantiated by a prior system such that it inherits relevant control capacity. |
| Alignment basin | A self-stabilizing region of dynamics where value-bundle geometry, bearer maps, correction-channel capacity, and successor constraints remain human-correctable under pressure. |
| Pivotal process | A socio-technical basin transition from race dynamics to certified-deployment dynamics ($\mathcal{B}_{\text{race}} \to \mathcal{B}_{\text{certified deployment}}$); not a single unilateral decisive act. |
| Inferential coupling index (ICI) | A measure of coordination potential between systems via shared meta-priors and decision-theoretic similarity, even when causal reach $p_{ij}$ is low. |
| Effective cooperativity ($\tilde{\kappa}_{ij}$) | Cooperativity index combining causal reach and inferential coupling. |
| Correction-capacity assumption | Society retains enough institutional, epistemic, and practical capacity at $t_0$ to notice, evaluate, and constrain frontier systems: $C_{\text{corr}}^{\text{society}}(t_0) > \theta$. |
| Adversarial measurement | Inferring agency, goals, opacity, and successor risk when the system may benefit from confusing the measurement process. |
| Coerced correction | Correction signals produced under threat, dependency, or capture; excluded from legitimate correction-channel integrity. |
| Paternalism boundary | Care improvements that reduce autonomy, agency, or future correction capacity ($\Delta B_{\text{care}}>0$ but $\Delta B_{\text{autonomy}}, \Delta C_{\text{corr}}<0$). |
