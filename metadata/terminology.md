# Terminology

Operational definitions for core terms. Canonical reader surface: Appendix F (`appendices/appF-glossary.tex`). Editorial rules: `INSTRUCTIONS.md` §5.

| Term | Operational definition |
|------|------------------------|
| Agent | A bounded dynamical process whose internal states help predict and control future interaction with its environment. |
| Boundary | A statistical and causal interface that makes internal and external dynamics approximately separable for prediction and control. |
| Capability | The degree to which a system can predict and control relevant future states through its boundary, after accounting for memory cost and surprise. |
| Value bundle | A low-dimensional latent control direction that changes policy across many contexts. |
| Bearer map | A mapping specifying what entities, states, or processes a value bundle applies to. |
| Goal inference | Finding latent objectives or value-bundle structures that make observed behavior more compressible. |
| Goal transport | Preservation of goal-relevant structure across transformation. |
| Correction channel | The pathway by which humans or human institutions observe a system, judge, deliberate, issue corrections, and change its future behaviour before irreversible damage; formally, a correcting agent \(G_t\) that sufficiently coincides with legitimate human correction controls handles \(\mathcal{H}_t\) that reach the target's update and later behaviour. Canonical definition: **ch24** (`eq:handle-controlled-correction-channel-ch24`; trace `eq:correction-chain-ch24`). |
| Correction-channel integrity | The weakest effective capacity of those controlled, reaching handles after penalties for latency, manipulation/capture, irreversibility, and ontology mismatch. Formal definition: **ch25** (`eq:cci-ch25`). |
| Deployment/control mass | In selection environment \(E\), the aggregate effective selection capacity over handles controlled in \(E\) that reach system \(A\). Formal definition: **ch32** (`eq:deployment-mass-ch32`). |
| Fitness | Environment-relative rate of deployment-mass accumulation, \(\mathrm{Fit}_E(A)=\frac{d}{dt}\log\mu_E(A)\); relative ordering uses \(\mu_E\). Not moral value; capability, revenue, and benchmarks enter only as drivers of selection-handle exercise. Formal definition: **ch32** (`eq:fitness-ch32`). |
| Successor | Any system created, copied, delegated to, fine-tuned, empowered, or instantiated by a prior system such that it inherits relevant control capacity. |
| Alignment basin | A self-stabilizing region of dynamics where value-bundle geometry, bearer maps, correction-channel capacity, and successor constraints remain human-correctable under pressure. |
| Pivotal process | A socio-technical basin transition from race dynamics to certified-deployment dynamics ($\mathcal{B}_{\text{race}} \to \mathcal{B}_{\text{certified deployment}}$); not a single unilateral decisive act. |
| Inferential coupling index (ICI) | A measure of coordination potential between systems via shared meta-priors and decision-theoretic similarity, even when causal reach $p_{ij}$ is low. |
| Effective cooperativity ($\tilde{\kappa}_{ij}$) | Cooperativity index combining causal reach and inferential coupling. |
| Correction-capacity assumption | Society retains enough institutional, epistemic, and practical capacity at $t_0$ to notice, evaluate, and constrain frontier systems: $C_{\text{corr}}^{\text{society}}(t_0) > \theta$. |
| Adversarial measurement | Inferring agency, goals, opacity, and successor risk when the system may benefit from confusing the measurement process. |
| Coerced correction | Correction signals produced under threat, dependency, or capture; excluded from legitimate correction-channel integrity. |
| Paternalism boundary | Care improvements that reduce autonomy, agency, or future correction capacity ($\Delta B_{\text{care}}>0$ but $\Delta B_{\text{autonomy}}, \Delta C_{\text{corr}}<0$). |
