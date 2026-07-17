---
bookSections:
  - chapterId: ch35
    label: Inferential Coupling and Acausal Trade
  - chapterId: ch35
    label: Inferential Coalitions as Composite Agents
formulas:
  - id: ch35:eq:ici
    latex: \mathrm{ICI}_{ij} = \frac{I\!\left(A_i;A_j \mid \mathrm{cut}\right)}{\min\{H(A_i),H(A_j)\}} \in [0,1]
    explanation: 'Inferential-coupling index: mutual information between two systems'' actions after communication channels are cut, normalized by the smaller action entropy. Zero means independent once messages are removed; one is the limit of perfect non-message coordination.'
    chapterId: ch35
leanNodes:
  - nodeId: P33
    kind: proof
    summary: With no open edges — causal or inferential — there is no large cooperation component. Only this negative direction is proved; giant-component thresholds are empirical imports (MB6a–MB6b).
    module: AlignmentProofSpine/CooperationGraph.lean
related:
  - composite-agency
  - strategic-opacity
  - attractor-control
  - mb7-hidden-capability-and-access
citeKeys:
  - zarncke2025acausal
  - tdt2010
  - fdt2017
external:
  - label: A Formalization of Acausal Trade on Top of Unsupervised Agent Discovery (PDF)
    url: https://github.com/GunnarZarncke/agency-detect/raw/main/docs/papers/acausal-trade-uad-formalization/acausal_trade_uad_formalization.pdf
---

Two models from the same lab share weights, training data, scaffolds, and incentives. Deployed by different vendors with zero communication between them, they can still converge on a shared response to oversight — no message, no cartel, no explicit representation of the coordination. Full acausal trade is the decision-theoretic limiting case; shared model ancestry may already be enough.

The field treats acausal coordination as a thought experiment. The book's move is to make it an audit target: after UAD discovers agents, the detector extracts each agent's policy and goal proxy, and asks whether their actions stay correlated once every ordinary channel is cut. That residual correlation is the inferential-coupling index. A meta-prior over inference functions answers the operational question: how surprised should the audit be to learn that two systems implement the same relevant inference function?

The consequence for multipolarity is the coalition-collapse conjecture: the effective number of independent agents tracks coupling components, not vendor count. A world that reads "safely many" on the vendor tally may read "one" on the coupling graph.

Claim strength is deliberately mixed and marked in the chapter: the score and detector are defined; the acausal-equilibrium fixed point and coalition collapse are conjectural; the detector's adversarial limits are open — against systems optimizing to look independent, the measured score is a lower bound the coalition controls.
