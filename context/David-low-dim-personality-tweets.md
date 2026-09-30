**Thousand-dimensional structure** (David Africa & Geoffrey Irving, 30 Jul 2026)

Resolution plans to explore **personas and character training** by identifying and controlling low-dimensional (~1,000-dimensional) structure in AI models. This structure emerges during pretraining from correlated behaviors in data about people/characters/contexts and persists through post-training, potentially offering a tractable handle on alignment-relevant properties instead of trying to control trillions of parameters.

Key supporting phenomena include:
- Emergent misalignment (fine-tuning on narrow bad behaviors spreads broadly)
- Subliminal learning (preferences transfer via seemingly unrelated data)
- Persona vectors / activation- and weight-space directions for traits
- Alignment pretraining effects
- Related findings on simulators, logits structure, self-beliefs, character training methods, etc.

These are interpreted as evidence of coupled traits rather than independent effects (consistent with models like the Persona Selection Model). Pretraining learns useful predictive correlations even when they “shouldn’t” hold for alignment purposes.

**Optimistic case**: A manageable low-dimensional space of behavior exists that can be steered toward a point that extrapolates to aligned superintelligence, especially under self-referential training pipelines.

**Pessimistic case / challenges**: Interventions on the known dimensions may simply push undesirable behavior into other (hidden) dimensions. Rough optimization can also degrade monitoring channels (e.g., chain-of-thought faithfulness). Gentle measurement and careful objectives are needed to avoid this. Structure after pretraining is human-level and will not be identical to any eventual superintelligent structure, so the research must couple with scalable oversight.

The authors call for systematic theory (toy models of modern training dynamics that capture these phenomena in different regimes) plus empirics, and note that the “character” chosen by different labs is already a highly consequential free variable that produces observably different models. Independence from any single lab’s frame is presented as an advantage for studying this.

Full post:  
https://www.lesswrong.com/posts/sFhW3ZnPMJdnB4Dd6/thousand-dimensional-structure-1  
https://www.alignmentforum.org/posts/sFhW3ZnPMJdnB4Dd6/thousand-dimensional-structure-1  

Careers at Resolution: https://resolution.org/careers  

Original X thread: https://x.com/DavidDAfrica/status/2082837198290682084