Cooperative inverse reinforcement learning (CIRL) asks a robot to infer a human's reward from interaction and act to maximize cooperative return. The field object is usually **scalar**: one reward coordinate to learn.

The book's target is **bundle inference** — multiple value directions, bearer maps, and transport that survives representation change. Scalar CIRL is the **k = 1 embed**: lifting a single reward to a constant bundle coordinate (`scalar_assistance_game_is_bundle_game_k1`).

**Short answer:** Scalar CIRL is a strict projection, not the full problem. Lean proves full finite transport implies cooperative reward inference (forward), and proves the separation: cooperative scalar inference can hold while bundle geometry fails to preserve across profiles that share the same scalar marginal (`cirl_separation_profiles`).

Lean does not prove that real CIRL training finds the intended bundle, or that assistance-game optimality carries over under optimization pressure — those remain field stories plus MB2/MB3 bridges.
