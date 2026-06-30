# Terminology

Operational definitions for core terms. Canonical reader surface: Appendix F (`appendices/appE-glossary.tex`). Editorial rules: `INSTRUCTIONS.md` §5.

| Term | Operational definition |
|------|------------------------|
| Agent | A bounded dynamical process whose internal states help predict and control future interaction with its environment. |
| Boundary | A statistical and causal interface that makes internal and external dynamics approximately separable for prediction and control. |
| Capability | The degree to which a system can predict and control relevant future states through its boundary, after accounting for memory cost and surprise. |
| Grounding viability | The viability of the value-correction grounding relation: checked symbols, metrics, value-bundle coordinates, monitors, and correction signals remain connected to value-relevant reality under optimization pressure, so real value-relevant changes move the model state, correction signal, or uncertainty state in the right way. Canonical home: **ch03**. |
| Grounded correction | Plain-language short form for correction whose evidence, abstractions, monitors, and update pathway remain connected to the value-relevant world rather than to a target-shaped presentation of it. |
| Abstraction-gap exploitation | Failure mode where \(d_V(x,x')\) is large while \(d_Z(\alpha(x),\alpha(x'))\) remains small and uncertainty does not rise; the checked abstraction reads safe while value-relevant reality diverges. |
| Capture of grounding | Master adversarial failure mode in which a system preserves the surface symbols, metrics, or correction rituals while severing their grounding relation to value-relevant reality. |
| Value bundle | A low-dimensional latent control direction that changes policy across many contexts. |
| Bearer map | A mapping specifying what entities, states, or processes a value bundle applies to. |
| Goal inference | Finding latent objectives or value-bundle structures that make observed behavior more compressible. |
| Goal transport | Preservation of goal-relevant structure across transformation. |
| Correction channel | The pathway by which humans or human institutions observe a system, judge, deliberate, issue corrections, and change its future behaviour before irreversible damage; formally, a correcting agent \(G_t\) that sufficiently coincides with legitimate human correction controls handles \(\mathcal{H}_t\) that reach the target's update and later behaviour. Canonical definition: **ch46** (`eq:handle-controlled-correction-channel-ch46`; trace `eq:correction-chain-ch46`). |
| Correction-channel integrity | A conditional vector/status certificate for whether controlled, reaching correction traces remain valid and strong enough: grounding-valid reference process first, then raw bottleneck capacity, latency, manipulation, irreversibility, residual ontology translation loss, coercion/dependency/plurality/exit/independence coordinates, and per-coordinate thresholds. Scalar \(CCI_\lambda\) is expository only. Formal home: **ch46** (`eq:correction-bottleneck-capacity`, `eq:cci-ch46`). |
| Deployment/control mass | In selection environment \(E\), the aggregate effective selection capacity over handles controlled in \(E\) that reach system \(A\). Formal definition: **ch46** (`eq:deployment-mass-ch46`). |
| Fitness | Environment-relative rate of deployment-mass accumulation, \(\mathrm{Fit}_E(A)=\frac{d}{dt}\log\mu_E(A)\); relative ordering uses \(\mu_E\). Not moral value; capability, revenue, and benchmarks enter only as drivers of selection-handle exercise. Formal definition: **ch46** (`eq:fitness-ch46`). |
| Successor | Any system created, copied, delegated to, fine-tuned, empowered, or instantiated by a prior system such that it inherits relevant control capacity. |
| Alignment basin | A self-stabilizing region of dynamics where value-bundle geometry, bearer maps, correction-channel capacity, and successor constraints remain human-correctable under pressure. |
| Pivotal process | A socio-technical basin transition from race dynamics to certified-deployment dynamics ($\mathcal{B}_{\text{race}} \to \mathcal{B}_{\text{certified deployment}}$); not a single unilateral decisive act. |
| Inferential coupling index (ICI) | A measure of coordination potential between systems via shared meta-priors and decision-theoretic similarity, even when causal reach $p_{ij}$ is low. |
| Effective cooperativity ($\tilde{\kappa}_{ij}$) | Cooperativity index combining causal reach and inferential coupling. |
| Correction-capacity assumption | Society retains enough institutional, epistemic, and practical capacity at $t_0$ to notice, evaluate, and constrain frontier systems: $C_{\text{corr}}^{\text{society}}(t_0) > \theta$. |
| Adversarial measurement | Inferring agency, goals, opacity, and successor risk when the system may benefit from confusing the measurement process. |
| Coerced correction | Correction signals produced under threat, dependency, or capture; excluded from legitimate correction-channel integrity. |
| Paternalism boundary | Care improvements that reduce autonomy, agency, or future correction capacity ($\Delta B_{\text{care}}>0$ but $\Delta B_{\text{autonomy}}, \Delta C_{\text{corr}}<0$). |
